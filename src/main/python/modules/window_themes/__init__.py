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

from .actions import ModuleActions


class Loader(object):

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    @inject.params(config='config')
    def _widget_settings_themes(self, options, args, config):
        from .gui.settings.themes import WidgetSettingsThemes
        widget = WidgetSettingsThemes()
        return widget

    def enabled(self, options=None, args=None):
        return options.console is None

    @inject.params(factory='settings_factory')
    def boot(self, options=None, args=None, factory=None):
        factory.addWidget(functools.partial(
            self._widget_settings_themes,
            options=options, args=args
        ))
