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

from PyQt5 import QtGui
from PyQt5 import QtWidgets

from lib.plugin import Loader


class Loader(Loader):
    _widget = None

    @property
    def enabled(self):
        """

        :return:
        """
        return True

    @inject.params(dispatcher='event_dispatcher')
    def boot(self, dispatcher=None):
        """

        :param dispatcher:.
        :return:.
        """
        dispatcher.add_listener('window.notepad.rightbar', self._onWindowNotepadToolbar, 100)

    def _onWindowNotepadToolbar(self, event=None, dispather=None, storage=None):
        """
        
        :param event: 
        :param dispather: 
        :param storage: 
        :return: 
        """
        self._editor, self._toolbar = event.data
        if self._editor is None or self._toolbar is None:
            raise 'Editor or Toolbar object can not be empty'

        self._widget = QtWidgets.QAction(QtGui.QIcon("icons/font-black.svg"), self._editor.tr("Change the text color to green"), self._toolbar)
        self._widget.setStatusTip(self._editor.tr("Change the text color to green"))
        self._widget.triggered.connect(self._onButtonPressed)

        self._toolbar.addAction(self._widget)

    @inject.params(dispatcher='event_dispatcher')
    def _onButtonPressed(self, event=None, dispatcher=None):
        """
        #7f7f7f
        :param event: 
        :param dispatcher: 
        :return: 
        """
        if self._editor is None or self._editor.text is None:
            msg = QtWidgets.QMessageBox(self._editor)
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setWindowTitle("Select the Note")
            msg.setText(self._editor.tr('Please select the Note first'))
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            return msg.show()

        color = QtGui.QColor.fromRgb(0, 0, 0)
        self._editor.text.setTextColor(color)
