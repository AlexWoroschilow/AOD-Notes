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

    @inject.params(storage='storage')
    def _onWindowFirstTab(self, event=None, dispatcher=None, storage=None):
        """
        
        :param event: 
        :param dispatcher: 
        :return: 
        """

        self.list = FolderList()
        self.list.toolbar.newAction.triggered.connect(self._onNewEvent)
        self.list.toolbar.copyAction.triggered.connect(self._onCopyEvent)
        self.list.toolbar.refreshAction.triggered.connect(self._onRefreshEvent)
        self.list.list.doubleClicked.connect(self._onFolderSelected)
        self.list.list.selectionChanged = self._onFolderSelected

        first = None
        self.list.list.clear()
        for folder in storage.folders:
            if first is None:
                first = folder
            self.list.addLine(folder)

        if first is not None:
            dispatcher.dispatch('window.notepad.folder_selected', first)

        container, parent = event.data
        container.addWidget(self.list)

    @inject.params(dispatcher='event_dispatcher')
    def _onNewEvent(self, event=None, dispatcher=None):
        """

        :param event: 
        :return: 
        """
        self.list.addLine(FolderModel('New folder', 'New folder description'))
        dispatcher.dispatch('window.notepad.folder_new', FolderModel('New folder', 'New folder description'))

    @inject.params(dispatcher='event_dispatcher')
    def _onCopyEvent(self, event=None, dispatcher=None):
        """

        :param event: 
        :return: 
        """
        dispatcher.dispatch('window.notepad.folder_copy')

    @inject.params(dispatcher='event_dispatcher', storage='storage')
    def _onRefreshEvent(self, event=None, dispatcher=None, storage=None):
        """

        :param event: 
        :param dispatcher: 
        :param storage: 
        :return: 
        """
        self.list.list.clear()
        for entity in storage.folders:
            self.list.addLine(entity)

    @inject.params(dispatcher='event_dispatcher')
    def _onFolderSelected(self, event=None, selection=None, dispatcher=None):
        """

        :param event: 
        :param selection: 
        :param dispatcher: 
        :return: 
        """
        for index in self.list.list.selectedIndexes():
            item = self.list.list.itemFromIndex(index)
            if item is not None and item.folder is not None:
                dispatcher.dispatch('window.notepad.folder_selected', item.folder)
