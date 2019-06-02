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
from .gui.settings.search import WidgetSettingsSearch


class Loader(Loader):
    actions = ModuleActions()

    def __init__(self, options=None, args=None):
        if options is None or args is None:
            return None

        self.buttonGroup = None
        self.buttonNote = None
        self.buttonImport = None
        self.search = None
        self.spacer = None

    @inject.params(dashboard='notepad.dashboard')
    def _widget_button_note(self, dashboard=None):
        tooltip = 'Create new note. The new note will be created as a part of the selected group or in the root group.'
        button = PictureButton(QtGui.QIcon("icons/note"), tooltip)
        button.clicked.connect(functools.partial(dashboard.actions.onActionNoteCreate, widget=dashboard))
        return button

    @inject.params(dashboard='notepad.dashboard')
    def _widget_button_group(self, dashboard=None):
        tooltip = 'Create new note. The new note will be created as a part of the selected group or in the root group.'
        button = PictureButton(QtGui.QIcon("icons/book"), tooltip)
        button.clicked.connect(functools.partial(dashboard.actions.onActionFolderCreate, widget=dashboard))
        return button

    @inject.params(dashboard='notepad.dashboard')
    def _widget_button_import(self, dashboard=None):
        button = PictureButton(QtGui.QIcon("icons/import"), 'Import File')
        button.clicked.connect(self.actions.onActionNoteImport)
        return button

    @inject.params(dashboard='notepad.dashboard', kernel='kernel')
    def _widget_settings_search(self, kernel=None, dashboard=None):
        if kernel is None or dashboard is None:
            return None

        widget = WidgetSettingsSearch()
        destination = os.path.dirname(kernel.options.config)
        widget.searchIndex.setText(destination)

        return widget

    def _widget_search(self):

        search = SearchField()
        search.clearFocus()

        search.focusInEvent = functools.partial(self.onSearchFocusIn, widget=search)
        search.focusOutEvent = functools.partial(self.onSearchFocusOut, widget=search)
        search.returnPressed.connect(functools.partial(self.actions.onActionSearchRequest, widget=search))

        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+f"), search)
        shortcut.activated.connect(self.onSearchFocusActivate)
        shortcut.setEnabled(True)

        return search

    def enabled(self, options=None, args=None):
        return options.console is None

    def config(self, binder=None):
        pass

    @inject.params(config='config', factory='window.header_factory', factory_settings='settings_factory')
    def boot(self, options=None, args=None, config=None, factory=None, factory_settings=None):
        if options is None or args is None or factory is None:
            return None

        self.spacer = QtWidgets.QWidget()
        self.spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)

        self.buttonNote = factory.addWidget(self._widget_button_note())
        self.buttonGroup = factory.addWidget(self._widget_button_group())
        self.buttonImport = factory.addWidget(self._widget_button_import())

        factory.addWidget(self.spacer)

        self.search = factory.addWidget(self._widget_search())

        if factory_settings is not None and factory_settings:
            factory_settings.addWidget(self._widget_settings_search)

    def onSearchFocusActivate(self, event=None):
        if self.search is not None:
            self.search.clearFocus()
            self.search.setFocus()

    def onSearchFocusIn(self, event=None, widget=None):

        if self.search is not None:
            self.search.setAlignment(Qt.AlignCenter)

        if self.spacer is not None:
            self.spacer.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
            self.spacer.setVisible(False)

        if self.buttonGroup is not None:
            self.buttonGroup.setVisible(False)

        if self.buttonNote is not None:
            self.buttonNote.setVisible(False)

        if self.buttonImport is not None:
            self.buttonImport.setVisible(False)

    def onSearchFocusOut(self, event, widget):
        if self.search is not None:
            self.search.setAlignment(Qt.AlignLeft)

        if self.spacer is not None:
            self.spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
            self.spacer.setVisible(True)

        if self.buttonGroup is not None:
            self.buttonGroup.setVisible(True)

        if self.buttonNote is not None:
            self.buttonNote.setVisible(True)

        if self.buttonImport is not None:
            self.buttonImport.setVisible(True)
