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


class WidgetSettingsSearch(WidgetSettings):

    def __init__(self):
        super(WidgetSettingsSearch, self).__init__()

        self.layout = QtWidgets.QGridLayout()
        self.layout.setAlignment(Qt.AlignLeft)

        self.layout.addWidget(SettingsTitle('Search engine settings'), 0, 0, 1, 5)
        self.layout.addWidget(QtWidgets.QLabel('Index location:'), 1, 0)

        self.searchIndex = QtWidgets.QLabel('...')
        self.layout.addWidget(self.searchIndex, 1, 1)

        self.layout.addWidget(QtWidgets.QLabel('Rebuild index:'), 2, 0)
        
        self.rebuild = QtWidgets.QPushButton('Start indexation process')
        self.rebuild.setToolTip("Rebuild the search index")
        self.rebuild.setFlat(True)
        self.layout.addWidget(self.rebuild, 2, 1)

        self.setLayout(self.layout)

        self.show()

