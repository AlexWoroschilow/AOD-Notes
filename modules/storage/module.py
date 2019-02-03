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


class Loader(Loader):

    @property
    def enabled(self):
        return True

    def config(self, binder=None):
        binder.bind_to_constructor('storage', self._config)
        binder.bind_to_constructor('encryptor', self._encryptor)

    @inject.params(storage='storage', encryptor='encryptor')
    def boot(self, options, args, storage, encryptor):
#         for index in storage.entities():
#             if storage.isDir(index):
#                 continue
#             content = storage.fileContent(index)
#             storage.setFileContent(index, content)
        pass

    @inject.params(config='config')
    def _config(self, config=None):

        storage = config.get('storage.location')
        if len(storage) and storage.find('~') >= 0:
            storage = os.path.expanduser(storage)
        if not os.path.exists(storage):
            if not os.path.exists(storage):
                os.makedirs(storage)

        from .filesystem import FilesystemStorage
        return FilesystemStorage(storage)
 
    @inject.params(config='config')
    def _encryptor(self, config=None):
        from .cryptography import CryptoAES 
        return CryptoAES(config.get('cryptography.password'))
 
