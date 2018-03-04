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
from PyQt5.Qt import Qt
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtSvg


class ToolbarbarWidget(QtWidgets.QToolBar):
    def __init__(self):
        super(ToolbarbarWidget, self).__init__()
        self.setOrientation(Qt.Vertical)
        self.setContentsMargins(0, 0, 0, 0)

        self.newAction = QtWidgets.QAction(QtGui.QIcon("icons/new.svg"), "New", self)
        self.newAction.setShortcut("Ctrl+N")
        self.newAction.setStatusTip("Create a new document from scratch.")

        self.copyAction = QtWidgets.QAction(QtGui.QIcon("icons/copy.svg"), "Copy to clipboard", self)
        self.copyAction.setStatusTip("Copy text to clipboard")
        self.copyAction.setShortcut("Ctrl+C")

        self.removeAction = QtWidgets.QAction(QtGui.QIcon("icons/remove.svg"), "Remove selected folder", self)
        self.removeAction.setStatusTip("Remove selected folder")

        self.refreshAction = QtWidgets.QAction(QtGui.QIcon("icons/refresh.svg"), "Refresh selected folder", self)
        self.refreshAction.setStatusTip("Refresh selected folder")

        self.addAction(self.newAction)
        self.addAction(self.copyAction)
        self.addAction(self.refreshAction)
        self.addAction(self.removeAction)
