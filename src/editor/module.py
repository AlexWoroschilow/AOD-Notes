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
from PyQt5 import QtCore

from lib.plugin import Loader
from .gui.widget import TextEditor


class Loader(Loader):
    _entity = None
    _editor = None

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
        dispatcher.add_listener('window.notepad.note_edit', self._onWindowNoteEdit)
        dispatcher.add_listener('window.notepad.note_tab', self._onWindowNoteTab)

    def _onWindowStart(self, event=None, dispatcher=None):
        """
        
        :param event: 
        :param dispatcher: 
        :return: 
        """
        self.parent = None
        self._editor = TextEditor()

    def _onWindowFirstTab(self, event=None, dispatcher=None):
        """

        :param event: 
        :param dispatcher: 
        :return: 
        """
        self.container, self.parent = event.data
        if self._editor is None:
            return None

        self.container.addWidget(self._editor)

    def _onWindowNoteEdit(self, event=None, dispatcher=None):
        """
        
        :param event: 
        :param dispatcher: 
        :return: 
        """
        if event.data is None:
            return None

        if self._editor is None:
            return None

        entity = event.data
        self._editor.edit(entity)

    def _onWindowNoteTab(self, event=None, dispatcher=None):
        """
        
        :param event: 
        :param dispatcher: 
        :return: 
        """
        if self.parent is None:
            return None

        editor = TextEditor()
        editor.edit(event.data)

        name = event.data.name
        self.parent.addTab(editor, name)

        index = self.parent.indexOf(editor)
        self.parent.setCurrentIndex(index)
