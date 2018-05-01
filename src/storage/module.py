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
from datetime import datetime

from lib.plugin import Loader
from .sqlalchemy import Note
from .sqlalchemy import Folder
from .sqlalchemy import SQLAlechemyStorage


class Loader(Loader):

    @property
    def enabled(self):
        return True

    def config(self, binder=None):
        binder.bind_to_constructor('storage', self._bind_storage)

    @inject.params(kernel='kernel')
    def _bind_storage(self, kernel=None):
        if kernel.options.storage is None:
            raise "Storage destination can not be empty"
        storage = kernel.options.storage
        folder = os.path.dirname(storage)
        if not os.path.exists(storage):
            if not os.path.exists(folder):
                os.makedirs(folder)
                
        return SQLAlechemyStorage(kernel.options.storage)

    @inject.params(kernel='kernel')
    def boot(self, options=None, args=None, kernel=None):
        kernel.listen('window.notepad.folder_new', self._onNotepadFolderNew, 0)
        kernel.listen('window.notepad.folder_update', self._onNotepadFolderUpdate, 0)
        kernel.listen('window.notepad.folder_remove', self._onNotepadFolderRemove, 0)

        kernel.listen('window.notepad.note_new', self._onNotepadNoteNew)
        kernel.listen('window.notepad.note_update', self._onNotepadNoteUpdate)
        kernel.listen('window.notepad.note_remove', self._onNotepadNoteRemove)

    @inject.params(storage='storage', logger='logger')
    def _onNotepadFolderNew(self, event=None, storage=None, logger=None):
        logger.debug('[storage] - _onNotepadFolderNew')
        if event.data is None:
            return None
        name, text = event.data 
        entity = Folder(name=name, createdAt=datetime.now(), total=0)        
        event.data = storage.create(entity)

    @inject.params(storage='storage', logger='logger')
    def _onNotepadFolderUpdate(self, event=None, storage=None, logger=None):
        logger.debug('[storage] - _onNotepadFolderUpdate')
        if event.data is None:
            return None
        storage.update(event.data)

    @inject.params(storage='storage', logger='logger')
    def _onNotepadFolderRemove(self, event=None, storage=None, logger=None):
        logger.debug('[storage] - _onNotepadFolderRemove')
        if event.data is None:
            return None
        storage.delete(event.data)

    @inject.params(storage='storage', logger='logger')
    def _onNotepadNoteNew(self, event=None, storage=None, logger=None):
        logger.debug('[storage] - _onNotepadNoteNew')
        if event.data is None:
            return None
        name, text, folder = event.data
        entity = Note(name=name, text=text, folder=folder, createdAt=datetime.now())        
        event.data = storage.create(entity)

    @inject.params(storage='storage', logger='logger')
    def _onNotepadNoteUpdate(self, event=None, storage=None, logger=None):
        logger.debug('[storage] - _onNotepadNoteUpdate')
        if event.data is None:
            return None
        storage.update(event.data)

    @inject.params(storage='storage', logger='logger')
    def _onNotepadNoteRemove(self, event=None, storage=None, logger=None):
        logger.debug('[storage] - _onNotepadNoteRemove')
        if event.data is None:
            return None
        storage.delete(event.data)
