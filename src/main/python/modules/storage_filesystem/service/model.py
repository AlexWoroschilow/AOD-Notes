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
import shutil
import inject
import functools

import glob


class Group(object):
    def __init__(self, path, children):
        self.children = children
        self.path = path

    def __eq__(self, other=None):
        if other is None: return False
        return self.path == other.path

    @property
    def name(self):
        return os.path.basename(self.path)

    @name.setter
    def name(self, value, counter=1):
        if value == self.name:
            return self
        try:
            destination = "{}/{}".format(os.path.dirname(self.path), value)
            while os.path.exists(destination):
                destination = "{} ({})".format(destination, counter)
                counter += 1
            shutil.move(self.path, destination)
            self.path = destination
        except OSError as ex:
            return self
        return self

    @property
    def parent(self):
        return os.path.dirname(self.path)

    @parent.setter
    def parent(self, entity, counter=1):
        if entity.path == self.parent:
            return self
        try:
            shutil.move(self.path, entity.path)
            self.path = "{}/{}".format(entity.path, self.name)
        except OSError as ex:
            return self
        return self

    def __str__(self):
        return self.name


class Document(object):
    def __init__(self, path):
        self.path = path

    def __eq__(self, other):
        if other is None: return False
        return self.path == other.path

    @property
    def name(self):
        return os.path.basename(self.path)

    @name.setter
    def name(self, value, counter=1):
        if value == self.name:
            return self
        try:
            destination = "{}/{}".format(os.path.dirname(self.path), value)
            while os.path.exists(destination):
                destination = "{} ({})".format(destination, counter)
                counter += 1
            shutil.move(self.path, destination)
            self.path = destination
        except OSError as ex:
            return self
        return self

    @property
    def parent(self):
        return os.path.dirname(self.path)

    @parent.setter
    def parent(self, entity, counter=1):
        if entity.path == self.parent:
            return self
        try:
            shutil.move(self.path, entity.path)
            self.path = "{}/{}".format(entity.path, self.name)
        except OSError as ex:
            return self
        return self

    @property
    def content(self):
        try:
            return open(self.path, 'r').read()
        except (OSError, UnicodeDecodeError) as ex:
            return ''

    @content.setter
    def content(self, value):
        return open(self.path, 'w').write(value)

    def __str__(self):
        return self.name
