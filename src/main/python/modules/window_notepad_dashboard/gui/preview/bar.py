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
import functools

from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui

from .button import PictureButtonFlat
from .button import SearchField
from .button import ButtonDisabled


class DashboardDocumentPreviewToolbar(QtWidgets.QFrame):
    settingsAction = QtCore.pyqtSignal(object)
    searchAction = QtCore.pyqtSignal(object)

    def __init__(self):
        super(DashboardDocumentPreviewToolbar, self).__init__()

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(ButtonDisabled(QtGui.QIcon("icons/plus-light"), None))

        self.spacer = QtWidgets.QWidget()
        self.spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.layout.addWidget(self.spacer)

        self.search = SearchField()
        self.search.returnPressed.connect(self.searchEvent)
        self.layout.addWidget(self.search)

        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+f"), self.search)
        shortcut.activatedAmbiguously.connect(self.search.setFocus)
        shortcut.activated.connect(self.search.setFocus)
        shortcut.setEnabled(True)

        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Esc"), self.search)
        shortcut.activated.connect(lambda event=None: self.search.setText(None))
        shortcut.activatedAmbiguously.connect(self.search.clearFocus)
        shortcut.activated.connect(self.search.clearFocus)

        self.search.focusInEvent = self.searchFocusIn
        self.search.focusOutEvent = self.searchFocusOut

        tooltip = 'Create new note. The new note will be created as a part of the selected group or in the root group.'
        self.button_settings = PictureButtonFlat(QtGui.QIcon("icons/icons"), tooltip)
        self.button_settings.clicked.connect(self.settingsAction.emit)
        self.button_settings.setFlat(True)
        self.layout.addWidget(self.button_settings)

        self.setLayout(self.layout)

    def searchEvent(self, event=None):
        self.searchAction.emit(self.search.text())
        self.search.clearFocus()

    def searchFocusIn(self, event=None):
        self.search.setAlignment(Qt.AlignCenter)
        self.spacer.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.spacer.setVisible(False)

    def searchFocusOut(self, event=None):
        self.search.setAlignment(Qt.AlignLeft)
        self.spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.spacer.setVisible(True)

    def close(self):
        super(DashboardDocumentPreviewToolbar, self).deleteLater()
        return super(DashboardDocumentPreviewToolbar, self).close()
