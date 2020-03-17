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

from .service.config import ConfigFile


class Loader(object):

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def _construct(self, options, args):
        return ConfigFile(options.config)

    def enabled(self, options=None, args=None):
        return True

    def configure(self, binder, options, args):
        binder.bind_to_constructor('config', functools.partial(
            self._construct, options=options, args=args
        ))

    @inject.params(store='store')
    def boot(self, options, args, store):
        store.subscribe(self.update)

    @inject.params(config='config', store='store')
    def update(self, config=None, store=None):
        state = store.get_state()
        if state is None: return None

        if 'group' in state.keys():
            self.updateGroupAction(state['group'])

        if 'document' in state.keys():
            self.updateNoteAction(state['document'])

    @inject.params(config='config')
    def updateGroupAction(self, entity=None, config=None):
        if entity is None: return None
        if not len(entity.path): return None
        if not os.path.exists(entity.path): return None
        config.set('storage.selected.group', entity.path)

    @inject.params(config='config')
    def updateNoteAction(self, entity=None, config=None):
        if entity is None: return None
        if not len(entity.path): return None
        if not os.path.exists(entity.path): return None
        config.set('storage.selected.document', entity.path)
