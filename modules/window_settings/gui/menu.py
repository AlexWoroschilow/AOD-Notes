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


class SettingsMenu(QtWidgets.QWidgetAction):

    def __init__(self, parent):
        QtWidgets.QWidgetAction.__init__(self, parent)
        
        layout = QtWidgets.QGridLayout()

        self.editorName = QtWidgets.QCheckBox('Show name field')
        layout.addWidget(self.editorName, 0, 1)
        
        self.editorToolbarFormat = QtWidgets.QCheckBox('Show format bar')
        layout.addWidget(self.editorToolbarFormat, 1, 1)
        
        self.editorToolbarRight = QtWidgets.QCheckBox('Show right toolbar (editor)')
        layout.addWidget(self.editorToolbarRight, 2, 1)
        
        self.editorToolbarLeft = QtWidgets.QCheckBox('Show left toolbar (editor)')
        layout.addWidget(self.editorToolbarLeft, 3, 1)

        self.tags = QtWidgets.QCheckBox('Show keywords')
        layout.addWidget(self.tags, 4, 1)
        
        self.toolbar = QtWidgets.QCheckBox('Show folders toolbar')
        layout.addWidget(self.toolbar, 5, 1)
        
        container = QtWidgets.QWidget()
        container.setContentsMargins(0, 0, 0, 0)
        container.setLayout(layout)
        
        self.setDefaultWidget(container)
