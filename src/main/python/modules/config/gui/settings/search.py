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
import os
import inject
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from . import SettingsTitle
from . import WidgetSettings
from PyQt5 import QtCore


class CryptographyThread(QtCore.QThread):
    progress = QtCore.pyqtSignal(int)

    @inject.params(storage='storage', search='search', config='config')
    def run(self, storage, search, config):
        if not search.clean(): return None
        collection = storage.entities()
        for progress, index in enumerate(collection, start=1):
            self.progress.emit(progress / len(collection) * 100)
            if not storage.isFile(index): continue
            path = storage.filePath(index)
            if path is None: continue
            name = storage.fileName(path)
            if name is None: continue
            content = storage.fileContent(path)
            if content is None: continue
            search.append(name, path, content)

        self.progress.emit(100)


class WidgetSettingsSearch(WidgetSettings):
    thread = CryptographyThread()

    def __init__(self):
        super(WidgetSettingsSearch, self).__init__()

        self.layout = QtWidgets.QGridLayout()
        self.layout.setAlignment(Qt.AlignLeft)

        self.layout.addWidget(SettingsTitle('Search engine settings'), 0, 0, 1, 5)
        self.layout.addWidget(QtWidgets.QLabel('Index location:'), 1, 0)

        self.searchIndex = QtWidgets.QLabel('...')
        self.layout.addWidget(self.searchIndex, 1, 1)

        self.layout.addWidget(QtWidgets.QLabel('Rebuild index:'), 2, 0)

        self.rebuild = QtWidgets.QPushButton('Start indexation process')
        self.rebuild.setToolTip("Rebuild the search index")
        self.rebuild.clicked.connect(self.onActionRebuild)
        self.rebuild.setFlat(True)
        self.layout.addWidget(self.rebuild, 2, 1)

        self.progress = QtWidgets.QProgressBar(self)
        self.progress.setVisible(False)
        self.layout.addWidget(self.progress, 3, 0, 1, 5)

        self.setLayout(self.layout)

        self.show()

    def onActionRebuild(self, event):
        self.thread.progress.connect(self.onActionRebuildProgress)
        self.thread.start()
        self.thread.exit()

    def onActionRebuildProgress(self, value):
        if not self.progress.isVisible() and value > 0:
            self.progress.setVisible(True)
        self.progress.setValue(value)
        if self.progress.isVisible() and value == 100:
            self.progress.setVisible(False)

    def quit(self):
        self.thread.exit()
