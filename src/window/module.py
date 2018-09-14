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

from lib.plugin import Loader

from PyQt5 import QtWidgets
from PyQt5 import QtCore

from PyQt5.QtCore import Qt

from .gui.window import MainWindow


class Loader(Loader):

    @property
    def enabled(self):
        return True

    def config(self, binder=None):
        binder.bind_to_constructor('window', self._constructor_window)

    @inject.params(config='config', statusbar='widget.statusbar')
    def _constructor_window(self, config=None, statusbar=None):
        
        widget = MainWindow()
        widget.statusBar().addWidget(statusbar);
        
        width = int(config.get('window.width'))
        height = int(config.get('window.height'))
        widget.resize(width, height)

        widget.resizeEvent = functools.partial(
            self.onActionWindowResize
        )
        
        return widget

    @inject.params(config='config')
    def onActionWindowResize(self, event=None, config=None):
        config.set('window.width', '%s' % event.size().width())
        config.set('window.height', '%s' % event.size().height())
        return event.accept()
