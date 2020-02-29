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
    settings = QtCore.pyqtSignal(object)
    search = QtCore.pyqtSignal(object)

    def __init__(self):
        super(DashboardDocumentPreviewToolbar, self).__init__()

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(ButtonDisabled(QtGui.QIcon("icons/plus-light"), None))

        self.spacer = QtWidgets.QWidget()
        self.spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.layout.addWidget(self.spacer)

        self.text_search = SearchField()
        self.text_search.returnPressed.connect(lambda event=None: self.search.emit(self.text_search))
        self.text_search.returnPressed.connect(self.text_search.clearFocus)
        self.layout.addWidget(self.text_search)

        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+f"), self.text_search)
        shortcut.activatedAmbiguously.connect(self.text_search.setFocus)
        shortcut.activated.connect(self.text_search.setFocus)
        shortcut.setEnabled(True)

        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Esc"), self.text_search)
        shortcut.activated.connect(lambda event=None: self.text_search.setText(None))
        shortcut.activatedAmbiguously.connect(self.text_search.clearFocus)
        shortcut.activated.connect(self.text_search.clearFocus)

        self.text_search.focusInEvent = self.on_search_focus_in
        self.text_search.focusOutEvent = self.on_search_focus_out

        tooltip = 'Create new note. The new note will be created as a part of the selected group or in the root group.'
        self.button_settings = PictureButtonFlat(QtGui.QIcon("icons/icons"), tooltip)
        self.button_settings.clicked.connect(lambda event=None: self.settings.emit(self.button_settings))
        self.button_settings.setFlat(True)
        self.layout.addWidget(self.button_settings)

        self.setLayout(self.layout)

    def on_search_focus_in(self, event):
        self.text_search.setAlignment(Qt.AlignCenter)
        self.spacer.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.spacer.setVisible(False)

    def on_search_focus_out(self, event):
        self.text_search.setAlignment(Qt.AlignLeft)
        self.spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.spacer.setVisible(True)

    def close(self):
        super(DashboardDocumentPreviewToolbar, self).deleteLater()
        return super(DashboardDocumentPreviewToolbar, self).close()
