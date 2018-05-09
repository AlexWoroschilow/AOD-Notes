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

        kernel.listen('window.notepad.folder_update', self._OnFolderUpdate, 128)
        kernel.listen('window.notepad.folder_remove', self._OnFolderUpdate, 128)
        kernel.listen('window.notepad.folder_new', self._OnFolderUpdate, 128)

    @inject.params(storage='storage')
    def _OnFolderUpdate(self, event=None, storage=None):
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

    def setFolder(self, value=None):
        self.blockSignals(True)
        self._setFolder(value)
        self.blockSignals(False)

    def _setFolder(self, entity=None):
        if entity is None:
            return None
        for index in range(0, self.count()):
            folder = self.itemData(index)
            if entity != folder:
                continue
            return self.setCurrentIndex(index)

