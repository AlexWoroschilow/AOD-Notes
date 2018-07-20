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
import textwrap
import time
import random 
import string 

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
    def boot(self, options=None, args=None, kernel=None):
        kernel.listen('folder_new', self._onFolderNew, 0)
        kernel.listen('folder_update', self._onFolderUpdate, 0)
        kernel.listen('folder_remove', self._onFolderRemove, 0)

        kernel.listen('note_new', self._onNoteNew)
        kernel.listen('note_update', self._onNoteUpdate)
        kernel.listen('note_remove', self._onNoteRemove)
        
        kernel.listen('synchronisation_update', self.onActionSynchronisation)
        kernel.listen('synchronisation_create', self.onActionSynchronisation)

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

    @inject.params(storage='storage')
    def _synchroniseFolder(self, candidate=None, storage=None):
        if candidate is None or not candidate:
            return (None, None)
        
        assert('name' in candidate.keys())
        assert('total' in candidate.keys())
        assert('unique' in candidate.keys())

        folder = storage.folder(candidate['name'])
        if folder is not None and folder:
            return (folder, False)
            
        folder = storage.create(Folder(
                    name=candidate['name'],
                    unique=candidate['unique'],
                    total=candidate['total'],
                    createdAt=datetime.now()
                ))   
        
        if folder is not None and folder:
            return (folder, True)

    @inject.params(storage='storage')
    def _synchroniseNote(self, candidate=None, folder=None, storage=None):

        assert('name' in candidate.keys())
        assert('unique' in candidate.keys())
        assert('description' in candidate.keys())
        assert('version' in candidate.keys())
        assert('text' in candidate.keys())
        assert('tags' in candidate.keys())

        note = storage.note(candidate['unique'])
        if note is not None and note:
            note.name = candidate['name']
            note.version = candidate['version']
            note.description = candidate['description']
            note.text = candidate['text']
            note.tags = candidate['tags']
            note.folder = folder
            
            return (storage.update(note), False)

        return (storage.create(Note(name=candidate['name'], text=candidate['text'],
           description=candidate['description'], unique=candidate['unique'],
           version=candidate['version'], createdAt=datetime.now(), folder=folder 
        )), True)
        
    @inject.params(kernel='kernel', storage='storage')
    def onActionSynchronisation(self, event=None, kernel=None, storage=None):
        entity = event.data
        if entity is None:
            return None

        assert('folder' in entity.keys())
        folder, folder_created = self._synchroniseFolder(entity['folder'])

        assert('note' in entity.keys())
        note, note_created = self._synchroniseNote(entity['note'], folder)

        if note is not None and note_created == True:
            kernel.dispatch('notes_refresh', (note, None))

        if note is not None and note_created == False:
            kernel.dispatch(note.unique, (note, None))
        
        if folder is not None and folder_created == True:
            kernel.dispatch('folders_refresh', (folder, None))
            
        if folder is not None and folder_created == False:
            kernel.dispatch(folder.id, (folder, None))

    @property
    def unique_string(self):
        return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(32))

    @inject.params(storage='storage', logger='logger')
    def _onFolderNew(self, event=None, storage=None, logger=None):
        entity, widget = event.data
        if entity is None or widget is None:
            return None
        
        name, text = entity
        entity = Folder(name=name, createdAt=datetime.now(), total=0, unique=self.unique_string)        
        event.data = (storage.create(entity), widget)

    @inject.params(storage='storage', logger='logger')
    def _onFolderUpdate(self, event=None, storage=None, logger=None):
        logger.debug('[storage] - _onFolderUpdate')
        entity, widget = event.data
        if entity is None or widget is None:
            return None
        storage.update(entity)

    @inject.params(storage='storage', logger='logger')
    def _onFolderRemove(self, event=None, storage=None, logger=None):
        entity, widget = event.data
        if entity is None or widget is None:
            return None
        storage.delete(entity)

    @inject.params(storage='storage', kernel='kernel', logger='logger')
    def _onNoteNew(self, event=None, storage=None, kernel=None, logger=None):
        logger.debug('[storage] - _onNoteNew')
        if event.data is None:
            return None
        name, text, folder = event.data

        entity = Note(
            name=name, text=text, folder=folder,
            createdAt=datetime.now(), version=int(time.time()),
            unique=self.unique_string
        )
        
        event.data = storage.create(entity)
        
        if folder is None or kernel is None:
            return None
        
        event = (folder, self)
        kernel.dispatch(folder.id, event)

    @inject.params(storage='storage', kernel='kernel', logger='logger')
    def _onNoteUpdate(self, event=None, storage=None, kernel=None, logger=None):
        logger.debug('[storage] - _onNoteUpdate')
        entity, widget = event.data 
        if entity is None:
            return None
        
        if entity.description is not None and len(entity.description):
            text = entity.description.replace('\r', ' ').replace('\n', ' ')
            entity.description = '%s...' % textwrap.fill(text[0:200], 80)

        entity.version = int(time.time())

        storage.update(entity)

        folder = entity.folder 
        if folder is None or kernel is None:
            return None

        event = (folder, self)
        kernel.dispatch(folder.id, event)

    @inject.params(storage='storage', kernel='kernel', logger='logger')
    def _onNoteRemove(self, event=None, storage=None, kernel=None, logger=None):
        logger.debug('[storage] - _onNoteRemove')
        if event.data is None:
            return None
        folder = event.data.folder
        storage.delete(event.data)
        
        if folder is None or kernel is None:
            return None
        
        event = (folder, self)
        kernel.dispatch(folder.id, event)
