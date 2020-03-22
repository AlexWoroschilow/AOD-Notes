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
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from . import SettingsTitle
from . import WidgetSettings
from . import PictureButton

from PyQt5 import QtCore
from PyQt5 import QtGui


class WidgetSettingsSearch(WidgetSettings):
    indexAction = QtCore.pyqtSignal(object)

    def __init__(self):
        super(WidgetSettingsSearch, self).__init__()

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setAlignment(Qt.AlignLeft)

        self.layout().addWidget(SettingsTitle('Fulltext search'))

        self.rebuild = PictureButton('update search index')
        self.layout().addWidget(self.rebuild)

        self.rebuild.setIcon(QtGui.QIcon("icons/refresh"))
        self.rebuild.setToolTip("Rebuild the search index")
        self.rebuild.clicked.connect(self.indexAction.emit)
        self.rebuild.setFlat(True)
