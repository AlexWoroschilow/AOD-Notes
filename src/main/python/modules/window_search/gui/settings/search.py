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
from PyQt5.QtCore import Qt

from . import SettingsTitle
from . import WidgetSettings
from . import PictureButton

from PyQt5 import QtCore
from PyQt5 import QtGui


class SearchThread(QtCore.QThread):
    progress = QtCore.pyqtSignal(object)
    started = QtCore.pyqtSignal(object)
    finished = QtCore.pyqtSignal(object)

    @inject.params(storage='storage', search='search')
    def run(self, storage=None, search=None):
        if not search.clean():
            return None

        self.started.emit(0)
        collection = storage.entities()
        for progress, index in enumerate(collection, start=1):
            self.progress.emit(progress / len(collection) * 100)
            if not storage.isFile(index):
                continue

            path = storage.filePath(index)
            if path is None:
                continue

            name = storage.fileName(path)
            if name is None:
                continue

            content = storage.fileContent(path)
            if content is None:
                continue

            search.append(name, path, content)
        self.progress.emit(100)
        self.finished.emit(100)


class WidgetSettingsSearch(WidgetSettings):
    thread = SearchThread()

    def __init__(self):
        super(WidgetSettingsSearch, self).__init__()

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setAlignment(Qt.AlignLeft)

        self.layout.addWidget(SettingsTitle('Fulltext search'))

        self.rebuild = PictureButton('update search index')
        self.rebuild.setIcon(QtGui.QIcon("icons/refresh"))
        self.rebuild.setToolTip("Rebuild the search index")
        self.rebuild.clicked.connect(self.thread.start)
        self.rebuild.setFlat(True)
        self.layout.addWidget(self.rebuild)

        self.progress = QtWidgets.QProgressBar(self)
        self.progress.setVisible(False)
        self.layout.addWidget(self.progress)

        self.setLayout(self.layout)

        self.thread.started.connect(lambda x: self.rebuild.setVisible(False))
        self.thread.progress.connect(lambda x: self.rebuild.setVisible(False))
        self.thread.finished.connect(lambda x: self.rebuild.setVisible(True))

        self.thread.started.connect(lambda x: self.progress.setVisible(True))
        self.thread.progress.connect(lambda x: self.progress.setVisible(True))
        self.thread.progress.connect(lambda x: self.progress.setValue(x))
        self.thread.finished.connect(lambda x: self.progress.setVisible(False))

        self.thread.finished.connect(self.thread.exit)
        self.show()

    def quit(self):
        self.thread.exit()
