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
import pydux
import inject
import shutil

from .model import Storage


class Loader(object):

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def __construct_store(self):
        return pydux.create_store(self.init_store, Storage())

    @property
    def enabled(self):
        return True

    def configure(self, binder, options, args):
        binder.bind_to_constructor('store', self.__construct_store)

    @inject.params(store='store')
    def boot(self, options, args, store):
        store.replace_reducer(self.update_store)

    @inject.params(filesystem='store.filesystem')
    def init_store(self, state=None, action=None, filesystem=None):
        state.document = filesystem.document()
        state.group = filesystem.group()

        state.documents.collection = filesystem.documents()
        state.groups.collection = filesystem.groups()
        return state

    @inject.params(filesystem='store.filesystem')
    def update_store(self, state=None, action=None, filesystem=None):
        if action.get('type') == '@@app/storage/resource/selected/document':
            state.document = action.get('entity')
            return state

        if action.get('type') == '@@app/storage/resource/selected/group':
            state.group = action.get('entity')
            if state.group is None: return None
            state.documents.collection = filesystem.documents(state.group)
            return state

        if action.get('type') == '@@app/storage/resource/create/document':
            document = filesystem.document_create(state.group)
            if document is None or not document: return state
            state.documents.collection = filesystem.documents(state.group)
            state.document = document
            return state

        if action.get('type') == '@@app/storage/resource/create/group':
            if state.group is None: return None
            group = filesystem.group_create(state.group)
            if group is None or not group: return state
            state.documents.collection = filesystem.documents(group)
            state.groups.collection = filesystem.groups()
            state.group = group
            return state

        if action.get('type') == '@@app/storage/resource/update/document':
            print('update', action.get('entity'))
            return state

        if action.get('type') == '@@app/storage/resource/remove':
            filesystem.remove(action.get('entity'))
            state.document = filesystem.document()
            state.documents.collection = filesystem.documents()

            state.group = filesystem.group()
            state.groups.collection = filesystem.groups()

            return state

        if action.get('type') == '@@app/storage/resource/clone':
            filesystem.clone(action.get('entity'))
            state.document = filesystem.document()
            state.documents.collection = filesystem.documents()

            state.group = filesystem.group()
            state.groups.collection = filesystem.groups()

            return state

        if action.get('type') == '@@app/storage/resource/rename':
            state.documents.collection = filesystem.documents()
            state.groups.collection = filesystem.groups()

            return state

        if action.get('type') == '@@app/storage/resource/move':
            state.documents.collection = filesystem.documents()
            state.groups.collection = filesystem.groups()

            return state

        return state


module = Loader()
