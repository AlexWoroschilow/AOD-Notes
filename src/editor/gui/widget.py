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
from PyQt5.QtCore import Qt

from PyQt5 import QtCore
from PyQt5 import QtPrintSupport
from PyQt5 import QtWidgets
from PyQt5 import QtGui

from .text import TextEditorWidget
from .text import NameEditor
from .text import TextWriter

from .bar import ToolbarbarWidgetLeft
from .bar import ToolbarbarWidgetRight
from .bar import FormatbarWidget
from .list import RecordList


class NoteModel(object):
    def __init__(self, name=None, text=None, folder=None):
        """

        :param name: 
        :param text: 
        """
        self._name = name
        self._folder = folder
        self._text = text

    @property
    def folder(self):
        """

        :return: 
        """
        return self._folder

    @property
    def name(self):
        """

        :return: 
        """
        return self._name

    @property
    def text(self):
        """

        :return: 
        """
        return self._text


class NotepadEditorWidget(QtWidgets.QSplitter):
    _entity = None
    _editor = None
    _folder = None
    _search = None

    @inject.params(dispatcher='event_dispatcher', storage='storage')
    def __init__(self, parent=None, dispatcher=None, storage=None):
        """
        
        :param parent: 
        :param dispatcher: 
        :param storage: 
        """
        super(NotepadEditorWidget, self).__init__(parent)

        dispatcher.add_listener('window.notepad.note_update', self._onNotepadNoteUpdate, 128)

        self._list = RecordList()
        self._editor = TextEditorWidget()

        self._list.toolbar.newAction.triggered.connect(self._onNotepadNoteNewEvent)
        self._list.toolbar.copyAction.triggered.connect(self._onNotepadNoteCopyEvent)
        self._list.toolbar.removeAction.triggered.connect(self._onRemoveEvent)
        self._list.toolbar.refreshAction.triggered.connect(self._onRefreshEvent)
        self._list.folderEditor.returnPressed.connect(self._onFolderUpdated)
        self._list.list.doubleClicked.connect(self._onNotepadNoteDoubleClick)
        self._list.list.selectionChanged = self._onNotepadNoteSelected

        self.addWidget(self._list)
        self.addWidget(self._editor)

    @inject.params(storage='storage')
    def setContent(self, data=None, storage=None):
        """
        
        :param folder: 
        :param storage: 
        :return: 
        """

        self._folder, self._entity, self._search = data

        self._first = None
        self._list.list.clear()
        if self._folder is not None:
            for entity in storage.notesByFolder(self._folder, self._search):
                if self._first is None:
                    self._first = entity
                self._list.addLine(entity)
        self._list.setFolder(self._folder)
        self._editor.setEntity(self._first if self._entity is None else self._entity)

    @inject.params(dispatcher='event_dispatcher')
    def _onNotepadNoteNewEvent(self, event=None, dispatcher=None):
        """

        :param event: 
        :param dispatcher: 
        :return: 
        """
        model = NoteModel('New note', 'New description', self._folder.index)
        event = dispatcher.dispatch('window.notepad.note_new', model)
        if event is not None and event.data is not None:
            self._list.addLine(event.data)
            self._first = event.data

        self._onRefreshEvent(event, dispatcher)

    @inject.params(dispatcher='event_dispatcher')
    def _onNotepadNoteCopyEvent(self, event=None, dispatcher=None):
        """

        :param event: 
        :param dispatcher: 
        :return: 
        """
        for index in self._list.selectedIndexes():
            item = self._list.itemFromIndex(index)
            if item is not None and item.entity is not None:
                event = dispatcher.dispatch('window.notepad.note_new', item.entity)
                self._list.addLine(event.data)

        self._onRefreshEvent(event, dispatcher)

    @inject.params(dispatcher='event_dispatcher')
    def _onRemoveEvent(self, event=None, dispatcher=None):
        """

        :param event: 
        :param dispatcher: 
        :return: 
        """
        message = self._list.tr("Are you sure you want to remove this Note?")
        reply = QtWidgets.QMessageBox.question(self._list, 'Remove note', message, QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.No:
            return None

        for index in self._list.selectedIndexes():
            item = self._list.itemFromIndex(index)
            if item is not None and item.entity is not None:
                dispatcher.dispatch('window.notepad.note_remove', item.entity)
                self._list.takeItem(index)

    @inject.params(dispatcher='event_dispatcher', storage='storage')
    def _onRefreshEvent(self, event=None, dispatcher=None, storage=None):
        """

        :param event: 
        :param dispatcher: 
        :param storage: 
        :return: 
        """
        if self._folder is None:
            return None

        self._list.list.clear()
        for entity in storage.notesByFolder(self._folder):
            self._list.addLine(entity)
        self._list.setFolder(self._folder)

    @inject.params(dispatcher='event_dispatcher')
    def _onFolderUpdated(self, event=None, dispatcher=None):
        """

        :param event: 
        :param dispatcher: 
        :return: 
        """
        folder = self._list.folder
        folder.name = self._list.folderEditor.text()
        dispatcher.dispatch('window.notepad.folder_update', folder)

    @inject.params(dispatcher='event_dispatcher')
    def _onNotepadNoteSelected(self, event=None, selection=None, dispatcher=None):
        """

        :param event: 
        :param selection: 
        :param dispatcher: 
        :return: 
        """
        for index in self._list.list.selectedIndexes():
            item = self._list.list.itemFromIndex(index)
            if item is not None and item.entity is not None:
                self._editor.setEntity(item.entity)

    @inject.params(dispatcher='event_dispatcher')
    def _onNotepadNoteDoubleClick(self, event=None, dispatcher=None):
        """

        :param event: 
        :param dispatcher: 
        :return: 
        """
        item = self._list.itemFromIndex(event)
        if item is None and item.entity is None:
            return None

        self._entity = item.entity
        if self._entity is None:
            return None

        editor = TextEditorWidget()
        editor.setEntity(self._entity)

        dispatcher.dispatch('window.tab', (editor, self._entity))

    @inject.params(storage='storage')
    def _onNotepadNoteUpdate(self, event=None, dispatcher=None, storage=None):
        """

        :param event: 
        :param dispather: 
        :param storage: 
        :return: 
        """

        self._entity = event.data
        self.setContent((self._folder, self._entity, self._search))
