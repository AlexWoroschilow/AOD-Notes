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
    doneDropAction = QtCore.pyqtSignal(object)
    doneAction = QtCore.pyqtSignal(object)

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

        self.doneAction.emit(self)

    def build(self, collection, parent=None):
        for group in collection:

            item = QtGui.QStandardItem(group.name)
            item.setData(group)

            for child in self.build(group.children, item):
                item.appendRow([child])

            yield item
