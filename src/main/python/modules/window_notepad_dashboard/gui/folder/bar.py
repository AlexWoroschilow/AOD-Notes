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
import os
import inject
import functools

from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui

from .button import PictureButton


class DashboardFolderTreeToolbar(QtWidgets.QFrame):
    newNoteAction = QtCore.pyqtSignal(object)
    importNoteAction = QtCore.pyqtSignal(object)
    newGroupAction = QtCore.pyqtSignal(object)

    def __init__(self):
        super(DashboardFolderTreeToolbar, self).__init__()

        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setAlignment(Qt.AlignCenter)

        tooltip = 'Create new note. The new note will be created as a part of the selected group or in the root group.'
        self.note = PictureButton(QtGui.QIcon("icons/note-main"), tooltip)
        self.note.clicked.connect(self.newNoteAction.emit)
        self.layout().addWidget(self.note)

        tooltip = 'Create new note. The new note will be created as a part of the selected group or in the root group.'
        self.group = PictureButton(QtGui.QIcon("icons/book-main"), tooltip)
        self.group.clicked.connect(self.newGroupAction.emit)
        self.layout().addWidget(self.group)

        tooltip = 'Create new note. The new note will be created as a part of the selected group or in the root group.'
        self.importing = PictureButton(QtGui.QIcon("icons/import-main"), tooltip)
        self.importing.clicked.connect(self.importNoteAction.emit)
        self.layout().addWidget(self.importing)

    def close(self):
        super(DashboardFolderTreeToolbar, self).deleteLater()
        return super(DashboardFolderTreeToolbar, self).close()
