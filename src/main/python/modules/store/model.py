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
import pydux
import inject
import shutil


class StorageCollection(object):
    def __init__(self):
        self._collection = []
        self._current = 0
        self._last = 0

    @property
    def fresh(self):
        return self._current != self._last

    @property
    def collection(self):
        self._last = self._current
        return self._collection

    @collection.setter
    def collection(self, collection=None):
        if collection is None: return self
        self._collection = collection
        self._current += 1
        return self


class Storage(object):
    documents = StorageCollection()
    groups = StorageCollection()
    selections = []
    document = None
    group = None
