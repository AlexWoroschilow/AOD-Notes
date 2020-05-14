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
import functools
from logging import getLogger

from PyQt5 import QtWidgets
from PyQt5 import QtGui

from .gui.menu import SettingsMenu
from .gui.menu import FolderTreeMenu


class ModuleActions(object):

    @inject.params(store='store')
    def onActionSearch(self, string, store):
        event = {}
        event['type'] = '@@app/search/request'
        event['string'] = string
        store.dispatch(event)

    @inject.params(store='store')
    def onActionCreateNote(self, event, store):
        store.dispatch({
            'type': '@@app/storage/resource/create/document'
        })

    @inject.params(store='store')
    def onActionCreateGroup(self, event, store):
        store.dispatch({
            'type': '@@app/storage/resource/create/group'
        })

    @inject.params(store='store')
    def onActionClone(self, entity, store):
        store.dispatch({
            'type': '@@app/storage/resource/clone',
            'entity': entity
        })

    @inject.params(store='store')
    def onActionRename(self, entity, store):
        store.dispatch({
            'type': '@@app/storage/resource/rename',
            'entity': entity
        })

    @inject.params(store='store')
    def onActionMove(self, event, store):

        entity, destination = event
        if destination is None: return None
        if entity is None: return None

        store.dispatch({
            'type': '@@app/storage/resource/move',
            'destination': destination,
            'entity': entity
        })

    @inject.params(store='store', widget='notepad.dashboard')
    def onActionUpdate(self, store, widget):

        state = store.get_state()
        if state is None:
            return None

        group = state['group'] \
            if 'group' in state.keys() \
            else None

        groups = state['groups'] \
            if 'groups' in state.keys() \
            else None

        document = state['document'] \
            if 'document' in state.keys() \
            else None

        documents = state['documents'] \
            if 'documents' in state.keys() \
            else None

        progress = state['progress'] \
            if 'progress' in state.keys() \
            else None

        widget.setFolders(groups, group)
        widget.setFolderCurrent(group)
        widget.setDocuments(documents, document)
        widget.setProgress(progress)

    @inject.params(store='store', dashboard='notepad.dashboard')
    def onActionMoveNote(self, entity, store, dashboard):
        state = store.get_state()
        if state is None:
            return None

        def moveNoteAction(note, group):
            store.dispatch({
                'type': '@@app/storage/resource/move',
                'destination': group,
                'entity': note
            })

        menu = FolderTreeMenu(dashboard)
        menu.clickedAction.connect(lambda group: moveNoteAction(entity, group))
        menu.clickedAction.connect(lambda group: menu.close())
        menu.setModel(dashboard.model())
        menu.exec_(QtGui.QCursor.pos())

    @inject.params(store='store')
    def onActionGroup(self, entity, store):
        store.dispatch({
            'type': '@@app/storage/resource/selected/group',
            'entity': entity
        })

    @inject.params(store='store')
    def onActionSelectNote(self, entity, store):
        event = {}
        event['type'] = '@@app/storage/resource/selected/document'
        event['entity'] = entity
        store.dispatch(event)

    @inject.params(store='store')
    def onActionSaveNote(self, entity, store):
        event = {}
        event['type'] = '@@app/storage/resource/update/document'
        event['entity'] = entity
        store.dispatch(event)

    @inject.params(store='store')
    def onActionEditNote(self, entity, store):
        event = {}
        event['type'] = '@@app/storage/resource/selected/document'
        event['entity'] = entity
        store.dispatch(event)

    @inject.params(window='window', editor='notepad.editor')
    def onActionFullScreen(self, entity, window, editor):
        editor = editor.open(entity)
        editor.saveNoteAction.connect(self.onActionSaveNote)
        window.newTabAction.emit((editor, entity.name))

    @inject.params(store='store', status='status', window='window')
    def onActionRemove(self, entity, store, status, window):

        message = window.tr('Are you sure you want to remove this element: "{}" ?'.format(
            entity.name
        ))

        reply = QtWidgets.QMessageBox.question(
            window, 'Remove "{}" ?'.format(entity.name),
            message, QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No
        )

        if reply == QtWidgets.QMessageBox.No:
            return None

        store.dispatch({
            'type': '@@app/storage/resource/remove',
            'entity': entity
        })

    @inject.params(store='store', window='window')
    def onActionContextMenu(self, event, entity, window, store):

        state = store.get_state()
        if state is None: return None

        menu = SettingsMenu(window)
        menu.addAction(QtGui.QIcon("icons/note"), 'New Document', lambda: self.onActionCreateNote(entity))
        menu.addAction(QtGui.QIcon("icons/book"), 'New Group', lambda: self.onActionCreateGroup(entity))
        menu.addSeparator()
        menu.addAction(QtGui.QIcon("icons/copy"), 'Clone', lambda: self.onActionClone(entity))
        menu.addAction(QtGui.QIcon("icons/trash"), 'Remove', lambda: self.onActionRemove(entity))

        menu.exec_(QtGui.QCursor.pos())

    @inject.params(store='store', config='config', widget='window')
    def onActionNoteImport(self, event=None, store=None, config=None, widget=None):

        currentwd = config.get('storage.lastimport', os.path.expanduser('~'))
        selector = QtWidgets.QFileDialog(None, 'Select file', currentwd)
        if not selector.exec_(): return None

        for path in selector.selectedFiles():
            if not os.path.exists(path) or os.path.isdir(path): continue
            config.set('storage.lastimport', os.path.dirname(path))

            if os.path.getsize(path) / 1000000 >= 1:
                message = "The file  '{}' is about {:>.2f} Mb, are you sure?".format(path,
                                                                                     os.path.getsize(path) / 1000000)
                reply = QtWidgets.QMessageBox.question(widget, 'Message', message, QtWidgets.QMessageBox.Yes,
                                                       QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.No: continue

            with open(path, 'r') as stream:
                store.dispatch({
                    'type': '@@app/storage/resource/create/document',
                    'content': stream.read()
                })
                stream.close()
