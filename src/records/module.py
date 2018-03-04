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
from .gui.widget import RecordList


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
        dispatcher.add_listener('window.notepad.note_update', self._onNotepadNoteUpdate)

    @inject.params(storage='storage', dispatcher='event_dispatcher')
    def _onWindowFirstTab(self, event=None, dispatcher=None, storage=None):
        """

        :param event: 
        :param dispatcher: 
        :return: 
        """

        self.list = RecordList()
        self.list.toolbar.newAction.triggered.connect(self._onNewEvent)
        self.list.toolbar.copyAction.triggered.connect(self._onCopyEvent)
        self.list.toolbar.savePdf.triggered.connect(self._onSavePdfEvent)

        self.list.list.selectionChanged = self._onNoteSelected

        for entity in storage.notes:
            self.list.addLine(
                entity.index,
                entity.name,
                entity.text
            )

        dispatcher.dispatch('window.notepad.note_edit', (
            entity.index, entity.name, entity.text
        ))

        event.data.addWidget(self.list)

    @inject.params(dispatcher='event_dispatcher')
    def _onNoteSelected(self, event=None, selection=None, dispatcher=None):
        """
        
        :param event: 
        :param dispatcher: 
        :return: 
        """
        for index in self.list.list.selectedIndexes():
            item = self.list.list.itemFromIndex(index)
            dispatcher.dispatch('window.notepad.note_edit', (
                item.index, item.name, item.text
            ))

    @inject.params(storage='storage')
    def _onNotepadNoteUpdate(self, event=None, dispather=None, storage=None):
        """

        :param event: 
        :param dispather: 
        :return: 
        """
        index, name, text = event.data
        for index in self.list.list.selectedIndexes():
            item = self.list.list.itemFromIndex(index)
            item.name = name
            item.text = text

    @inject.params(dispatcher='event_dispatcher')
    def _onNewEvent(self, event=None, dispatcher=None):
        """
        
        :param event: 
        :return: 
        """
        name = 'Note 1'
        description = 'Note description 1'
        self.list.addLine(None, name, description)
        dispatcher.dispatch('window.notepad.note_new', (
            name, description
        ))

    @inject.params(dispatcher='event_dispatcher')
    def _onCopyEvent(self, event=None, dispatcher=None):
        """

        :param event: 
        :return: 
        """
        for index in self.list.list.selectedIndexes():
            item = self.list.list.itemFromIndex(index)
            self.list.addLine(None, item.name, item.text)
            dispatcher.dispatch('window.notepad.note_new', (
                item.name, item.text
            ))

    @inject.params(dispatcher='event_dispatcher')
    def _onSavePdfEvent(self, event=None, dispatcher=None):
        """

        :param event: 
        :return: 
        """
        dispatcher.dispatch('window.notepad.note_export')
