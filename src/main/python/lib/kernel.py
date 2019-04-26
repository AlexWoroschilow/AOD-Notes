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
import logging
import inject

import importlib
from lib.event import Dispatcher


class Kernel(object):

    def __init__(self, options=None, args=None, sources=["plugins/**/module.py", "modules/**/module.py"]):
        self.options = options
        self.sources = sources
        self.args = args
        self.loaders = []

        inject.configure(self._configure)

        logger = logging.getLogger('kernel')
        for loader in self.loaders:
            if not hasattr(loader.__class__, 'boot'): continue
            if not callable(getattr(loader.__class__, 'boot')): continue
            logger.debug("boot: {}".format(loader.__class__))
            loader.boot(options, args)

    def _configure(self, binder):

        logger = logging.getLogger('app')
        binder.bind('logger', logger)

        logger = logging.getLogger('dispatcher')
        binder.bind('event_dispatcher', Dispatcher(logger))

        logger = logging.getLogger('kernel')
        for module_source in self.__modules(self.sources):
            try:
                module = importlib.import_module(module_source, False)
                with module.Loader(self.options, self.args) as loader:
                    if not loader.enabled(self.options, self.args): continue
                    if not hasattr(loader.__class__, 'config'): continue
                    if not callable(getattr(loader.__class__, 'config')): continue
                    logger.debug("bind: {}".format(loader.__class__))
                    binder.install(loader.config)

                    self.loaders.append(loader)

            except (SyntaxError, RuntimeError) as err:
                logger.critical("{}: {}".format(module_source, err))
                continue

        binder.bind('kernel', self)

    def __modules(self, masks=None):
        location = os.path.dirname(__file__)
        logger = logging.getLogger('kernel')
        for mask in masks:
            logger.info('module mask: {}/{}'.format(location, mask))
            for source in glob.glob(mask):
                if os.path.exists(source):
                    logger.debug("config: %s" % source)
                    yield source[:-3].replace('/', '.')

    def get(self, name=None):
        container = inject.get_injector()
        return container.get_instance(name)

    def dispatch(self, name=None, event=None):
        dispatcher = self.get('event_dispatcher')
        dispatcher.dispatch(name, event)

    def listen(self, name=None, action=None, priority=0):
        dispatcher = self.get('event_dispatcher')
        dispatcher.add_listener(name, action, priority)

    def unlisten(self, name=None, action=None):
        dispatcher = self.get('event_dispatcher')
        dispatcher.remove_listener(name, action)
