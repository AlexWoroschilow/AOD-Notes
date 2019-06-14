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

from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui

from . import ToolBarButton
from . import PictureButton
from . import SearchField

from .button import ButtonDisabled


class FolderTreeToolbarTop(QtWidgets.QWidget):
    storage = QtCore.pyqtSignal(object)
    storage_changed = QtCore.pyqtSignal(object)

    @inject.params(config='config')
    def __init__(self, config):
        super(FolderTreeToolbarTop, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)

        self.location = ToolBarButton(config.get('storage.location'))
        self.location.setIcon(QtGui.QIcon("icons/plus-light"))
        self.location.setToolTip("Clone selected preview")

        self.location.clicked.connect(
            lambda event=None: self.storage.emit(event)
        )

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignLeft)
        self.layout.addWidget(self.location)

        self.storage_changed.connect(
            lambda text: self.location.setText(text)
        )

        self.setLayout(self.layout)


class NotepadEditorToolbarTop(QtWidgets.QGroupBox):
    note_new = QtCore.pyqtSignal(object)
    note_import = QtCore.pyqtSignal(object)
    group_new = QtCore.pyqtSignal(object)
    settings = QtCore.pyqtSignal(object)
    search = QtCore.pyqtSignal(object)

    @inject.params(config='config')
    def __init__(self, parent=None, config=None):
        super(NotepadEditorToolbarTop, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(ButtonDisabled(QtGui.QIcon("icons/plus"), None))

        tooltip = 'Create new note. The new note will be created as a part of the selected group or in the root group.'
        self.note = PictureButton(QtGui.QIcon("icons/note"), tooltip)
        self.note.clicked.connect(lambda event=None: self.note_new.emit(event))
        self.layout.addWidget(self.note)

        tooltip = 'Create new note. The new note will be created as a part of the selected group or in the root group.'
        self.group = PictureButton(QtGui.QIcon("icons/book"), tooltip)
        self.group.clicked.connect(lambda event=None: self.group_new.emit(event))
        self.layout.addWidget(self.group)

        tooltip = 'Create new note. The new note will be created as a part of the selected group or in the root group.'
        self.importing = PictureButton(QtGui.QIcon("icons/import"), tooltip)
        self.importing.clicked.connect(lambda event=None: self.note_import.emit(event))
        self.layout.addWidget(self.importing)

        self.spacer = QtWidgets.QWidget()
        self.spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.layout.addWidget(self.spacer)

        self.text_search = SearchField()
        self.text_search.returnPressed.connect(lambda event=None: self.search.emit(self.text_search))
        self.text_search.returnPressed.connect(self.text_search.clearFocus)
        self.layout.addWidget(self.text_search)

        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+f"), self.text_search)
        shortcut.activatedAmbiguously.connect(self.text_search.setFocus)
        shortcut.activated.connect(self.text_search.setFocus)
        shortcut.setEnabled(True)

        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Esc"), self.text_search)
        shortcut.activatedAmbiguously.connect(self.text_search.clearFocus)
        shortcut.activated.connect(lambda event=None: self.text_search.setText(None))
        shortcut.activated.connect(self.text_search.clearFocus)

        self.text_search.focusInEvent = functools.partial(
            self.on_search_focus_in, widget=self.text_search
        )
        self.text_search.focusOutEvent = functools.partial(
            self.on_search_focus_out, widget=self.text_search
        )

        tooltip = 'Create new note. The new note will be created as a part of the selected group or in the root group.'
        self.button_settings = PictureButton(QtGui.QIcon("icons/settings"), tooltip)
        self.button_settings.clicked.connect(lambda event=None: self.settings.emit(self.button_settings))
        self.button_settings.setFlat(True)
        self.layout.addWidget(self.button_settings)

        self.setLayout(self.layout)

    def on_search_focus_in(self, event=None, widget=None):
        self.text_search.setAlignment(Qt.AlignCenter)

        self.spacer.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.spacer.setVisible(False)
        self.importing.setVisible(False)
        self.group.setVisible(False)
        self.note.setVisible(False)

    def on_search_focus_out(self, event=None, widget=None):
        self.text_search.setAlignment(Qt.AlignLeft)

        self.spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.spacer.setVisible(True)
        self.importing.setVisible(True)
        self.group.setVisible(True)
        self.note.setVisible(True)

    def close(self):
        super(NotepadEditorToolbarTop, self).deleteLater()
        return super(NotepadEditorToolbarTop, self).close()
