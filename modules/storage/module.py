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

from .filesystem import FilesystemStorage
from .filesystem import Note
from .filesystem import Folder


class Loader(Loader):

    @property
    def enabled(self):
        return True

    def config(self, binder=None):
        binder.bind_to_constructor('storage', self._construct)
        binder.bind_to_provider('storage.note', Note)
        binder.bind_to_provider('storage.folder', Folder)

    @inject.params(config='config')
    def _construct(self, config=None):

        storage = config.get('storage.location')
        if len(storage) and storage.find('~') >= 0:
            storage = os.path.expanduser(storage)
        folder = os.path.dirname(storage)
        if not os.path.exists(storage):
            if not os.path.exists(folder):
                os.makedirs(folder)
                
        return FilesystemStorage(folder)
 
