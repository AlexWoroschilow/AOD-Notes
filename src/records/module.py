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
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui

from lib.plugin import Loader
from .gui.widget import RecordList


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


class Loader(Loader):
    _list = None
    _folder = None
    _first = None

    @property
    def enabled(self):
        """

        :return:
        """
        return True

    def config(self, binder=None):
        """

        :param binder:
        :return:
        """

    @inject.params(dispatcher='event_dispatcher')
    def boot(self, dispatcher=None):
        """

        :param dispatcher:.
        :return:.
        """
        dispatcher.add_listener('window.first_tab.content', self._onWindowFirstTab)
        dispatcher.add_listener('window.notepad.note_update', self._onNotepadNoteUpdate)
        dispatcher.add_listener('window.notepad.folder_selected', self._onNotepadFolderSelected)

        # listen for the search request from the search module
        # the request string will be given as a data object to the event
        dispatcher.add_listener('window.search.request', self._onSearchRequest, 50)

    @inject.params(storage='storage', dispatcher='event_dispatcher')
    def _onWindowFirstTab(self, event=None, dispatcher=None, storage=None):
        """
        
        :param event: 
        :param dispatcher: 
        :param storage: 
        :return: 
        """
        self._list = RecordList()
        container, parent = event.data
        container.addWidget(self._list)

        self._list.toolbar.newAction.triggered.connect(self._onNotepadNoteNewEvent)
        self._list.toolbar.copyAction.triggered.connect(self._onNotepadNoteCopyEvent)
        self._list.toolbar.savePdf.triggered.connect(self._onSavePdfEvent)
        self._list.toolbar.removeAction.triggered.connect(self._onRemoveEvent)
        self._list.toolbar.refreshAction.triggered.connect(self._onRefreshEvent)
        self._list.folderEditor.returnPressed.connect(self._onFolderUpdated)
        self._list.list.doubleClicked.connect(self._onNotepadNoteDoubleClick)
        self._list.list.selectionChanged = self._onNotepadNoteSelected

        if self._folder is None:
            return None

        self._first = None
        self._list.list.clear()
        for entity in storage.notesByFolder(self._folder):
            if self._first is None:
                self._first = entity
            self._list.addLine(entity)
        self._list.setFolder(self._folder)

        dispatcher.dispatch('window.notepad.note_edit', self._first)

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
                dispatcher.dispatch('window.notepad.note_edit', item.entity)
                self._first = item.entity

    @inject.params(storage='storage')
    def _onNotepadNoteUpdate(self, event=None, dispatcher=None, storage=None):
        """
        
        :param event: 
        :param dispather: 
        :param storage: 
        :return: 
        """
        for index in self._list.list.selectedIndexes():
            item = self._list.list.itemFromIndex(index)
            item.entity = event.data

        self._onRefreshEvent(event, dispatcher)

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
    def _onSavePdfEvent(self, event=None, dispatcher=None):
        """
        
        :param event: 
        :param dispatcher: 
        :return: 
        """
        dispatcher.dispatch('window.notepad.note_export')

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
    def _onNotepadNoteDoubleClick(self, event=None, dispatcher=None):
        """
        
        :param event: 
        :param dispatcher: 
        :return: 
        """
        item = self._list.itemFromIndex(event)
        if item is None and item.entity is None:
            return None

        dispatcher.dispatch('window.notepad.note_select', item.entity)


    @inject.params(dispatcher='event_dispatcher', storage='storage')
    def _onNotepadFolderSelected(self, event=None, dispatcher=None, storage=None):
        """
        
        :param event: 
        :param dispatcher: 
        :return: 
        """
        self._folder, self._search = event.data
        if self._folder is None:
            return None

        if self._list is None:
            return None

        self._first = None
        self._list.list.clear()
        for entity in storage.notesByFolder(self._folder, self._search):
            if self._first is None:
                self._first = entity
            self._list.addLine(entity)
        self._list.setFolder(self._folder)

        dispatcher.dispatch('window.notepad.note_edit', self._first)

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

    @inject.params(dispatcher='event_dispatcher', storage='storage')
    def _onSearchRequest(self, event=None, dispatcher=None, storage=None):
        """
        
        :param event: 
        :param dispatcher: 
        :return: 
        """
        self._list.list.clear()
