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
import time
import inject
import functools

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5 import QtGui

from .model import NotepadDashboardTreeModel


class QCustomDelegate(QtWidgets.QStyledItemDelegate):
    renameAction = QtCore.pyqtSignal(object)

    def setModelData(self, editor, model, index):
        item = model.itemFromIndex(index)
        if item is None: return None
        entity = item.data()
        if entity is None: return None

        try:
            response = super(QCustomDelegate, self).setModelData(editor, model, index)
            entity.name = editor.text()
            self.renameAction.emit(entity)
            return response
        except OSError as ex:
            print(ex)
        return None


class DashboardFolderTree(QtWidgets.QTreeView):
    editNoteAction = QtCore.pyqtSignal(object)
    groupAction = QtCore.pyqtSignal(object)
    removeAction = QtCore.pyqtSignal(object)
    renameAction = QtCore.pyqtSignal(object)
    moveAction = QtCore.pyqtSignal(object)
    menuAction = QtCore.pyqtSignal(object, object)

    def __init__(self):
        super(DashboardFolderTree, self).__init__()
        self.setEditTriggers(QtWidgets.QAbstractItemView.EditKeyPressed)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setUniformRowHeights(True)
        self.setIconSize(QtCore.QSize(10, 10))
        self.setMinimumWidth(200)

        self.setModel(NotepadDashboardTreeModel())

        delegate = QCustomDelegate()
        delegate.renameAction.connect(self.renameAction.emit)
        self.setItemDelegate(delegate)

        self.customContextMenuRequested.connect(self.menuEvent)
        self.clicked.connect(self.clickedEvent)

        self.setHeaderHidden(True)
        self.setAnimated(True)
        self.expandAll()

        self.setColumnHidden(1, True)
        self.setColumnHidden(2, True)
        self.setColumnHidden(3, True)

    def setFolderCurrent(self, selected=None):
        if selected is None: return self
        model = self.model()
        if model is None: return None

        index = model.getIndexByData(selected)
        if index is None: return None

        print(index, selected)
        self.setCurrentIndex(index)
        self.scrollTo(self.indexBelow(index))

        return self

    def setFolders(self, collection=None, selected=None):

        index = self.model(). \
            setFolders(collection, selected)

        self.expandAll()

        if index is None:
            return None

        self.setCurrentIndex(index)
        self.scrollTo(self.indexBelow(index))

    def dragEnterEvent(self, QDragEnterEvent):
        return QDragEnterEvent.acceptProposedAction()

    def dropEvent(self, QDropEvent):
        item_current = self.model().itemFromIndex(self.currentIndex())
        if item_current is None: return QDropEvent.ignore()

        index_parent = self.indexAt(QDropEvent.pos())
        item_parent = self.model().itemFromIndex(index_parent)
        if item_parent is None: return QDropEvent.ignore()

        data_current = item_current.data()
        if data_current is None: return QDropEvent.ignore()
        self.moveAction.emit((data_current, item_parent.data()))
        return QDropEvent.accept()

    def menuEvent(self, event):
        index = self.currentIndex()
        if index is None: return None

        item = self.model().itemFromIndex(index)
        if item is None: return None

        return self.menuAction.emit(event, item.data())

    def keyPressEvent(self, event):
        if event.key() in [Qt.Key_Delete, Qt.Key_Backspace]:
            index = self.currentIndex()
            if index is None: return None

            item = self.model().itemFromIndex(index)
            if item is None: return None

            return self.removeAction.emit(item.data())
        if event.key() in [Qt.Key_Space, Qt.Key_Return]:

            index = self.currentIndex()
            if index is None: return None

            item = self.model().itemFromIndex(index)
            if item is None: return None

            return self.editNoteAction.emit(item.data())
        return super(DashboardFolderTree, self).keyPressEvent(event)

    def clickedEvent(self, index=None):
        if index is None: return None

        model = self.model()
        if model is None: return None

        item = model.itemFromIndex(index)
        if item is None: return None

        return self.groupAction.emit(item.data())

    def close(self):
        super(DashboardFolderTree, self).deleteLater()
        return super(DashboardFolderTree, self).close()
