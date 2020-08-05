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
from .decorators import service_search_decorator
from .decorators import service_config_decorator
from .thread import SearchThread


class StorageActions(object):
    thread = SearchThread()

    @inject.params(filesystem='store.filesystem')
    def searchIndexProgressAction(self, state, action, filesystem):
        """

        :param state:
        :param action:
        :param filesystem:
        :return:
        """
        return {'progress': action.get('progress')}

    @inject.params(filesystem='store.filesystem')
    def searchIndexAction(self, state, action, filesystem):
        """

        :param state:
        :param action:
        :param filesystem:
        :return:
        """
        self.thread.start()
        return state

    @service_config_decorator
    @inject.params(filesystem='store.filesystem')
    def locationSwitchAction(self, state, action, filesystem):
        """

        :param state:
        :param action:
        :param filesystem:
        :return:
        """
        response = {}
        response['documents'] = filesystem.documents()
        response['groups'] = filesystem.groups()
        response['document'] = filesystem.document()
        response['group'] = filesystem.group()
        response['progress'] = state['progress'] \
            if 'progress' in state.keys() \
            else None

        return response

    @service_config_decorator
    @inject.params(filesystem='store.filesystem')
    def initAction(self, state, action, filesystem):
        """

        :param state:
        :param action:
        :param filesystem:
        :return:
        """
        response = {}
        response['documents'] = filesystem.documents()
        response['groups'] = filesystem.groups()
        response['document'] = filesystem.document()
        response['group'] = filesystem.group()
        response['progress'] = state['progress'] \
            if 'progress' in state.keys() \
            else None

        return response

    @inject.params(search='search', filesystem='store.filesystem')
    def searchAction(self, state, action, search, filesystem):
        """

        :param state:
        :param action:
        :param search:
        :param filesystem:
        :return:
        """
        progress = state['progress'] \
            if 'progress' in state.keys() \
            else None

        string = action.get('string')
        if not len(string): return None

        search_result = {
            'title': string,
            'documents': []
        }

        for path in search.search(string):
            model = type("Document", (object,), {})()
            model.path = path

            document = filesystem.document(model)
            if document is None:
                continue

            search_result['documents'] \
                .append(document)

        return {
            'progress': progress,
            'group': filesystem.group(),
            'search': [search_result]
        }

    @service_config_decorator
    @inject.params(filesystem='store.filesystem')
    def selectDocumentEvent(self, state, action, filesystem):
        """

        :param state:
        :param action:
        :param filesystem:
        :return:
        """
        progress = state['progress'] \
            if 'progress' in state.keys() \
            else None

        entity = action.get('entity')
        if entity is None: return state

        group = type("Group", (object,), {})()
        group.path = entity.parent

        return {
            'progress': progress,
            'document': entity
        }

    @service_config_decorator
    @inject.params(filesystem='store.filesystem')
    def foundDocumentEvent(self, state, action, filesystem):
        """

        :param state:
        :param action:
        :param filesystem:
        :return:
        """
        progress = state['progress'] \
            if 'progress' in state.keys() \
            else None

        entity = action.get('entity')
        if entity is None: return state

        group = type("Group", (object,), {})()
        group.path = entity.parent

        return {
            'progress': progress,
            'documents': filesystem.documents(group),
            'group': filesystem.group(group),
            'document': entity
        }

    @service_config_decorator
    @inject.params(filesystem='store.filesystem')
    def selectGroupEvent(self, state, action, filesystem):
        """

        :param state:
        :param action:
        :param filesystem:
        :return:
        """
        progress = state['progress'] \
            if 'progress' in state.keys() \
            else None

        group = action.get('entity')
        if group is None: return state

        return {
            'progress': progress,
            'groups': filesystem.groups(),
            'documents': filesystem.documents(group),
            'group': group
        }

    @service_search_decorator
    @inject.params(filesystem='store.filesystem')
    def createDocumentEvent(self, state, action, filesystem):
        """

        :param state:
        :param action:
        :param filesystem:
        :return:
        """
        if 'group' not in state.keys():
            return state

        progress = state['progress'] \
            if 'progress' in state.keys() \
            else None

        group = state['group']
        if group is None: return state

        document = filesystem.document_create(group)
        if document is None: return state

        content = action.get('content')
        if content is not None and len(content):
            document.content = content

        return {
            'progress': progress,
            'document': document,
            'documents': filesystem.documents(group),
            'group': filesystem.group(group)
        }

    @inject.params(filesystem='store.filesystem')
    def createGroupEvent(self, state, action, filesystem):
        """

        :param state:
        :param action:
        :param filesystem:
        :return:
        """
        progress = state['progress'] \
            if 'progress' in state.keys() \
            else None

        group = state['group']
        if group is None: return state

        group = filesystem.group_create(group)
        if group is None: return state

        return {
            'progress': progress,
            'groups': filesystem.groups(),
            'documents': filesystem.documents(group),
            'group': group
        }

    @service_search_decorator
    @inject.params(filesystem='store.filesystem')
    def updateDocumentEvent(self, state, action, filesystem):
        """

        :param state:
        :param action:
        :param filesystem:
        :return:
        """
        if 'search' in state.keys():
            del (state['search'])

        state['document'] = filesystem.document()
        state['progress'] = state['progress'] \
            if 'progress' in state.keys() \
            else None

        return state

    @service_search_decorator
    @inject.params(filesystem='store.filesystem')
    def removeResourceEvent(self, state, action, filesystem):
        """

        :param state:
        :param action:
        :param filesystem:
        :return:
        """
        progress = state['progress'] \
            if 'progress' in state.keys() \
            else None

        entity = action.get('entity')
        if entity is None: return state

        filesystem.remove(entity)

        group = type("Group", (object,), {})()
        group.path = entity.parent

        return {
            'progress': progress,
            'groups': filesystem.groups(),
            'documents': filesystem.documents(group),
            'document': filesystem.document(),
            'group': filesystem.group(group)
        }

    @service_search_decorator
    @inject.params(filesystem='store.filesystem')
    def cloneResourceEvent(self, state, action, filesystem):
        """

        :param state:
        :param action:
        :param filesystem:
        :return:
        """
        progress = state['progress'] \
            if 'progress' in state.keys() \
            else None

        entity = action.get('entity')
        if entity is None: return state

        filesystem.clone(entity)

        group = type("Group", (object,), {})()
        group.path = entity.parent

        return {
            'progress': progress,
            'groups': filesystem.groups(),
            'documents': filesystem.documents(group),
            'document': filesystem.document(),
            'group': filesystem.group(group)
        }

    @service_search_decorator
    @inject.params(filesystem='store.filesystem')
    def moveResourceEvent(self, state, action, filesystem):
        """

        :param state:
        :param action:
        :param filesystem:
        :return:
        """
        progress = state['progress'] \
            if 'progress' in state.keys() \
            else None

        entity = action.get('entity')
        if entity is None: return state

        destination = action.get('destination')
        if destination is None: return state

        entity.parent = destination

        return {
            'progress': progress,
            'groups': filesystem.groups(),
            'documents': filesystem.documents(destination),
            'document': filesystem.document(),
            'group': filesystem.group(destination)
        }

    @service_search_decorator
    @inject.params(filesystem='store.filesystem')
    def renameResourceEvent(self, state, action, filesystem):
        """

        :param state:
        :param action:
        :param filesystem:
        :return:
        """
        progress = state['progress'] \
            if 'progress' in state.keys() \
            else None

        return {
            'progress': progress,
            'groups': filesystem.groups(),
            'documents': filesystem.documents(),
            'document': filesystem.document(),
            'group': filesystem.group()
        }
