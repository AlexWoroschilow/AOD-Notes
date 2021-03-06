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

from PyQt5 import QtCore
from PyQt5 import QtWidgets

from .bar import NotepadDashboardToolbar
from .splitter import NotepadDashboardSplitter


class NotepadDashboard(QtWidgets.QWidget):
    newNoteAction = QtCore.pyqtSignal(object)
    importNoteAction = QtCore.pyqtSignal(object)
    newGroupAction = QtCore.pyqtSignal(object)
    fullscreenNoteAction = QtCore.pyqtSignal(object)
    removeNoteAction = QtCore.pyqtSignal(object)
    renameNoteAction = QtCore.pyqtSignal(object)
    cloneNoteAction = QtCore.pyqtSignal(object)
    editNoteAction = QtCore.pyqtSignal(object)
    saveNoteAction = QtCore.pyqtSignal(object)
    selectNoteAction = QtCore.pyqtSignal(object)
    renameAction = QtCore.pyqtSignal(object)
    menuAction = QtCore.pyqtSignal(object, object)
    moveAction = QtCore.pyqtSignal(object)
    groupAction = QtCore.pyqtSignal(object)
    moveNoteAction = QtCore.pyqtSignal(object)
    updateAction = QtCore.pyqtSignal()
    settingsAction = QtCore.pyqtSignal(object)
    searchAction = QtCore.pyqtSignal(object)
    createdAction = QtCore.pyqtSignal(object)
    removedAction = QtCore.pyqtSignal(object)
    updatedAction = QtCore.pyqtSignal(object)

    def __init__(self):
        super(NotepadDashboard, self).__init__()
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.toolbar = NotepadDashboardToolbar()
        self.toolbar.newNoteAction.connect(self.newNoteAction.emit)
        self.toolbar.importNoteAction.connect(self.importNoteAction.emit)
        self.toolbar.newGroupAction.connect(self.newGroupAction.emit)

        self.splitter = NotepadDashboardSplitter()
        self.splitter.fullscreenNoteAction.connect(self.fullscreenNoteAction.emit)
        self.splitter.editNoteAction.connect(self.editNoteAction.emit)
        self.splitter.removeNoteAction.connect(self.removeNoteAction.emit)
        self.splitter.renameNoteAction.connect(self.renameNoteAction.emit)
        self.splitter.cloneNoteAction.connect(self.cloneNoteAction.emit)
        self.splitter.saveNoteAction.connect(self.saveNoteAction.emit)
        self.splitter.selectNoteAction.connect(self.selectNoteAction.emit)
        self.splitter.renameAction.connect(self.renameAction.emit)
        self.splitter.moveNoteAction.connect(self.moveNoteAction.emit)
        self.splitter.menuAction.connect(self.menuAction.emit)
        self.splitter.moveAction.connect(self.moveAction.emit)
        self.splitter.groupAction.connect(self.groupAction.emit)
        self.splitter.settingsAction.connect(self.settingsAction.emit)
        self.splitter.searchAction.connect(self.searchAction.emit)

        self.layout().addWidget(self.splitter)
        self.layout().addWidget(self.toolbar)

    def setProgress(self, value):
        self.toolbar.setProgress(value)
        return self

    def model(self):
        return self.splitter.panelLeft.tree.model()

    def setFolderCurrent(self, selected=None):
        if selected is None: return self
        self.splitter.setFolderCurrent(selected)
        return self

    def setFolders(self, collection, selected):
        self.splitter.setFolders(collection, selected)
        return self

    def setDocuments(self, collection, selected):
        self.splitter.setDocuments(collection, selected)
        return self

    def note(self, index=None, storage=None):
        return self

    def close(self):
        super(NotepadDashboard, self).deleteLater()
        return super(NotepadDashboard, self).close()
