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
from PyQt5 import QtWidgets

from .bar import ToolbarbarWidget
from .list import ItemList

from .text import TextEditor


class FolderList(QtWidgets.QSplitter):

    def __init__(self, storage=None):
        super(FolderList, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.setObjectName('foldersWidget')

        self.storage = storage

        self.toolbar = ToolbarbarWidget()
        self.addWidget(self.toolbar)

        self.list = ItemList()
        self.list.setMinimumWidth(180)

        containerLayout = QtWidgets.QVBoxLayout()
        containerLayout.setContentsMargins(0, 0, 0, 0)
        containerLayout.addWidget(self.list)
        
        self.tags = TextEditor() 
        containerLayout.addWidget(self.tags)

        container = QtWidgets.QWidget()
        container.setContentsMargins(0, 0, 0, 0)
        container.setLayout(containerLayout)
        
        self.addWidget(container)
        
        self.setCollapsible(0, True)
        self.setCollapsible(1, False)
        
        self.reload()

    def reload(self, string=None):
        self.list.clear()
        for folder in self.storage.folders(string):
            self.list.addLine(folder)
        self.list.setCurrentRow(0)

    @property
    def selected(self):
        return self.current

    @property
    def current(self):
        for index in self.selectedIndexes():
            item = self.itemFromIndex(index)
            if item is not None:
                return item.folder
        item = self.list.item(0)
        if item is not None and item.entity is not None:
            return item.folder
        return None

    def selectedIndexes(self):
        return self.list.selectedIndexes()

    def itemFromIndex(self, index=None):
        if index is None:
            return None
        return self.list.itemFromIndex(index)

    def takeItem(self, index=None):
        if index is None:
            return None
        self.list.takeItem(index.row())

