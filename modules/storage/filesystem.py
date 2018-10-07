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
from scipy.optimize._tstutils import description


class IconProvider(QtWidgets.QFileIconProvider):

    def icon(self, fileInfo):
        if fileInfo.isDir():
            return QtGui.QIcon("icons/folder-light.svg") 
        return QtGui.QIcon("icons/file-light.svg") 


class Folder(object):

    def __init__(self, path=None, name='New folder'):
        self.description = None
        self.name = name
        self.path = path

        self._folder = None

    @property
    def folder(self):
        return self._folder

    @folder.setter        
    def folder(self, folder=None):
        if folder is None:
            return None
        
        self.path = folder.path
        self._folder = folder

    @property
    def count(self):
        response = []
        for path in glob.glob('%s/*' % self.path):
            response.append(path)
        return len(response)

    @property
    @inject.params(storage='storage')
    def entities(self, storage):
        response = []
        for path in glob.glob('%s/*' % self.path):
            response.append(storage.entity(path))
        return response

    def __str__(self):
        return "%s" % self.path


class Note(object):

    def __init__(self, path=None, name='New Note', text='Note description'):
        self.path = path
        self.name = name
        self.text = text
        self._folder = None
    
    @property
    def folder(self):
        return self._folder

    @folder.setter        
    def folder(self, folder=None):
        if folder is None:
            return None
        
        self.path = folder.path
        self._folder = folder

    def __str__(self):
        return "%s" % self.path


class FilesystemStorage(QtWidgets.QFileSystemModel):
    
    def __init__(self, location=None):
        super(FilesystemStorage, self).__init__()
        self.setIconProvider(IconProvider())
        self.setRootPath(location)
        self.setReadOnly(False)

        self._location = location
        
    def _update_document(self, entity=None):
        destination = "%s/%s" % (
            os.path.dirname(entity.path),
            entity.name
        )
        
        if not os.path.exists(destination):
            shutil.move(entity.path, destination)
            entity.path = destination
            
        if os.path.exists(entity.path):
            with open(entity.path, 'w+') as stream:
                stream.write(entity.text)
                stream.close()
                
        return entity

    def _create_folder(self, entity=None):
        entity.path = "%s/%s" % (
            entity.path,
            entity.name,
        )
        
        if not os.path.exists(entity.path):
            os.makedirs(entity.path)            
        return entity

    def _create_document(self, entity=None):
        if os.path.isfile(entity.path):
            entity.path = os.path.dirname(entity.path) 
        
        entity.path = "%s/%s" % (
            entity.path,
            entity.name,
        )
        
        if not os.path.exists(entity.path):
            with open(entity.path, 'w+') as stream:
                stream.write(entity.text)
                stream.close()
                
        return entity

    def create(self, entity=None):
        
        if type(entity) == Folder:
            return self._create_folder(entity)
        
        if type(entity) == Note:
            return self._create_document(entity)

        return None

    def update(self, entity=None):

        if type(entity) == Folder:
            return None
        
        if type(entity) == Note:
            return self._update_document(entity)

        return None

    def clone(self, path=None):
        destination = "%s(copy)" % path
        if not os.path.exists(path):
            return None

        if os.path.isdir(path):
            shutil.copytree(path, destination)
        
        if not os.path.exists(destination):
            shutil.copy(path, destination)

    def delete(self, path=None):
        if not os.path.exists(path):
            return None
            
        if os.path.isdir(path):
            return shutil.rmtree(path)
        
        if os.path.isfile(path):
            return os.remove(path)

    def entity(self, path=None):
        if os.path.isdir(path):
            name = os.path.basename(path)
            return Folder(path, name)

        with open(path, 'r') as stream:
            text = stream.read()
            name = os.path.basename(path)
            return Note(path, name, text)            

    def note(self, path=None):
        if os.path.isdir(path):
            return None

        with open(path, 'r') as stream:
            text = stream.read()
            name = os.path.basename(path)
            return Note(path, name, text)            

    def entities(self, path=None):
        response = []
        for path in glob.glob('%s/*' % path):
            response.append(self.entity(path))
        return response
    
