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

from .filesystem import Note
from .filesystem import Folder
from .filesystem import FilesystemStorage


class Loader(Loader):

    @property
    def enabled(self):
        return True

    def config(self, binder=None):
        binder.bind_to_constructor('storage', self._construct)

    @inject.params(kernel='kernel', settings='widget.settings', config='config')
    def _construct(self, kernel=None, settings=None, config=None):

        from .gui.widget import WidgetSettings
        settings.addWidget(WidgetSettings())

        kernel.listen('folder_new', self._onFolderNew, 0)
        kernel.listen('folder_update', self._onFolderUpdate, 0)
        kernel.listen('folder_remove', self._onFolderRemove, 0)

        kernel.listen('note_new', self._onNoteNew)
        kernel.listen('note_update', self._onNoteUpdate)
        kernel.listen('note_remove', self._onNoteRemove)
        
        storage = config.get('storage.database')
        if len(storage) and storage.find('~') >= 0:
            storage = os.path.expanduser(storage)
        folder = os.path.dirname(storage)
        if not os.path.exists(storage):
            if not os.path.exists(folder):
                os.makedirs(folder)
                
        return FilesystemStorage(folder)

    @inject.params(storage='storage', logger='logger')
    def _onFolderNew(self, event=None, storage=None, logger=None):
        name, text = event.data
        logger.debug('[storage] folder create event: %s, %s' % (name, text))
        storage.create(Folder(name=name))        

    @inject.params(storage='storage', logger='logger')
    def _onNoteNew(self, event=None, storage=None, logger=None):
        name, text, folder = event.data
        logger.debug('[storage] document create event: %s, %s' % (name, text))
        event.data = storage.create(Note(name=name, text=text, folder=folder))        

    @inject.params(storage='storage', logger='logger')
    def _onFolderUpdate(self, event=None, storage=None, logger=None):
        logger.debug('[storage] folder update event: %s' % event.data.path)
        storage.update(event.data)

    @inject.params(storage='storage', logger='logger')
    def _onNoteUpdate(self, event=None, storage=None, logger=None):
        logger.debug('[storage] document update event: %s' % event.data.path)
        storage.update(event.data)

    @inject.params(storage='storage', logger='logger')
    def _onFolderRemove(self, event=None, storage=None, logger=None):
        logger.debug('[storage] folder remove event: %s' % event.data.path)
        storage.delete(event.data)

    @inject.params(storage='storage', logger='logger')
    def _onNoteRemove(self, event=None, storage=None, logger=None):
        logger.debug('[storage] document remove event: %s' % event.data.path)
        storage.delete(event.data)
