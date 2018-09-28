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

from PyQt5 import QtGui

from lib.plugin import Loader
from lib.widget.button import ToolBarButton

from .actions import ModuleActions


class Loader(Loader):

    actions = ModuleActions()

    @property
    def enabled(self):
        return True

    @inject.params(kernel='kernel')
    def boot(self, options=None, args=None, kernel=None):
        kernel.listen('window.notepad.leftbar', self._widget, 512)

    def _widget(self, event=None):
        
        zoomIn = ToolBarButton()
        zoomIn.setShortcut("Ctrl+=")
        
        zoomIn.editor, toolbar = event.data
        if zoomIn.editor is None or toolbar is None:
            raise 'Editor or Toolbar object can not be empty'
        zoomIn.setIcon(QtGui.QIcon("icons/zoomIn.svg"))
        zoomIn.setToolTip(zoomIn.tr("Change the text color to blue"))
        zoomIn.clicked.connect(functools.partial(
            self.actions.onActionZoomIn, widget=zoomIn
        ))
        
        zoomOut = ToolBarButton()
        zoomOut.setShortcut("Ctrl+-")
        zoomOut.editor, zoomOut.toolbar = event.data
        if zoomOut.editor is None or toolbar is None:
            raise 'Editor or Toolbar object can not be empty'
        zoomOut.setIcon(QtGui.QIcon("icons/zoomOut.svg"))
        zoomOut.setToolTip(zoomOut.tr("Change the text color to blue"))
        zoomOut.clicked.connect(functools.partial(
            self.actions.onActionZoomOut, widget=zoomOut
        ))
        
        toolbar.addSeparator()
        toolbar.addWidget(zoomIn)
        toolbar.addWidget(zoomOut)

