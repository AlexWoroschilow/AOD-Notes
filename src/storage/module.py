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
from .service import SQLiteStorage


class Loader(Loader):

    @property
    def enabled(self):
        return True

    def config(self, binder=None):
        binder.bind('storage', SQLiteStorage("storage.dhf"))

    @inject.params(kernel='kernel')
    def boot(self, options=None, args=None, kernel=None):
        kernel.listen('window.notepad.folder_new', self._onNotepadFolderNew, 0)
        kernel.listen('window.notepad.folder_update', self._onNotepadFolderUpdate, 0)
        kernel.listen('window.notepad.folder_remove', self._onNotepadFolderRemove, 0)

        kernel.listen('window.notepad.note_new', self._onNotepadNoteNew)
        kernel.listen('window.notepad.note_update', self._onNotepadNoteUpdate)
        kernel.listen('window.notepad.note_update.folder', self._onNotepadNoteFolder)
        kernel.listen('window.notepad.note_remove', self._onNotepadNoteRemove)

    @inject.params(storage='storage')
    def _onNotepadFolderNew(self, event=None, dispather=None, storage=None):
        if event.data is None:
            return None
        event.data = storage.addFolder(event.data.name, event.data.text)

    @inject.params(storage='storage')
    def _onNotepadFolderUpdate(self, event=None, dispather=None, storage=None):
        folder = event.data
        storage.updateFolder(folder.index, folder.name, folder.text)

    @inject.params(storage='storage')
    def _onNotepadFolderRemove(self, event=None, dispather=None, storage=None):
        folder = event.data
        storage.removeFolder(folder.index, folder.name, folder.text)

    @inject.params(storage='storage')
    def _onNotepadNoteNew(self, event=None, dispather=None, storage=None):
        entity = event.data
        event.data = storage.addNote(entity.name, entity.text, entity.folder)

    @inject.params(storage='storage')
    def _onNotepadNoteUpdate(self, event=None, dispather=None, storage=None):
        entity = event.data
        storage.updateNote(entity.index, entity.name, entity.text)

    @inject.params(storage='storage')
    def _onNotepadNoteRemove(self, event=None, dispather=None, storage=None):
        note = event.data
        storage.removeNote(note.index)

    @inject.params(storage='storage')
    def _onNotepadNoteFolder(self, event=None, dispather=None, storage=None):
        entity, folder = event.data
        if entity is not None and folder is not None:
            storage.updateNoteFolder(entity.index, folder.index)
