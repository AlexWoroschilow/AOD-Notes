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
from PyQt5.QtWidgets import QTreeView 
from PyQt5.QtWidgets import QFileSystemModel


class FolderTree(QTreeView):

    @inject.params(config='config')
    def __init__(self, config=None):
        QTreeView.__init__(self)
        
        self.setObjectName('FolderTree')
        self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        
        root = config.get('storage.database')

        model = QFileSystemModel()
        model.setRootPath(root)
        model.setReadOnly(False)
        
        index = model.index(root)
        if index is None:
            return None
        
        self.setModel(model)
        self.setRootIndex(index)
        self.setHeaderHidden(True)

        self.setColumnHidden(1, True)
        self.setColumnHidden(2, True)
        self.setColumnHidden(3, True)


    @property
    def selected(self):
        for index in self.selectedIndexes():
            return self.model().filePath(index)
        return None

    @property
    def index(self):
        for index in self.selectedIndexes():
            return index
        return None