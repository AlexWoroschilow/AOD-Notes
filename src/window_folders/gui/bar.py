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


class ToolbarbarWidget(QtWidgets.QToolBar):

    @inject.params(kernel='kernel')
    def __init__(self, parent=None, kernel=None):
        super(ToolbarbarWidget, self).__init__()
        self.setObjectName('folderToolbarWidgetLeft')
        self.setContentsMargins(0, 0, 0, 0)
        self.setOrientation(Qt.Vertical)
        self.setMaximumWidth(35)

        self.newAction = ToolBarButton()
        self.newAction.setIcon(QtGui.QIcon("icons/new-light.svg"))
        self.newAction.setToolTip("Create a new folder")
        self.newAction.setShortcut("Ctrl+N")

        self.copyAction = ToolBarButton()
        self.copyAction.setIcon(QtGui.QIcon("icons/copy-light.svg"))
        self.copyAction.setToolTip("Clone selected folder")
        self.copyAction.setShortcut("Ctrl+C")

        self.removeAction = ToolBarButton()
        self.removeAction.setIcon(QtGui.QIcon("icons/remove-light.svg"))
        self.removeAction.setToolTip("Remove selected folder")

        self.refreshAction = ToolBarButton()
        self.refreshAction.setIcon(QtGui.QIcon("icons/refresh-light.svg"))
        self.refreshAction.setToolTip("Refresh list")

        self.addWidget(self.newAction)
        self.addWidget(self.copyAction)
        self.addWidget(self.removeAction)
        self.addWidget(self.refreshAction)

