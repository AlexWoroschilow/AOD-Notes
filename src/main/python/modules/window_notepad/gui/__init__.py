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
from PyQt5 import QtCore
from PyQt5 import QtWidgets

import inject
import functools

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import Qt


class PictureButton(QtWidgets.QPushButton):
    def __init__(self, icon=None, text=None):
        super(PictureButton, self).__init__(icon, None)
        self.setToolTipDuration(0)
        self.setToolTip(text)

    def event(self, QEvent):
        if QEvent.type() == QtCore.QEvent.Enter:
            effect = QtWidgets.QGraphicsDropShadowEffect()
            effect.setColor(QtGui.QColor('#1E90FF'))
            effect.setBlurRadius(10)
            effect.setOffset(0)

            self.setGraphicsEffect(effect)
        if QEvent.type() == QtCore.QEvent.Leave:
            self.setGraphicsEffect(None)

        if QEvent.type() == QtCore.QEvent.MouseButtonRelease:
            effect = QtWidgets.QGraphicsDropShadowEffect()
            effect.setColor(QtGui.QColor('#1E90FF'))
            effect.setBlurRadius(10)
            effect.setOffset(0)

        return super(PictureButton, self).event(QEvent)


class ToolBarButton(QtWidgets.QPushButton):
    activate = QtCore.pyqtSignal(object)

    def __init__(self, name=None):
        super(ToolBarButton, self).__init__(name)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)

        self.setFlat(True)

    def connected(self):
        try:
            receiversCount = self.receivers(self.clicked)
            return receiversCount > 0
        except (SyntaxError, RuntimeError) as err:
            return False


class SearchField(QtWidgets.QLineEdit):

    def __init__(self, parent=None):
        super(SearchField, self).__init__(parent)
        self.setPlaceholderText('Enter the search string...')
        self.setObjectName('searchSearchField')
        self.setFocusPolicy(Qt.StrongFocus)

        effect = QtWidgets.QGraphicsDropShadowEffect()
        effect.setBlurRadius(3)
        effect.setOffset(0)

        self.setGraphicsEffect(effect)
