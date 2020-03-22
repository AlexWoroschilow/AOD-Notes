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
import inject

from .actions import ModuleActions
from .service.storage import StoreFileSystem

from .gui.settings.storage import WidgetSettingsStorage


class Loader(object):
    actions = ModuleActions()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def enabled(self, options=None, args=None):
        return True

    def configure(self, binder, options, args):
        """
        Setup services for the current module
        :param binder:
        :param options:
        :param args:
        :return:
        """
        binder.bind('store.filesystem', StoreFileSystem())

    @inject.params(factory='settings_factory')
    def boot(self, options, args, factory):
        """
        Do some actions after the modules and plugins were loaded
        :param options:
        :param args:
        :param factory:
        :return:
        """

        def settings():
            widget = WidgetSettingsStorage()
            widget.locationAction.connect(self.actions.onActionLocation)
            return widget

        factory.addWidget(settings)
