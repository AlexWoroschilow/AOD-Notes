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


class FolderBomboBox(QtWidgets.QComboBox):

    @inject.params(storage='storage', kernel='kernel')
    def __init__(self, storage=None, kernel=None):
        super(FolderBomboBox, self).__init__()
        self.setObjectName('folderBomboBox')
        self._note = None

        for folder in storage.folders():
            self.addItem(folder.name, folder)

        kernel.listen('window.notepad.folder_update', self._OnUpdate, 128)
        kernel.listen('window.notepad.folder_remove', self._OnRefresh, 128)
        kernel.listen('window.notepad.folder_new', self._OnRefresh, 128)

    @inject.params(storage='storage')
    def _OnUpdate(self, event=None, storage=None):
        entity, widget = event.data
        if entity is None or widget is None:
            return None
        
        for index in range(0, self.count()):
            folder = self.itemData(index)
            if folder is None:
                continue
            if folder != entity:
                continue
            self.setItemText(index, folder.name)

    @property
    def entity(self):
        if self.count() == 0:
            return None
        index = self.currentIndex()
        return self.itemData(index)

    @entity.setter
    def entity(self, entity=None):
        if entity is None:
            return None
        self.blockSignals(True)
        for index in range(0, self.count()):
            folder = self.itemData(index)
            if folder is not None and entity == folder:
                self.setCurrentIndex(index)
        self.blockSignals(False)

    @inject.params(storage='storage')
    def _OnRefresh(self, event=None, storage=None):
        entity, widget = event.data
        if entity is None or widget is None:
            return None
        
        current_folder = None
        current_index = self.currentIndex();
        if current_index is not None:
            current_folder = self.itemData(current_index) 
        
        self.clear()
        for index, folder in enumerate(storage.folders(), start=0):
            self.addItem(folder.name, folder)
            if current_folder != folder:
                continue
            self.setCurrentIndex(index)
