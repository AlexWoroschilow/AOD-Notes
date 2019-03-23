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
import shutil
import secrets

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5 import QtCore

from . import SettingsTitle
from . import WidgetSettings


class CryptographyThread(QtCore.QThread):
    progress = QtCore.pyqtSignal(int)

    @inject.params(storage='storage', encryptor='encryptor')
    def run(self, storage, encryptor):

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

        total = len(folders) + len(files)
        for index, path in enumerate(files, start=1):
            self.progress.emit(index / total * 100)
            if not os.path.exists(path): continue
            with open(path, 'r', encoding='utf-8', errors='ignore') as stream:
                content = stream.read()
                # If the file has all of this strings we assume that this file was
                # already encoded and do not encode it again
                if content.find('===HEADER BEGIN===') != -1 \
                        and content.find('===HEADER END===') != -1 \
                        and content.find('===CONTENT BEGIN===') != -1 \
                        and content.find('===CONTENT END===') != -1:
                    continue

                folder = os.path.dirname(path)
                if not os.path.exists(folder): continue
                # Crate a new file with an encoded file name fill it
                # with the content of a given one and remove the donor
                unique = storage.touch(folder, os.path.basename(path))
                if not os.path.exists(storage.filePath(unique)): continue
                storage.setFileContent(unique, content)
                os.remove(path)

        for index, path_old in enumerate(folders, start=index):
            self.progress.emit(index / total * 100)
            # check if the metadata file already there
            # that means the folder was already encrypted
            if not os.path.exists(path_old): continue
            metadata = os.path.join(path_old, '.metadata')
            if os.path.exists(metadata): continue
            open(metadata, 'w+').write('')
            if not os.path.exists(metadata): continue
            # The metadata content play the role of the folder name for now
            storage.setFileContent(metadata, os.path.basename(path_old))

            root = os.path.dirname(path_old)
            if not os.path.exists(root): continue

            unique = secrets.token_hex(16)
            while os.path.exists(os.path.join(root, unique)):
                unique = secrets.token_hex(16)

            path_new = os.path.join(root, unique)
            if os.path.exists(path_new): continue

            os.rename(path_old, path_new)

        self.progress.emit(100)


class WidgetSettingsCryptography(WidgetSettings):
    thread = CryptographyThread()

    def __init__(self):
        super(WidgetSettingsCryptography, self).__init__()

        self.layout = QtWidgets.QGridLayout()
        self.layout.setAlignment(Qt.AlignLeft)

        self.layout.addWidget(SettingsTitle('Cryptography settings'), 0, 0, 1, 5)
        self.layout.addWidget(QtWidgets.QLabel('Password:'), 1, 0)

        self.code = QtWidgets.QLabel('...')
        self.layout.addWidget(self.code, 1, 1)

        self.layout.addWidget(QtWidgets.QLabel('Algorithm:'), 2, 0)

        self.algorithm = QtWidgets.QLabel('AES-128')
        self.layout.addWidget(self.algorithm, 2, 1)

        self.layout.addWidget(QtWidgets.QLabel('Unencrypted entries:'), 3, 0)

        self.encrypt = QtWidgets.QPushButton('Encrypt')
        self.encrypt.clicked.connect(self.onActionEncrypt)
        self.encrypt.setFlat(True)

        self.layout.addWidget(self.encrypt, 3, 1)

        self.progress = QtWidgets.QProgressBar(self)
        self.progress.setVisible(False)
        self.layout.addWidget(self.progress, 4, 0, 1, 5)

        self.setLayout(self.layout)

        self.show()

    def onActionEncrypt(self, event):
        self.thread.progress.connect(self.onActionEncryptProgress)
        self.thread.start()
        self.thread.exit()

    def onActionEncryptProgress(self, value):
        if not self.progress.isVisible() and value > 0:
            self.progress.setVisible(True)
        self.progress.setValue(value)
        if self.progress.isVisible() and value == 100:
            self.progress.setVisible(False)

    def quit(self):
        self.thread.exit()
