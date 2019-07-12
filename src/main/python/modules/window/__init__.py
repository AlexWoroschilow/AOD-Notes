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

from .gui.window import MainWindow
from .actions import ModuleActions


class Loader(object):
    actions = ModuleActions()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    @inject.params(config='config', notepad='notepad')
    def _widget(self, config=None, notepad=None):

        widget = MainWindow()
        width = int(config.get('window.width'))
        height = int(config.get('window.height'))
        widget.resize(width, height)

        widget.setMainWidget(notepad)

        widget.footer = widget.statusBar()
        if widget.footer is None: return None
        widget.resizeEvent = self.actions.onActionWindowResize

        return widget

    @inject.params(window='window')
    def _widget_header(self, window=None):
        if window is None: return None
        if window.header is None: return None
        return window.header

    @inject.params(window='window')
    def _widget_content(self, window=None):
        if window is None: return None
        if window.content is None: return None
        return window.content

    @inject.params(window='window')
    def _widget_footer(self, window=None):
        if window is None: return None
        if window.footer is None: return None
        return window.footer

    @inject.params(window='window')
    def _widget_status(self, window=None):
        if window is None: return None
        return window.statusBar()

    def enabled(self, options=None, args=None):
        return options.console is None

    def configure(self, binder, options, args):

        binder.bind_to_constructor('window', self._widget)
        binder.bind_to_provider('window.header', self._widget_header)
        binder.bind_to_provider('window.content', self._widget_content)
        binder.bind_to_provider('window.footer', self._widget_footer)
        binder.bind_to_provider('window.status', self._widget_status)
