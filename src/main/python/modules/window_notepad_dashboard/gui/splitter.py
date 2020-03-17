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


class NotepadDashboardSplitter(QtWidgets.QSplitter):
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

    settingsAction = QtCore.pyqtSignal(object)
    searchAction = QtCore.pyqtSignal(object)

    saveAction = QtCore.pyqtSignal(object)

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
        self.panelLeft.moveAction.connect(self.moveAction.emit)
        self.panelLeft.groupAction.connect(self.groupAction.emit)

        self.panelRight = DashboardPanelRight()
        self.panelRight.fullscreenNoteAction.connect(self.fullscreenNoteAction.emit)
        self.panelRight.editNoteAction.connect(self.editNoteAction.emit)
        self.panelRight.removeNoteAction.connect(self.removeNoteAction.emit)
        self.panelRight.renameNoteAction.connect(self.renameNoteAction.emit)
        self.panelRight.cloneNoteAction.connect(self.cloneNoteAction.emit)
        self.panelRight.selectNoteAction.connect(self.selectNoteAction.emit)
        self.panelRight.saveNoteAction.connect(self.saveNoteAction.emit)
        self.panelRight.moveNoteAction.connect(self.moveNoteAction.emit)
        self.panelRight.settingsAction.connect(self.settingsAction.emit)
        self.panelRight.searchAction.connect(self.searchAction.emit)

        self.addWidget(self.panelLeft)
        self.addWidget(self.panelRight)

        self.setCollapsible(0, True)
        self.setCollapsible(1, False)

        self.setStretchFactor(0, 1)
        self.setStretchFactor(1, 2)

    def setFolders(self, collection, selected):
        self.panelLeft.setFolders(collection, selected)
        return self

    def setDocuments(self, collection, selected):
        self.panelRight.setDocuments(collection, selected)
        return self

    def close(self):
        super(NotepadDashboardSplitter, self).deleteLater()
        return super(NotepadDashboardSplitter, self).close()
