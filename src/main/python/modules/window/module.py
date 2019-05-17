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

from lib.plugin import Loader

from .gui.window import MainWindow
from .gui.header import WidgetHeaderFactory

from .actions import ModuleActions


class Loader(Loader):
    actions = ModuleActions()

    def enabled(self, options=None, args=None):
        return options.console is None

    def config(self, binder=None):
        binder.bind('window.header_factory', WidgetHeaderFactory())

        binder.bind_to_constructor('window', self._widget)
        binder.bind_to_provider('window.header', self._widget_header)
        binder.bind_to_provider('window.content', self._widget_content)
        binder.bind_to_provider('window.footer', self._widget_footer)
        binder.bind_to_provider('window.status', self._widget_status)

    @inject.params(window='window')
    def _widget_header(self, window=None):
        if window.header is None: return None
        return window.header

    @inject.params(window='window')
    def _widget_content(self, window=None):
        if window.content is None: return None
        return window.content

    @inject.params(window='window')
    def _widget_footer(self, window=None):
        if window.footer is None: return None
        return window.footer

    @inject.params(window='window')
    def _widget_status(self, window=None):
        return window.statusBar()

    @inject.params(config='config', factory='window.header_factory')
    def _widget(self, config=None, factory=None):
        container = inject.get_injector()
        if container is None: return None

        widget = MainWindow()
        width = int(config.get('window.width'))
        height = int(config.get('window.height'))
        widget.resize(width, height)

        wizard = container.get_instance('wizard')
        if wizard is not None and wizard:
            wizard.start.connect(self.test)
            widget.setMainWidget(wizard)
            return widget

        notepad = container.get_instance('notepad')
        if notepad is None: return None
        widget.setMainWidget(notepad)

        widget.footer = widget.statusBar()
        if widget.footer is None: return None
        widget.resizeEvent = self.actions.onActionWindowResize

        return widget

    @inject.params(window='window')
    def test(self, event, window=None):
        container = inject.get_injector()
        if container is None: return None
        notepad = container.get_instance('notepad')
        if notepad is None: return None
        window.setMainWidget(notepad)
