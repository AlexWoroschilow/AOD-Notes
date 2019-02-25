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

from .actions import ModuleActions


class Loader(Loader):

    actions = ModuleActions()

    @property
    def enabled(self):
        return True

    @inject.params(factory='toolbar_factory.leftbar')
    def boot(self, options=None, args=None, factory=None):

        widget = ToolBarButton()
        widget.setIcon(QtGui.QIcon("icons/html.svg"))
        widget.setToolTip(widget.tr("Export document to HTML"))
        widget.clickedEvent = self.clickedEvent
        
        factory.addWidget(widget)

    def clickedEvent(self, event=None, widget=None):
        self.actions.onActionButtonPressed(widget)
