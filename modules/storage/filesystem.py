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
import inject

from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore

from .gui.icons import IconProvider


class FilesystemStorage(QtWidgets.QFileSystemModel):
    
    def __init__(self, location=None):
        super(FilesystemStorage, self).__init__()
        self.setIconProvider(IconProvider())
        self.setRootPath(location)
        self.setReadOnly(False)
        self._location = location
        
        # self.fileRenamed.connect(self.test)
         
#    def test(self, path, old, new):
#        print(self.data(self.index("{}/{}".format(path, old))))
#        print(path, old, new)
        
    def isDir(self, index):
        source = self.filePath(index)
        return os.path.isdir(source)

    def isFile(self, index):
        source = self.filePath(index)
        return os.path.isfile(source)

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
            return True
        return False
        
    def touch(self, path, name):
        if os.path.isfile("{}/{}".format(path, name)):
            return None
        if not os.path.isdir(path):
            return None
        with open("{}/{}".format(path, name), 'w+') as stream:
            stream.close()

    def clone(self, index=None):
        source = self.filePath(index)
        if not os.path.exists(source):
            return None

        if os.path.isdir(source):
            destination = "{}(clone)".format(source)
            shutil.copytree(source, destination)
            return True
        
        destination = "{}(clone)".format(source)
        shutil.copy(source, destination)
        return True

    def entities(self, index=None):
        source = self.filePath(index)
        if not os.path.exists(source):
            return None

        response = []
        for path in glob.glob('{}/*'.format(source)):
            if os.path.isdir(path):
                response = response + self.entities(path)
                continue
            response.append(self.entity(path))
        return response
    
