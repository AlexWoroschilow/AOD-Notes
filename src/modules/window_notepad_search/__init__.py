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

from .actions import ModuleActions
from .gui.settings.search import WidgetSettingsSearch
from .gui.preview.list import PreviewScrollArea


class Loader(object):
    actions = ModuleActions()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def __construct(self):
        widget = WidgetSettingsSearch()
        widget.indexAction.connect(self.actions.onActionIndexation)
        return widget

    @inject.params(store='store', factory='settings_factory')
    def boot(self, options=None, args=None, store=None, factory=None):
        factory.addWidget(self.__construct)

        store.subscribe(self.update)

    @inject.params(store='store', window='window')
    def update(self, store=None, window=None):
        state = store.get_state()
        if state is None: return None

        if 'search' not in state.keys():
            return None

        for search in state['search']:
            if search is None: continue

            preview = PreviewScrollArea(window)
            preview.selectAction.connect(self.actions.onActionSelect)
            for documents in search['documents']:
                preview.addPreview(documents)

            window.newTabAction.emit((preview, search['title']))
