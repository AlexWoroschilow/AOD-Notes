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


class FolderList(QtWidgets.QSplitter):

    def __init__(self, parent=None):
        super(FolderList, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setObjectName('foldersWidget')

        self.toolbar = ToolbarbarWidget()
        self.addWidget(self.toolbar)

        self.list = ItemList()
        self.list.setMinimumWidth(180)
        self.addWidget(self.list)
        
        self.setCollapsible(0, True)
        self.setCollapsible(1, False)

    def addLine(self, folder=None):
        self.list.addLine(folder)

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

