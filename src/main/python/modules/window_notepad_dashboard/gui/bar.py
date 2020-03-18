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
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui

from .button import PictureButtonFlat


class NotepadDashboardToolbar(QtWidgets.QFrame):
    newNoteAction = QtCore.pyqtSignal(object)
    importNoteAction = QtCore.pyqtSignal(object)
    newGroupAction = QtCore.pyqtSignal(object)

    def __init__(self):
        super(NotepadDashboardToolbar, self).__init__()

        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setAlignment(Qt.AlignCenter)

        self.note = PictureButtonFlat(QtGui.QIcon("icons/note"))
        self.note.clicked.connect(self.newNoteAction.emit)
        self.note.setText(' New Note')
        self.layout().addWidget(self.note)

        self.group = PictureButtonFlat(QtGui.QIcon("icons/book"))
        self.group.clicked.connect(self.newGroupAction.emit)
        self.group.setText(' New Group')
        self.layout().addWidget(self.group)

        self.importing = PictureButtonFlat(QtGui.QIcon("icons/import"))
        self.importing.clicked.connect(self.importNoteAction.emit)
        self.importing.setText(' Import Note')
        self.layout().addWidget(self.importing)

        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+n"), self.note)
        shortcut.activatedAmbiguously.connect(lambda x=None: self.newNoteAction.emit(self.note))
        shortcut.activated.connect(lambda x=None: self.newNoteAction.emit(self.note))
        shortcut.setEnabled(True)

        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+g"), self.group)
        shortcut.activatedAmbiguously.connect(lambda x=None: self.newGroupAction.emit(self.group))
        shortcut.activated.connect(lambda x=None: self.newGroupAction.emit(self.group))
        shortcut.setEnabled(True)

        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+i"), self.importing)
        shortcut.activatedAmbiguously.connect(lambda x=None: self.importNoteAction.emit(self.importing))
        shortcut.activated.connect(lambda x=None: self.importNoteAction.emit(self.importing))
        shortcut.setEnabled(True)

    def close(self):
        super(NotepadDashboardToolbar, self).deleteLater()
        return super(NotepadDashboardToolbar, self).close()
