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
        if options.console:
            return None

        container = inject.get_injector()
        if container is None:
            return None

        factory = container.get_instance('settings_factory')
        if factory is None:
            return None

        factory.addWidget(self._widget_settings_storage)
        factory.addWidget(self._widget_settings_search)

    @inject.params(kernel='kernel')
    def _config(self, kernel=None):
        from .service.config import ConfigFile
        return ConfigFile(kernel.options.config)

    @inject.params(kernel='kernel')
    def _widget_settings_search(self, kernel=None):
        if kernel is None:
            return None

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
