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


class NotepadDashboard(QtWidgets.QSplitter):
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

    def __init__(self):
        super(NotepadDashboard, self).__init__()
        self.removed.connect(self.open)
        self.created.connect(self.open)
        self.edit.connect(lambda x: self.open(x[0]))
        self.setContentsMargins(0, 0, 0, 0)

        self.tree = NotepadDashboardTree()
        self.tree.note.connect(lambda x: self.open(x[0]))
        self.tree.group.connect(lambda x: self.open(x[0]))
        self.tree.delete.connect(self.delete.emit)
        self.tree.menu.connect(self.menu.emit)

        self.container_left = NotepadDashboardLeft()
        self.container_left.addWidget(self.tree)

        self.addWidget(self.container_left)

        self.container_right = NotepadDashboardRight()
        self.addWidget(self.container_right)

        self.setCollapsible(0, True)
        self.setCollapsible(1, False)
        self.setCollapsible(2, False)

        self.setStretchFactor(1, 2)
        self.setStretchFactor(2, 3)

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

    @inject.params(storage='storage')
    def note(self, index=None, storage=None):
        self.scrollTo(index)
        if storage.isDir(index):
            return self

        preview = NotepadEditorToolbarTop()
        preview.note_new.connect(self.note_new.emit)
        preview.group_new.connect(self.group_new.emit)
        preview.note_import.connect(self.note_import.emit)
        preview.settings.connect(self.settings.emit)
        preview.search.connect(self.search.emit)

        splitter = DashboardSplitter(index)
        splitter.delete.connect(self.delete.emit)
        splitter.fullscreen.connect(self.fullscreen.emit)
        splitter.clicked.connect(self.scrollTo)
        splitter.clone.connect(self.clone.emit)
        splitter.open(index)

        self.container_right.clean()
        self.container_right.addWidget(preview)
        self.container_right.addWidget(splitter)
        self.container_right.show()

        self.tree.note.disconnect()
        # Reconnect event to work locally without
        # the recreation of the all note environment
        self.tree.note.connect(splitter.previewSelected)

        return self

    @inject.params(storage='storage')
    def group(self, index=None, storage=None):

        toolbar = NotepadEditorToolbarTop()
        toolbar.note_new.connect(self.note_new.emit)
        toolbar.group_new.connect(self.group_new.emit)
        toolbar.note_import.connect(self.note_import.emit)
        toolbar.settings.connect(self.settings.emit)
        toolbar.search.connect(self.search.emit)

        preview = PreviewScrollArea(self, [])
        preview.fullscreenAction.connect(self.fullscreen.emit)
        preview.deleteAction.connect(self.delete.emit)
        preview.cloneAction.connect(self.clone.emit)
        preview.editAction.connect(self.edit.emit)
        preview.open(index)

        self.container_right.clean()
        self.container_right.addWidget(toolbar)
        self.container_right.addWidget(preview)
        self.container_right.show()

        self.tree.note.disconnect()
        # Reconnect event to be able
        # to open the notes as usial
        self.tree.note.connect(lambda x: self.note(x[0]))

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
