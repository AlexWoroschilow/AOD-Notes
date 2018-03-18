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

from lib.plugin import Loader

from .gui.widget import FolderList
from PyQt5.QtWidgets import QTreeView, QFileSystemModel, QApplication


class FolderModel(object):
    def __init__(self, name=None, text=None):
        """
        
        :param name: 
        :param text: 
        """
        self._name = name
        self._text = text

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
        dispatcher.add_listener('window.notepad.folder_update', self._onFolderUpdated)

    @inject.params(storage='storage')
    def _onWindowFirstTab(self, event=None, dispatcher=None, storage=None):
        """
        
        :param event: 
        :param dispatcher: 
        :return: 
        """

        self._list = FolderList()
        self._list.toolbar.newAction.triggered.connect(self._onFolderNewEvent)
        self._list.toolbar.copyAction.triggered.connect(self._onFolderCopyEvent)
        self._list.toolbar.refreshAction.triggered.connect(self._onRefreshEvent)
        self._list.toolbar.removeAction.triggered.connect(self._onFolderRemoveEvent)

        self._list.list.doubleClicked.connect(self._onFolderSelected)
        self._list.list.selectionChanged = self._onFolderSelected

        first = None
        self._list.list.clear()
        for folder in storage.folders:
            if first is None:
                first = folder
            self._list.addLine(folder)

        if first is not None:
            dispatcher.dispatch('window.notepad.folder_selected', first)

        container, parent = event.data
        container.addWidget(self._list)

    @inject.params(dispatcher='event_dispatcher')
    def _onFolderNewEvent(self, event=None, dispatcher=None):
        """

        :param event: 
        :return: 
        """

        model = FolderModel('New folder', 'New folder description')
        event = dispatcher.dispatch('window.notepad.folder_new', model)
        if event is not None and event.data is not None:
            self._list.addLine(event.data)

    @inject.params(dispatcher='event_dispatcher')
    def _onFolderCopyEvent(self, event=None, dispatcher=None):
        """

        :param event: 
        :return: 
        """
        for index in self._list.list.selectedIndexes():
            item = self._list.list.itemFromIndex(index)
            if item is not None and item.folder is not None:
                model = FolderModel(item.folder.name, item.folder.text)
                event = dispatcher.dispatch('window.notepad.folder_new', item.folder)
                if event is not None and event.data is not None:
                    self._list.addLine(event.data)

    @inject.params(dispatcher='event_dispatcher')
    def _onFolderRemoveEvent(self, event=None, dispatcher=None):
        """
        
        :param event: 
        :param dispatcher: 
        :return: 
        """
        message = self._list.tr("Are you sure you want to remove this Folder?")
        reply = QtWidgets.QMessageBox.question(self._list, 'Remove folder', message, QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.No:
            return None

        for index in self._list.list.selectedIndexes():
            item = self._list.list.itemFromIndex(index)
            if item is not None and item.folder is not None:
                dispatcher.dispatch('window.notepad.folder_remove', item.folder)
                self._list.list.takeItem(index.row())

    @inject.params(dispatcher='event_dispatcher', storage='storage')
    def _onRefreshEvent(self, event=None, dispatcher=None, storage=None):
        """

        :param event: 
        :param dispatcher: 
        :param storage: 
        :return: 
        """
        self._list.list.clear()
        for entity in storage.folders:
            self._list.addLine(entity)

    @inject.params(dispatcher='event_dispatcher')
    def _onFolderSelected(self, event=None, selection=None, dispatcher=None):
        """

        :param event: 
        :param selection: 
        :param dispatcher: 
        :return: 
        """
        for index in self._list.list.selectedIndexes():
            item = self._list.list.itemFromIndex(index)
            if item is not None and item.folder is not None:
                dispatcher.dispatch('window.notepad.folder_selected', item.folder)

    def _onFolderUpdated(self, event=None, dispatcher=None):
        """
        
        :param event: 
        :param dispatcher: 
        :return: 
        """
        if len(self._list.list.selectedIndexes()):
            for index in self._list.list.selectedIndexes():
                item = self._list.list.itemFromIndex(index)
                item.folder = event.data
            return None
        item = self._list.list.item(0)
        item.folder = event.data
