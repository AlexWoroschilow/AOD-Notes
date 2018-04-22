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
from PyQt5 import QtWidgets

from lib.plugin import Loader
from .gui.widget import NotepadEditorWidget


class Loader(Loader):

    @property
    def enabled(self):
        return True

    @inject.params(kernel='kernel')
    def boot(self, options=None, args=None, kernel=None):
        self._folder = None

        kernel.listen('window.notepad.folder_open', self._onNotepadFolderOpen, 128)
        kernel.listen('window.notepad.folder_selected', self._onNotepadFolderSelect, 128)
        kernel.listen('window.first_tab.content', self._onWindowFirstTab, 128)
        kernel.listen('application.start', self._onWindowStart)

    @inject.params(storage='storage', kernel='kernel')
    def _onWindowStart(self, event=None, kernel=None, storage=None):
        self._editor = NotepadEditorWidget()
        self._parent = None

        if self._folder is None:
            return None

        self._first = None
        self._editor.list.clear()
        for entity in storage.notesByFolder(self._folder):
            self._first = entity if self._first is None else self._first 
            self._editor._list.addLine(entity)
        self._editor._list.setFolder(self._folder)

        kernel.dispatch('window.notepad.note_edit', self._first)

    def _onWindowFirstTab(self, event=None, dispatcher=None):
        self.container, self._parent = event.data
        if self._editor is None:
            return None

        self.container.addWidget(self._editor)

    @inject.params(dispatcher='event_dispatcher', storage='storage')
    def _onNotepadFolderSelect(self, event=None, dispatcher=None, storage=None):
        self._folder, self._search, self._entity = event.data
        if self._editor is None:
            return None
        self._editor.setContent((self._folder, self._entity, self._search))

    @inject.params(kernel='kernel', storage='storage')
    def _onNotepadFolderOpen(self, event=None, kernel=None, storage=None):
        self._folder, self._search = event.data
        if self._folder is None:
            return None

        editor = NotepadEditorWidget()
        editor.setContent((self._folder, None, self._search))
        kernel.dispatch('window.tab', (editor, self._folder))

