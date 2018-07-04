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

    @inject.params(kernel='kernel')
    def _constructor_synchronisation(self, kernel=None):
        destination = os.path.expanduser('~/FitbaseCloud/CloudNotes')
        if not os.path.exists(destination):
            if not os.path.exists(destination):
                os.makedirs(destination)
        return SynchronisationService(destination)

    @property
    def enabled(self):
        return True
    
    def config(self, binder=None):
        binder.bind_to_constructor('synchronisation', self._constructor_synchronisation)

    @inject.params(kernel='kernel')
    def boot(self, options=None, args=None, kernel=None):

        kernel.listen('note_new', self._onNoteNew, 128)
        kernel.listen('note_update', self._onNoteUpdate, 128)
        kernel.listen('note_remove', self._onNoteRemove, 128)

    @inject.params(storage='synchronisation', kernel='kernel', logger='logger')
    def _onNoteNew(self, event=None, storage=None, kernel=None, logger=None):
        note = event.data
        storage.dump(note.unique, note.toJson())

    @inject.params(storage='synchronisation', kernel='kernel', logger='logger')
    def _onNoteUpdate(self, event=None, storage=None, kernel=None, logger=None):
        note, widget = event.data
        storage.dump(note.unique, note.toJson())

    @inject.params(storage='synchronisation', kernel='kernel', logger='logger')
    def _onNoteRemove(self, event=None, storage=None, kernel=None, logger=None):
        note = event.data
        storage.dump(note.unique, note.toJson())

