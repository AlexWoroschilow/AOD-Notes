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
from PyQt5 import QtCore

from PyQt5.QtCore import Qt

from .preview import NotePreviewDescription 


class NotePreviewContainer(QtWidgets.QWidget):

    edit = QtCore.pyqtSignal(object)
    delete = QtCore.pyqtSignal(object)
    clone = QtCore.pyqtSignal(object)

    def __init__(self):
        super(NotePreviewContainer, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)
        
        self.layout = QtWidgets.QGridLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)
        self.i = 0
        self.j = 0

    def addPreview(self, index):
        
        widget = NotePreviewDescription(index)
        widget.edit.connect(self.edit.emit)
        widget.delete.connect(self.delete.emit)
        widget.clone.connect(self.clone.emit)
        self.layout.addWidget(widget, self.i, self.j, 1, 1)
        
        self.j += 1
        if self.j > 1:
            self.i += 1
            self.j = 0


class FoldersScrollArea(QtWidgets.QScrollArea):

    edit = QtCore.pyqtSignal(object)
    delete = QtCore.pyqtSignal(object)
    clone = QtCore.pyqtSignal(object)

    def __init__(self):
        super(FoldersScrollArea, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setContentsMargins(0, 0, 0, 0)
        self.setWidgetResizable(True)

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.preview = NotePreviewContainer()
        self.preview.edit.connect(self.edit.emit)
        self.preview.delete.connect(self.delete.emit)
        self.preview.clone.connect(self.clone.emit)
        
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

    def addPreview(self, index):
        self.preview.addPreview(index)

