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

from .preview.scroll import PreviewScrollArea
from .document import HtmlDocument


class DashboardSplitter(QtWidgets.QSplitter):
    delete = QtCore.pyqtSignal(object)
    clicked = QtCore.pyqtSignal(object)
    fullscreen = QtCore.pyqtSignal(object)
    clone = QtCore.pyqtSignal(object)

    editor = None

    @inject.params(storage='storage', editor='notepad.editor')
    def __init__(self, index=None, storage=None, editor=None):
        super(DashboardSplitter, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.preview = PreviewScrollArea(self)
        self.preview.edit.connect(self.previewClickedEvent)
        self.preview.fullscreen.connect(self.fullscreen.emit)
        self.preview.delete.connect(self.delete.emit)
        self.preview.clone.connect(self.clone.emit)

        parent = storage.fileDir(index)
        self.preview.open(storage.entitiesByFileType(parent))
        self.preview.scrollTo((index, None))

        self.editor = editor
        self.editor.setMinimumWidth(500)
        self.editor.focus()

        self.addWidget(self.preview)
        self.addWidget(self.editor)

        self.setStretchFactor(1, 1)
        self.setStretchFactor(2, 2)
        self.show()

    def scrollTo(self, index=None):
        if index is None:
            return None

        self.preview.scrollTo((index, None))

    @inject.params(storage='storage')
    def previewSelected(self, event=None, storage=None):
        if self.preview is None:
            return None

        index, document = event
        if index is None: return None

        document = self.preview.getDocumentByIndex(index)
        if index is not None and document is not None:
            return self.preview.scrollTo((index, document))

        parent = storage.fileDir(index)
        if parent is None: return None

        self.preview.open(storage.entitiesByFileType(parent))
        document = self.preview.getDocumentByIndex(index)
        if index is not None and document is not None:
            return self.preview.scrollTo((index, document))

    @inject.params(storage='storage')
    def previewClickedEvent(self, event, storage):
        if self.editor is None:
            return None

        index, document = event
        if document is None or index is None:
            return None

        self.editor.setIndex(index)
        self.editor.setDocument(document)

        self.clicked.emit(index)

    def close(self):
        super(DashboardSplitter, self).deleteLater()
        return super(DashboardSplitter, self).close()
