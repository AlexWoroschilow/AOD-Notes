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

from lib.plugin import Loader
from .gui.widget import FolderList


class Loader(Loader):
    _first = None
    _search = None
    _widget = None

    @property
    def enabled(self):
        return True

    def config(self, binder=None):
        binder.bind('folders', self)

    @inject.params(kernel='kernel')
    def boot(self, options=None, args=None, kernel=None):
        # listen for the search request from the search module
        # the request string will be given as a data object to the event
        kernel.listen('window.search.request', self._onSearchRequest, 100)
        kernel.listen('window.dashboard.content', self._onWindowFirstTab, 100)
        kernel.listen('window.notepad.folder_update', self._onFolderUpdated, 128)
        kernel.listen('window.notepad.folder_new', self._onRefreshEvent, 128)

    @inject.params(kernel='kernel', storage='storage')
    def _onWindowFirstTab(self, event=None, kernel=None, storage=None):
        
        self._widget = FolderList()
        self._widget.toolbar.newAction.clicked.connect(self._onFolderNewEvent)
        self._widget.toolbar.copyAction.clicked.connect(self._onFolderCopyEvent)
        self._widget.toolbar.refreshAction.clicked.connect(self._onRefreshEvent)
        self._widget.toolbar.removeAction.clicked.connect(self._onFolderRemoveEvent)

        self._widget.list.doubleClicked.connect(self._onFolderOpen)
        self._widget.list.selectionChanged = self._onFolderSelected

        self._first = None
        self._widget.list.clear()
        for folder in storage.folders():
            if self._first is None:
                self._first = folder
            self._widget.addLine(folder)
        self._widget.list.setCurrentRow(0)

        container, parent = event.data
        container.addWidget(self._widget)

        if self._first is None:
            return None

        message = self._widget.tr('%d folders found' % self._widget.list.count())
        kernel.dispatch('window.status', (message, 10))

        kernel.dispatch('window.notepad.folder_selected', (
            self._first, self._search, None
        ))
        
    @property
    def selected(self):
        if self._widget is None:
            return None
        for index in self._widget.selectedIndexes():
            item = self._widget.itemFromIndex(index)
            if item is not None:
                return item.folder
        return None

    @inject.params(kernel='kernel')
    def _onFolderNewEvent(self, event=None, kernel=None):
        kernel.dispatch('window.notepad.folder_new', (
            'New folder', 'New folder description'
        ))

    @inject.params(kernel='kernel')
    def _onFolderCopyEvent(self, event=None, kernel=None):
        for index in self._widget.list.selectedIndexes():
            item = self._widget.list.itemFromIndex(index)
            if item is not None and item.folder is not None:
                kernel.dispatch('window.notepad.folder_new', item.folder)

    @inject.params(kernel='kernel')
    def _onFolderRemoveEvent(self, event=None, kernel=None):
        message = self._widget.tr("Are you sure you want to remove this Folder?")
        reply = QtWidgets.QMessageBox.question(self._widget, 'Remove folder', message, QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.No:
            return None

        for index in self._widget.selectedIndexes():
            item = self._widget.itemFromIndex(index)
            if item is None and item.folder is None:
                continue

            kernel.dispatch('window.notepad.folder_remove', item.folder)
            self._widget.takeItem(index)
            
        message = self._widget.tr('%d folders found' % self._widget.list.count())
        kernel.dispatch('window.status', (message, None))

    @inject.params(kernel='kernel', storage='storage')
    def _onRefreshEvent(self, event=None, kernel=None, storage=None):
        current = self._widget.list.currentIndex()
        
        self._widget.list.clear()
        for entity in storage.folders():
            self._widget.addLine(entity)

        if self._widget.list.item(current.row()) not in [0]:
            self._widget.list.setCurrentIndex(current)

        message = self._widget.tr('%d folders found' % self._widget.list.count())
        kernel.dispatch('window.status', (message, None))

    @inject.params(kernel='kernel')
    def _onFolderOpen(self, event=None, selection=None, kernel=None):
        for index in self._widget.selectedIndexes():
            item = self._widget.itemFromIndex(index)
            if item is None or item.folder is None:
                continue

            self._first = item.folder
            kernel.dispatch('window.notepad.folder_open', (
                self._first, self._search
            ))

    @inject.params(kernel='kernel')
    def _onFolderSelected(self, event=None, selection=None, kernel=None):
        for index in self._widget.selectedIndexes():
            item = self._widget.itemFromIndex(index)
            if item is None or item.folder is None:
                continue

            self._first = item.folder
            kernel.dispatch('window.notepad.folder_selected', (
                self._first, self._search, None
            ))

    def _onFolderUpdated(self, event=None):
        if len(self._widget.list.selectedIndexes()):
            for index in self._widget.list.selectedIndexes():
                item = self._widget.list.itemFromIndex(index)
                item.folder = event.data
            return None
        item = self._widget.list.item(0)
        item.folder = event.data

    @inject.params(kernel='kernel', storage='storage')
    def _onSearchRequest(self, event=None, kernel=None, storage=None):
        self._search = event.data
        if self._search is None:
            return None

        self._first = None
        self._widget.list.clear()
        for entity in storage.folders(string=self._search):
            if self._first is None:
                self._first = entity
            self._widget.addLine(entity)