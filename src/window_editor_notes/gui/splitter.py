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
from PyQt5 import QtWidgets

from .list import RecordList


class NotepadEditorWidget(QtWidgets.QSplitter):

    def __init__(self, kernel=None, config=None, editor=None):
        self._editor = editor
        self._folder = None
        self._search = None
        self._note = None
        self._entity = None

        super(NotepadEditorWidget, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.setObjectName('editorWidget')

        self.list = RecordList()
        self.list.toolbar.setVisible(bool(config.get('notes.leftbar')))
        self.list.list.selectionChanged = self.onActionSelectionChanged

        self.addWidget(self.list)

        self.addWidget(self._editor)
        
        self.setStretchFactor(0, 3)
        self.setStretchFactor(1, 3)

    @property
    def entity(self):
        return self._folder

    @entity.setter
    def entity(self, entity=None):
        self._folder = entity
        return self

    @property
    def search(self):
        return self._search

    @property
    def folder(self):
        return self._folder

    @folder.setter
    def folder(self, entity=None):
        self._folder = entity
        if self.list is not None:
            self.list.folder = entity
        return self

    @property
    def note(self):
        if self._note is not None:
            return self._note
        return None

    @note.setter
    def note(self, entity=None):
        self._note = entity
        if self._editor is not None:
            self._editor.entity = entity
        return self

    def clear(self):
        if self.list is None:
            return None
        self.list.clear()

    def add_note(self, note=None):
        if self.list is not None and note is not None:
            self.list.addLine(note)

    def onActionFolderUpdate(self, event):
        entity, widget = event.data
        if entity is None or widget is None:
            return None
        if self.list.folder == entity:
            self.list.folder = entity

    def onActionSelectionChanged(self, event=None, selection=None):
        for index in self.list.selectedIndexes():
            item = self.list.itemFromIndex(index)
            if item is not None and item.entity is not None:
                self._editor.entity = item.entity

    def onActionNoteRemove(self, event=None):
        entity = event.data
        if self._editor is None or entity is None:
            return None
        if self._editor.entity == event.data:
            self._editor.entity = None
        index = self.list.currentRow()
        if index is None:
            return None
        self.list.takeItem(index)

    def onActionNoteCreate(self, event=None):
        entity = event.data
        if entity is None:
            return None
        self.list.addLine(entity)
        total = self.list.count()
        if total is None and total <= 0:
            return None 
        self.list.setCurrentRow(total - 1)
