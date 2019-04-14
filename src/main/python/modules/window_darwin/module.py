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
import platform

from lib.plugin import Loader


class Loader(Loader):

    @property
    def enabled(self):
        if platform.system() in ["Darwin"]:
            return True
        return False

    @property
    def config(self, binder=None):
        pass

    @inject.params(config='config', storage='storage')
    def boot(self, options=None, args=None, config=None, storage=None):
        if config is None or storage is None: return None
