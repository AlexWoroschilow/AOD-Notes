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

from lib.widget.button import ToolBarButton


class ToolBarWidget(QtWidgets.QToolBar):

    @inject.params(kernel='kernel')
    def __init__(self, parent=None, kernel=None):
        super(ToolBarWidget, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.setOrientation(Qt.Vertical)
        self.setMaximumWidth(35)

        self.newAction = ToolBarButton()
        self.newAction.setIcon(QtGui.QIcon("icons/new.svg"))
        self.newAction.setToolTip("Create a new document.")
        self.newAction.setShortcut("Ctrl+N")

        self.copyAction = ToolBarButton()
        self.copyAction.setIcon(QtGui.QIcon("icons/copy.svg"))
        self.copyAction.setToolTip("Copy text to clipboard")

        self.removeAction = ToolBarButton()
        self.removeAction.setIcon(QtGui.QIcon("icons/remove.svg"))
        self.removeAction.setShortcut("Del")
        self.removeAction.setToolTip("Remove selected document")

        self.refreshAction = ToolBarButton()
        self.refreshAction.setIcon(QtGui.QIcon("icons/refresh.svg"))
        self.refreshAction.setShortcut("F5")
        self.refreshAction.setToolTip("Refresh list")

        self.addWidget(self.newAction)
        self.addWidget(self.copyAction)
        self.addWidget(self.removeAction)
        self.addWidget(self.refreshAction)

        kernel.dispatch('window.notelist.toolbar', (
            parent, self
        ))