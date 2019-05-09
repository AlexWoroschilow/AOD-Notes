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
import functools

from lib.plugin import Loader


class Loader(Loader):

    def enabled(self, options=None, args=None):
        return options.console is None

    def config(self, binder=None):
        binder.bind_to_constructor('search', self._service)

    @inject.params(kernel='kernel', config='config', storage='storage')
    def _service(self, kernel, config, storage):
        from .service import Search

        destination = os.path.dirname(kernel.options.config)
        destination = '{}/index'.format(destination)
        return Search(destination)
