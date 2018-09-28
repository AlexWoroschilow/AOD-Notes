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
        kernel.listen('window.notepad.rightbar', self._widget, 100)

    def _widget(self, event=None):
        widget = ToolBarButton()
        widget.editor, widget.toolbar = event.data
        if widget.editor is None or widget.toolbar is None:
            raise 'Editor or Toolbar object can not be empty'

        widget.setIcon(QtGui.QIcon("icons/font-black.svg"))
        widget.setToolTip(widget.tr("Change the text color to black"))

        widget.clicked.connect(functools.partial(
            self.actions.onActionButtonPressed, widget=widget
        ))

        widget.toolbar.addWidget(widget)
