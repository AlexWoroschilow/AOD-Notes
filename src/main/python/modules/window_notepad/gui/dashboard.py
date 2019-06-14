# -*- coding: utf-8 -*-
# Copyright 2015 Alex Woroschilow (alex.woroschilow@gmail.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import inject

from PyQt5 import QtCore
from PyQt5 import QtWidgets

from .folder.tree import FolderTree
from .demo.widget import DemoWidget
from .preview.widget import PreviewScrollArea

from .bar import FolderTreeToolbarTop
from .bar import NotepadEditorToolbarTop


class Notepad(QtWidgets.QTabWidget):

    def __init__(self):
        super(Notepad, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.setTabPosition(QtWidgets.QTabWidget.West)
        self.setTabsClosable(True)

    def close(self):
        super(Notepad, self).deleteLater()
        return super(Notepad, self).close()


class NotepadDashboardLeft(QtWidgets.QGroupBox):
    def __init__(self):
        super(NotepadDashboardLeft, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

    def addWidget(self, widget):
        self.layout().addWidget(widget)


class NotepadDashboardRight(QtWidgets.QGroupBox):
    def __init__(self):
        super(NotepadDashboardRight, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)

        self.setLayout(QtWidgets.QVBoxLayout(self))
        self.layout().setContentsMargins(0, 0, 0, 0)

    def addWidget(self, widget):
        self.layout().addWidget(widget)


class NotepadDashboard(QtWidgets.QSplitter):
    edit = QtCore.pyqtSignal(object)
    delete = QtCore.pyqtSignal(object)
    clone = QtCore.pyqtSignal(object)
    created = QtCore.pyqtSignal(object)
    removed = QtCore.pyqtSignal(object)
    updated = QtCore.pyqtSignal(object)
    note_new = QtCore.pyqtSignal(object)
    note_import = QtCore.pyqtSignal(object)
    group_new = QtCore.pyqtSignal(object)
    search = QtCore.pyqtSignal(object)
    settings = QtCore.pyqtSignal(object)
    saveAction = QtCore.pyqtSignal(object)
    storage = QtCore.pyqtSignal(object)
    storage_changed = QtCore.pyqtSignal(object)
    fullscreenAction = QtCore.pyqtSignal(object)
    editor = None

    def __init__(self, actions):
        super(NotepadDashboard, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)

        self.tree = FolderTree()
        self.tree.expandAll()

        self.tree_toolbar = FolderTreeToolbarTop()
        self.tree_toolbar.storage.connect(lambda event=None: self.storage.emit(event))
        self.storage_changed.connect(lambda text: self.tree_toolbar.storage_changed.emit(text))

        self.container_left = NotepadDashboardLeft()
        self.container_left.addWidget(self.tree_toolbar)
        self.container_left.addWidget(self.tree)

        self.addWidget(self.container_left)

        self.container = NotepadDashboardRight()
        self.addWidget(self.container)

        self.setCollapsible(0, True)
        self.setCollapsible(1, False)
        self.setCollapsible(2, False)

        self.setStretchFactor(1, 2)
        self.setStretchFactor(2, 3)

        self.actions = actions
        self.test = None

    @property
    def current(self):
        injector = inject.get_injector()
        storage = injector.get_instance('storage')
        if len(storage.filePath(self.tree.currentIndex())):
            return self.tree.currentIndex()
        return storage.rootIndex()

    def focus(self):
        if self.editor is None:
            self.editor.focus()
        return self

    @inject.params(storage='storage', config='config')
    def note(self, index, storage, config):
        if storage.isDir(index): return self
        current = storage.filePath(index)
        if current is None: return self
        config.set('editor.current', current)

        layout = self.container.layout()
        if layout is None: return self

        for i in range(layout.count()):
            layout.itemAt(i).widget().close()

        container = inject.get_injector()
        if container is None: return self

        self.editor = container.get_instance('notepad.editor')
        if self.editor is None: return self

        self.editor.index = index

        toolbar = NotepadEditorToolbarTop()
        toolbar.note_new.connect(lambda event=None: self.note_new.emit(event))
        toolbar.note_import.connect(lambda event=None: self.note_import.emit(event))
        toolbar.group_new.connect(lambda event=None: self.group_new.emit(event))
        toolbar.search.connect(lambda event=None: self.search.emit(event))
        toolbar.settings.connect(lambda event=None: self.settings.emit(event))
        layout.addWidget(toolbar)
        layout.addWidget(self.editor)
        self.editor.focus()

        if self.current == index: return self
        # highlight the current note if the
        # selected not and editable not are different
        # this happens of the edition was started programmatically
        # or in any other way except the preview tree view
        self.tree.setCurrentIndex(index)
        return self

    @inject.params(storage='storage', config='config')
    def group(self, index, storage, config):
        current = storage.filePath(index)
        config.set('editor.current', current)

        layout = self.container.layout()
        for i in range(0, layout.count()):
            item = layout.itemAt(i)
            if item is None: layout.takeAt(i)
            widget = item.widget()
            if item is not None:
                widget.close()

        widget = PreviewScrollArea(self)
        widget.edit.connect(self.edit.emit)
        widget.delete.connect(self.delete.emit)
        widget.delete.connect(lambda x: self.group(index))
        widget.clone.connect(self.clone.emit)
        widget.clone.connect(lambda x: self.group(index))

        for entity in storage.entities(index):
            if storage.isDir(entity):
                continue
            widget.addPreview(entity)

        toolbar = NotepadEditorToolbarTop()
        toolbar.note_new.connect(lambda event=None: self.note_new.emit(event))
        toolbar.note_import.connect(lambda event=None: self.note_import.emit(event))
        toolbar.group_new.connect(lambda event=None: self.group_new.emit(event))
        toolbar.search.connect(lambda event=None: self.search.emit(event))
        toolbar.settings.connect(lambda event=None: self.settings.emit(event))

        layout.addWidget(toolbar)
        layout.addWidget(widget)
        widget.show()
        return self

    def demo(self):
        layout = self.container.layout()
        for i in range(layout.count()):
            layout.itemAt(i).widget().close()
        layout.addWidget(DemoWidget())
        return self

    @inject.params(storage='storage')
    def toggle(self, collection=[], state=False, storage=None):
        for index in storage.entities():
            row, parent = (index.row(), index.parent())
            self.tree.setRowHidden(row, parent, state)
            if index not in collection:
                continue

            current = index
            while current != storage.rootIndex():
                row, parent = (current.row(), current.parent())
                self.tree.setRowHidden(row, parent, False)
                self.tree.expand(current)
                current = parent

        return True
