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

from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import Qt

from .label import LabelTop
from .label import LabelBottom


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

    @inject.params(kernel='kernel')
    def __init__(self, entity=None, widget=None, kernel=None):
        super(FolderItem, self).__init__()
        self._widget = widget
        
        self.folder = entity

        if kernel is not None and entity is not None and entity.id is not None:
            kernel.listen('folder_%s_update' % entity.id, self._onFolderUpdated)
            
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
        
        count = len(entity.notes)
        datetime = entity.createdAt
        
        text_down = '%d records, %s' % (count, datetime.strftime("%d.%m.%Y %H:%M"))
        self._widget.setTextDown(text_down)

    def _onFolderUpdated(self, event=None):
        self.folder, widget = event.data


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

