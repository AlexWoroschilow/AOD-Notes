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

from .gui.window import MainWindow


class Loader(Loader):

    @inject.params(kernel='kernel', config='config', statusbar='widget.statusbar')
    def _constructor_window(self, kernel=None, config=None, statusbar=None):
        widget = MainWindow()
        
        spacer = QtWidgets.QWidget();
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred);
        widget.statusBar().addWidget(spacer);
        
        widget.statusBar().addWidget(statusbar);
        
        width = int(config.get('window.width'))
        height = int(config.get('window.height'))
        widget.resize(width, height)

        widget.closeEvent = functools.partial(
            self.onActionClose, widget=widget
        )
        
        widget.resizeEvent = functools.partial(
            self.onActionResize, widget=widget
        )
        
        return widget

    @property
    def enabled(self):
        return True

    def config(self, binder=None):
        binder.bind_to_constructor('window', self._constructor_window)

    @inject.params(config='config')
    def onActionResize(self, event=None, widget=None, config=None):
        config.set('window.width', '%s' % event.size().width())
        config.set('window.height', '%s' % event.size().height())
        return event.accept()

    @inject.params(kernel='kernel')
    def onActionClose(self, event=None, widget=None, kernel=None):
        kernel.dispatch('window_toggle')
        return event.accept()

