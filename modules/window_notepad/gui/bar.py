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
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui

from lib.widget.button import ToolBarButton


class ToolBarWidget(QtWidgets.QToolBar):

    @inject.params(config='config')
    def __init__(self, parent=None, config=None):
        self.parent = parent
        super(ToolBarWidget, self).__init__(parent)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.onActionContextMenu)
        
        self.setObjectName('ToolBarWidget')
        self.setContentsMargins(0, 0, 0, 0)
        self.setOrientation(Qt.Vertical)
        self.setMaximumWidth(35)

        self.setVisible(int(config.get('folders.toolbar')))
        
        self.expandAction = ToolBarButton()
        self.expandAction.setIcon(QtGui.QIcon("icons/plus-light.svg"))
        self.expandAction.setToolTip("Expand all folders")
        self.addWidget(self.expandAction)

        self.collapseAction = ToolBarButton()
        self.collapseAction.setIcon(QtGui.QIcon("icons/minus-light.svg"))
        self.collapseAction.setToolTip("Collaps all folders")
        self.addWidget(self.collapseAction)

        self.copyAction = ToolBarButton()
        self.copyAction.setIcon(QtGui.QIcon("icons/copy-light.svg"))
        self.copyAction.setToolTip("Clone selected folder")
        self.copyAction.setShortcut("Ctrl+C")
        self.addWidget(self.copyAction)

        self.removeAction = ToolBarButton()
        self.removeAction.setIcon(QtGui.QIcon("icons/remove-light.svg"))
        self.removeAction.setToolTip("Remove selected folder")
        self.removeAction.setShortcut("Del")
        self.addWidget(self.removeAction)

    @inject.params(menu='settings_menu')
    def onActionContextMenu(self, event, menu):
        menu.exec_(self.mapToGlobal(event))
