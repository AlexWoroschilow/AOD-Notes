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

from . import SettingsTitle
from . import WidgetSettings


class WidgetSettingsEditor(WidgetSettings):

    def __init__(self):
        super(WidgetSettingsEditor, self).__init__()

        self.layout = QtWidgets.QVBoxLayout()

        label = SettingsTitle('Editor settings')
        self.layout.addWidget(label)

        self.formatbar = QtWidgets.QCheckBox('Formatting toolbar is visible')
        self.layout.addWidget(self.formatbar)

        self.rightbar = QtWidgets.QCheckBox('Toolbar at the rith side is visible')
        self.layout.addWidget(self.rightbar)

        self.leftbar = QtWidgets.QCheckBox('Toolbar at the left side is visible')
        self.layout.addWidget(self.leftbar)

        self.setLayout(self.layout)

        self.show()
