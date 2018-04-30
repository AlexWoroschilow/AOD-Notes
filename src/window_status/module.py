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
import threading
from PyQt5 import QtWidgets

from lib.plugin import Loader


class Loader(Loader):

    @property
    def enabled(self):
        return True

    @inject.params(kernel='kernel')
    def boot(self, options=None, args=None, kernel=None):
        kernel.listen('window.statusbar', self._onWindowStatusBar)
        kernel.listen('window.status', self._onWindowStatus)

    def _onWindowStatusBar(self, event):
        self._widget = QtWidgets.QLabel("Message in statusbar")
        statusbar, window = event.data

        spacer = QtWidgets.QWidget();
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred);
        statusbar.addWidget(spacer);

        statusbar.addWidget(self._widget);

    def _onWindowStatus(self, event):
        message, timeout = event.data
        if self._widget is None:
            return None
        self._widget.setText(message)
