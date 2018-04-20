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

from lib.plugin import Loader


class Loader(Loader):
    _widget = None

    @property
    def enabled(self):
        return True

    @inject.params(kernel='kernel')
    def boot(self, options=None, args=None, kernel=None):
        kernel.listen('window.notepad.formatbar', self._onWindowNotepadToolbar, 110)

    def _onWindowNotepadToolbar(self, event=None):
        self._editor, self._toolbar = event.data
        if self._editor is None or self._toolbar is None:
            raise 'Editor or Toolbar object can not be empty'

        self._widget = QtWidgets.QPushButton()
        self._widget.setIcon(QtGui.QIcon("icons/line.svg"))
        self._widget.setToolTip(self._editor.tr('Add a line'))
        self._widget.clicked.connect(self._onButtonPressed)
        self._widget.setMaximumWidth(35)
        self._widget.setFlat(True)

        self._toolbar.addWidget(self._widget)

    def _onButtonPressed(self, event=None):
        if self._editor is None or self._editor.text is None:
            msg = QtWidgets.QMessageBox(self._editor)
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setWindowTitle(self._editor.tr('Select the Note'))
            msg.setText(self._editor.tr('Please select the Note first'))
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            return msg.show()

        self._editor.text.insertHtml('<hr>< /hr>')
