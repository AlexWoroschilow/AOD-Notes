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
import json
import inject       

from watchdog.events import FileSystemEventHandler


class SynchronisationService(FileSystemEventHandler):

    def __init__(self, destination=None):
        self._destination = destination

    @property
    def destination(self):
        return self._destination

    @inject.params(storage='storage')
    def synchronise(self, path=None, storage=None):
        with open(path, 'r') as stream:
            
            storage.synchronise(
                json.loads(stream.read())                
            )
            
            stream.close()

    def dump(self, unique, json):
        
        self._file_last = '%s/%s' % (
            self._destination, unique
        )
        
        with open(self._file_last, 'w') as dump:
            dump.write(json)
            dump.close()

    def on_moved(self, event):
        super(SynchronisationService, self).on_moved(event)

    def on_created(self, event):
        super(SynchronisationService, self).on_created(event)

    def on_deleted(self, event):
        super(SynchronisationService, self).on_deleted(event)
        # if self._file_last == event.src_path:
            # return None 
        if not event.is_directory:
            self.synchronise(event.src_path)

    def on_modified(self, event):
        super(SynchronisationService, self).on_modified(event)
        # if self._file_last == event.src_path:
            # return None 
        if not event.is_directory:
            self.synchronise(event.src_path)

