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


class FilesystemStorage(QtWidgets.QFileSystemModel):
    
    def __init__(self, location=None):
        super(FilesystemStorage, self).__init__()
        self.setIconProvider(IconProvider())
        self.setRootPath(location)
        self.setReadOnly(False)
        
    def rootIndex(self):
        return self.index(self.rootPath())
        
    def isDir(self, index):
        source = self.filePath(index)
        return os.path.isdir(source)

    def isFile(self, index):
        source = self.filePath(index)
        return os.path.isfile(source)

    def fileName(self, index):
        source = self.filePath(index)
        return os.path.basename(source)

    @inject.params(encryptor='encryptor')
    def fileContent(self, index, encryptor):
        content = self.fileContentRaw(index)
        return encryptor.decrypt(content)
    
    def fileContentRaw(self, index):
        source = self.filePath(index)
        if not os.path.isfile(source):
            return None
        with open(source, 'r') as stream:
            return stream.read()
        return None

    @inject.params(encryptor='encryptor')
    def setFileContent(self, index, content, encryptor):
        content = encryptor.encrypt(content)
        return self.setFileContentRaw(index, content)

    def setFileContentRaw(self, index, content):
        destination = self.filePath(index)
        if not os.path.isfile(destination):
            return None
        with open(destination, 'w+') as stream:
            stream.write(content)
            stream.close()
            return index
        return False
        
    def touch(self, index, name):
        destination_root = self.filePath(index)
        if not os.path.isdir(destination_root):
            return None

        destination_file = "{}/{}".format(destination_root, name)
        if os.path.isfile(destination_file):
            return self.index(destination_file)

        open(destination_file, 'w+').close()
        return self.index(destination_file)

    def clone(self, index=None):
        source = self.filePath(index)
        if not os.path.exists(source):
            return None

        if os.path.isdir(source):
            destination = "{}(clone)".format(source)
            shutil.copytree(source, destination)
            return self.index(destination)
        
        destination = "{}(clone)".format(source)
        shutil.copy(source, destination)
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

