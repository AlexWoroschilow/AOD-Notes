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
from PyQt5 import QtWidgets

from .list import RecordList
from .widget import TextEditorWidget


class NotepadEditorWidget(QtWidgets.QSplitter):

    @inject.params(kernel='kernel', config='config')
    def __init__(self, parent=None, kernel=None, config=None):

        super(NotepadEditorWidget, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setObjectName('editorWidget')

        self._list = RecordList()
        self._list.toolbar.setVisible(bool(config.get('notes.leftbar')))
        self._list.toolbar.newAction.clicked.connect(self.onActionNotepadNoteCreateEvent)
        self._list.toolbar.copyAction.clicked.connect(self.onActionNotepadNoteCopyEvent)
        self._list.toolbar.removeAction.clicked.connect(self.onActionRemoveEvent)
        self._list.toolbar.refreshAction.clicked.connect(self.onActionRefreshEvent)
        self._list.folderEditor.returnPressed.connect(self.onActionFolderUpdated)
        self._list.list.doubleClicked.connect(self.onActionNotepadNoteDoubleClick)
        self._list.list.selectionChanged = self.onActionNotepadNoteSelected

        self.addWidget(self._list)

        self._editor = TextEditorWidget(self)
        self.addWidget(self._editor)
        
        self.setStretchFactor(0, 3)
        self.setStretchFactor(1, 3)
        
        if kernel is None or self._editor is None:
            return None
        
        kernel.listen('window.notepad.folder_update', self.onActionFolderUpdate, 128)
        kernel.listen('window.notepad_list.refresh', self.onActionRefreshEvent, 128)
        kernel.listen('window.notepad.note_update', self._editor.onActionNotepadUpdate, 100)
        kernel.listen('window.notepad.note_update', self.onActionUpdateEvent, 128)
        kernel.listen('window.notepad.note_remove', self.onActionNoteRemove, 100)
        kernel.listen('window.notepad.note_new', self.onActionNoteCreate, 128)

    @property
    def entity(self):
        return self._folder

    @entity.setter
    def entity(self, entity=None):
        self._folder = entity
        return self

    @inject.params(storage='storage', kernel='kernel')
    def setContent(self, data=None, storage=None, kernel=None):
        self._folder, self._editor.entity, self._search = data
 
        self._first = None
        self._list.list.clear()
 
        current_index = 0
        self._list.folder = self._folder
        for index, entity in enumerate(storage.notes(folder=self._folder, string=self._search), start=0):
            self._editor.entity = entity if self._editor.entity == None else self._editor.entity
            self._list.addLine(entity)
            if self._editor.entity == entity:
                current_index = index
                
        self._list.list.setCurrentRow(current_index)
        
        self._editor.entity = self._editor.entity
        if self._editor.entity is None:
            self._editor.entity = self._first             

        count = self._list.count()
        message = self.tr('%d records found' % count)
        if self._folder is not None:
            message = self.tr('%s in the folder "%s"' % (
                message, self._folder.name
            ))
         
        kernel.dispatch('window.status', (message, 10))

    @inject.params(kernel='kernel', logger='logger')
    def onActionNotepadNoteCreateEvent(self, event=None, kernel=None, logger=None):
        kernel.dispatch('window.notepad.note_new', (
            'New note', 'New description', self._folder
        ))

    @inject.params(kernel='kernel')
    def onActionNotepadNoteCopyEvent(self, event=None, kernel=None):
        for index in self._list.selectedIndexes():
            item = self._list.itemFromIndex(index)
            if item is not None and item.entity is not None:
                entity = item.entity
                kernel.dispatch('window.notepad.note_new', (
                    entity.name, entity.text, entity.folder
                ))

    @inject.params(kernel='kernel')
    def onActionRemoveEvent(self, event=None, kernel=None):
        message = self._list.tr("Are you sure you want to remove this Note?")
        reply = QtWidgets.QMessageBox.question(self._list, 'Remove note', message, QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.No:
            return None
        for index in self._list.selectedIndexes():
            item = self._list.itemFromIndex(index)
            if item is not None and item.entity is not None:
                kernel.dispatch('window.notepad.note_remove', item.entity)

    def onActionFolderUpdate(self, event):
        entity, widget = event.data
        if entity is None or widget is None:
            return None
        if self._list.folder == entity:
            self._list.folder = entity

    @inject.params(kernel='kernel')
    def onActionFolderUpdated(self, event=None, kernel=None):
        folder = self._list.folder
        folder.name = self._list.folderEditor.text()
        kernel.dispatch('window.notepad.folder_update', (folder, self))

    @inject.params(kernel='kernel')
    def onActionNotepadNoteSelected(self, event=None, selection=None, kernel=None):
        for index in self._list.selectedIndexes():
            item = self._list.itemFromIndex(index)
            if item is not None and item.entity is not None:
                self._editor.entity = item.entity

    def onActionNoteRemove(self, event):
        entity = event.data
        if self._editor is None or entity is None:
            return None
        if self._editor.entity == event.data:
            self._editor.entity = None
        index = self._list.currentRow()
        if index is None:
            return None
        self._list.takeItem(index)

    def onActionNoteCreate(self, event=None):
        entity = event.data
        if entity is None:
            return None
        self._list.addLine(entity)
        total = self._list.count()
        if total is None and total <= 0:
            return None 
        self._list.setCurrentRow(total - 1)

    @inject.params(storage='storage', kernel='kernel')
    def onActionRefreshEvent(self, event=None, kernel=None, storage=None):

        current = self._list.currentRow()
        
        self._list.list.clear()
        for entity in storage.notes(folder=self._folder, string=self._search):
            self._list.addLine(entity)
            
        if current >= self._list.count():
            current = current - 1 if current > 0 else 0
        self._list.setCurrentRow(current)

        count = self._list.count()
        message = self.tr('%d records found' % count)
        if self._folder is not None:
            message = self.tr('%s in the folder "%s"' % (
                message, self._folder.name
            ))
         
        kernel.dispatch('window.status', (message, 10))

    def onActionUpdateEvent(self, event=None):
        entity, widget = event.data
        if entity is None or widget is None:
            return None

        for index in range(0, self._list.count()):
            item = self._list.item(index)
            if item is not None and item.entity == entity:
                item.entity = entity

    @inject.params(kernel='kernel')
    def onActionNotepadNoteDoubleClick(self, event=None, kernel=None):
        item = self._list.item(
            self._list.currentRow()
        )
        if item is None and item.entity is None:
            return None
        
        self._editor.entity = item.entity
        
        editor = TextEditorWidget(self)
        editor.entity = item.entity
        kernel.listen('window.notepad.note_update', editor.onActionNotepadUpdate, 100)

        kernel.dispatch('window.tab', (editor, self._editor.entity))

