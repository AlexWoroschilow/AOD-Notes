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

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore

from lib.plugin import Loader


class Loader(Loader):
    _widget = None

    @property
    def enabled(self):
        return True

    @inject.params(kernel='kernel')
    def boot(self, options=None, args=None, kernel=None):
        kernel.listen('window.notepad.rightbar', self._onWindowNotepadToolbar, 0)

    def _onWindowNotepadToolbar(self, event=None):
        self._editor, self._toolbar = event.data
        if self._editor is None or self._toolbar is None:
            raise 'Editor or Toolbar object can not be empty'

        self._widget = QtWidgets.QPushButton()
        self._widget.setIcon(QtGui.QIcon("icons/h1.svg"))
        self._widget.setToolTip(self._editor.tr('Add a header 1'))
        self._widget.clicked.connect(self._onButtonPressed)
        self._widget.setIconSize(QtCore.QSize(20,20))
        self._widget.setFlat(True)

        self._toolbar.addWidget(self._widget)

    def _onButtonPressed(self, event=None):
        if self._editor is None or self._editor.text is None:
            return None
        self._editor.text.setFontPointSize(20)
