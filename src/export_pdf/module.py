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
from PyQt5 import QtGui

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
        dispatcher.add_listener('window.notepad.toolbar', self._onWindowNotepadToolbar)

    def _onWindowNotepadToolbar(self, event=None, dispather=None, storage=None):
        """
        
        :param event: 
        :param dispather: 
        :param storage: 
        :return: 
        """
        self._editor, self._toolbar = event.data

        if self._editor is None or self._toolbar is None:
            raise 'Editor or Toolbar object can note be empty'

        self._widget = QtWidgets.QAction(QtGui.QIcon("icons/pdf.svg"), self._editor.tr("Save as pdf"), self._toolbar)
        self._widget.setStatusTip(self._editor.tr("Export document as PDF"))
        self._widget.triggered.connect(self._onNoteExportPdf)
        self._widget.setShortcut("Ctrl+Shift+P")

        self._toolbar.addSeparator()
        self._toolbar.addAction(self._widget)

    @inject.params(dispatcher='event_dispatcher')
    def _onNoteExportPdf(self, event=None, dispatcher=None):
        """

        :param event: 
        :param dispatcher: 
        :return: 
        """
        entity = self._editor.entity
        if entity is None:
            return None

        print(entity)
