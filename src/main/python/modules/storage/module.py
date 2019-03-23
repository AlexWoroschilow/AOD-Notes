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
import secrets

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
#         path = storage.filePath(storage.rootIndex())
#         sourses = [os.path.join(path, o) for o in os.listdir(path) if os.path.isdir(os.path.join(path, o))]
#         for path in sourses:
#             for child in [os.path.join(path, o) for o in os.listdir(path) if os.path.isdir(os.path.join(path, o))]:
#                 sourses.append(child)
# 
#         print(sourses)
# 
#         for path in sourses:
#             for name in os.listdir(path):
#                 if name in ['.metadata']: continue
# 
#                 path_old = '{}/{}'.format(path, name)
#                 if not os.path.isfile(path_old): continue
#                 if not os.path.exists(path_old): continue
#                 
#                 new = secrets.token_hex(16)
#                 while os.path.exists('{}/{}'.format(path, new)):
#                     new = secrets.token_hex(16)
# 
#                 path_new = '{}/{}'.format(path, new)
#                 #os.rename(path_old, path_new)
        
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
 
