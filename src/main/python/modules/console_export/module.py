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

    def enabled(self, options=None, args=None):
        return options.console is True

    @inject.params(storage='storage')
    def boot(self, options=None, args=None, storage=None):
        export = options.console_export
        if export is None: return None
        if not os.path.exists(export):
            os.makedirs(export, exist_ok=True)

        root = storage.rootPath()
        self.export(root, export)

    @inject.params(storage='storage')
    def export(self, path, path_to, storage):
        for entity in storage.entitiesByPath(path, False):

            name = storage.fileName(entity)
            export = "{}/{}".format(path_to, name)
            if storage.isFile(entity):
                content_path = storage.filePath(entity)
                content = storage.fileContent(content_path)
                if content is None: continue
                open(export, 'w').write(content)
                print(export, len(content))
                continue

            if not os.path.exists(export):
                os.makedirs(export, exist_ok=True)

            path = storage.filePath(entity)
            self.export(path, export)
