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
from .service import Storage
from .gui.widget import TextEditor


class Loader(Loader):
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
        dispatcher.add_listener('window.first_tab.content', self._onWindowFirstTab, 128)
        dispatcher.add_listener('window.notepad.note_edit', self._onWindowNoteEdit)

    def _onWindowFirstTab(self, event=None, dispatcher=None):
        """

        :param event: 
        :param dispatcher: 
        :return: 
        """

        self.editor = TextEditor()
        event.data.addWidget(self.editor, 5)

    def _onWindowNoteEdit(self, event=None, dispatcher=None):
        """
        
        :param event: 
        :param dispatcher: 
        :return: 
        """
        index, name, text = event.data
        self.editor.edit(index, name, text)
