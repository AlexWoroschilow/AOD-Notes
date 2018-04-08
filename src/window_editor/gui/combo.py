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
from PyQt5.Qt import Qt
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtSvg


class FolderBomboBox(QtWidgets.QComboBox):
    @inject.params(storage='storage', dispatcher='event_dispatcher')
    def __init__(self, storage=None, dispatcher=None):
        """
        
        :param storage: 
        """
        super(FolderBomboBox, self).__init__()
        self._note = None

        for folder in storage.folders:
            self.addItem(folder.name, folder)
        self.currentIndexChanged.connect(self._OnFolderChanged)

        dispatcher.add_listener('window.notepad.note_edit', self._OnNoteSelected)

    def setFolder(self, value=None):
        """
        
        :param value: 
        :return: 
        """
        self.blockSignals(True)
        for index in range(0, self.count()):
            folder = self.itemData(index)
            if int(value) in [int(folder.index)]:
                self.setCurrentIndex(index)
        self.blockSignals(False)

    def _OnNoteSelected(self, event=None, dispatcher=None):
        """
        
        :param event: 
        :param dispatcher: 
        :return: 
        """
        self._note = event.data

    @inject.params(dispatcher='event_dispatcher')
    def _OnFolderChanged(self, event=None, dispatcher=None):
        """
        
        :param event: 
        :param dispatcher: 
        :return: 
        """
        dispatcher.dispatch('window.notepad.note_folder', (
            self._note, self.itemData(event)
        ))
