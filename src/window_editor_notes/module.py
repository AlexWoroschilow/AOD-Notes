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

    @inject.params(kernel='kernel', config='config', editor='widget.editor')
    def _constructor_widget_notes(self, kernel=None, config=None, editor=None):
        
        widget = NotepadEditorWidget(kernel, config, editor)
        
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

        kernel.listen('folder_update', widget.onActionFolderUpdate, 128)
        kernel.listen('note_remove', widget.onActionNoteRemove, 100)
        kernel.listen('note_new', widget.onActionNoteCreate, 128)
        
        return widget

    @inject.params(kernel='kernel', config='config', editor='widget.editor_provider')
    def _provider_widget_notes(self, kernel=None, config=None, editor=None):

        widget = NotepadEditorWidget(kernel, config, editor)

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
        
        kernel.listen('folder_update', widget.onActionFolderUpdate, 128)
        kernel.listen('note_remove', widget.onActionNoteRemove, 100)
        kernel.listen('note_new', widget.onActionNoteCreate, 128)
        
        return widget

    @property
    def enabled(self):
        return True
    
    def config(self, binder=None):
        binder.bind_to_constructor('widget.notes', self._constructor_widget_notes)
        binder.bind_to_provider('widget.notes_provider', self._provider_widget_notes)

    @inject.params(kernel='kernel')
    def boot(self, options=None, args=None, kernel=None):
        kernel.listen('dashboard_content', self.onWindowDashboard, 128)
        kernel.listen('search_request', self.onSearchRequest, 100)
        
        kernel.listen('folder_open', self.onNotepadFolderOpen, 128)
        kernel.listen('folder_select', self.onNotepadFolderSelect, 128)

        self._folder = None
        self._search = None
        self._note = None

    @inject.params(kernel='kernel', editor_new='widget.editor_provider')
    def onActionFullScreen(self, event=None, widget=None, kernel=None, editor_new=None):
        item = widget.list.item(widget.list.currentRow())
        if item is None:
            return None
        note = item.entity
        if note is None:
            return None
        
        widget.note = note
        editor_new.note = note

        event = (editor_new, editor_new.note)
        kernel.dispatch('window.tab', event)

    @inject.params(kernel='kernel')
    def onActionFolderUpdate(self, event=None, widget=None, kernel=None):
        if widget.folder is None:
            return None
        
        folder = widget.folder
        folder.name = widget.list.folderEditor.text()
        
        event = (folder, widget)
        kernel.dispatch('folder_update', event)
        if folder.id is not None:
            event = (folder, widget)
            kernel.dispatch('folder_%s_update' % folder.id, event)

    @inject.params(kernel='kernel')
    def onActionNoteCreate(self, event=None, widget=None, kernel=None):
        event = (widget.tr('New note'), widget.tr('New description'), widget.folder)
        kernel.dispatch('note_new', event)

    @inject.params(kernel='kernel')
    def onActionNoteCopy(self, event=None, widget=None, kernel=None):
        for index in widget.list.selectedIndexes():
            item = widget.list.itemFromIndex(index)
            if item is None:
                continue
            note = item.entity
            if note is None:
                continue
            
            event = (note.name, note.text, note.folder)
            kernel.dispatch('note_new', event)

    @inject.params(kernel='kernel')
    def onActionNoteRemove(self, event=None, widget=None, kernel=None):
        message = widget.tr("Are you sure you want to remove this Note?")
        reply = QtWidgets.QMessageBox.question(widget, 'Remove note', message, QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.No:
            return None
        for index in widget.list.selectedIndexes():
            item = widget.list.itemFromIndex(index)
            if item is None or item.entity is None:
                continue
            kernel.dispatch('note_remove', item.entity)

    @inject.params(storage='storage', kernel='kernel')
    def onActionRefresh(self, event=None, widget=None, storage=None, kernel=None):

        current = widget.list.currentRow()
        
        widget.list.list.clear()
        for entity in storage.notes(folder=widget.folder, string=widget.search):
            widget.list.addLine(entity)
            
        if current >= widget.list.count():
            current = current - 1 if current > 0 else 0
        widget.list.setCurrentRow(current)

        count = widget.list.count()
        message = widget.tr('%d records found' % count)
        if widget.folder is not None:
            message = widget.tr('%s in the folder "%s"' % (
                message, widget.folder.name
            ))
         
        kernel.dispatch('window.status', (message, 10))

    @inject.params(widget='widget.notes')
    def onWindowDashboard(self, event=None, widget=None):
        container, parent = event.data
        if container is not None:
            container.addWidget(widget)

    @inject.params(storage='storage', kernel='kernel', widget='widget.notes')
    def onNotepadFolderSelect(self, event=None, storage=None, kernel=None, widget=None):
        self._folder, self._search, self._note = event.data
        if self._folder is None:
            return None

        widget.clear()
        for note in storage.notes(folder=self._folder, string=self._search):
            widget.add_note(note)
            if self._note is None:
                self._note = note    
        if self._note is not None:
            widget.note = self._note
        widget.folder = self._folder

        count = widget.list.count()
        if widget.folder is None:
            event = (widget.tr('%d records found' % count), 10)
            return kernel.dispatch('window.status', event)

        event = (widget.tr('%s in the folder "%s"' % (
            widget.tr('%d records found' % count), widget.folder.name
        )), 10)
        
        return kernel.dispatch('window.status', event)

    @inject.params(kernel='kernel', storage='storage', editor='widget.notes_provider')
    def onNotepadFolderOpen(self, event=None, kernel=None, storage=None, editor=None):
        self._folder, self._search = event.data
        if self._folder is None:
            return None

        self._note = None    

        editor.clear()
        for note in storage.notes(folder=self._folder, string=self._search):
            editor.add_note(note)
            if self._note is None:
                self._note = note    
        if self._note is not None:
            editor.note = self._note
        editor.folder = self._folder

        event = (editor, self._folder)
        kernel.dispatch('window.tab', event)

    @inject.params(storage='storage', widget='widget.notes')
    def onSearchRequest(self, event=None, storage=None, widget=None):
        self._search = event.data
        if self._search is None:
            return None

        self._folder = None
        self._note = None
         
        widget.clear()
        for note in storage.notes(folder=self._folder, string=self._search):
            widget.add_note(note)
            if self._note is None:
                self._note = note    
        if self._note is not None:
            widget.note = self._note
        widget.folder = self._folder
