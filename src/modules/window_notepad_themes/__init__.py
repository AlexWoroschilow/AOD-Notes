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

from .actions import ModuleActions
from .service import ServiceTheme

from .decorators import service_settings_decorator


class Loader(object):

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    @inject.params(config='config')
    def __construct(self, config=None):
        return ServiceTheme([
            config.get('themes.default', 'themes/'),
            config.get('themes.custom', '~/.config/AOD-Notes/themes')
        ])

    def configure(self, binder, options, args):
        """
        Configure service container for the dependency injections
        :param binder:
        :param options:
        :param args:
        :return:
        """
        binder.bind_to_constructor('themes', self.__construct)

    @service_settings_decorator
    def boot(self, options=None, args=None):
        pass
