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


class StorageActions(object):
    def __init__(self):
        pass

    @inject.params(filesystem='store.filesystem')
    def initAction(self, state, action, filesystem):
        state.document = \
            filesystem.document()

        state.group = \
            filesystem.group()

        state.documents.collection = \
            filesystem.documents()

        state.groups.collection = \
            filesystem.groups()

        return state

    @inject.params(search='search')
    def searchAction(self, state, action):
        print(action.get('string'))
        return state

    @inject.params(filesystem='store.filesystem')
    def selectDocumentEvent(self, state, action, filesystem):
        state.document = action.get('entity')
        return state

    @inject.params(filesystem='store.filesystem')
    def selectGroupEvent(self, state, action, filesystem):
        state.group = action.get('entity')

        state.documents.collection = \
            filesystem.documents(state.group)

        return state

    @inject.params(filesystem='store.filesystem')
    def createDocumentEvent(self, state, action, filesystem):
        document = filesystem. \
            document_create(state.group)

        state.documents.collection = \
            filesystem.documents(state.group)

        state.document = document
        return state

    @inject.params(filesystem='store.filesystem')
    def createGroupEvent(self, state, action, filesystem):
        group = filesystem. \
            group_create(state.group)

        state.documents.collection = \
            filesystem.documents(group)

        state.groups.collection = \
            filesystem.groups()

        state.group = group
        return state

    @inject.params(filesystem='store.filesystem')
    def updateDocumentEvent(self, state, action, filesystem):
        return state

    @inject.params(filesystem='store.filesystem')
    def removeResourceEvent(self, state, action, filesystem):
        entity = action.get('entity')

        filesystem.remove(entity)

        state.groups.collection = \
            filesystem.groups()

        state.document = \
            filesystem.document()

        group = type("Group", (object,), {})()
        group.path = entity.parent
        state.group = filesystem.group(group)

        state.documents.collection = \
            filesystem.documents()

        return state

    @inject.params(filesystem='store.filesystem')
    def cloneResourceEvent(self, state, action, filesystem):
        filesystem.clone(action.get('entity'))

        state.group = \
            filesystem.group()

        state.groups.collection = \
            filesystem.groups()

        state.document = \
            filesystem.document()

        state.documents.collection = \
            filesystem.documents()

        return state

    @inject.params(filesystem='store.filesystem')
    def moveResourceEvent(self, state, action, filesystem):

        entity = action.get('entity')
        if entity is None: return state

        destination = action.get('destination')
        if destination is None: return state

        entity.parent = destination
        state.group = destination

        state.groups.collection = \
            filesystem.groups()

        state.documents.collection = \
            filesystem.documents(destination)

        return state

    @inject.params(filesystem='store.filesystem')
    def renameResourceEvent(self, state, action, filesystem):
        state.groups.collection = \
            filesystem.groups()

        state.documents.collection = \
            filesystem.documents()

        return state
