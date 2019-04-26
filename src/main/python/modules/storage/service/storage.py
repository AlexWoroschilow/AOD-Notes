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
import glob
import logging

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import Qt

from .gui.icons import IconProvider

from . import cryptography
from .cryptography import CryptoFile


class QCustomDelegate(QtWidgets.QStyledItemDelegate):

    def setEditorData(self, editor, index):
        model = index.model()
        if model.isFile(index) == True:
            return super(QCustomDelegate, self).setEditorData(editor, index)
        editor.setText(model.fileName(index))

    def setModelData(self, editor, model, index):
        cryptography.rename(model.filePath(index), editor.text())


class FilesystemStorage(QtWidgets.QFileSystemModel):

    def __init__(self, location=None):
        super(FilesystemStorage, self).__init__()
        self.setIconProvider(IconProvider())
        self.setRootPath(location)
        self.setReadOnly(False)

    def getItemDelegate(self):
        return QCustomDelegate()

    def mkdir(self, index, name):
        root = self.filePath(index)
        if root is None: return None
        path = cryptography.mkdir(root, name)
        if path is None: return None
        return self.index(path)

    def rename(self, path=None, name=None):
        if path is None or name is None: return None
        if isinstance(path, QtCore.QModelIndex):
            path = self.filePath(path)
        if path is None: return None
        # path = cryptography.rename(path, name)
        # if path is None: return None
        # return self.index(path)

    def touch(self, path=None, name=None):
        if path is None or name is None: return None
        if isinstance(path, QtCore.QModelIndex):
            path = self.filePath(path)
        if path is None: return None
        path = '{}/{}'.format(path, name)
        return open(path, 'w').write('')
        if path is None: return None
        return self.index(path)

    def clone(self, path=None):
        if isinstance(path, QtCore.QModelIndex):
            path = self.filePath(path)
        if path is None: return None
        path = cryptography.clone(path)
        if path is None: return None
        return self.index(path)

    def rootIndex(self):
        path = self.rootPath()
        return self.index(path)

    def isDir(self, path=None):
        if path is None: return None
        if isinstance(path, QtCore.QModelIndex):
            path = self.filePath(path)
        if path is None: return None
        return os.path.isdir(path)

    def isFile(self, path=None):
        if path is None: return None
        if isinstance(path, QtCore.QModelIndex):
            path = self.filePath(path)
        if path is None: return None
        return os.path.isfile(path)

    def fileName(self, path=None):
        if path is None: return None
        if isinstance(path, QtCore.QModelIndex):
            return super(FilesystemStorage, self).fileName(path)
        index = self.index(path)
        return super(FilesystemStorage, self).fileName(index)

    def fileContent(self, path=None):
        if path is None: return None
        if isinstance(path, QtCore.QModelIndex):
            path = self.filePath(path)
            return open(path, 'r').read()
        return open(path, 'r').read()

    def setFileContent(self, path, content):
        if path is None: return None
        if isinstance(path, QtCore.QModelIndex):
            path = self.filePath(path)
            return open(path, 'w').write(content)
        return open(path, 'w').write(content)

    def first(self):
        index = self.rootIndex()
        source = self.filePath(index)
        if not os.path.exists(source):
            return None

        sources = [self.filePath(index)]
        while len(sources):
            for path in glob.glob('{}/*'.format(sources.pop())):
                index = self.index(path)
                if self.isDir(index):
                    sources.append(path)
                    continue
                return index

    def entities(self, index=None):
        if index is None or not index:
            index = self.index(self.rootPath())

        source = self.filePath(index)
        return self.entitiesByPath(source)

    def entitiesByPath(self, source=None):
        if not os.path.exists(source): return None

        response = []
        for path in glob.glob('{}/*'.format(source)):
            index = self.index(path)
            if index is None: continue
            if not index: continue

            if os.path.isdir(path):
                response.append(index)
                children = self.entitiesByPath(path)
                response = response + children
                continue
            response.append(index)
        return response
