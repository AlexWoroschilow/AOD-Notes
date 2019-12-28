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
import functools

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui

from .preview.list import PreviewScrollArea


class DashboardSplitter(QtWidgets.QSplitter):
    delete = QtCore.pyqtSignal(object)
    edit = QtCore.pyqtSignal(object)
    clicked = QtCore.pyqtSignal(object)
    fullscreen = QtCore.pyqtSignal(object)
    clone = QtCore.pyqtSignal(object)

    editor = None

    @inject.params(storage='storage', editor='notepad.editor')
    def __init__(self, index=None, storage=None, editor=None):
        super(DashboardSplitter, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.preview = PreviewScrollArea(self, [])
        self.preview.editAction.connect(self.previewClickedEvent)
        self.preview.fullscreenAction.connect(self.fullscreen.emit)
        self.preview.deleteAction.connect(self.delete.emit)
        self.preview.cloneAction.connect(self.clone.emit)

        self.preview.setMinimumWidth(550)
        self.preview.open(index)

        self.editor = editor
        self.editor.focus()

        self.addWidget(self.preview)
        self.addWidget(self.editor)

        self.setStretchFactor(0, 3)
        self.setStretchFactor(1, 1)
        self.show()

    def open(self, index=None):
        if index is None: return None
        self.preview.open(index)
        return self

    @inject.params(storage='storage')
    def previewSelected(self, index=None, storage=None):
        if self.preview is None: return None
        if index is None: return None
        return self.preview.open(index)

    @inject.params(storage='storage')
    def previewClickedEvent(self, index, storage):
        if self.editor is None: return None
        if index is None: return None
        self.editor.setIndex(index)
        self.clicked.emit(index)

    def close(self):
        super(DashboardSplitter, self).deleteLater()
        return super(DashboardSplitter, self).close()
