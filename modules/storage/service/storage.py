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
import glob
import shutil

from PyQt5 import QtWidgets

from .gui.icons import IconProvider

from modules.storage.service.cryptography import CryptoFile


class FilesystemStorage(QtWidgets.QFileSystemModel):
    
    def __init__(self, location=None):
        super(FilesystemStorage, self).__init__()
        self.fileRenamed.connect(self.actionFileRename)
        self.setIconProvider(IconProvider())
        self.setRootPath(location)
        self.setReadOnly(False)

    def data(self, index=None, role=None):
        if index is not None and role == 0:
            #print(index, role, self.fileName(index))
            return self.fileName(index)
        return super(FilesystemStorage, self).data(index, role)

    def rootIndex(self):
        return self.index(self.rootPath())
        
    def isDir(self, index):
        source = self.filePath(index)
        return os.path.isdir(source)

    def isFile(self, index):
        source = self.filePath(index)
        return os.path.isfile(source)

    def fileName(self, index):
        return CryptoFile(self.filePath(index)).name
        
    @inject.params(logger='logger')
    def actionFileRename(self, path, name_old, name_new, logger):
        try:
            file = CryptoFile("{}/{}".format(path, name_new))
            file.name = name_new
        except(ValueError)  as ex:
            logger.debug(ex, "{}/{}".format(path, name_new))
            self.revert()

    @inject.params(logger='logger')
    def fileContent(self, index, logger):
        try:
            file = CryptoFile(self.filePath(index))
            return file.content
        except(ValueError)  as ex:
            logger.debug(ex)
    
    @inject.params(logger='logger')
    def setFileContent(self, index, content, logger):
        try:
            file = CryptoFile(self.filePath(index))
            file.content = content
        except(ValueError)  as ex:
            logger.debug(ex)

    @inject.params(logger='logger')
    def touch(self, index, name, logger):
        destination_root = self.filePath(index)
        if not os.path.isdir(destination_root):
            return None

        destination_file = "{}/{}".format(destination_root, name)
        if os.path.isfile(destination_file):
            return self.index(destination_file)

        try:
            file = CryptoFile(destination_file)
            file.name = name
        except(ValueError)  as ex:
            logger.debug(ex, destination_file)
        return self.index(destination_file)

    def clone(self, index=None):
        source = self.filePath(index)
        if not os.path.exists(source):
            return None

        destination = "{}(clone)".format(source)
        if os.path.isdir(source):
            shutil.copytree(source, destination)
            return self.index(destination)

        file_source = CryptoFile(source)
        file_desintation = CryptoFile(destination)
        file_desintation.name = "{}(clone)".format(file_source.name)
        file_desintation.content = file_source.content
        
        return self.index(destination)

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
            if index is None or not index:
                continue
                        
            if os.path.isdir(path):
                response.append(index)
                children = self.entitiesByPath(path)
                response = response + children 
                continue
            response.append(index)
        return response

