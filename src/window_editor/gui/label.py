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
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import Qt


class LabelTop(QtWidgets.QLabel):

    def __init__(self, parent=None):
        super(LabelTop, self).__init__(parent)
        self.setWordWrap(QtGui.QTextOption.WrapAnywhere)
        self.setObjectName('notesLabelTop')
        self.setWordWrap(True)


class LabelBottom(QtWidgets.QLabel):

    def __init__(self, parent=None):
        super(LabelBottom, self).__init__(parent)
        self.setObjectName('notesLabelBottom')
        self.setWordWrap(True)


class LabelDescription(QtWidgets.QPlainTextEdit):

    def __init__(self, parent=None):
        super(LabelDescription, self).__init__(parent)
        self.setWordWrapMode(QtGui.QTextOption.WrapAnywhere)
        self.setObjectName('notesLabelDescription')
        self.setMaximumHeight(80)
        self.setWordWrapMode(QtGui.QTextOption.WordWrap)

        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        size_policy = self.sizePolicy()
        size_policy.setVerticalPolicy(QtWidgets.QSizePolicy.Minimum)
        self.setSizePolicy(size_policy)

        self.setReadOnly(True)
                    
    def setText(self, text=None):
        super(LabelDescription, self).setPlainText(text)
        
