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
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt


class NotePreviewTitle(QtWidgets.QLabel):

    def __init__(self, text):
        super(NotePreviewTitle, self).__init__(text)
        self.setMaximumWidth(150)
        self.setWordWrap(True)


class Description(QtWidgets.QLabel):

    def __init__(self, parent=None):
        super(Description, self).__init__(parent)
        self.setWordWrap(True)


class NotePreviewDescription(QtWidgets.QWidget):

    def __init__(self, content):
        super(NotePreviewDescription, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)
        
        root = os.path.dirname(os.path.abspath(__file__))
        with open('{}/css/{}.qss'.format(root, self.__class__.__name__), 'r') as stream:
            self.setStyleSheet(stream.read())

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)

        description = Description(content)
        self.layout.addWidget(description)

        self.setLayout(self.layout)
