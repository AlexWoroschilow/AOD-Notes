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


class FolderTree(QtWidgets.QTreeView):

    @inject.params(config='config', storage='storage')
    def __init__(self, config=None, storage=None):
        super(FolderTree, self).__init__()

        self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setAnimated(True)

        self.setHeaderHidden(True)
        self.setModel(storage)

        delegate = storage.getItemDelegate()
        self.setItemDelegate(delegate)
        
        location = config.get('storage.location') 
        self.setRootIndex(storage.index(location))
        
        self.setColumnHidden(1, True)
        self.setColumnHidden(2, True)
        self.setColumnHidden(3, True)
        
        self.expandAll(storage)

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
