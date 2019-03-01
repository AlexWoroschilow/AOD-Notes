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
import shutil
import logging

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import Qt

from .gui.icons import IconProvider

from . import cryptography
from .cryptography import CryptoFile


class QCustomDelegate (QtWidgets.QItemDelegate):

    def setEditorData(self, editor, index):
        model = index.model()
        if model.isFile(index) == True: 
            return super(QCustomDelegate, self).setEditorData(editor, index)
        metadata = '{}/.metadata'.format(model.filePath(index)) 
        editor.setText(model.fileContent(metadata))

    def setModelData (self, editor, model, index):
        cryptography.rename(model.filePath(index), editor.text())


class FilesystemStorage(QtWidgets.QFileSystemModel):
    
    def __init__(self, location=None):
        super(FilesystemStorage, self).__init__()
        self.setIconProvider(IconProvider())
        self.setRootPath(location)
        self.setReadOnly(False)

    def getItemDelegate(self):
        return QCustomDelegate()

    def data(self, index=None, role=None):
        if index is None: return super(FilesystemStorage, self).data(index, role)
        if role not in [Qt.DisplayRole, Qt.EditRole]:
            return super(FilesystemStorage, self).data(index, role)

        if self.isFile(index): return self.fileName(index)
        metadata = '{}/.metadata'.format(self.filePath(index)) 
        return self.fileContent(metadata)
        
    def mkdir(self, index, name):
        root = self.filePath(index)
        if root is None: return None
        path = cryptography.mkdir(root, name)
        if path is None: return None
        return self.index(path)

    def touch(self, index, name):
        root = self.filePath(index)
        if root is None: return None
        path = cryptography.touch(root, name)
        if path is None: return None
        return self.index(path)

    def clone(self, index=None):
        root = self.filePath(index)
        if root is None: return None
        path = cryptography.clone(root)
        if path is None: return None
        return self.index(path)

    def rootIndex(self):
        return self.index(self.rootPath())
        
    def isDir(self, path=None):
        if path is None: return None
        if isinstance(path, QtCore.QModelIndex):
            path = self.filePath(path)
        return os.path.isdir(path)

    def isFile(self, path=None):
        if path is None: return None
        if isinstance(path, QtCore.QModelIndex):
            path = self.filePath(path)
        return os.path.isfile(path)

    def fileName(self, path=None):
        if path is None: return None
        if isinstance(path, QtCore.QModelIndex):
            path = self.filePath(path)
        
        file = CryptoFile(path)
        return file.name

    def fileContent(self, path=None):
        if path is None: return None
        if isinstance(path, QtCore.QModelIndex):
            path = self.filePath(path)
        try:
            file = CryptoFile(path)
            return file.content
        except(ValueError)  as ex:
            logger = logging.getLogger('storage')
            logger.debug(ex)
    
    def setFileContent(self, path, content):
        if path is None: return None
        if isinstance(path, QtCore.QModelIndex):
            path = self.filePath(path)

        try:
            file = CryptoFile(path)
            file.content = content
        except(ValueError)  as ex:
            logger = logging.getLogger('storage')
            logger.debug(ex)

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

