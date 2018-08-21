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
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets


class WidgetSettings(QtWidgets.QWidget):

    def __init__(self):
        super(WidgetSettings, self).__init__()
        self.setAutoFillBackground(True)
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.setGeometry(0, 0, 300, 100)        
        self.setObjectName('WidgetSettings')
        
    def addWidget(self, widget):
        self.layout.addWidget(widget)
        
        spacer = QtWidgets.QWidget();
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred);
        self.layout.addWidget(spacer)


class SettingsScrollArea(QtWidgets.QScrollArea):

    def __init__(self, parent=None):
        super(SettingsScrollArea, self).__init__(parent)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setAlignment(Qt.AlignHCenter)
        self.setObjectName('SettingsScrollArea')

        self.setContentsMargins(0, 0, 0, 0)

        self.container = WidgetSettings()
        self.setWidgetResizable(True)
        self.setWidget(self.container)

    def addWidget(self, widget):
        self.container.addWidget(widget)
