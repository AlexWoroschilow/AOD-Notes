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
from PyQt5.QtCore import Qt

from PyQt5 import QtWidgets
from PyQt5 import QtGui


class TextEditor(QtWidgets.QTextEdit):

    def __init__(self, parent=None):
        super(TextEditor, self).__init__(parent)
        self.setObjectName('editorTextEditor')
        self.setWordWrapMode(QtGui.QTextOption.WordWrap)
        self.setViewportMargins(40, 20, 20, 20)
        self.setAcceptRichText(True)
        self.setAcceptDrops(True)
        self.setFontPointSize(14)

        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self._entity = None
        
    @property
    def entity(self):
        return self._entity

    @entity.setter
    def entity(self, value):
        self.entity = value

