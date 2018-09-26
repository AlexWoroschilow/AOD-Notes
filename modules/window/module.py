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
from .gui.header import WidgetHeaderFactory


class Loader(Loader):

    @property
    def enabled(self):
        return True

    def config(self, binder=None):
        """
        Store the settings widgets from te different 
        modules in the factory and access them all the time
        """
        binder.bind('window.header_factory', WidgetHeaderFactory())
        
        binder.bind_to_constructor('window', self._constructor_window)
        binder.bind_to_constructor('window.header', self._constructor_window_header)
        binder.bind_to_constructor('window.footer', self._constructor_window_footer)

    @inject.params(config='config', factory='window.header_factory')
    def _constructor_window(self, config=None, factory=None):
        
        widget = MainWindow()
        widget.resize(int(config.get('window.width')),
                      int(config.get('window.height')))
        
        widget.header = widget.addToolBar('main')
        widget.header.setIconSize(QtCore.QSize(20, 20))
        widget.header.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        widget.header.setObjectName('MainToolbar')
        widget.header.setFloatable(False)
        widget.header.setMovable(False)
        
        for header_widget in factory.widgets:
            if isinstance(header_widget, QtWidgets.QAction):
                widget.header.addAction(header_widget)
            if isinstance(header_widget, QtWidgets.QWidget):
                widget.header.addWidget(header_widget)

        widget.footer = widget.statusBar()

        widget.resizeEvent = functools.partial(
            self.onActionWindowResize
        )
        
        return widget

    @inject.params(window='window')
    def _constructor_window_header(self, window=None):
        if window.header is not None:
            return window.header
        return None

    @inject.params(window='window')
    def _constructor_window_footer(self, window=None):
        if window.footer is not None:
            return window.footer
        return None

    @inject.params(config='config')
    def onActionWindowResize(self, event=None, config=None):
        config.set('window.width', '%s' % event.size().width())
        config.set('window.height', '%s' % event.size().height())
        return event.accept()
