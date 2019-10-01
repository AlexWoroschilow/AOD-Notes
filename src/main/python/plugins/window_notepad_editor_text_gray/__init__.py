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

    def _constructor(self):
        widget = ToolBarButton()
        widget.setIcon(QtGui.QIcon("icons/font-gray.svg"))
        widget.setToolTip(widget.tr("Change the text color to gray"))
        widget.clickedEvent = self.clickedEvent
        return widget

    def enabled(self, options=None, args=None):
        return options.console is None

    @inject.params(factory='toolbar_factory.rightbar')
    def boot(self, options=None, args=None, factory=None):
        factory.addWidget(self._constructor, 52)

    def clickedEvent(self, event=None, widget=None):
        widget.setTextColor(QtGui.QColor.fromRgb(127, 127, 127))
