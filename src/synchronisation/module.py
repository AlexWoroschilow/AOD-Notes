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

from lib.plugin import Loader

from .services import SynchronisationService


class Loader(Loader):

    @property
    def enabled(self):
        return True
    
    def config(self, binder=None):
        binder.bind_to_constructor('synchronisation', self._constructor_synchronisation)

    @inject.params(kernel='kernel')
    def boot(self, options=None, args=None, kernel=None):

        kernel.listen('folder_update', self._onFolderUpdate, 128)
        
        kernel.listen('note_new', self._onNoteNew, 128)
        kernel.listen('note_remove', self._onNoteRemove, 128)
        kernel.listen('note_update', self._onNoteUpdate, 128)

    @inject.params(config='config')
    def _constructor_synchronisation(self, config=None):
        destination = os.path.expanduser(config.get('synchronisation.folder'))
        if not os.path.exists(destination):
            if not os.path.exists(destination):
                os.makedirs(destination)
        return SynchronisationService(destination)

    @inject.params(storage='synchronisation', config='config')
    def _onNoteNew(self, event=None, storage=None, config=None):
        note = event.data
        if note is None:
            return None

        if bool(config.get('synchronisation.enabled')):
            storage.dump(note.unique, note.toJson())

    @inject.params(storage='synchronisation', config='config')
    def _onNoteUpdate(self, event=None, storage=None, config=None):
        note, widget = event.data
        if note is None:
            return None
        if bool(config.get('synchronisation.enabled')):
            storage.dump(note.unique, note.toJson())

    @inject.params(storage='synchronisation', config='config')
    def _onNoteRemove(self, event=None, storage=None, config=None):
        note = event.data
        if note is None:
            return None

        if bool(config.get('synchronisation.enabled')):
            storage.dump(note.unique, note.toJson())

    @inject.params(storage='synchronisation', config='config')
    def _onFolderUpdate(self, event=None, storage=None, config=None):
        folder, widget = event.data
        if folder is None:
            return None

        if bool(config.get('synchronisation.enabled')):
            for note in folder.notes: 
                storage.dump(note.unique, note.toJson())
        
