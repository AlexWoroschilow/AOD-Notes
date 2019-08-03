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
    clone = QtCore.pyqtSignal(object)

    @inject.params(storage='storage')
    def __init__(self, index=None, storage=None):
        super(DashboardSplitter, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.preview = PreviewScrollArea(self)
        self.preview.edit.connect(self.previewClickedEvent)
        self.preview.delete.connect(self.delete.emit)
        self.preview.clone.connect(self.clone.emit)
        self.preview.setMinimumWidth(400)

        parent = storage.fileDir(index)
        self.preview.open(storage.entitiesByFileType(parent))
        self.preview.scrollTo((index, None))

        self.editor = inject.instance('notepad.editor')
        self.editor.setMinimumWidth(500)
        content = storage.fileContent(index)
        self.editor.setDocument(HtmlDocument(content))
        self.editor.setIndex(index)
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
        index, document = event
        if self.preview is None or index is None:
            return None

        document = self.preview.getDocumentByIndex(index)
        if document is None or not document:
            parent = storage.fileDir(index)
            self.preview.open(storage.entitiesByFileType(parent))
            document = self.preview.getDocumentByIndex(index)
        return self.preview.edit.emit((index, document))

    def previewClickedEvent(self, event):
        index, document = event
        if index is None or document is None:
            return None

        if self.editor is None:
            return None

        self.editor.setDocument(document)
        self.editor.setIndex(index)

        self.clicked.emit(index)

    def close(self):
        super(DashboardSplitter, self).deleteLater()
        return super(DashboardSplitter, self).close()
