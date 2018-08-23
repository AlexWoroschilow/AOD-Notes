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

from lib.plugin import Loader
from PyQt5 import QtWidgets


class Loader(Loader):

    @property
    def enabled(self):
        return True

    def config(self, binder=None):
        binder.bind_to_constructor('settings_factory', self._get_widget)
        binder.bind_to_constructor('button.settings', self._get_button)
        binder.bind_to_provider('settings_menu', self._get_menu)

    @inject.params(dispatcher='event_dispatcher')
    def boot(self, options=None, args=None, dispatcher=None):
        dispatcher.add_listener('header_content', self.onActionHeader, 128)

    def _get_button(self):

        from PyQt5 import QtGui

        widget = QtWidgets.QAction(QtGui.QIcon("icons/settings.svg"), None)
        widget.triggered.connect(self.onActionSettings)

        return widget

    def _get_widget(self):

        from .gui.widget import WidgetSettingsFactory

        return WidgetSettingsFactory()

    @inject.params(config='config', notepad='notepad')
    def _get_menu(self, config, notepad):

        from .gui.menu import SettingsMenu

        menu = QtWidgets.QMenu()

        widget = SettingsMenu(menu)
        widget.editorName.setChecked(int(config.get('editor.name')))
        widget.editorName.stateChanged.connect(functools.partial(
            self.onActionToggle, variable='editor.name',
        ))

        widget.editorToolbarFormat.setChecked(int(config.get('editor.formatbar')))
        widget.editorToolbarFormat.stateChanged.connect(functools.partial(
            self.onActionToggle, variable='editor.formatbar',
        ))

        widget.editorToolbarRight.setChecked(int(config.get('editor.rightbar')))
        widget.editorToolbarRight.stateChanged.connect(functools.partial(
            self.onActionToggle, variable='editor.rightbar',
        ))

        widget.editorToolbarLeft.setChecked(int(config.get('editor.leftbar')))
        widget.editorToolbarLeft.stateChanged.connect(functools.partial(
            self.onActionToggle, variable='editor.leftbar',
        ))

        widget.tags.setChecked(int(config.get('folders.keywords')))
        widget.tags.stateChanged.connect(functools.partial(
            self.onActionToggle, variable='folders.keywords',
        ))

        widget.toolbar.setChecked(int(config.get('folders.toolbar')))
        widget.toolbar.stateChanged.connect(functools.partial(
            self.onActionToggle, variable='folders.toolbar',
        ))
        
        menu.addAction(widget)
        
        return menu

    @inject.params(button='button.settings')
    def onActionHeader(self, event=None, button=None):
        self.container, self.parent = event.data
        self.container.addAction(button)

    @inject.params(kernel='kernel', factory='settings_factory', logger='logger')
    def onActionSettings(self, event=None, factory=None, kernel=None, logger=None):
        logger.debug('[search] settings event')
        kernel.dispatch('window.tab', (factory.widget, 'Settings'))

    @inject.params(config='config', kernel='kernel')
    def onActionToggle(self, status, variable, config, kernel):
        config.set(variable, '%s' % status)
        kernel.dispatch('config_updated')
