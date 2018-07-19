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
import json

from watchdog.events import FileSystemEventHandler


class SynchronisationService(FileSystemEventHandler):

    def __init__(self, destination=None):
        self._destination = destination
        self._current = None
        self._thread = None        

    @property
    def thread(self):
        return self._thread

    @thread.setter
    def thread(self, value):
        self._thread = value

    @property
    def destination(self):
        return self._destination

    def read(self, path=None):
        if self.thread is None:
            return None
        
        with open(path, 'r') as stream:
            entity = json.loads(stream.read())
            stream.close()
            return entity
        return None

    def dump(self, unique=None, json=None):
        
        self._current = '%s/%s' % (
            self.destination, unique
        )
        
        with open(self._current, 'w') as dump:
            dump.write(json)
            dump.close()

    def on_moved(self, event):
        super(SynchronisationService, self).on_moved(event)
        pass

    def on_created(self, event):
        super(SynchronisationService, self).on_created(event)
        if not event.is_directory and os.path.exists(event.src_path):
            entity = self.read(event.src_path)
            if entity is not None and entity:
                self.thread.create.emit(entity)

    def on_modified(self, event):
        super(SynchronisationService, self).on_modified(event)
        if not event.is_directory and os.path.exists(event.src_path):
            entity = self.read(event.src_path)
            if entity is not None and entity:
                self.thread.update.emit(entity)

    def on_deleted(self, event):
        super(SynchronisationService, self).on_deleted(event)
        if not event.is_directory and os.path.exists(event.src_path):
            print('on_deleted', event.src_path)
