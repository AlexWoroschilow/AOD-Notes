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

from lib.plugin import Loader
from .service import Storage

from .gui.widget import FolderList


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

        self.list.list.clear()
        for folder in storage.folders:
            self.list.addLine(folder.index, folder.name, folder.text)

        container, parent = event.data
        container.addWidget(self.list)

    @inject.params(dispatcher='event_dispatcher')
    def _onNewEvent(self, event=None, dispatcher=None):
        """

        :param event: 
        :return: 
        """
        name = 'Folder 1'
        description = 'Folder description 1'
        self.list.addLine(None, name, description)
        dispatcher.dispatch('window.notepad.folder_new', (
            name, description
        ))

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
            self.list.addLine(entity.index, entity.name, entity.text)
