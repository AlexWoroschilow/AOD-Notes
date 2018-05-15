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

from lib.plugin import Loader

from .gui.splitter import NotepadEditorWidget


class Loader(Loader):

    @property
    def enabled(self):
        return True

    @inject.params(kernel='kernel')
    def boot(self, options=None, args=None, kernel=None):
        kernel.listen('application.start', self._onWindowStart)
        kernel.listen('window.dashboard.content', self._onWindowDashboard, 128)
        kernel.listen('window.notepad.folder_open', self._onNotepadFolderOpen, 128)
        kernel.listen('window.notepad.folder_selected', self._onNotepadFolderSelect, 128)
        kernel.listen('window.search.request', self._onSearchRequest, 100)

        self._widget = None
        self._folder = None
        self._search = None
        self._entity = None
        self._first = None

    @inject.params(kernel='kernel')
    def _onWindowStart(self, event=None, kernel=None):
        
        self._widget = NotepadEditorWidget()

    @inject.params(kernel='kernel', logger='logger')
    def _onNotepadFolderOpen(self, event=None, kernel=None, logger=None):
        self._folder, self._search = event.data
        if self._folder is None:
            return None

        editor = NotepadEditorWidget()
        
        editor.setContent((self._folder, None, self._search))
        kernel.dispatch('window.tab', (editor, self._folder))

    def _onWindowDashboard(self, event=None):
        container, parent = event.data
        if container is None or parent is None:
            return None
        if self._widget is not None:
            container.addWidget(self._widget)

    @inject.params(logger='logger', storage='storage')
    def _onNotepadFolderSelect(self, event=None, logger=None, storage=None):
        self._folder, self._search, self._entity = event.data
        if self._widget is None or self._folder is None:
            return None
        
        self._widget._list.clear()
        for entity in storage.notes(folder=self._folder, string=self._search):
            self._widget._list.addLine(entity)
        
        self._widget.setContent((
            self._folder,
            self._entity,
            self._search
        ))

    @inject.params(storage='storage', logger='logger')
    def _onSearchRequest(self, event=None, storage=None, logger=None):
        self._search = event.data
        if self._search is None:
            return None

        self._folder = None
        self._entity = None
         
        self._widget.setContent((self._folder,
            self._entity, self._search 
        ))
