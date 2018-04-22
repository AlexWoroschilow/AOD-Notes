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
from PyQt5 import QtCore


class Loader(Loader):

    @property
    def enabled(self):
        return True

    @inject.params(kernel='kernel')
    def boot(self, options=None, args=None, kernel=None):
        kernel.listen('window.notepad.rightbar', self._onWindowNotepadToolbar, 100)

    def _onWindowNotepadToolbar(self, event=None, dispather=None, storage=None):
        widget = QtWidgets.QPushButton()
        widget.editor, widget.toolbar = event.data
        if widget.editor is None or widget.toolbar is None:
            raise 'Editor or Toolbar object can not be empty'

        widget.setIcon(QtGui.QIcon("icons/font-red.svg"))
        widget.setToolTip(widget.tr("Change the text color to red"))
        widget.setIconSize(QtCore.QSize(20, 20))
        widget.setFlat(True)
        
        widget.clicked.connect(functools.partial(
            self._onButtonPressed, widget=widget
        ))

        widget.toolbar.addWidget(widget)

    def _onButtonPressed(self, event=None, widget=None):
        if widget.editor is not None and widget.editor.text is not None:
            color = QtGui.QColor.fromRgb(127, 0, 0)
            widget.editor.text.setTextColor(color)
