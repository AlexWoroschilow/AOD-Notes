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

    def __init__(self, storage=None, config=None, editor=None):
        self.storage = storage
        self.string = None

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
            self._editor.note = entity
        return self

    @property
    def current(self):
        """
        Get current selected document
        if no document was selected return 
        the first document in the list
        """
        for index in self.list.list.selectedIndexes():
            item = self.list.list.itemFromIndex(index)
            if item is not None and item.entity is not None:
                return item.entity
        item = self.list.item(0)
        if item is not None and item.entity is not None:
            return item.entity
        return None

    def reload(self, folder=None, string=None):
        self.folder = folder if folder is not None else self.folder 
        self.string = string if string is not None else self.string 

        cache = self.list.currentRow()
        self.list.list.clear()
        for entity in self.storage.notes(folder=self.folder, string=self.string):
            self.list.addLine(entity)
        if cache >= self.list.count():
            cache = cache - 1 if cache > 0 else 0
        self.list.setCurrentRow(cache)

    def clear(self):
        if self.list is None:
            return None
        self.list.clear()

    def onActionFolderUpdate(self, event):
        if self.list.folder == event.data:
            self.list.folder = event.data

    def onActionNoteRemove(self, event=None):
        entity = event.data
        if self._editor is None or entity is None:
            return None
        if self._editor.note == event.data:
            self._editor.note = None
        index = self.list.currentRow()
        if index is None:
            return None
        self.list.takeItem(index)

    def onActionNoteCreate(self, event=None):
        self.reload(None, None)
