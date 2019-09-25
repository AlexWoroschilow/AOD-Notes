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
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from . import SettingsTitle
from . import WidgetSettings
from . import PictureButton

from PyQt5 import QtCore
from PyQt5 import QtGui


class PreviewLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal(object)

    def __init__(self, parent, picture=None):
        super(PreviewLabel, self).__init__(parent)
        self.setPixmap(picture.scaledToWidth(300, Qt.FastTransformation))

    def mousePressEvent(self, event):
        self.clicked.emit(event)

    def event(self, QEvent):
        if QEvent.type() == QtCore.QEvent.Enter:
            effect = QtWidgets.QGraphicsDropShadowEffect()
            effect.setColor(QtGui.QColor('#6cccfc'))
            effect.setBlurRadius(20)
            effect.setOffset(0)

            self.setGraphicsEffect(effect)
        if QEvent.type() == QtCore.QEvent.Leave:
            self.setGraphicsEffect(None)

        if QEvent.type() == QtCore.QEvent.MouseButtonRelease:
            effect = QtWidgets.QGraphicsDropShadowEffect()
            effect.setColor(QtGui.QColor('#6cccfc'))
            effect.setBlurRadius(20)
            effect.setOffset(0)

        return super(PreviewLabel, self).event(QEvent)


class WidgetSettingsThemes(WidgetSettings):

    def __init__(self):
        super(WidgetSettingsThemes, self).__init__()

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setAlignment(Qt.AlignLeft)

        self.layout.addWidget(SettingsTitle('Themes'))

        pixmap = QtGui.QPixmap('themes/light/preview.png')
        label = PreviewLabel(self, pixmap)
        label.setToolTip('Apply light theme')

        self.layout.addWidget(label)

        self.setLayout(self.layout)

        self.show()
