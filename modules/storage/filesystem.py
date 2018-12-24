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

from .gui.icons import IconProvider


class FilesystemStorage(QtWidgets.QFileSystemModel):
    
    def __init__(self, location=None):
        super(FilesystemStorage, self).__init__()
        self.setIconProvider(IconProvider())
        self.setRootPath(location)
        self.setReadOnly(False)
        
    def isDir(self, index):
        source = self.filePath(index)
        return os.path.isdir(source)

    def isFile(self, index):
        source = self.filePath(index)
        return os.path.isfile(source)

    def fileName(self, index):
        source = self.filePath(index)
        return os.path.basename(source)

    def fileContent(self, index):
        source = self.filePath(index)
        if not os.path.isfile(source):
            return None
        with open(source, 'r') as stream:
            return stream.read()
        return None
    
    def setFileContent(self, index, content):
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
                response = response + self.entitiesByPath(path)
                continue
            response.append(index)
        return response

