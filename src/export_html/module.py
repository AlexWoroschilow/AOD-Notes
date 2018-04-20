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
from PyQt5 import QtCore

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
    def boot(self, options=None, args=None, dispatcher=None):
        """

        :param dispatcher:.
        :return:.
        """
        dispatcher.add_listener('window.notepad.leftbar', self._onWindowNotepadToolbar, 200)
        dispatcher.add_listener('window.notelist.toolbar', self._onWindowNotepadToolbar, 200)

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

        self._widget = QtWidgets.QPushButton()
        self._widget.setIcon(QtGui.QIcon("icons/html.svg"))
        self._widget.setToolTip("Export document to HTML")
        self._widget.clicked.connect(self._onNotepadExportHtml)
        self._widget.setFlat(True)

        self._toolbar.addWidget(self._widget)

    @inject.params(dispatcher='event_dispatcher')
    def _onNotepadExportHtml(self, event=None, dispatcher=None):
        """

        :param event: 
        :param dispatcher: 
        :return: 
        """
        if self._editor is None or self._editor.entity is None:
            return None

        selector = QtWidgets.QFileDialog()
        if not selector.exec_():
            return None

        for path in selector.selectedFiles():

            document = QtGui.QTextDocument()
            document.setHtml(self._editor.entity.text)
            encoding = QtCore.QByteArray(bytes('UTF8', 'utf-8'))

            if not os.path.exists(path):
                with open(path, 'w+') as stream:
                    stream.write(document.toHtml(encoding=encoding))
                    stream.close()
                continue

            message = self._editor.tr("Are you sure you want to overwrite the file '%s' ?" % path)
            reply = QtWidgets.QMessageBox.question(self._editor, 'Message', message, QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.No:
                continue

            with open(path, 'w+') as stream:
                stream.write(document.toHtml(encoding=encoding))
                stream.close()
