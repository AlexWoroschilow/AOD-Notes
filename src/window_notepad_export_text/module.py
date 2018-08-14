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

from PyQt5 import QtGui
from PyQt5 import QtWidgets

from lib.plugin import Loader
from lib.widget.button import ToolBarButton


class Loader(Loader):

    @property
    def enabled(self):
        return True

    @inject.params(kernel='kernel')
    def boot(self, options=None, args=None, kernel=None):
        kernel.listen('window.notepad.leftbar', self._onWindowNotepadToolbar, 300)
        kernel.listen('window.notelist.toolbar', self._onWindowNotepadToolbar, 300)

    def _onWindowNotepadToolbar(self, event=None, storage=None):
        widget = ToolBarButton()
        widget.editor, widget.toolbar = event.data
        if widget.editor is None or widget.toolbar is None:
            raise 'Editor or Toolbar object can not be empty'
        
        widget.setIcon(QtGui.QIcon("icons/text.svg"))
        widget.setToolTip(widget.tr("Export document to text"))
        
        widget.clicked.connect(functools.partial(
            self._onNotepadExportText, widget=widget
        ))

        widget.toolbar.addWidget(widget)

    @inject.params(kernel='kernel')
    def _onNotepadExportText(self, event=None, widget=None, kernel=None):
        if widget.editor is None or widget.editor.note is None:
            return None

        selector = QtWidgets.QFileDialog()
        if not selector.exec_():
            return None

        for path in selector.selectedFiles():

            document = QtGui.QTextDocument()
            document.setHtml(widget.editor.note.text)

            if not os.path.exists(path):
                with open(path, 'w+') as stream:
                    stream.write(document.toPlainText())
                    stream.close()
                continue

            message = widget.editor.tr("Are you sure you want to overwrite the file '%s' ?" % path)
            reply = QtWidgets.QMessageBox.question(widget.editor, 'Message', message, QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.No:
                continue

            with open(path, 'w+') as stream:
                stream.write(document.toPlainText())
                stream.close()
