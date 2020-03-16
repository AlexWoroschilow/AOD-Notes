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
from .gui.preview.list import PreviewScrollArea


class Loader(object):
    actions = ModuleActions()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def enabled(self, options=None, args=None):
        return options.console is None

    @inject.params(store='store', factory='settings_factory')
    def boot(self, options=None, args=None, store=None, factory=None):
        """

        :param options:
        :param args:
        :param store:
        :param factory:
        :return:
        """
        factory.addWidget(WidgetSettingsSearch)

        store.subscribe(self.searchEvent)

    @inject.params(search='search', storage='storage', window='window')
    def searchEvent(self, text=None, search=None, storage=None, window=None):
        if not len(text): return None

        preview = PreviewScrollArea(window)
        preview.editAction.connect(self.actions.onActionEditRequest)

        for index, path in enumerate(search.search(text), start=1):
            preview.addPreview(storage.index(path))

        title = text if len(text) <= 25 else \
            "{}...".format(text[0:22])

        window.tab.emit((preview, title))
