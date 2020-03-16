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

    @inject.params(store='store', status='status')
    def onActionSearch(self, string, store, status):
        try:
            store.dispatch({
                'type': '@@app/search/request',
                'string': string
            })
        except Exception as ex:
            status.error(ex.__str__())

    @inject.params(store='store', status='status')
    def onActionCreateNote(self, event, store, status):
        try:
            store.dispatch({'type': '@@app/storage/resource/create/document'})
        except Exception as ex:
            status.error(ex.__str__())

    @inject.params(store='store', status='status')
    def onActionCreateGroup(self, event, store, status):
        try:
            store.dispatch({'type': '@@app/storage/resource/create/group'})
        except Exception as ex:
            status.error(ex.__str__())

    @inject.params(store='store', status='status')
    def onActionClone(self, entity, store, status):
        try:
            store.dispatch({'type': '@@app/storage/resource/clone',
                            'entity': entity})
        except Exception as ex:
            status.error(ex.__str__())

    @inject.params(store='store', status='status')
    def onActionRename(self, entity, store, status):
        try:
            store.dispatch({'type': '@@app/storage/resource/rename',
                            'entity': entity})
        except Exception as ex:
            status.error(ex.__str__())

    @inject.params(store='store', status='status')
    def onActionMove(self, event, store, status):
        try:

            entity, destination = event
            if destination is None: return None
            if entity is None: return None

            store.dispatch({
                'type': '@@app/storage/resource/move',
                'destination': destination,
                'entity': entity
            })
        except Exception as ex:
            status.error(ex.__str__())

    @inject.params(store='store', widget='notepad.dashboard')
    def onActionUpdate(self, store, widget):
        try:

            state = store.get_state()
            if state is None: return None

            groups = state.groups
            if not groups.fresh:
                return None

            widget.setFolders(groups.collection, state.group)

        except Exception as ex:
            print(ex)

    @inject.params(store='store', status='status', window='window')
    def onActionMoveNote(self, entity, store, status, window):
        try:

            state = store.get_state()
            if state is None: return None

            def moveNoteAction(note, group):
                store.dispatch({
                    'type': '@@app/storage/resource/move',
                    'destination': group,
                    'entity': note
                })

            menu = FolderTreeMenu(window)
            menu.clickedAction.connect(lambda group: moveNoteAction(entity, group))
            menu.clickedAction.connect(lambda group: menu.close())
            menu.setFolders(state.groups.collection, state.group)
            menu.exec_(QtGui.QCursor.pos())

        except Exception as ex:
            print(ex)
            status.error(ex.__str__())

    @inject.params(store='store', status='status')
    def onActionGroup(self, entity, store, status):
        try:
            store.dispatch({'type': '@@app/storage/resource/selected/group',
                            'entity': entity})
        except Exception as ex:
            status.error(ex.__str__())

    @inject.params(store='store', status='status')
    def onActionSelectNote(self, entity, store, status):
        try:
            store.dispatch({
                'type': '@@app/storage/resource/selected/document',
                'entity': entity
            })
        except Exception as ex:
            status.error(ex.__str__())

    @inject.params(store='store', status='status')
    def onActionSaveNote(self, entity, store, status):
        try:
            store.dispatch({'type': '@@app/storage/resource/update/document',
                            'entity': entity})
        except Exception as ex:
            status.error(ex.__str__())

    @inject.params(store='store', status='status')
    def onActionEditNote(self, entity, store, status):
        try:
            store.dispatch({'type': '@@app/storage/resource/selected/document',
                            'entity': entity})
        except Exception as ex:
            status.error(ex.__str__())

    @inject.params(window='window', editor='notepad.editor')
    def onActionFullScreen(self, entity, window, editor):
        try:

            editor = editor.open(entity)
            editor.saveNoteAction.connect(self.onActionSaveNote)
            window.tab.emit((editor, entity.name))

        except Exception as ex:
            getLogger('app').exception(ex)

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

        try:
            store.dispatch({'type': '@@app/storage/resource/remove',
                            'entity': entity})
        except Exception as ex:
            status.error(ex.__str__())

    @inject.params(config='config', status='status')
    def onActionConfigUpdated(self, event, config, widget, status):

        try:
            visible = int(config.get('folders.toolbar'))
            widget.toolbar.setVisible(visible)

        except AttributeError as ex:
            getLogger('app').exception(ex)
            status.error(ex.__str__())

        self.onActionConfigUpdatedEditor(event, widget=widget.editor)

    @inject.params(config='config', logger='logger')
    def onActionConfigUpdatedEditor(self, event, widget, config, logger):

        try:
            visible = int(config.get('editor.formatbar'))
            widget.formatbar.setVisible(visible)
        except AttributeError as ex:
            logger.exception(ex)

        try:
            visible = int(config.get('editor.leftbar'))
            widget.leftbar.setVisible(visible)
        except AttributeError as ex:
            logger.exception(ex)

        try:
            visible = int(config.get('editor.rightbar'))
            widget.rightbar.setVisible(visible)
        except AttributeError as ex:
            logger.exception(ex)

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

    @inject.params(storage='storage', config='config')
    def onActionNoteImport(self, event=None, storage=None, config=None, widget=None):
        if widget is None or storage is None or config is None: return None

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

            with open(path, 'r') as source:
                index = widget.current
                if index is None or not index:
                    index = config.get('storage.location')
                    index = storage.index(index)

                if not storage.isDir(index):
                    index = config.get('storage.location')
                    index = storage.index(index)

                if storage.isFile(index):
                    index = config.get('storage.location')
                    index = storage.index(index)

                name = os.path.basename(path)
                index = storage.touch(index, name)
                if index is None:
                    return None

                index = storage.setFileContent(index, source.read())
                if index is None:
                    return None

                widget.created.emit(index)

                source.close()

    @inject.params(storage='storage', dashboard='notepad.dashboard')
    def onActionStorageChanged(self, destination, storage, dashboard, widget):
        dashboard.tree.setModel(storage)
        index = storage.setRootPath(destination)
        dashboard.tree.setRootIndex(index)
        dashboard.group(index)
