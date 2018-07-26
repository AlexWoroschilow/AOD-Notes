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


class Loader(Loader):

    @property
    def enabled(self):
        return True

    def config(self, binder=None):
        binder.bind_to_provider('widget.settings', self._get_widget)
        binder.bind_to_constructor('button.settings', self._get_button)

    @inject.params(dispatcher='event_dispatcher')
    def boot(self, options=None, args=None, dispatcher=None):
        dispatcher.add_listener('header_content', self.onActionHeader, 128)

    @inject.params(config='config')
    def _get_button(self, config=None):

        from PyQt5 import QtWidgets
        from PyQt5 import QtGui

        widget = QtWidgets.QAction(QtGui.QIcon("icons/settings.svg"), None)
        widget.triggered.connect(self.onActionSettings)

        return widget

    @inject.params(config='config')
    def _get_widget(self, config=None):

        from .gui.widget import WidgetSettings

        return WidgetSettings()

    @inject.params(button='button.settings')
    def onActionHeader(self, event=None, button=None):
        self.container, self.parent = event.data
        self.container.addAction(button)

    @inject.params(kernel='kernel', widget='widget.settings', logger='logger')
    def onActionSettings(self, event=None, widget=None, kernel=None, logger=None):
        logger.debug('[search] settings event')
        kernel.dispatch('window.tab', (widget, 'Settings'))

