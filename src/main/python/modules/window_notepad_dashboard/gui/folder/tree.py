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
from PyQt5 import QtGui


class NotepadDashboardTreeModel(QtGui.QStandardItemModel):
    done = QtCore.pyqtSignal(object)

    @inject.params(store='store')
    def __init__(self, store=None):
        super(NotepadDashboardTreeModel, self).__init__()

        state = store.get_state()
        if state is None: return None
        store.subscribe(self.update)

    @inject.params(store='store')
    def update(self, action=None, store=None):
        state = store.get_state()
        if state is None: return None

        self.clear()
        for item in self.build(state.groups, None):
            self.appendRow(item)

        self.done.emit(self)

    def build(self, collection, parent=None):
        for group in collection:

            item = QtGui.QStandardItem(group.name)
            item.setData(group)

            for child in self.build(group.children, item):
                item.appendRow([child])

            yield item


class DashboardFolderTree(QtWidgets.QTreeView):
    editNoteAction = QtCore.pyqtSignal(object)
    removeAction = QtCore.pyqtSignal(object)
    group = QtCore.pyqtSignal(object)
    menuAction = QtCore.pyqtSignal(object, object)

    def __init__(self):
        super(DashboardFolderTree, self).__init__()

        model = NotepadDashboardTreeModel()
        model.done.connect(lambda: self.expandToDepth(3))
        self.setModel(model)

        self.customContextMenuRequested.connect(self.menuEvent)
        self.clicked.connect(self.noteSelectEvent)

        self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setUniformRowHeights(True)
        self.setIconSize(QtCore.QSize(0, 0))
        self.setMinimumWidth(200)

        self.setHeaderHidden(True)
        self.setAnimated(True)
        self.expandAll()

        self.setColumnHidden(1, True)
        self.setColumnHidden(2, True)
        self.setColumnHidden(3, True)

    def menuEvent(self, event):
        index = self.currentIndex()
        if index is None: return None
        entity = self.model().itemFromIndex(index)
        if entity is None: return None
        return self.menuAction.emit(event, entity.data())

    def keyPressEvent(self, event):
        if event.key() in [Qt.Key_Delete, Qt.Key_Backspace]:
            index = self.currentIndex()
            if index is None: return None
            return self.removeAction.emit(index)
        if event.key() in [Qt.Key_Space, Qt.Key_Return]:
            index = self.currentIndex()
            if index is None: return None
            self.model().itemFromIndex(index)
            return self.editNoteAction.emit(index)
        return super(DashboardFolderTree, self).keyPressEvent(event)

    @inject.params(store='store')
    def noteSelectEvent(self, index=None, store=None):
        if index is None: return None

        model = self.model()
        if model is None: return None

        item = model.itemFromIndex(index)
        if item is None: return None

        store.dispatch({
            'type': '@@app/storage/resource/selected/group',
            'entity': item.data()
        })

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

    def close(self):
        super(DashboardFolderTree, self).deleteLater()
        return super(DashboardFolderTree, self).close()
