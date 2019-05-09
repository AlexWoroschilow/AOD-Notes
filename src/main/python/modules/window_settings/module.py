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

from PyQt5 import QtGui
from PyQt5 import QtWidgets

from .actions import ModuleActions

from lib.plugin import Loader
from .gui.button import PictureButton


class Loader(Loader):
    actions = ModuleActions()

    def enabled(self, options=None, args=None):
        return options.console is None

    def config(self, binder=None):
        binder.bind_to_constructor('settings_factory', self._settings)

    @inject.params(config='config', factory='window.header_factory')
    def boot(self, options=None, args=None, config=None, factory=None):
        if not len(config.get('storage.location')): return None

        widget = PictureButton(QtGui.QIcon("icons/settings"), None)
        widget.clicked.connect(self.actions.onActionSettings)

        factory.addWidget(widget, 128)

    def _settings(self):
        from .settings import SettingsFactory
        return SettingsFactory()
