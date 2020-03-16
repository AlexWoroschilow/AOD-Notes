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
import inject
from logging import getLogger


class ModuleActions(object):

    @inject.params(store='store', window='window')
    def onActionEditRequest(self, entity, store, window):
        try:

            print(entity)

            window.tabSwitch.emit(0)
            return None

        except Exception as ex:
            getLogger('search') \
                .exception(ex)

    @inject.params(storage='storage', search='search')
    def onNoteCreated(self, index, storage, search):

        try:
            # update search index only after
            # the update was successful
            name = storage.fileName(index)
            path = storage.filePath(index)

            content = storage.fileContent(index)
            if content is None or not len(content):
                return None

            search.append(name, path, content)

        except Exception as ex:
            logger = getLogger('search')
            logger.exception(ex)

    @inject.params(storage='storage', search='search')
    def onNoteUpdated(self, index, storage, search):

        try:
            # update search index only after
            # the update was successful
            name = storage.fileName(index)
            path = storage.filePath(index)

            content = storage.fileContent(index)
            if content is None or not len(content):
                return None

            search.update(name, path, content)

        except Exception as ex:
            logger = getLogger('search')
            logger.exception(ex)

    @inject.params(storage='storage', search='search')
    def onNoteRemoved(self, index, storage, search):

        try:
            # update search index only after
            # the update was successful
            path = storage.filePath(index)
            if path is None or not len(path):
                return None

            search.remove(path)

        except Exception as ex:
            logger = getLogger('search')
            logger.exception(ex)
