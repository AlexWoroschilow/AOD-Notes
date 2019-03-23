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


class ToolbarFactory(object):

    def __init__(self):
        self.collection = []

    def addWidget(self, constructor=None):
        if constructor is None: return None
        if not callable(constructor): return None
        self.collection.append(constructor)

    @property
    def widgets(self):
        for constructor in self.collection:
            if not callable(constructor): continue
            yield constructor()
