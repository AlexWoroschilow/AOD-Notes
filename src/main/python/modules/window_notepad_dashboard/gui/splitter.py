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

from .panel import DashboardPanelLeft
from .panel import DashboardPanelRight
from .preview.list import PreviewScrollArea


class NotepadDashboardSplitter(QtWidgets.QSplitter):
    newNoteAction = QtCore.pyqtSignal(object)
    importNoteAction = QtCore.pyqtSignal(object)
    newGroupAction = QtCore.pyqtSignal(object)
    fullscreenNoteAction = QtCore.pyqtSignal(object)
    removeNoteAction = QtCore.pyqtSignal(object)
    cloneNoteAction = QtCore.pyqtSignal(object)
    editNoteAction = QtCore.pyqtSignal(object)
    saveNoteAction = QtCore.pyqtSignal(object)
    renameAction = QtCore.pyqtSignal(object)
    menuAction = QtCore.pyqtSignal(object, object)

    settings = QtCore.pyqtSignal(object)

    saveAction = QtCore.pyqtSignal(object)
    search = QtCore.pyqtSignal(object)

    storage = QtCore.pyqtSignal(object)
    storage_changed = QtCore.pyqtSignal(object)

    editor = None

    def __init__(self):
        super(NotepadDashboardSplitter, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setContentsMargins(0, 0, 0, 0)

        self.panelLeft = DashboardPanelLeft()
        self.panelLeft.newNoteAction.connect(self.newNoteAction.emit)
        self.panelLeft.importNoteAction.connect(self.importNoteAction.emit)
        self.panelLeft.newGroupAction.connect(self.newGroupAction.emit)
        self.panelLeft.menuAction.connect(self.menuAction.emit)
        self.panelLeft.renameAction.connect(self.renameAction.emit)

        self.panelRight = DashboardPanelRight()
        self.panelRight.fullscreenNoteAction.connect(self.fullscreenNoteAction.emit)
        self.panelRight.fullscreenNoteAction.connect(lambda x: print(x))
        self.panelRight.editNoteAction.connect(self.editNoteAction.emit)
        self.panelRight.removeNoteAction.connect(self.removeNoteAction.emit)
        self.panelRight.cloneNoteAction.connect(self.cloneNoteAction.emit)
        self.panelRight.saveNoteAction.connect(self.saveNoteAction.emit)

        self.addWidget(self.panelLeft)
        self.addWidget(self.panelRight)

        self.setCollapsible(0, True)
        self.setCollapsible(1, False)

        self.setStretchFactor(0, 1)
        self.setStretchFactor(1, 2)

    def note(self, index=None, storage=None):
        return self

    def close(self):
        super(NotepadDashboardSplitter, self).deleteLater()
        return super(NotepadDashboardSplitter, self).close()


class DashboardDocumentPreview(QtWidgets.QSplitter):
    delete = QtCore.pyqtSignal(object)
    edit = QtCore.pyqtSignal(object)
    clicked = QtCore.pyqtSignal(object)
    fullscreen = QtCore.pyqtSignal(object)
    clone = QtCore.pyqtSignal(object)

    editor = None

    @inject.params(store='store')
    def __init__(self, index=None, store=None):
        super(DashboardDocumentPreview, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.preview = PreviewScrollArea()
        self.preview.setMinimumWidth(410)

        # self.preview.editAction.connect(self.previewClickedEvent)
        # self.preview.fullscreenAction.connect(self.fullscreen.emit)
        # self.preview.deleteAction.connect(self.delete.emit)
        # self.preview.cloneAction.connect(self.clone.emit)

        container = inject.get_injector_or_die()
        if container is None: return None

        self.editor = container.get_instance('notepad.editor')
        self.editor.focus()

        self.addWidget(self.preview)
        self.addWidget(self.editor)

        self.setStretchFactor(0, 5)
        self.setStretchFactor(1, 2)

        state = store.get_state()
        if state is None: return None
        store.subscribe(self.refresh)

    @inject.params(store='store')
    def refresh(self, store=None):

        state = store.get_state()
        if state is None: return None

        self.preview.clear()
        for document in state.documents:
            item, widget = self.preview.getItemNew(document)
            self.preview.addItem(item)
            self.preview.setItemWidget(item, widget)

        self.editor.open(state.document)

    def open(self, index=None):
        pass

    def previewSelected(self, index=None, storage=None):
        pass

    def previewClickedEvent(self, index=None, storage=None):
        pass

    def close(self):
        super(DashboardDocumentPreview, self).deleteLater()
        return super(DashboardDocumentPreview, self).close()
