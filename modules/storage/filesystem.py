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
        self.fileRenamed.connect(self.printRenamed)
        self.setIconProvider(IconProvider())
        self.setRootPath(location)
        self.setReadOnly(False)

    @inject.params(encryptor='encryptor', logger='logger')
    def printRenamed(self, path, name_old, name_new, length=80, encryptor=None, logger=None):
        index = self.index("{}/{}".format(path, name_new))
        if index is None or not index:
            return self.revert()

        try:
            
            header = encryptor.encrypt(name_new)
            chunks = [header[i:i + length] for i in range(0, len(header), length)]
            header = "===HEADER BEGIN===\n{}\n===HEADER END===\n".format("\n".join(chunks))
            
            content = self.fileContentRaw(index)
            chunks = [content[i:i + length] for i in range(0, len(content), length)]
            content = "===CONTENT BEGIN===\n{}\n===CONTENT END===\n".format("\n".join(chunks)) 
            
            self.writeFileContentRaw(index, "{}{}".format(header, content))
        except(ValueError)  as ex:
            logger.debug(ex, "{}/{}".format(path, name_new))
            self.revert()
        
    def rootIndex(self):
        return self.index(self.rootPath())
        
    def isDir(self, index):
        source = self.filePath(index)
        return os.path.isdir(source)

    def isFile(self, index):
        source = self.filePath(index)
        return os.path.isfile(source)

    @inject.params(encryptor='encryptor')
    def fileName(self, index, encryptor):
        content = self.fileHeaderRaw(index)
        return encryptor.decrypt(content)
        
    @inject.params(logger='logger', encryptor='encryptor')
    def fileHeaderRaw(self, index, encryptor, logger):
        source = self.filePath(index)
        if not os.path.isfile(source):
            return None
        try:
            content = self.readContentRaw(index)
            lines = content.split("\n")
            if lines is None or not len(lines):
                return ""
            
            begin = lines.index("===HEADER BEGIN===")
            end = lines.index("===HEADER END===")
            return "".join(lines[begin + 1:end])
        except(ValueError)  as ex:
            logger.debug(ex)
        parent = super(FilesystemStorage, self)
        return encryptor.encrypt(parent.fileName(index))

    @inject.params(encryptor='encryptor')
    def fileContent(self, index, encryptor):
        content = self.fileContentRaw(index)
        return encryptor.decrypt(content)
    
    @inject.params(logger='logger', encryptor='encryptor')
    def fileContentRaw(self, index, encryptor, logger):
        try:
            content = self.readContentRaw(index)
            if content is None:
                return ""

            lines = content.split("\n")
            if lines is None or not len(lines):
                return ""
            
            begin = lines.index("===CONTENT BEGIN===")
            end = lines.index("===CONTENT END===")
            return "".join(lines[begin + 1:end])
        except(ValueError)  as ex:
            logger.debug(ex)
        return encryptor.encrypt('')

    @inject.params(encryptor='encryptor')
    def setFileContent(self, index, content, length=80, encryptor=None):
            
        header = self.fileHeaderRaw(index)
        chunks = [header[i:i + length] for i in range(0, len(header), length)]
        header = "===HEADER BEGIN===\n{}\n===HEADER END===\n".format("\n".join(chunks))
            
        content = encryptor.encrypt(content)
        chunks = [content[i:i + length] for i in range(0, len(content), length)]
        content = "===CONTENT BEGIN===\n{}\n===CONTENT END===\n".format("\n".join(chunks)) 
            
        return self.writeFileContentRaw(index, "{}{}".format(header, content))

    def writeFileContentRaw(self, index, content):
        destination = self.filePath(index)
        if not os.path.isfile(destination):
            return None
        with open(destination, 'w+') as stream:
            stream.write(content)
            stream.close()
            return index
        return False
    
    def readContentRaw(self, index):
        source = self.filePath(index)
        if not os.path.isfile(source):
            return None
        with open(source, 'r') as stream:
            return stream.read()
        return None
        
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

