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
from PyQt5.QtCore import Qt
from PyQt5 import QtCore


class WizardSettings(QtWidgets.QGroupBox):
    columns = 1

    def __init__(self):
        super(WizardSettings, self).__init__()
        self.setAutoFillBackground(True)
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.setLayout(self.layout)

    def addWidget(self, widget):
        self.layout.addWidget(widget)


class WizardDashboardScrollArea(QtWidgets.QScrollArea):
    start = QtCore.pyqtSignal(object)

    def __init__(self):
        super(WizardDashboardScrollArea, self).__init__()
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setAlignment(Qt.AlignCenter)

        self.setContentsMargins(0, 0, 0, 0)

        self.container = WizardSettings()
        self.setWidgetResizable(True)
        self.setWidget(self.container)

    def addWidget(self, widget):
        self.container.addWidget(widget)
