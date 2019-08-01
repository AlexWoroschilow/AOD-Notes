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
from PyQt5 import QtGui

from .folder.tree import FolderTree
from .demo.widget import DemoWidget
from .preview.widget import PreviewScrollArea

from .bar import FolderTreeToolbarTop
from .bar import NotepadEditorToolbarTop

from .splitter import DashboardSplitter
from .frame import NotepadDashboardLeft
from .frame import NotepadDashboardRight


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

    settings = QtCore.pyqtSignal(object)

    saveAction = QtCore.pyqtSignal(object)
    search = QtCore.pyqtSignal(object)

    storage = QtCore.pyqtSignal(object)
    storage_changed = QtCore.pyqtSignal(object)

    fullscreenAction = QtCore.pyqtSignal(object)

    editor = None

    def __init__(self, actions):
        super(NotepadDashboard, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)

        self.tree = FolderTree()
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

    def _note(self, event=None):
        index, document = event
        if index is None or document is None:
            return None

        if self.editor is None:
            return None

        self.editor.setDocument(document)
        self.editor.setIndex(index)

    @property
    @inject.params(storage='storage')
    def current(self, storage):
        index = self.tree.currentIndex()
        if len(storage.filePath(index)):
            return index
        return storage.rootIndex()

    def focus(self):
        if self.editor is None:
            self.editor.focus()
        return self

    @inject.params(storage='storage')
    def open(self, index, storage):
        if storage.isFile(index):
            return self.note(index)
        return self.group(index)

    @inject.params(storage='storage', config='config', editor='notepad.editor')
    def note(self, index, storage, config, editor):
        if storage.isDir(index):
            return self

        config.set('editor.current', storage.filePath(index))

        splitter = DashboardSplitter()

        toolbar = NotepadEditorToolbarTop()
        toolbar.note_new.connect(self.note_new.emit)
        toolbar.group_new.connect(self.group_new.emit)
        toolbar.note_import.connect(self.note_import.emit)
        toolbar.settings.connect(self.settings.emit)
        toolbar.search.connect(self.search.emit)

        parent = storage.fileDir(index)
        collection = [x for x in storage.entities(parent) if storage.isFile(x)]

        preview = PreviewScrollArea(self, collection)
        preview.delete.connect(self.delete.emit)
        preview.clone.connect(self.clone.emit)
        preview.edit.connect(self.edit.emit)
        preview.scrollTo((index, None))
        preview.setMinimumWidth(350)

        self.editor = editor
        self.editor.setMinimumWidth(500)
        document = preview.getDocumentByIndex(index)
        if document is not None and document:
            self.editor.setDocument(document)
            self.editor.setIndex(index)

        splitter.addWidget(preview)
        splitter.addWidget(self.editor)
        splitter.setStretchFactor(1, 1)
        splitter.setStretchFactor(2, 2)

        self.container.clean()
        self.container.addWidget(toolbar)
        self.container.addWidget(splitter)
        self.editor.focus()

        if self.current == index:
            return self

        self.tree.setCurrentIndex(index)

        return self

    @inject.params(storage='storage', config='config')
    def group(self, index, storage, config):
        if storage.isFile(index):
            index = storage.fileDir(index)

        config.set('editor.current', storage.filePath(index))

        collection = [x for x in storage.entities(index) if storage.isFile(x)]

        preview = PreviewScrollArea(self, collection)
        preview.edit.connect(self.edit.emit)
        preview.delete.connect(self.delete.emit)
        preview.clone.connect(self.clone.emit)
        preview.scrollTo((collection[0], None))
        preview.setMinimumWidth(350)

        toolbar = NotepadEditorToolbarTop()
        toolbar.note_new.connect(self.note_new.emit)
        toolbar.group_new.connect(self.group_new.emit)
        toolbar.note_import.connect(self.note_import.emit)
        toolbar.settings.connect(self.settings.emit)
        toolbar.search.connect(self.search.emit)

        self.container.clean()
        self.container.addWidget(toolbar)
        self.container.addWidget(preview)

        return self

    def demo(self):
        demo = DemoWidget()

        self.container.clean()
        self.container.addWidget(demo)

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

    def clean(self):
        layout = self.layout()
        for i in range(0, layout.count()):
            item = layout.itemAt(i)
            if item is None:
                layout.takeAt(i)

            widget = item.widget()
            if item is not None:
                widget.close()

    def close(self):
        super(NotepadDashboard, self).deleteLater()
        return super(NotepadDashboard, self).close()
