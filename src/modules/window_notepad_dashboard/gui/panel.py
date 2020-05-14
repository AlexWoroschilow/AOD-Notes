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

from .folder.tree import DashboardFolderTree

from .preview.bar import DashboardDocumentPreviewToolbar
from .preview.splitter import DashboardDocumentPreview


class DashboardPanelLeft(QtWidgets.QFrame):
    newNoteAction = QtCore.pyqtSignal(object)
    importNoteAction = QtCore.pyqtSignal(object)
    newGroupAction = QtCore.pyqtSignal(object)
    renameAction = QtCore.pyqtSignal(object)
    menuAction = QtCore.pyqtSignal(object, object)
    moveAction = QtCore.pyqtSignal(object)
    groupAction = QtCore.pyqtSignal(object)

    def __init__(self):
        super(DashboardPanelLeft, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.tree = DashboardFolderTree()
        self.tree.menuAction.connect(self.menuAction.emit)
        self.tree.renameAction.connect(self.renameAction.emit)
        self.tree.moveAction.connect(self.moveAction.emit)
        self.tree.groupAction.connect(self.groupAction.emit)

        self.layout().addWidget(self.tree)

    def setFolderCurrent(self, selected=None):
        if selected is None: return self
        self.tree.setFolderCurrent(selected)
        return self

    def setFolders(self, collection, selected):
        self.tree.setFolders(collection, selected)
        return self

    def close(self):
        super(DashboardPanelLeft, self).deleteLater()
        return super(DashboardPanelLeft, self).close()


class DashboardPanelRight(QtWidgets.QFrame):
    fullscreenNoteAction = QtCore.pyqtSignal(object)
    editNoteAction = QtCore.pyqtSignal(object)
    removeNoteAction = QtCore.pyqtSignal(object)
    cloneNoteAction = QtCore.pyqtSignal(object)
    renameNoteAction = QtCore.pyqtSignal(object)
    saveNoteAction = QtCore.pyqtSignal(object)
    selectNoteAction = QtCore.pyqtSignal(object)
    moveNoteAction = QtCore.pyqtSignal(object)
    settingsAction = QtCore.pyqtSignal(object)
    searchAction = QtCore.pyqtSignal(object)

    def __init__(self):
        super(DashboardPanelRight, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.preview = DashboardDocumentPreview()
        self.preview.fullscreenNoteAction.connect(self.fullscreenNoteAction.emit)
        self.preview.editNoteAction.connect(self.editNoteAction.emit)
        self.preview.removeNoteAction.connect(self.removeNoteAction.emit)
        self.preview.cloneNoteAction.connect(self.cloneNoteAction.emit)
        self.preview.renameNoteAction.connect(self.renameNoteAction.emit)
        self.preview.selectNoteAction.connect(self.selectNoteAction.emit)
        self.preview.saveNoteAction.connect(self.saveNoteAction.emit)
        self.preview.moveNoteAction.connect(self.moveNoteAction.emit)

        self.toolbar = DashboardDocumentPreviewToolbar()
        self.toolbar.settingsAction.connect(self.settingsAction.emit)
        self.toolbar.searchAction.connect(self.searchAction.emit)

        self.layout().addWidget(self.toolbar)
        self.layout().addWidget(self.preview)

    def setDocuments(self, collection, selected):
        self.preview.setDocuments(collection, selected)
        return self

    def close(self):
        super(DashboardPanelRight, self).deleteLater()
        return super(DashboardPanelRight, self).close()
