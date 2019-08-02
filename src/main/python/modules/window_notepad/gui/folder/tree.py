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
from PyQt5.QtCore import Qt


class NotepadDashboardTree(QtWidgets.QTreeView):
    note = QtCore.pyqtSignal(object)
    group = QtCore.pyqtSignal(object)
    menu = QtCore.pyqtSignal(object)

    @inject.params(config='config', storage='storage')
    def __init__(self, config=None, storage=None):
        super(NotepadDashboardTree, self).__init__()
        self.customContextMenuRequested.connect(self.menu.emit)
        self.clicked.connect(self.noteSelectEvent)

        self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHeaderHidden(True)
        self.setAnimated(True)
        self.expandAll()

        self.setModel(storage)

        location = config.get('storage.location')
        self.setRootIndex(storage.index(location))

        self.setColumnHidden(1, True)
        self.setColumnHidden(2, True)
        self.setColumnHidden(3, True)

    @inject.params(config='config', storage='storage')
    def noteSelectEvent(self, index=None, config=None, storage=None):
        if index is None:
            return None

        path = storage.filePath(index)
        config.set('editor.current', path)

        if storage.isDir(index):
            return self.group.emit((index, None))
        return self.note.emit((index, None))

    @inject.params(storage='storage')
    def expandAll(self, storage):
        for index in storage.entities():
            self.expand(index)

    @inject.params(storage='storage')
    def collapseAll(self, storage):
        for index in storage.entities():
            self.collapse(index)

    @property
    def current(self):
        for index in self.selectedIndexes():
            return index
        return None

    @property
    @inject.params(config='config')
    def selected(self, config=None):
        for index in self.selectedIndexes():
            if index is not None and index:
                return self.model().filePath(index)
        return config.get('storage.location')

    @property
    def index(self):
        for index in self.selectedIndexes():
            return index
        return None
