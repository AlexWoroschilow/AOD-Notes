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
from PyQt5.QtCore import Qt

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets


class TextWriter(QtWidgets.QScrollArea):
    def __init__(self, parent=None):
        """

        :param parent: 
        """
        super(TextWriter, self).__init__(parent)

        self.text = TextEditor(self)

        self.setWidgetResizable(True)
        self.setWidget(self.text)

        # Align the scrollArea's widget in the center
        self.setAlignment(Qt.AlignHCenter)
        self.setStyleSheet("background-color: #A0A0A0;")
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)


class TextEditor(QtWidgets.QTextEdit):
    def __init__(self, parent=None):
        super(TextEditor, self).__init__(parent)

        self.setAcceptDrops(True)
        self.setAcceptRichText(True)
        self.setWordWrapMode(QtGui.QTextOption.WordWrap)
        self.setViewportMargins(40, 20, 20, 20)

        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.setStyleSheet("background-color: #FFFFFF;")
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)


class NameEditor(QtWidgets.QLineEdit):
    def __init__(self, parent=None):
        """

        :param parent: 
        """
        super(NameEditor, self).__init__(parent)
        self.setPlaceholderText('Write a title here...')

        font = self.font()
        font.setPixelSize(24)
        self.setFont(font)
