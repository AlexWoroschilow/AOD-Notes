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


class WidgetSettingsStorage(WidgetSettings):

    def __init__(self):
        super(WidgetSettingsStorage, self).__init__()

        self.layout = QtWidgets.QVBoxLayout()

        label = SettingsTitle('Storage settings')
        self.layout.addWidget(label)
        
        self.layout.addSpacing(1)

        self.location = QtWidgets.QPushButton('Change')
        self.location.setToolTip("Clone selected folder")
        self.layout.setAlignment(Qt.AlignLeft)
        self.location.setFlat(True)
        self.layout.addWidget(self.location)
        
        self.layout.addSpacing(1)

        self.setLayout(self.layout)

        self.show()
