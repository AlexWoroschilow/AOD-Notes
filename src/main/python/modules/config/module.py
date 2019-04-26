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

from lib.plugin import Loader

from .actions import ModuleActions


class Loader(Loader):
    actions = ModuleActions()

    def enabled(self, options=None, args=None):
        return True

    def config(self, binder=None):
        binder.bind_to_constructor('config', self._config)

    def boot(self, options=None, args=None):
        if options.console: return None

        container = inject.get_injector()
        if container is None: return None

        factory = container.get_instance('settings_factory')
        if factory is None: return None

        factory.addWidget(self._widget_settings_storage)
        factory.addWidget(self._widget_settings_navigator)
        factory.addWidget(self._widget_settings_editor)
        factory.addWidget(self._widget_settings_search)

    @inject.params(kernel='kernel')
    def _config(self, kernel=None):
        from .service.config import ConfigFile
        return ConfigFile(kernel.options.config)

    @inject.params(config='config')
    def _widget_settings_cryptography(self, config=None):
        if config is None: return None

        from .gui.settings.cryptography import WidgetSettingsCryptography

        widget = WidgetSettingsCryptography()
        widget.code.setText(config.get('cryptography.password'))
        return widget

    @inject.params(config='config')
    def _widget_settings_navigator(self, config=None):
        if config is None: return None

        from .gui.settings.navigator import WidgetSettingsNavigator

        widget = WidgetSettingsNavigator()
        widget.toolbar.setChecked(int(config.get('folders.toolbar')))
        action = functools.partial(self.actions.onActionCheckboxToggle, variable='folders.toolbar')
        widget.toolbar.stateChanged.connect(action)

        return widget

    @inject.params(config='config')
    def _widget_settings_editor(self, config=None):
        if config is None: return None

        from .gui.settings.editor import WidgetSettingsEditor

        widget = WidgetSettingsEditor()

        widget.formatbar.setChecked(int(config.get('editor.formatbar')))
        action = functools.partial(self.actions.onActionCheckboxToggle, variable='editor.formatbar')
        widget.formatbar.stateChanged.connect(action)

        widget.rightbar.setChecked(int(config.get('editor.rightbar')))
        action = functools.partial(self.actions.onActionCheckboxToggle, variable='editor.rightbar')
        widget.rightbar.stateChanged.connect(action)

        widget.leftbar.setChecked(int(config.get('editor.leftbar')))
        action = functools.partial(self.actions.onActionCheckboxToggle, variable='editor.leftbar')
        widget.leftbar.stateChanged.connect(action)

        return widget

    @inject.params(kernel='kernel')
    def _widget_settings_search(self, kernel=None):
        if kernel is None: return None

        from .gui.settings.search import WidgetSettingsSearch

        widget = WidgetSettingsSearch()
        destination = os.path.dirname(kernel.options.config)
        widget.searchIndex.setText(destination)

        return widget

    @inject.params(config='config')
    def _widget_settings_storage(self, config=None):
        if config is None: return None

        from .gui.settings.storage import WidgetSettingsStorage

        widget = WidgetSettingsStorage()
        widget.location.setText(config.get('storage.location'))
        action = functools.partial(self.actions.onActionStorageLocationChange, widget=widget)
        widget.location.clicked.connect(action)

        return widget
