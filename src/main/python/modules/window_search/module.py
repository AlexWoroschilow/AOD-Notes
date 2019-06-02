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

from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import Qt

from lib.plugin import Loader

from .actions import ModuleActions
from .gui.widget import SearchField
from .gui.button import PictureButton


class Loader(Loader):
    actions = ModuleActions()

    def __init__(self, options=None, args=None):
        if options is None or args is None: return None
        self.buttonGroup = None
        self.buttonNote = None
        self.buttonImport = None
        self.search = None
        self.spacer = None

    def enabled(self, options=None, args=None):
        return options.console is None

    def config(self, binder=None):
        pass

    @inject.params(config='config', factory='window.header_factory', dashboard='notepad.dashboard')
    def boot(self, options=None, args=None, config=None, factory=None, dashboard=None):
        if not len(config.get('storage.location')): return None

        if dashboard is None: return None
        if options is None: return None
        if args is None: return None

        tooltip = 'Create new note. The new note will be created as a part of the selected group or in the root group.'
        self.buttonNote = PictureButton(QtGui.QIcon("icons/note"), tooltip)
        action = functools.partial(dashboard.actions.onActionNoteCreate, widget=dashboard)
        self.buttonNote.clicked.connect(action)

        tooltip = 'Create new group. The new group will be created as in the selected group or in the root group.'
        self.buttonGroup = PictureButton(QtGui.QIcon("icons/book"), tooltip)
        action = functools.partial(dashboard.actions.onActionFolderCreate, widget=dashboard)
        self.buttonGroup.clicked.connect(action)

        self.buttonImport = PictureButton(QtGui.QIcon("icons/import"), 'Import File')
        self.buttonImport.clicked.connect(self.actions.onActionNoteImport)

        self.search = SearchField()
        self.search.setFocusPolicy(Qt.StrongFocus)
        self.search.clearFocus()

        action = functools.partial(self.onSearchFocusIn, widget=self.search)
        self.search.focusInEvent = action
        action = functools.partial(self.onSearchFocusOut, widget=self.search)
        self.search.focusOutEvent = action

        action = functools.partial(self.actions.onActionSearchRequest, widget=self.search)
        self.search.returnPressed.connect(action)

        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+f"), self.search)
        shortcut.activated.connect(self.onSearchFocusActivate)
        shortcut.setEnabled(True)

        self.spacer = QtWidgets.QWidget()
        self.spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)

        if factory is None: return None
        factory.addWidget(self.buttonNote)
        factory.addWidget(self.buttonGroup)
        factory.addWidget(self.buttonImport)
        factory.addWidget(self.spacer)
        factory.addWidget(self.search)

    def onSearchFocusActivate(self, event=None):
        if self.search is None: return None
        self.search.clearFocus()
        self.search.setFocus()

    def onSearchFocusIn(self, event=None, widget=None):

        if self.search is None: return None
        self.search.setAlignment(Qt.AlignCenter)

        if self.spacer is None: return None
        self.spacer.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.spacer.setVisible(False)

        if self.buttonGroup is None: return None
        self.buttonGroup.setVisible(False)

        if self.buttonNote is None: return None
        self.buttonNote.setVisible(False)

        if self.buttonImport is None: return None
        self.buttonImport.setVisible(False)

    def onSearchFocusOut(self, event, widget):
        if self.search is None: return None
        self.search.setAlignment(Qt.AlignLeft)

        if self.spacer is None: return None
        self.spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.spacer.setVisible(True)

        if self.buttonGroup is None: return None
        self.buttonGroup.setVisible(True)

        if self.buttonNote is None: return None
        self.buttonNote.setVisible(True)

        if self.buttonImport is None: return None
        self.buttonImport.setVisible(True)
