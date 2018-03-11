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
from .service import SQLiteStorage


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

        binder.bind('storage', SQLiteStorage("storage.dhf"))

    @inject.params(dispatcher='event_dispatcher')
    def boot(self, dispatcher=None):
        """

        :param dispatcher:.
        :return:.
        """
        dispatcher.add_listener('window.notepad.folder_new', self._onNotepadFolderNew)
        dispatcher.add_listener('window.notepad.folder_copy', self._onNotepadFolderCopy)
        dispatcher.add_listener('window.notepad.folder_update', self._onNotepadFolderUpdate)

        dispatcher.add_listener('window.notepad.note_new', self._onNotepadNoteNew)
        dispatcher.add_listener('window.notepad.note_update', self._onNotepadNoteUpdate)
        dispatcher.add_listener('window.notepad.note_remove', self._onNotepadNoteRemove)
        dispatcher.add_listener('window.notepad.note_copy', self._onNotepadNoteCopy)
        dispatcher.add_listener('window.notepad.note_export', self._onNotepadNoteExport)
        dispatcher.add_listener('window.notepad.note_folder', self._onNotepadNoteFolder)

        # dispatcher.dispatch('window.notepad.note_update', (
        #     self._index, self.name.text(), self.text.toHtml()
        # ))

    @inject.params(storage='storage')
    def _onNotepadFolderNew(self, event=None, dispather=None, storage=None):
        """

        :param event: 
        :param dispather: 
        :return: 
        """
        model = event.data
        storage.addFolder(model.name, model.text)

    @inject.params(storage='storage')
    def _onNotepadFolderCopy(self, event=None, dispather=None, storage=None):
        """

        :param event: 
        :param dispather: 
        :return: 
        """

    @inject.params(storage='storage')
    def _onNotepadFolderUpdate(self, event=None, dispather=None, storage=None):
        """
        
        :param event: 
        :param dispather: 
        :param storage: 
        :return: 
        """
        folder = event.data
        storage.updateFolder(folder.index, folder.name, folder.text)

    @inject.params(storage='storage')
    def _onNotepadNoteNew(self, event=None, dispather=None, storage=None):
        """

        :param event: 
        :param dispather: 
        :return: 
        """
        entity = event.data
        folder = entity.folder.index if entity.folder is not None else None
        event.data = storage.addNote(entity.name, entity.text, folder)

    @inject.params(storage='storage')
    def _onNotepadNoteCopy(self, event=None, dispather=None, storage=None):
        """

        :param event: 
        :param dispather: 
        :return: 
        """
        print(event)

    @inject.params(storage='storage')
    def _onNotepadNoteUpdate(self, event=None, dispather=None, storage=None):
        """

        :param event: 
        :param dispather: 
        :return: 
        """
        entity = event.data
        storage.updateNote(entity.index, entity.name, entity.text)

    @inject.params(storage='storage')
    def _onNotepadNoteRemove(self, event=None, dispather=None, storage=None):
        """

        :param event: 
        :param dispather: 
        :return: 
        """
        note = event.data
        storage.removeNote(note.index)

    @inject.params(storage='storage')
    def _onNotepadNoteExport(self, event=None, dispather=None, storage=None):
        """

        :param event: 
        :param dispather: 
        :return: 
        """
        print(event)

    @inject.params(storage='storage')
    def _onNotepadNoteFolder(self, event=None, dispather=None, storage=None):
        """
        
        :param event: 
        :param dispather: 
        :param storage: 
        :return: 
        """
        entity, folder = event.data
        if entity is not None and folder is not None:
            storage.updateNoteFolder(entity.index, folder.index)
