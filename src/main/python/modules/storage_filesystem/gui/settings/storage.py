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
import os
import inject

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5 import QtCore

from . import SettingsTitle
from . import WidgetSettings
from . import PictureButton

from PyQt5 import QtGui


class WidgetSettingsStorage(WidgetSettings):
    locationAction = QtCore.pyqtSignal(object)

    @inject.params(config='config')
    def __init__(self, config):
        super(WidgetSettingsStorage, self).__init__()

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setAlignment(Qt.AlignLeft)

        self.layout.addWidget(SettingsTitle('Shortcuts'))

        self.layout.addWidget(QtWidgets.QLabel('Ctl+N - create new note'))
        self.layout.addWidget(QtWidgets.QLabel('Ctl+R - create new group'))
        self.layout.addWidget(QtWidgets.QLabel('Ctl+I - import note from a file'))
        self.layout.addWidget(QtWidgets.QLabel('Ctl+F - start fulltext search'))

        spacer = QtWidgets.QWidget()
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.layout.addWidget(spacer)

        location = config.get('storage.location')
        location = location.replace(os.path.expanduser('~'), '~')

        self.layout.addWidget(SettingsTitle('Storage'))

        self.location = PictureButton(' {}'.format(location))
        self.location.clicked.connect(self.locationAction.emit)
        self.location.setIcon(QtGui.QIcon("icons/save"))
        self.location.setToolTip("Clone selected preview")
        self.location.setFlat(True)
        self.layout.addWidget(self.location)

        self.setLayout(self.layout)

    def quit(self):
        self.thread.exit()
