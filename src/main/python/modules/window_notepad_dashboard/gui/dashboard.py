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
    cloneNoteAction = QtCore.pyqtSignal(object)
    editNoteAction = QtCore.pyqtSignal(object)
    saveNoteAction = QtCore.pyqtSignal(object)
    menuAction = QtCore.pyqtSignal(object, object)

    edit = QtCore.pyqtSignal(object)
    delete = QtCore.pyqtSignal(object)
    clone = QtCore.pyqtSignal(object)

    created = QtCore.pyqtSignal(object)
    removed = QtCore.pyqtSignal(object)
    updated = QtCore.pyqtSignal(object)

    note_new = QtCore.pyqtSignal(object)
    note_import = QtCore.pyqtSignal(object)
    group_new = QtCore.pyqtSignal(object)

    settings = QtCore.pyqtSignal(object)

    saveAction = QtCore.pyqtSignal(object)
    search = QtCore.pyqtSignal(object)

    storage = QtCore.pyqtSignal(object)
    storage_changed = QtCore.pyqtSignal(object)

    fullscreen = QtCore.pyqtSignal(object)

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
        self.splitter.cloneNoteAction.connect(self.cloneNoteAction.emit)
        self.splitter.saveNoteAction.connect(self.saveNoteAction.emit)
        self.splitter.menuAction.connect(self.menuAction.emit)

        self.layout().addWidget(self.splitter)
        self.layout().addWidget(self.toolbar)

    def note(self, index=None, storage=None):
        return self

    def close(self):
        super(NotepadDashboard, self).deleteLater()
        return super(NotepadDashboard, self).close()
