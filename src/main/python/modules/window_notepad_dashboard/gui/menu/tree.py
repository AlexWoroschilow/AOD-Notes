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
from PyQt5 import QtCore
from PyQt5.QtCore import Qt

from .model import FolderTreeModel


class FolderTree(QtWidgets.QTreeView):
    clickedAction = QtCore.pyqtSignal(object)

    def __init__(self):
        super(FolderTree, self).__init__()
        self.clicked.connect(self.clickedEvent)

        self.setEditTriggers(QtWidgets.QAbstractItemView.EditKeyPressed)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setUniformRowHeights(True)
        self.setIconSize(QtCore.QSize(10, 10))
        self.setMinimumSize(QtCore.QSize(200, 600))

        self.setModel(FolderTreeModel())

        self.setHeaderHidden(True)
        self.setAnimated(True)
        self.expandAll()

        self.setColumnHidden(1, True)
        self.setColumnHidden(2, True)
        self.setColumnHidden(3, True)

    def setModel(self, model):
        super(FolderTree, self).setModel(model)
        self.expandAll()

    def clickedEvent(self, index=None):
        if index is None: return None

        model = self.model()
        if model is None: return None

        item = model.itemFromIndex(index)
        if item is None: return None

        return self.clickedAction.emit(item.data())
