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

from .list import PreviewScrollArea


class DashboardDocumentPreview(QtWidgets.QSplitter):
    fullscreenNoteAction = QtCore.pyqtSignal(object)
    editNoteAction = QtCore.pyqtSignal(object)
    saveNoteAction = QtCore.pyqtSignal(object)
    removeNoteAction = QtCore.pyqtSignal(object)
    cloneNoteAction = QtCore.pyqtSignal(object)
    renameNoteAction = QtCore.pyqtSignal(object)
    selectNoteAction = QtCore.pyqtSignal(object)
    moveNoteAction = QtCore.pyqtSignal(object)

    delete = QtCore.pyqtSignal(object)
    edit = QtCore.pyqtSignal(object)
    clicked = QtCore.pyqtSignal(object)
    fullscreen = QtCore.pyqtSignal(object)
    clone = QtCore.pyqtSignal(object)

    editor = None

    def __init__(self, index=None):
        super(DashboardDocumentPreview, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.preview = PreviewScrollArea()
        self.preview.editNoteAction.connect(self.editNoteAction.emit)
        self.preview.fullscreenNoteAction.connect(self.fullscreenNoteAction.emit)
        self.preview.removeNoteAction.connect(self.removeNoteAction.emit)
        self.preview.cloneNoteAction.connect(self.cloneNoteAction.emit)
        self.preview.selectNoteAction.connect(self.selectNoteAction.emit)

        self.preview.setMinimumWidth(410)

        container = inject.get_injector_or_die()
        if container is None: return None

        self.editor = container.get_instance('notepad.editor')
        self.editor.fullscreenNoteAction.connect(self.fullscreenNoteAction.emit)
        self.editor.renameNoteAction.connect(self.renameNoteAction.emit)
        self.editor.saveNoteAction.connect(self.saveNoteAction.emit)
        self.editor.moveNoteAction.connect(self.moveNoteAction.emit)

        self.editor.focus()

        self.addWidget(self.preview)
        self.addWidget(self.editor)

        self.setStretchFactor(0, 5)
        self.setStretchFactor(1, 2)

    def setDocuments(self, collection=None, selected=None):

        if collection is not None:
            self.preview.clear()
            for document in collection:
                self.preview.addItemRow(document, selected)
            self.preview.scrollTo(self.preview.currentIndex())

        if selected is not None:
            self.editor.open(selected)
            
        return self

    def open(self, index=None):
        pass

    def previewSelected(self, index=None, storage=None):
        pass

    def previewClickedEvent(self, index=None, storage=None):
        pass

    def close(self):
        super(DashboardDocumentPreview, self).deleteLater()
        return super(DashboardDocumentPreview, self).close()
