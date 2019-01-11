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

from .preview import NotePreviewDescription 


class NotePreviewContainer(QtWidgets.QWidget):

    def __init__(self):
        super(NotePreviewContainer, self).__init__()
        self.setObjectName('NotePreviewContainer')
        self.setContentsMargins(0, 0, 0, 0)
        
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)

    def addPreview(self, name, content):
        widget = NotePreviewDescription(content)
        self.layout.addWidget(widget)


class FolderViewWidget(QtWidgets.QScrollArea):

    def __init__(self):
        super(FolderViewWidget, self).__init__()
        self.setObjectName('FolderViewWidget')
        self.setContentsMargins(0, 0, 0, 0)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setContentsMargins(0, 0, 0, 0)
        self.setWidgetResizable(True)

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.preview = NotePreviewContainer()
        self.setWidget(self.preview)
        
        self._entity = None

    def zoomIn(self, value):
        if self.text is None:
            return None
        self.text.zoomIn(value)
        
    def zoomOut(self, value):
        if self.text is None:
            return None
        self.text.zoomOut(value)

    def resizeEvent(self, *args, **kwargs):
        self.preview.resizeEvent(*args, **kwargs)
        return super(FolderViewWidget, self)\
            .resizeEvent(*args, **kwargs)
        
    def addPreview(self, name, content):
        self.preview.addPreview(name, content)        

