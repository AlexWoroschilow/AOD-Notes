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
import functools

from PyQt5 import QtWidgets

from lib.plugin import Loader

from .gui.splitter import NotepadEditorWidget


class Loader(Loader):

    @property
    def enabled(self):
        return True
    
    def config(self, binder=None):
        binder.bind_to_constructor('widget.notes', self._constructor_widget_notes)
        binder.bind_to_provider('widget.notes_provider', self._provider_widget_notes)

    @inject.params(kernel='kernel', storage='storage', config='config', folders='widget.folders', editor='widget.editor')
    def _constructor_widget_notes(self, kernel=None, storage=None, config=None, folders=None, editor=None):
        
        widget = NotepadEditorWidget(storage, config, editor)
        widget.reload(folders.selected)
        
        action = functools.partial(self.onActionNoteCreate, widget=widget)
        widget.list.toolbar.newAction.clicked.connect(action)
        
        action = functools.partial(self.onActionNoteCopy, widget=widget)
        widget.list.toolbar.copyAction.clicked.connect(action)
        
        action = functools.partial(self.onActionNoteRemove, widget=widget)
        widget.list.toolbar.removeAction.clicked.connect(action)
        
        action = functools.partial(self.onActionRefresh, widget=widget)
        widget.list.toolbar.refreshAction.clicked.connect(action)

        action = functools.partial(self.onActionFolderUpdate, widget=widget)
        widget.list.folderEditor.returnPressed.connect(action)
        
        action = functools.partial(self.onActionFullScreen, widget=widget)
        widget.list.list.doubleClicked.connect(action)

        action = functools.partial(self.onNoteSelected, widget=widget)
        widget.list.list.clicked.connect(action)

        action = functools.partial(self.onActionRefresh, widget=widget)        
        kernel.listen('folder_update', action, 128)

        action = functools.partial(self.onActionRefresh, widget=widget)        
        kernel.listen('note_remove', action, 100)

        action = functools.partial(self.onActionRefresh, widget=widget)        
        kernel.listen('note_new', action, 128)
        
        action = functools.partial(self.onActionRefresh, widget=widget)        
        kernel.listen('notes_refresh', action, 100)
        
        action = functools.partial(self.onNotepadFolderSelect, widget=widget)        
        kernel.listen('folder_current', action, 128)

        action = functools.partial(self.onSearchRequest, widget=widget)        
        kernel.listen('search_request', action, 100)

        kernel.listen('folder_gointo', self.onNotepadFolderOpen, 128)

        return widget

    @inject.params(kernel='kernel', storage='storage', config='config', folders='widget.folders', editor='widget.editor_provider')
    def _provider_widget_notes(self, kernel=None, storage=None, config=None, folders=None, editor=None):

        widget = NotepadEditorWidget(storage, config, editor)
        widget.reload(folders.selected)

        action = functools.partial(self.onActionNoteCreate, widget=widget)
        widget.list.toolbar.newAction.clicked.connect(action)
        
        action = functools.partial(self.onActionNoteCopy, widget=widget)
        widget.list.toolbar.copyAction.clicked.connect(action)
        
        action = functools.partial(self.onActionNoteRemove, widget=widget)
        widget.list.toolbar.removeAction.clicked.connect(action)
        
        action = functools.partial(self.onActionRefresh, widget=widget)
        widget.list.toolbar.refreshAction.clicked.connect(action)

        action = functools.partial(self.onActionFolderUpdate, widget=widget)
        widget.list.folderEditor.returnPressed.connect(action)
        
        action = functools.partial(self.onActionFullScreen, widget=widget)
        widget.list.list.doubleClicked.connect(action)

        action = functools.partial(self.onNoteSelected, widget=widget)
        widget.list.list.clicked.connect(action)

        action = functools.partial(self.onActionRefresh, widget=widget)        
        kernel.listen('folder_update', action, 128)

        action = functools.partial(self.onActionRefresh, widget=widget)        
        kernel.listen('note_remove', action, 100)

        action = functools.partial(self.onActionRefresh, widget=widget)        
        kernel.listen('note_new', action, 128)
        
        action = functools.partial(self.onActionRefresh, widget=widget)        
        kernel.listen('notes_refresh', action, 100)
        
        return widget

    @inject.params(logger='logger')
    def onNoteSelected(self, event=None, selection=None, widget=None, logger=None):
        logger.debug('[notes] document create event: %s' % widget.current.path)
        widget.note = widget.current

    @inject.params(kernel='kernel', editor='widget.editor_provider')
    def onActionFullScreen(self, event=None, widget=None, kernel=None, editor=None):
        editor.note = widget.current
        kernel.dispatch('window.tab', (editor, editor.note.name))

    @inject.params(kernel='kernel', logger='logger')
    def onActionFolderUpdate(self, event=None, widget=None, kernel=None, logger=None):
        logger.debug('[notes] folder update event: %s' % widget.folder.name)
        widget.folder.name = widget.list.folderEditor.text()
        kernel.dispatch('folder_update', widget.folder)
        kernel.dispatch(widget.folder.id, widget.folder)

    @inject.params(kernel='kernel', logger='logger')
    def onActionNoteCreate(self, event=None, widget=None, kernel=None, logger=None):
        logger.debug('[notes] document create event')
        kernel.dispatch('note_new', ('New note', 'New description', widget.folder))
        widget.reload()

    @inject.params(kernel='kernel', logger='logger')
    def onActionNoteCopy(self, event=None, widget=None, kernel=None, logger=None):
        document = widget.current
        if document is None:
            return None
        logger.debug('[notes] document copy event: %s' % document.path)
        kernel.dispatch('note_new', ('%s (copy)' % document.name, document.text, widget.folder))
        widget.reload(widget.folder)

    @inject.params(kernel='kernel')
    def onActionNoteRemove(self, event=None, widget=None, kernel=None):
        message = widget.tr("Are you sure you want to remove this Note?")
        reply = QtWidgets.QMessageBox.question(widget, 'Remove note', message, QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            kernel.dispatch('note_remove', widget.current)
            widget.reload(None)
            return None

    @inject.params(logger='logger')
    def onActionRefresh(self, event=None, widget=None, logger=None):
        logger.debug('[notes] folder refresh: %s' % widget.folder)
        widget.reload(None)

    @inject.params(logger='logger')
    def onNotepadFolderSelect(self, event=None, widget=None, logger=None):
        logger.debug('[notes] folder selected: %s' % event.data.name)
        widget.reload(event.data)

    @inject.params(kernel='kernel', storage='storage', widget='widget.notes_provider')
    def onNotepadFolderOpen(self, event=None, kernel=None, storage=None, widget=None):
        kernel.dispatch('window.tab', (widget, event.data.name))

    @inject.params(logger='logger')
    def onSearchRequest(self, event=None, widget=None, logger=None):
        logger.debug('[notes] folder search: %s' % event.data.name)
        widget.reload(None, event.data)
