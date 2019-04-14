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
import secrets

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5 import QtCore

from . import SettingsTitle
from . import SettingsSubtitle
from . import WidgetSettings
from . import WizardButton


class WizardSettingsCryptography(WidgetSettings):
    password = QtCore.pyqtSignal(object)

    @inject.params(config='config')
    def __init__(self, config=None):
        super(WizardSettingsCryptography, self).__init__()

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(SettingsTitle('Cryptography settings'))
        self.textarea = QtWidgets.QLineEdit('...')
        self.textarea.setReadOnly(True)
        self.layout.addWidget(self.textarea)

        self.algorithm = SettingsSubtitle('Algorithm: AES-256')
        self.algorithm.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.algorithm)

        self.button = WizardButton('Generate new password')
        self.button.setToolTip("Clone selected preview")
        self.button.clicked.connect(lambda x: self.password.emit(secrets.token_hex(32)))
        self.layout.addWidget(self.button)

        self.setLayout(self.layout)
        self.password.connect(self.applyPasword)

        self.password.emit(config.get('cryptography.password', secrets.token_hex(32)))

        self.show()

    def applyPasword(self, password=None):
        if len(password) == 32:
            self.algorithm.setText('Algorithm: AES-256')
        if len(password) == 24:
            self.algorithm.setText('Algorithm: AES-196')
        if len(password) == 16:
            self.algorithm.setText('Algorithm: AES-128')

        self.textarea.setText(password)
