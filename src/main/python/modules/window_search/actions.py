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
import logging
from PyQt5 import QtWidgets

from .gui.preview.widget import PreviewScrollArea


class ModuleActions(object):

    @inject.params(search='search', storage='storage', window='window')
    def onActionSearchRequest(self, widget=None, search=None, storage=None, window=None):
        if widget is None or window is None: return None

        text = widget.text()
        if text is None: return None
        if not len(text): return None

        preview = PreviewScrollArea(window)
        preview.edit.connect(self.onActionEditRequest)
        #
        result = search.search(text)
        result = [x['path'] for x in result]
        if result is None: return None
        if not len(result): return None

        for path in result:
            index = storage.index(path)
            if index is None: continue
            preview.addPreview(index)

        title = text if len(text) <= 25 else "{}...".format(text[0:22])
        window.tab.emit((preview, title))

    @inject.params(storage='storage', window='window', dashboard='notepad.dashboard')
    def onActionEditRequest(self, index, storage, window, dashboard):
        try:
            if storage.isDir(index):
                dashboard.group(index)
                window.tabSwitch.emit(0)
                return None
            if storage.isFile(index):
                dashboard.note(index)
                window.tabSwitch.emit(0)
                return None
            return None
        except Exception as ex:
            logger = logging.getLogger('search')
            logger.exception(ex)

    @inject.params(storage='storage', search='search')
    def onNoteCreated(self, index, storage, search):
        # update search index only after
        # the update was successful
        name = storage.fileName(index)
        path = storage.filePath(index)

        content = storage.fileContent(index)
        if not len(content): return None

        search.append(name, path, content)

    @inject.params(storage='storage', search='search')
    def onNoteUpdated(self, index, storage, search):
        # update search index only after
        # the update was successful
        name = storage.fileName(index)
        path = storage.filePath(index)

        content = storage.fileContent(index)
        if not len(content): return None

        search.update(name, path, content)

    @inject.params(storage='storage', search='search')
    def onNoteRemoved(self, index, storage, search):
        # update search index only after
        # the update was successful
        path = storage.filePath(index)
        if not len(path): return None

        search.remove(path)
