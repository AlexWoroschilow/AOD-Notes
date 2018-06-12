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
import textwrap
from bs4 import BeautifulSoup

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

    @inject.params(config='config')
    def _bind_storage(self, config=None):
        storage = config.get('storage.database')
        if len(storage) and storage.find('~') >= 0:
            storage = os.path.expanduser(storage)
        folder = os.path.dirname(storage)
        if not os.path.exists(storage):
            if not os.path.exists(folder):
                os.makedirs(folder)
        return SQLAlechemyStorage(storage)

    @inject.params(kernel='kernel')
    def boot(self, options=None, args=None, kernel=None):
        kernel.listen('folder_new', self._onNotepadFolderNew, 0)
        kernel.listen('folder_update', self._onNotepadFolderUpdate, 0)
        kernel.listen('folder_remove', self._onNotepadFolderRemove, 0)

        kernel.listen('note_new', self._onNotepadNoteNew)
        kernel.listen('note_update', self._onNotepadNoteUpdate)
        kernel.listen('note_remove', self._onNotepadNoteRemove)

    @inject.params(storage='storage', logger='logger')
    def _onNotepadFolderNew(self, event=None, storage=None, logger=None):
        entity, widget = event.data
        if entity is None or widget is None:
            return None
        
        name, text = entity 
        entity = Folder(name=name, createdAt=datetime.now(), total=0)        
        event.data = (storage.create(entity), widget)

    @inject.params(storage='storage', logger='logger')
    def _onNotepadFolderUpdate(self, event=None, storage=None, logger=None):
        logger.debug('[storage] - _onNotepadFolderUpdate')
        entity, widget = event.data
        if entity is None or widget is None:
            return None
        storage.update(entity)

    @inject.params(storage='storage', logger='logger')
    def _onNotepadFolderRemove(self, event=None, storage=None, logger=None):
        entity, widget = event.data
        if entity is None or widget is None:
            return None
        storage.delete(entity)

    @inject.params(storage='storage', kernel='kernel', logger='logger')
    def _onNotepadNoteNew(self, event=None, storage=None, kernel=None, logger=None):
        logger.debug('[storage] - _onNotepadNoteNew')
        if event.data is None:
            return None
        name, text, folder = event.data

        entity = Note(name=name, text=text, folder=folder, createdAt=datetime.now())
        event.data = storage.create(entity)
        
        if folder is None or kernel is None:
            return None
        
        event = (folder, self)
        kernel.dispatch('folder_%s_update' % folder.id, event)

    @inject.params(storage='storage', kernel='kernel', logger='logger')
    def _onNotepadNoteUpdate(self, event=None, storage=None, kernel=None, logger=None):
        logger.debug('[storage] - _onNotepadNoteUpdate')
        entity, widget = event.data 
        if entity is None:
            return None
        
        text = entity.description.replace('\r', ' ').replace('\n', ' ')
        entity.description = '%s...' % textwrap.fill(text[0:200], 80)
        storage.update(entity)

        folder = entity.folder 
        if folder is None or kernel is None:
            return None

        event = (folder, self)
        kernel.dispatch('folder_%s_update' % folder.id, event)

    @inject.params(storage='storage', kernel='kernel', logger='logger')
    def _onNotepadNoteRemove(self, event=None, storage=None, kernel=None, logger=None):
        logger.debug('[storage] - _onNotepadNoteRemove')
        if event.data is None:
            return None
        folder = event.data.folder
        storage.delete(event.data)
        
        if folder is None or kernel is None:
            return None
        
        event = (folder, self)
        kernel.dispatch('folder_%s_update' % folder.id, event)
