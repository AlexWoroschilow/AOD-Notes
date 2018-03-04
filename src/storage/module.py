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

        binder.bind_to_constructor('storage', Storage())

    @inject.params(dispatcher='event_dispatcher')
    def boot(self, dispatcher=None):
        """

        :param dispatcher:.
        :return:.
        """
        dispatcher.add_listener('window.notepad.folder_new', self._onNotepadFolderNew)
        dispatcher.add_listener('window.notepad.folder_copy', self._onNotepadFolderCopy)
        dispatcher.add_listener('window.notepad.note_new', self._onNotepadNoteNew)
        dispatcher.add_listener('window.notepad.note_copy', self._onNotepadNoteCopy)
        dispatcher.add_listener('window.notepad.note_export', self._onNotepadNoteExport)

    def _onNotepadFolderNew(self, event=None, dispather=None):
        """
        
        :param event: 
        :param dispather: 
        :return: 
        """
        print(event)

    def _onNotepadFolderNew(self, event=None, dispather=None):
        """

        :param event: 
        :param dispather: 
        :return: 
        """
        print(event)

    def _onNotepadFolderCopy(self, event=None, dispather=None):
        """

        :param event: 
        :param dispather: 
        :return: 
        """
        print(event)

    def _onNotepadNoteNew(self, event=None, dispather=None):
        """

        :param event: 
        :param dispather: 
        :return: 
        """
        print(event)

    def _onNotepadNoteCopy(self, event=None, dispather=None):
        """

        :param event: 
        :param dispather: 
        :return: 
        """
        print(event)

    def _onNotepadNoteExport(self, event=None, dispather=None):
        """

        :param event: 
        :param dispather: 
        :return: 
        """
        print(event)
