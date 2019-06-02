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
import gc
import inject
from PyQt5 import QtCore
from PyQt5 import QtWidgets

from .folder.tree import FolderTree
from .demo.widget import DemoWidget
from .preview.widget import PreviewScrollArea


class NotepadDashboard(QtWidgets.QSplitter):
    edit = QtCore.pyqtSignal(object)
    delete = QtCore.pyqtSignal(object)
    clone = QtCore.pyqtSignal(object)

    saveAction = QtCore.pyqtSignal(object)
    fullscreenAction = QtCore.pyqtSignal(object)
    editor = None

    def __init__(self, actions):
        super(NotepadDashboard, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)

        container_layout = QtWidgets.QGridLayout()
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        self.tree = FolderTree()
        self.tree.expandAll()

        container_layout.addWidget(self.tree, 0, 1)

        container = QtWidgets.QWidget()

        container.setContentsMargins(0, 0, 0, 0)

        container.setLayout(container_layout)
        self.addWidget(container)

        self.container = QtWidgets.QWidget()
        self.container.setContentsMargins(0, 0, 0, 0)
        self.container.setObjectName('FolderListContainer')
        self.container.setLayout(QtWidgets.QVBoxLayout())
        self.container.layout().setContentsMargins(0, 0, 0, 0)

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
            if storage.isFile(entity):
                widget.addPreview(entity)

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
