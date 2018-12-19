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


class NotePreviewTitle(QtWidgets.QLabel):

    def __init__(self, text):
        super(NotePreviewTitle, self).__init__(text)
        self.setMaximumWidth(150)
        self.setWordWrap(True)


class NotePreviewDescription(QtWidgets.QLabel):

    def __init__(self, parent=None):
        super(NotePreviewDescription, self).__init__(parent)
        self.setWordWrap(True)


class NotePreviewWidget(QtWidgets.QWidget):

    def __init__(self, name, content):
        super(NotePreviewWidget, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)
        
        label = QtWidgets.QGridLayout()
        label.setContentsMargins(0, 10, 0, 10)
        
        title = NotePreviewTitle(name)
        label.addWidget(title, 0, 0, 1, 1)

        description = NotePreviewDescription()
        label.addWidget(description, 0, 1, 10, 5)
        
        description.setText(content)
        
        self.setLayout(label)
