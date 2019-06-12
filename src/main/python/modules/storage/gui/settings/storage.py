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
from PyQt5 import QtCore

from . import SettingsTitle
from . import WidgetSettings


class StorageThread(QtCore.QThread):
    progress = QtCore.pyqtSignal(int)
    destination = None

    @inject.params(storage='storage')
    def run(self, storage):
        files = []
        folders = []

        root = storage.filePath(storage.rootIndex())
        sources = [root]
        while len(sources):
            source = sources.pop()
            if os.path.isfile(source):
                files.append(source)
                continue

            for name in os.listdir(source):
                sources.append(os.path.join(source, name))
            if source != root: folders.append(source)

        folders.sort(key=len, reverse=True)
        files.sort(key=len, reverse=True)

        self.progress.emit(100)


class WidgetSettingsStorage(WidgetSettings):
    thread = StorageThread()

    def __init__(self):
        super(WidgetSettingsStorage, self).__init__()

        self.layout = QtWidgets.QGridLayout()
        self.layout.setAlignment(Qt.AlignLeft)

        self.layout.addWidget(SettingsTitle('Storage settings'), 0, 0, 1, 5)
        self.layout.addWidget(QtWidgets.QLabel('Database:'), 1, 0)

        self.location = QtWidgets.QPushButton('Change')
        self.location.setToolTip("Clone selected preview")
        self.location.setFlat(True)
        self.layout.addWidget(self.location, 1, 1)

        self.layout.addWidget(QtWidgets.QLabel('Export to:'), 2, 0)
        self.export = QtWidgets.QPushButton('Choose folder to export')
        self.export.clicked.connect(self.onActionExport)
        self.export.setToolTip("Export your notes to some external folder")
        self.export.setFlat(True)
        self.layout.addWidget(self.export, 2, 1)

        self.progress = QtWidgets.QProgressBar(self)
        self.progress.setVisible(False)
        self.layout.addWidget(self.progress, 3, 0, 1, 5)

        self.setLayout(self.layout)

        self.show()

    def onActionExport(self, event):
        message = self.tr("Select Directory to export the notes")
        self.destination = str(QtWidgets.QFileDialog.getExistingDirectory(self, message, os.path.expanduser('~')))
        if self.destination is None:
            return None

        self.thread.progress.connect(self.onActionProgress)
        self.thread.start()
        self.thread.exit()

    def onActionProgress(self, value):
        if not self.progress.isVisible() and value > 0:
            self.progress.setVisible(True)

        self.progress.setValue(value)

        if self.progress.isVisible() and value == 100:
            self.progress.setVisible(False)

    def quit(self):
        self.thread.exit()
