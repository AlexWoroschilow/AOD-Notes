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
from .gui.settings.search import WidgetSettingsSearch


class Loader(object):
    actions = ModuleActions()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    @inject.params(config='config')
    def _widget_settings_search(self, options, args, config):
        widget = WidgetSettingsSearch()

        return widget

    def enabled(self, options=None, args=None):
        return options.console is None

    @inject.params(dashboard='notepad.dashboard', factory='settings_factory')
    def boot(self, options=None, args=None, dashboard=None, factory=None):
        dashboard.created.connect(self.actions.onNoteCreated)
        dashboard.updated.connect(self.actions.onNoteUpdated)
        dashboard.search.connect(self.actions.onActionSearchRequest)
        dashboard.removed.connect(self.actions.onNoteRemoved)

        factory.addWidget(functools.partial(
            self._widget_settings_search,
            options=options, args=args
        ))
