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

from . import SettingsTitle
from . import SettingsSubtitle
from . import WidgetSettings
from . import WizardButton
from PyQt5.QtCore import Qt
from PyQt5 import QtCore


class WizardSettingsStorage(WidgetSettings):
    location = QtCore.pyqtSignal(object)

    @inject.params(config='config')
    def __init__(self, config=None):
        super(WizardSettingsStorage, self).__init__()

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(SettingsTitle('Where to store the notes'))

        self.storage = SettingsSubtitle(config.get('storage.location'))
        self.layout.addWidget(self.storage)

        self.button = WizardButton('Change')
        self.button.setToolTip("Clone selected preview")
        self.button.clicked.connect(self.chooseLocation)
        self.layout.addWidget(self.button)

        self.setLayout(self.layout)

        self.show()

    def chooseLocation(self, event=None):
        destination = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory", os.path.expanduser('~')))
        if destination is None: return None
        self.storage.setText(destination)
        self.location.emit(destination)
