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
from datetime import datetime

from glob import glob


class Folder(object):

    def __init__(self, name=None, path=None):
        self.name = name
        self.path = path
        self.id = path
        self.createdAt = datetime.now()
        self.notes = []

    def __str__(self):
        return "%s" % self.path


class Note(object):

    def __init__(self, name=None, text=None, folder=None):
        self.name = name
        self.folder = folder
        self.path = "%s/%s" % (
            folder.path if folder is not None else None, name
        )
        self.unique = self.path
        self.id = self.path
        self.text = text
        self.description = text
        self.createdAt = datetime.now()
        self.tags = None
        self.version = None

#     
    def __str__(self):
        return "%s" % self.path


class FilesystemStorage(object):
    
    def __init__(self, location=None):
        self._location = location

    def create(self, entity=None):
        
        if type(entity) == Folder:
            entity.path = "%s/%s" % (self._location, entity.name)
            if not os.path.exists(entity.path):
                os.makedirs(entity.path)
            return entity
        
        if type(entity) == Note:
            
            entity.path = "%s/%s" % (
                entity.folder.path, entity.name
            )
            
            if not os.path.exists(entity.path):
                with open(entity.path, 'w+') as stream:
                    stream.write(entity.text)
                    stream.close()
                    
            return entity

    def update(self, entity=None):
        if type(entity) == Folder:
            return self._update_folder(entity)
        if type(entity) == Note:
            return self._update_document(entity)
        return None

    def _update_folder(self, entity=None):
        destination = "%s/%s" % (
            self._location, entity.name
        )
        if not os.path.exists(destination):
            shutil.move(entity.path, destination)
            entity.path = destination
        return entity
        
    def _update_document(self, entity=None):
        destination = "%s/%s" % (
            entity.folder.path, entity.name
        )
        if not os.path.exists(destination):
            shutil.move(entity.path, destination)
            entity.path = destination
        if os.path.exists(entity.path):
            with open(entity.path, 'w+') as stream:
                stream.write(entity.text)
                stream.close()
        return entity

    def delete(self, entity=None):
        
        if type(entity) == Folder:
            
            if os.path.exists(entity.path):
                return shutil.rmtree(entity.path)
            
        if type(entity) == Note:

            entity.path = "%s/%s" % (
                entity.folder.path, entity.name
            )

            if os.path.exists(entity.path):
                return os.remove(entity.path)

    def folders(self, string=None):
        result = []
        for path in glob("%s/*" % self._location):
            
            if not os.path.isdir(path):
                continue
            
            if string is not None:
                if not path.find(string) < 0:
                    continue
                
            result.append(Folder(
                os.path.basename(path), path
            ))
            
        return result

    def folder(self, name=None):
        return None

    def note(self, unique=None):
        return None

    def notes(self, folder=None, string=None):
        result = []
        for path in glob("%s/*" % folder):
            
            if os.path.isdir(path):
                continue
            
            if string is not None:
                if not path.find(string) < 0:
                    continue
                
            with open(path, 'r') as stream:
                result.append(Note(
                    os.path.basename(path),
                    stream.read(), folder
                ))

        return result

    @property
    def count(self):
        return None

