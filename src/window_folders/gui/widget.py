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
import random
import datetime

from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import Qt

from .bar import ToolbarbarWidget


class LabelTop(QtWidgets.QLabel):

    def __init__(self, parent=None):
        super(LabelTop, self).__init__(parent)
        self.setObjectName('folderLabelTop')


class LabelBottom(QtWidgets.QLabel):

    def __init__(self, parent=None):
        super(LabelBottom, self).__init__(parent)
        self.setObjectName('folderLabelBottom')


class QCustomQWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(QCustomQWidget, self).__init__(parent)
        self.textQVBoxLayout = QtWidgets.QVBoxLayout()
        self.textQVBoxLayout.setContentsMargins(10, 10, 0, 10)
        self.textQVBoxLayout.setSpacing(0)

        self.textUpQLabel = LabelTop()
        self.textQVBoxLayout.addWidget(self.textUpQLabel)

        self.textDownQLabel = LabelBottom()
        self.textQVBoxLayout.addWidget(self.textDownQLabel)

        self.setLayout(self.textQVBoxLayout)

    def setTextUp(self, text=None):
        self.textUpQLabel.setText(text)

    def setTextDown(self, text=None):
        self.textDownQLabel.setText(text)

    def setIcon(self, imagePath=None):
        self.iconQLabel.setPixmap(QtGui.QPixmap(imagePath))


class FolderItem(QtWidgets.QListWidgetItem):

    def __init__(self, entity=None, widget=None):
        super(FolderItem, self).__init__()
        self._widget = widget
        
        self.folder = entity

    @property
    def widget(self):
        return self._widget

    @property
    def folder(self):
        return self._entity

    @folder.setter
    def folder(self, entity=None):
        self._entity = entity

        self._widget.setTextUp(entity.name)
        
        count = random.randrange(0, 100)
        self._widget.setTextDown('%d records cound' % count)


class ItemList(QtWidgets.QListWidget):

    def __init__(self, parent=None):
        super(ItemList, self).__init__(parent)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setContentsMargins(0, 0, 0, 0)
        self.setObjectName('foldersList')

    def addLine(self, folder=None):
        item = FolderItem(folder, QCustomQWidget())
        item.setSizeHint(item.widget.sizeHint())

        self.addItem(item)
        self.setItemWidget(item, item.widget)


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

