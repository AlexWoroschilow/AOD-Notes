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

from PyQt5 import QtGui
from PyQt5 import QtWidgets

from .actions import ModuleActions

from lib.plugin import Loader
from .gui.button import PictureButton

class Loader(Loader):
    actions = ModuleActions()

    @property
    def enabled(self):
        return True

    def config(self, binder=None):
        binder.bind_to_provider('settings_menu', self._menu)
        binder.bind_to_constructor('settings_factory', self._settings)

    @inject.params(factory='window.header_factory')
    def boot(self, options=None, args=None, factory=None):
        widget = PictureButton(QtGui.QIcon("icons/settings.svg"), None)
        widget.clicked.connect(self.actions.onActionSettings)

        factory.addWidget(widget, 128)

    def _settings(self):
        from .settings import SettingsFactory
        return SettingsFactory()

    @inject.params(config='config')
    def _menu(self, config):
        from .gui.menu import SettingsMenu

        menu = QtWidgets.QMenu()

        widget = SettingsMenu(menu)
        widget.editorName.setChecked(int(config.get('editor.name')))
        action = functools.partial(self.actions.onActionToggle, variable='editor.name')
        widget.editorName.stateChanged.connect(action)

        widget.editorToolbarFormat.setChecked(int(config.get('editor.formatbar')))
        action = functools.partial(self.actions.onActionToggle, variable='editor.formatbar')
        widget.editorToolbarFormat.stateChanged.connect(action)

        widget.editorToolbarRight.setChecked(int(config.get('editor.rightbar')))
        action = functools.partial(self.actions.onActionToggle, variable='editor.rightbar')
        widget.editorToolbarRight.stateChanged.connect(action)

        widget.editorToolbarLeft.setChecked(int(config.get('editor.leftbar')))
        action = functools.partial(self.actions.onActionToggle, variable='editor.leftbar')
        widget.editorToolbarLeft.stateChanged.connect(action)

        widget.toolbar.setChecked(int(config.get('folders.toolbar')))
        action = functools.partial(self.actions.onActionToggle, variable='folders.toolbar')
        widget.toolbar.stateChanged.connect(action)

        menu.addAction(widget)

        return menu
