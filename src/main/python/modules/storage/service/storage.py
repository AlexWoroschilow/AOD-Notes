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

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import Qt

from .gui.icons import IconProvider


class FilesystemStorage(QtWidgets.QFileSystemModel):

    def __init__(self, location=None):
        super(FilesystemStorage, self).__init__()
        self.setIconProvider(IconProvider())
        self.setRootPath(location)
        self.setReadOnly(False)

    def touch(self, path=None, name=None):
        if path is None or name is None:
            return None

        if isinstance(path, QtCore.QModelIndex):
            path = self.filePath(path)

        if path is None:
            return None

        path = '{}/{}'.format(path, name)
        if os.path.exists(path):
            raise Exception('File exists')

        open(path, 'w').write('')

        if path is None:
            return None

        return self.index(path)

    def clone(self, path=None):
        if isinstance(path, QtCore.QModelIndex):
            path = self.filePath(path)

        if path is None:
            return None

        destination = '{}(clone)'.format(path)
        if os.path.exists(path):
            raise Exception('File exists')

        shutil.copy2(path, destination)

        return self.index(destination)

    def rootIndex(self):
        path = self.rootPath()
        return self.index(path)

    def isDir(self, path=None):
        if isinstance(path, QtCore.QModelIndex):
            path = self.filePath(path)

        if path is None:
            return None

        return os.path.isdir(path)

    def isFile(self, path=None):
        if isinstance(path, QtCore.QModelIndex):
            path = self.filePath(path)

        if path is None:
            return None

        return os.path.isfile(path)

    def fileName(self, path=None):
        if not isinstance(path, QtCore.QModelIndex):
            path = self.index(path)

        return super(FilesystemStorage, self).fileName(path)

    def fileContent(self, path=None):
        if isinstance(path, QtCore.QModelIndex):
            path = self.filePath(path)

        if self.isDir(path):
            return None

        return open(path, 'r').read()

    def setFileContent(self, path, content):
        if isinstance(path, QtCore.QModelIndex):
            path = self.filePath(path)

        open(path, 'w').write(content)

        return self.index(path)

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
        if not os.path.exists(source):
            return None

        response = []
        for path in glob.glob('{}/*'.format(source)):
            index = self.index(path)

            if index is None:
                continue

            if not index:
                continue

            if os.path.isdir(path):
                response.append(index)
                children = self.entitiesByPath(path)
                response = response + children
                continue
            response.append(index)
        return response
