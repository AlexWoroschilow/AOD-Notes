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
        return {
            'document': filesystem.document(),
            'documents': filesystem.documents(),
            'group': filesystem.group(),
            'groups': filesystem.groups(),
        }

    @inject.params(search='search')
    def searchAction(self, state, action, search):
        print(action.get('string'))
        return state

    @inject.params(filesystem='store.filesystem')
    def selectDocumentEvent(self, state, action, filesystem):
        entity = action.get('entity')
        if entity is None:
            return state

        group = type("Group", (object,), {})()
        group.path = entity.parent

        return {
            'group': filesystem.group(group),
            'document': entity,
        }

    @inject.params(filesystem='store.filesystem')
    def selectGroupEvent(self, state, action, filesystem):
        group = action.get('entity')
        if group is None:
            return state

        return {
            'groups': filesystem.groups(),
            'documents': filesystem.documents(group),
            'group': group
        }

    @inject.params(filesystem='store.filesystem')
    def createDocumentEvent(self, state, action, filesystem):
        group = state['group']
        if group is None:
            return state

        return {
            'document': filesystem.document_create(group),
            'documents': filesystem.documents(group),
            'group': filesystem.group(group)
        }

    @inject.params(filesystem='store.filesystem')
    def createGroupEvent(self, state, action, filesystem):

        group = state['group']
        if group is None:
            return state

        group = filesystem.group_create(group)
        if group is None:
            return state

        return {
            'groups': filesystem.groups(),
            'documents': filesystem.documents(group),
            'group': group
        }

    @inject.params(filesystem='store.filesystem')
    def updateDocumentEvent(self, state, action, filesystem):
        return state

    @inject.params(filesystem='store.filesystem')
    def removeResourceEvent(self, state, action, filesystem):
        entity = action.get('entity')
        if entity is None:
            return state

        filesystem.remove(entity)

        group = type("Group", (object,), {})()
        group.path = entity.parent

        return {
            'groups': filesystem.groups(),
            'documents': filesystem.documents(group),
            'document': filesystem.document(),
            'group': filesystem.group(group)
        }

    @inject.params(filesystem='store.filesystem')
    def cloneResourceEvent(self, state, action, filesystem):
        entity = action.get('entity')
        if entity is None:
            return state

        filesystem.clone(entity)

        group = type("Group", (object,), {})()
        group.path = entity.parent

        return {
            'groups': filesystem.groups(),
            'documents': filesystem.documents(group),
            'document': filesystem.document(),
            'group': filesystem.group(group)
        }

    @inject.params(filesystem='store.filesystem')
    def moveResourceEvent(self, state, action, filesystem):
        entity = action.get('entity')
        if entity is None:
            return state

        destination = action.get('destination')
        if destination is None:
            return state

        entity.parent = destination

        return {
            'groups': filesystem.groups(),
            'documents': filesystem.documents(destination),
            'document': filesystem.document(),
            'group': filesystem.group(destination)
        }

    @inject.params(filesystem='store.filesystem')
    def renameResourceEvent(self, state, action, filesystem):
        return {
            'groups': filesystem.groups(),
            'documents': filesystem.documents(),
            'document': filesystem.document(),
            'group': filesystem.group()
        }
