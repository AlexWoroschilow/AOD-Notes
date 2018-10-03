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
from PyQt5 import QtWidgets

from .preview import NotePreviewWidget 
from builtins import range


class NotePreviewContainer(QtWidgets.QWidget):

    @inject.params(storage='storage')
    def __init__(self, path=None, storage=None):
        super(NotePreviewContainer, self).__init__()
        
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        for entity in storage.entities(path):
            widget = NotePreviewWidget(entity)
            self.layout.addWidget(widget)

        spacer = QtWidgets.QWidget();
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding);
        self.layout.addWidget(spacer)

    @inject.params(storage='storage')
    def resizeEvent(self, event=None, storage=None):
        self.setFixedWidth(event.size().width())
        
        for index in range(0, self.layout.count()):
            widget = self.layout.itemAt(index).widget()
            widget.setFixedWidth(event.size().width())
        return super(NotePreviewContainer, self).resizeEvent(event)


class TextView(QtWidgets.QScrollArea):

    def __init__(self, entity=None):
        super(TextView, self).__init__()
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setContentsMargins(0, 0, 0, 0)
        self.setWidgetResizable(True)

        self.preview = NotePreviewContainer(entity)
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
        return super(TextView, self)\
            .resizeEvent(*args, **kwargs)
