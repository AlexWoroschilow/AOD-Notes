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
import hashlib
import functools
from .service import Search


class Loader(object):

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def enabled(self, options=None, args=None):
        return options.console is None

    @property
    @inject.params(config='config')
    def identifier(self, config):
        location = config.get('storage.location')
        if location is None:
            return None

        hasher = hashlib.sha224()
        hasher.update(location.encode('utf8'))

        return hasher.hexdigest()

    @inject.params(kernel='kernel')
    def _construct_search(self, kernel, options, args):
        return Search('{}/index/{}'.format(
            os.path.dirname(options.config),
            self.identifier
        ))

    def configure(self, binder, options, args):
        binder.bind_to_provider('search', functools.partial(
            self._construct_search, options=options, args=args
        ))
