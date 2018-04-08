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
    _entity = None
    _editor = None
    _folder = None

    @property
    def enabled(self):
        """

        :return:
        """
        return True

    def config(self, binder=None):
        """

        :param binder:
        :return:
        """

    @inject.params(dispatcher='event_dispatcher')
    def boot(self, dispatcher=None):
        """

        :param dispatcher:.
        :return:.
        """
        dispatcher.add_listener('application.start', self._onWindowStart)

        dispatcher.add_listener('window.first_tab.content', self._onWindowFirstTab, 128)
        dispatcher.add_listener('window.notepad.note_update', self._onNotepadNoteUpdate, 128)

        dispatcher.add_listener('window.notepad.folder_open', self._onNotepadFolderOpen)
        dispatcher.add_listener('window.notepad.folder_selected', self._onNotepadFolderSelect)

    @inject.params(storage='storage', dispatcher='event_dispatcher')
    def _onWindowStart(self, event=None, dispatcher=None, storage=None):
        """
        
        :param event: 
        :param dispatcher: 
        :return: 
        """
        self._parent = None
        self._editor = NotepadEditorWidget()

        if self._folder is None:
            return None

        self._first = None
        self._editor.list.clear()
        for entity in storage.notesByFolder(self._folder):
            if self._first is None:
                self._first = entity
            self._editor._list.addLine(entity)
        self._editor._list.setFolder(self._folder)

        dispatcher.dispatch('window.notepad.note_edit', self._first)

    def _onWindowFirstTab(self, event=None, dispatcher=None):
        """

        :param event: 
        :param dispatcher: 
        :return: 
        """
        self.container, self._parent = event.data
        if self._editor is None:
            return None

        self.container.addWidget(self._editor)

    @inject.params(dispatcher='event_dispatcher', storage='storage')
    def _onNotepadFolderOpen(self, event=None, dispatcher=None, storage=None):
        """

        :param event: 
        :param dispatcher: 
        :param storage: 
        :return: 
        """
        self._folder, self._search = event.data
        if self._folder is None:
            return None

        editor = NotepadEditorWidget()
        editor.setContent((self._folder, None, self._search))

        dispatcher.dispatch('window.tab', (
            editor, self._folder
        ))

    @inject.params(storage='storage')
    def _onNotepadNoteUpdate(self, event=None, dispatcher=None, storage=None):
        """

        :param event: 
        :param dispather: 
        :param storage: 
        :return: 
        """
        self._editor._onRefreshEvent(event, dispatcher)

    @inject.params(dispatcher='event_dispatcher', storage='storage')
    def _onNotepadFolderSelect(self, event=None, dispatcher=None, storage=None):
        """

        :param event: 
        :param dispatcher: 
        :return: 
        """
        self._folder, self._search = event.data
        if self._editor is None:
            return None
        self._editor.setContent((self._folder, None, self._search))
