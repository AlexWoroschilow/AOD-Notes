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
import shutil

from lib.plugin import Loader


class Loader(Loader):

    @property
    def enabled(self):
        return True

    def config(self, binder=None):
        binder.bind_to_constructor('encryptor', self._encryptor)
        binder.bind_to_constructor('storage', self._storage)

    @inject.params(storage='storage', encryptor='encryptor')
    def boot(self, options, args, storage, encryptor):
        path = storage.filePath(storage.rootIndex())
        sourses = [os.path.join(path, o) for o in os.listdir(path) if os.path.isdir(os.path.join(path, o))]
        while len(sourses) > 0:
            path = sourses.pop()
            for child in [os.path.join(path, o) for o in os.listdir(path) if os.path.isdir(os.path.join(path, o))]:
                sourses.append(child)
#                 
#             if os.path.exists('{}/.metadata'.format(path)):
#                 os.remove('{}/.metadata'.format(path))
# 
#             metadata = storage.touch(storage.index(path), '.metadata')
#             storage.setFileContent(metadata, os.path.basename(path))
# 
            #print(path, os.path.basename(path))

#         for index in storage.entities():
#             if not storage.isDir(index):
#                 continue
#             index_metadata = storage.index('{}/.metadata'.format(storage.filePath(index)))
#              
#             name = os.path.basename(storage.filePath(index))
#             storage.setFileContent(index_metadata, name)
        pass

    @inject.params(config='config')
    def _storage(self, config=None):

        storage = config.get('storage.location')
        if len(storage) and storage.find('~') >= 0:
            storage = os.path.expanduser(storage)
        if not os.path.exists(storage):
            if not os.path.exists(storage):
                os.makedirs(storage)

        from .service.storage import FilesystemStorage
        return FilesystemStorage(storage)
 
    @inject.params(config='config')
    def _encryptor(self, config=None):
        from .service.cryptography import CryptoAES 
        return CryptoAES(config.get('cryptography.password'))
 
