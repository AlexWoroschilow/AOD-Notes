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
import functools

from .actions import ModuleActions

from .settings import SettingsFactory


class Loader(object):
    actions = ModuleActions()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def configure(self, binder, options, args):
        """
        Configure service container for the dependency injections
        :param binder:
        :param options:
        :param args:
        :return:
        """
        binder.bind('settings_factory', SettingsFactory())

    @inject.params(dashboard='notepad.dashboard')
    def boot(self, options, args, dashboard):
        dashboard.settingsAction.connect(functools.partial(
            self.actions.onActionSettings, widget=dashboard
        ))
