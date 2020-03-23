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
    current = None

    def setFolders(self, collection=None, current=None):

        if collection is not None:
            self.clear()

            for item in self.buildFolder(collection, current):
                self.appendRow(item)

        if current is None:
            return None

        return self.indexFromItem(self.current)

    def buildFolder(self, collection, current=None):
        for group in collection:
            item = QtGui.QStandardItem(group.name)
            item.setData(group)

            if group == current:
                self.current = item

            for child in self.buildFolder(group.children, current):
                item.appendRow([child])

            yield item