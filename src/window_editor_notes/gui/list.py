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
import functools
from PyQt5 import QtWidgets

from PyQt5.QtCore import Qt

from .bar import ToolBarWidget
from .line import NameEditor
from .label import LabelTop
from .label import LabelDescription
from .label import LabelBottom


class QCustomQWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(QCustomQWidget, self).__init__(parent)
        self.textQVBoxLayout = QtWidgets.QVBoxLayout()

        self.name = LabelTop()
        self.textQVBoxLayout.addWidget(self.name)

        self.date = LabelBottom(self)
        self.textQVBoxLayout.addWidget(self.date)

        self.description = LabelDescription(self)
        self.textQVBoxLayout.addWidget(self.description)

        self.setLayout(self.textQVBoxLayout)

    @property
    def entity(self):
        pass

    @entity.setter
    def entity(self, entity=None):
        
        try:
            if entity.name is not None:
                self.name.setText(entity.name)
            
            if entity.description is not None and len(entity.description):
                self.description.setText(entity.description)
            else:
                self.description.setVisible(False)
            
            if entity.createdAt is not None:
                datetime = entity.createdAt
                self.date.setText(datetime.strftime("%d.%m.%Y %H:%M"))

        except (RuntimeError, TypeError, NameError):

            self.name = LabelTop()
            self.description = LabelDescription() 
            self.date = LabelBottom()
            
            if entity.name is not None and entity.name:
                self.name.setText(entity.name)
            
            if entity.createdAt is not None and entity.createdAt:
                datetime = entity.createdAt.strftime("%d.%m.%Y %H:%M")
                self.date.setText(datetime)
                         
            if entity.description is not None and entity.description:
                self.description.setText(entity.description)

        return self.name.text()

    def setName(self, value=None):
        if value is not None:
            self.name.setText(value)

    def resizeEvent(self, event):
        width = event.size().width()
        self.name.setFixedWidth(width - 20)
        self.description.setFixedWidth(width - 20)
        super(QCustomQWidget, self).resizeEvent(event)


class NoteItem(QtWidgets.QListWidgetItem):

    @inject.params(kernel='kernel')
    def __init__(self, entity=None, widget=None, kernel=None):
        super(NoteItem, self).__init__()
        self._widget = widget
        self.entity = entity

    @property
    def widget(self):
        return self._widget

    @property
    def entity(self):
        return self._entity

    @entity.setter
    def entity(self, entity=None):
        if entity is None:
            return None
        self.widget.entity = entity
        self._entity = entity

    def resizeEvent(self, event):
        self._widget.resizeEvent(event)


class ItemList(QtWidgets.QListWidget):

    def __init__(self, parent=None):
        super(ItemList, self).__init__(parent)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.setContentsMargins(0, 0, 0, 0)
        self.setMinimumWidth(200)
        self.setWordWrap(True)

    @inject.params(kernel='kernel')
    def addLine(self, entity=None, kernel=None):
        item = NoteItem(entity, QCustomQWidget())
        item.setSizeHint(item.widget.sizeHint())

        self.addItem(item)
        self.setItemWidget(item, item.widget)
        
        kernel.listen(entity.unique, functools.partial(
            self.onActionNoteUpdate, item=item            
        ))
        
    def onActionNoteUpdate(self, event, item):
        note, parent = event.data
        if note is None:
            return None
        item.widget.entity = note


class RecordList(QtWidgets.QSplitter):

    def __init__(self, parent=None, storage=None):
        super(RecordList, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setObjectName('widgetRecordList')

        self._folder = None

        self.toolbar = ToolBarWidget(self)
        self.addWidget(self.toolbar)

        layout = QtWidgets.QGridLayout()
        layout.setContentsMargins(0, 10, 0, 0)
        
        self.folderEditor = NameEditor()
        layout.addWidget(self.folderEditor, 0, 0)
        
        self.list = ItemList()
        layout.addWidget(self.list, 1, 0)

        content = QtWidgets.QWidget()
        content.setContentsMargins(0, 0, 0, 0)
        content.setLayout(layout)
        
        self.addWidget(content)

        self.setCollapsible(0, True)
        self.setCollapsible(1, False)

    @property
    def entity(self):
        for index in self.list.selectedIndexes():
            item = self.list.itemFromIndex(index)
            if item is not None and item.entity is not None:
                return item.entity
        return None

    @property
    def folder(self):
        return self._folder

    @folder.setter
    def folder(self, folder=None):
        if folder is not None:
            self._folder = folder
            self.folderEditor.setText(folder.name)
            self.folderEditor.setVisible(True)
            return None
        
        self.folderEditor.setVisible(False)
        return None

    def count(self):
        return self.list.count()

    def clear(self):
        return self.list.clear()

    def addLine(self, entity=None):
        self.list.addLine(entity)

    def selectedIndexes(self):
        return self.list.selectedIndexes()

    def itemFromIndex(self, index=None):
        if index is None:
            return None

        return self.list.itemFromIndex(index)

    def takeItem(self, index=None):
        if index is None:
            return None

        self.list.takeItem(index)

    def item(self, index=None):
        if index is None:
            return None
        return self.list.item(index)

    def currentRow(self):
        return self.list.currentRow()

    def setCurrentRow(self, row=None):
        if row is None or self.list is None:
            return None
        return self.list.setCurrentRow(row)
