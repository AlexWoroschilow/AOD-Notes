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

from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui

from . import ToolBarButton
from . import PictureButton
from . import SearchField


class ButtonDisabled(QtWidgets.QPushButton):

    def __init__(self, icon=None, text=None):
        super(ButtonDisabled, self).__init__(icon, None)
        self.setCheckable(False)
        self.setFlat(True)
        self.setDisabled(True)


class ButtonPicture(QtWidgets.QPushButton):
    def __init__(self, icon=None, text=None):
        super(ButtonPicture, self).__init__(icon, None)
        self.setToolTipDuration(0)
        self.setToolTip(text)


class ButtonToolBar(QtWidgets.QPushButton):
    activate = QtCore.pyqtSignal(object)

    def __init__(self, name=None):
        super(ButtonToolBar, self).__init__(name)
        self.setFlat(True)

    def connected(self):
        try:
            receiversCount = self.receivers(self.clicked)
            return receiversCount > 0
        except (SyntaxError, RuntimeError) as err:
            return False
