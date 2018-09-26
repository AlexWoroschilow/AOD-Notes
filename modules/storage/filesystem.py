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
import shutil


class Folder(object):

    def __init__(self, path=None, name=None):
        self.path = path
        self.name = name

    def __str__(self):
        return "%s" % self.path


class Note(object):

    def __init__(self, path=None, name=None, text=None):
        self.path = path
        self.name = name
        self.text = text

    def __str__(self):
        return "%s" % self.path


class FilesystemStorage(object):
    
    def __init__(self, location=None):
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

    def note(self, path=None):
        if os.path.isdir(path):
            return None

        with open(path, 'r') as stream:
            text = stream.read()
            name = os.path.basename(path)
            return Note(path, name, text)            

