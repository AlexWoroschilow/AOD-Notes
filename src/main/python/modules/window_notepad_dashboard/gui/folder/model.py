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

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5 import QtGui


class NotepadDashboardTreeModel(QtGui.QStandardItemModel):
    doneAction = QtCore.pyqtSignal(object)

    current = None

    collection = []

    def fill(self, collection=None, current=None):

        self.clear()

        for item in self.build(collection, current):
            self.appendRow(item)

        self.doneAction.emit(self.indexFromItem(self.current))
        return self.indexFromItem(self.current)

    def build(self, collection, current=None):
        for group in collection:
            item = QtGui.QStandardItem(group.name)
            item.setData(group)

            if group == current:
                self.current = item

            for child in self.build(group.children, current):
                self.collection.append(child)
                item.appendRow([child])

            self.collection.append(item)
            yield item

    def indexFromData(self, element=None):
        # for index, item in enumerate(self.collection, start=0):
        #     if item.data() == element:
        #         return self.indexFromItem(item)
        return self.createIndex(0, 0)

    def clear(self):
        self.collection = []
        return super(NotepadDashboardTreeModel, self).clear()
