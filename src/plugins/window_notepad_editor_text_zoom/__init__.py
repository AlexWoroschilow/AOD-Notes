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

from PyQt5 import QtGui

from .gui.button import ToolBarButton


class Loader(object):

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def enabled(self, options=None, args=None):
        return options.console is None

    @inject.params(factory='toolbar_factory.leftbar')
    def boot(self, options=None, args=None, factory=None):
        factory.addWidget(self._zoomIn, 70)
        factory.addWidget(self._zoomOut, 71)

    def _zoomIn(self):
        zoomIn = ToolBarButton()
        zoomIn.setShortcut("Ctrl+=")
        zoomIn.setIcon(QtGui.QIcon("icons/zoomIn.svg"))
        zoomIn.setToolTip(zoomIn.tr("Change the text color to blue"))
        zoomIn.clickedEvent = self.zoomInEvent
        return zoomIn

    def _zoomOut(self):
        zoomOut = ToolBarButton()
        zoomOut.setShortcut("Ctrl+-")
        zoomOut.setIcon(QtGui.QIcon("icons/zoomOut.svg"))
        zoomOut.setToolTip(zoomOut.tr("Change the text color to blue"))
        zoomOut.clickedEvent = self.zoomOutEvent
        return zoomOut

    def zoomOutEvent(self, event=None, widget=None):
        widget.zoomOut(5)

    def zoomInEvent(self, event=None, widget=None):
        widget.zoomIn(5)
