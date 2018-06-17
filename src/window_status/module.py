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

from PyQt5 import QtWidgets

from lib.plugin import Loader


class Loader(Loader):

    @inject.params(kernel='kernel')
    def _constructor_statusbar(self, kernel=None):

        widget = QtWidgets.QLabel()
        
        kernel.listen('window_status', functools.partial(
            self.onActionStatus, widget=widget
        ))
        
        return widget
        
    @property
    def enabled(self):
        return True

    def config(self, binder=None):
        binder.bind_to_constructor('widget.statusbar', self._constructor_statusbar)

    def onActionStatus(self, event, widget=None):
        message, timeout = event.data
        print(message, timeout)
        if widget is not None:
            widget.setText(message)
