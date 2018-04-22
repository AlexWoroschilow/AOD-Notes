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

from .text import TextEditorWidget
from .list import RecordList


class NoteModel(object):

    def __init__(self, name=None, text=None, folder=None):
        self._name = name
        self._folder = folder
        self._text = text

    @property
    def folder(self):
        return self._folder

    @property
    def name(self):
        return self._name

    @property
    def text(self):
        return self._text


class NotepadEditorWidget(QtWidgets.QSplitter):

    @inject.params(kernel='kernel', storage='storage')
    def __init__(self, parent=None, kernel=None, storage=None):
        kernel.listen('window.notepad.note_update', self._onRefreshEvent, 128)
        kernel.listen('window.notepad.note_new', self._onRefreshEvent, 128)
        
        super(NotepadEditorWidget, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setObjectName('editorWidget')

        self._list = RecordList()
        self._list.toolbar.newAction.clicked.connect(self._onNotepadNoteNewEvent)
        self._list.toolbar.copyAction.clicked.connect(self._onNotepadNoteCopyEvent)
        self._list.toolbar.removeAction.clicked.connect(self._onRemoveEvent)
        self._list.toolbar.refreshAction.clicked.connect(self._onRefreshEvent)
        self._list.folderEditor.returnPressed.connect(self._onFolderUpdated)
        self._list.list.doubleClicked.connect(self._onNotepadNoteDoubleClick)
        self._list.list.selectionChanged = self._onNotepadNoteSelected
        self.addWidget(self._list)

        self._editor = TextEditorWidget()
        self.addWidget(self._editor)
        
        self.setStretchFactor(0, 3)
        self.setStretchFactor(1, 3)

    @inject.params(storage='storage')
    def setContent(self, data=None, storage=None):

        self._folder, self._entity, self._search = data
 
        self._first = None
        self._list.list.clear()
        if self._folder is None:
            return None
 
        current_index = 0
        self._list.setFolder(self._folder)
        for index, entity in enumerate(storage.notesByFolder(self._folder, self._search), start=0):
            self._entity = entity if self._entity == None else self._entity
            self._list.addLine(entity)
 
            if self._entity == entity:
                current_index = index
             
        self._list.list.setCurrentRow(current_index)

        self._editor.entity = self._entity
        if self._entity is None:
            self._editor.entity = self._first             

    @inject.params(kernel='kernel')
    def _onNotepadNoteNewEvent(self, event=None, kernel=None):
        model = NoteModel('New note', 'New description', self._folder.index)
        kernel.dispatch('window.notepad.note_new', model)

    @inject.params(dispatcher='kernel')
    def _onNotepadNoteCopyEvent(self, event=None, kernel=None):
        for index in self._list.selectedIndexes():
            item = self._list.itemFromIndex(index)
            if item is not None and item.entity is not None:
                kernel.dispatch('window.notepad.note_new', item.entity)

    @inject.params(kernel='kernel')
    def _onRemoveEvent(self, event=None, kernel=None):
        message = self._list.tr("Are you sure you want to remove this Note?")
        reply = QtWidgets.QMessageBox.question(self._list, 'Remove note', message, QtWidgets.QMessageBox.Yes,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.No:
            return None

        for index in self._list.selectedIndexes():
            item = self._list.itemFromIndex(index)
            if item is not None and item.entity is not None:
                kernel.dispatch('window.notepad.note_remove', item.entity)
                self._list.takeItem(index)

    @inject.params(kernel='kernel')
    def _onFolderUpdated(self, event=None, kernel=None):
        folder = self._list.folder
        folder.name = self._list.folderEditor.text()
        kernel.dispatch('window.notepad.folder_update', folder)

    @inject.params(kernel='kernel')
    def _onNotepadNoteSelected(self, event=None, selection=None, kernel=None):
        for index in self._list.list.selectedIndexes():
            item = self._list.list.itemFromIndex(index)
            if item is not None and item.entity is not None:
                kernel.dispatch('window.notepad.note_edit', item.entity)
                self._editor.entity = item.entity

    @inject.params(kernel='kernel')
    def _onNotepadNoteDoubleClick(self, event=None, kernel=None):
        item = self._list.itemFromIndex(event)
        if item is None and item.entity is None:
            return None

        self._entity = item.entity
        if self._entity is None:
            return None

        editor = TextEditorWidget()
        editor.entity = self._entity

        kernel.dispatch('window.tab', (editor, self._entity))

    @inject.params(storage='storage')
    def _onRefreshEvent(self, event=None, dispatcher=None, storage=None):
        if self._folder is None:
            return None

        current = self._list.list.currentIndex()
        self._list.list.clear()
        for entity in storage.notesByFolder(self._folder):
            self._list.addLine(entity)
            
        if self._list.list.item(current.row()) not in [0]:
            self._list.list.setCurrentIndex(current)
        
        self._list.setFolder(self._folder)

