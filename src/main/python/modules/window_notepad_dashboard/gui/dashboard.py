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

from .folder.tree import NotepadDashboardTree
from .preview.list import PreviewScrollArea

from .bar import NotepadEditorToolbarTop

from .splitter import DashboardSplitter
from .frame import NotepadDashboardLeft
from .frame import NotepadDashboardRight
from .frame import NotepadDashboardTop

from .header import NotepadDashboardHeader


class NotepadDashboard(QtWidgets.QWidget):
    edit = QtCore.pyqtSignal(object)
    delete = QtCore.pyqtSignal(object)
    clone = QtCore.pyqtSignal(object)
    menu = QtCore.pyqtSignal(object)

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

    fullscreen = QtCore.pyqtSignal(object)

    editor = None
    preview = None

    @inject.params(editor='notepad.editor')
    def __init__(self, editor=None):
        super(NotepadDashboard, self).__init__()
        self.setLayout(QtWidgets.QVBoxLayout())

        self.editor = editor
        self.header = NotepadDashboardHeader()
        self.header.note_new.connect(self.note_new.emit)
        self.header.group_new.connect(self.group_new.emit)
        self.header.note_import.connect(self.note_import.emit)
        self.header.settings.connect(self.settings.emit)
        self.header.search.connect(self.search.emit)
        self.layout().addWidget(self.header)

        self.tree = NotepadDashboardTree()
        self.tree.note.connect(lambda x: self.open(x[0]))
        self.tree.group.connect(lambda x: self.open(x[0]))
        self.tree.delete.connect(self.delete.emit)
        self.tree.menu.connect(self.menu.emit)

        self.preview = PreviewScrollArea(self, [])
        self.preview.fullscreenAction.connect(self.fullscreen.emit)
        self.preview.deleteAction.connect(self.delete.emit)
        self.preview.cloneAction.connect(self.clone.emit)
        self.preview.editAction.connect(self.edit.emit)

        self.splitter = QtWidgets.QSplitter()
        self.splitter.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.splitter.addWidget(self.tree)
        self.splitter.addWidget(self.preview)
        self.splitter.addWidget(self.editor)

        self.splitter.setCollapsible(0, True)
        self.splitter.setCollapsible(1, False)
        self.splitter.setCollapsible(2, True)

        self.splitter.setStretchFactor(1, 2)
        self.splitter.setStretchFactor(2, 3)
        self.splitter.setStretchFactor(3, 3)
        self.splitter.setSizes([2, 0])

        self.layout().addWidget(self.splitter)

    @property
    @inject.params(storage='storage')
    def current(self, storage):
        index = self.tree.currentIndex()
        if len(storage.filePath(index)):
            return index
        return storage.rootIndex()

    @inject.params(storage='storage')
    def open(self, index=None, storage=None):
        if storage.isFile(index):
            return self.note(index)
        return self.group(index)

    def scrollTo(self, index=None):
        if self.tree is None or index is None:
            return None
        self.tree.setCurrentIndex(index)

    @inject.params(storage='storage', editor='notepad.editor')
    def note(self, index=None, storage=None, editor=None):
        self.scrollTo(index)
        if storage.isDir(index):
            return self

        if self.editor is not None:
            self.editor.open(index)
        return self

    @inject.params(storage='storage')
    def group(self, index=None, storage=None):

        if self.preview is not None:
            return self.preview.open(index)

        return self

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
