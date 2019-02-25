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

from lib.plugin import Loader
from lib.widget.button import ToolBarButton


class Loader(Loader):

    @property
    def enabled(self):
        return True

    @inject.params(factory='toolbar_factory.leftbar')
    def boot(self, options=None, args=None, factory=None):
        
        zoomIn = ToolBarButton()
        zoomIn.setShortcut("Ctrl+=")
        zoomIn.setIcon(QtGui.QIcon("icons/zoomIn.svg"))
        zoomIn.setToolTip(zoomIn.tr("Change the text color to blue"))
        zoomIn.clickedEvent = self.zoomInEvent

        factory.addWidget(zoomIn)

        zoomOut = ToolBarButton()
        zoomOut.setShortcut("Ctrl+-")
        zoomOut.setIcon(QtGui.QIcon("icons/zoomOut.svg"))
        zoomOut.setToolTip(zoomOut.tr("Change the text color to blue"))
        zoomOut.clickedEvent = self.zoomOutEvent
        
        factory.addWidget(zoomOut)

    def zoomOutEvent(self, event=None, widget=None):
        widget.zoomOut(5)

    def zoomInEvent(self, event=None, widget=None):
        widget.zoomIn(5)

