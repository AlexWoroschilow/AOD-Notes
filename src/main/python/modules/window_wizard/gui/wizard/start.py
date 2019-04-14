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

from . import SettingsTitle
from . import WidgetSettings
from PyQt5.QtCore import Qt
from PyQt5 import QtCore


class WizardButtonStart(QtWidgets.QPushButton):
    def __init__(self, name):
        super(WizardButtonStart, self).__init__(name)


class WizardSettingsStart(WidgetSettings):
    start = QtCore.pyqtSignal(object)

    def __init__(self):
        super(WizardSettingsStart, self).__init__()

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)

        self.button = WizardButtonStart('Start')
        self.button.setToolTip("Save changes and start use the programm")
        self.button.clicked.connect(self.start.emit)
        self.layout.addWidget(self.button)

        self.setLayout(self.layout)

        self.show()
