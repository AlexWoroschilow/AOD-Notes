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
from PyQt5.QtCore import Qt

from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
import base64


class ImageResizeToolbar(QtWidgets.QWidget):
    widthChanged = QtCore.pyqtSignal(object)
    heightChanged = QtCore.pyqtSignal(object)

    def __init__(self, widthMax=None, width=None):
        super().__init__()
        self.setLayout(QtWidgets.QVBoxLayout())

        self.layout().addWidget(QtWidgets.QLabel('Size:'))
        self.sliderWidth = QtWidgets.QSlider(Qt.Horizontal)
        self.sliderWidth.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.sliderWidth.setTickInterval(widthMax / 50)
        self.sliderWidth.valueChanged.connect(self.widthChanged.emit)
        self.sliderWidth.setMaximum(widthMax)
        self.sliderWidth.setValue(width)

        self.layout().addWidget(self.sliderWidth)


class ImageResizeWidget(QtWidgets.QWidget):
    sizeChanged = QtCore.pyqtSignal(object)

    def __init__(self, parent=None, content=None, width=None):
        super().__init__(parent)
        self.setLayout(QtWidgets.QVBoxLayout())
        self.setMinimumSize(QtCore.QSize(450, 450))

        if len(content.split(',')) == 2:
            header, content = content.split(',')
        content = content.encode('utf-8')

        self.image = QtGui.QPixmap()
        self.image.loadFromData(base64.decodebytes(content))

        self.label = QtWidgets.QLabel(self)
        self.label.setBackgroundRole(QtGui.QPalette.Base)
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.label.setScaledContents(True)

        image = self.image.scaledToWidth(width)
        self.label.setFixedHeight(image.height())
        self.label.setFixedWidth(image.width())
        self.label.setPixmap(image)

        self.scrollArea = QtWidgets.QScrollArea(self)
        self.scrollArea.setMinimumSize(QtCore.QSize(500, 300))
        self.scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
        self.scrollArea.setWidget(self.label)
        self.layout().addWidget(self.scrollArea)

        self.toolbar = ImageResizeToolbar(self.image.width(), width)
        self.toolbar.widthChanged.connect(self.changeWidthEvent)
        self.layout().addWidget(self.toolbar)

    def changeHeightEvent(self, height):
        if height <= 10: return False
        image = self.image.scaledToHeight(height)
        self.sizeChanged.emit((image.width(), image.height()))

        self.label.setFixedHeight(image.height())
        self.label.setFixedWidth(image.width())
        self.label.setPixmap(image)

    def changeWidthEvent(self, width):
        if width <= 10: return False
        image = self.image.scaledToWidth(width)
        self.sizeChanged.emit((image.width(), image.height()))

        self.label.setFixedHeight(image.height())
        self.label.setFixedWidth(image.width())
        self.label.setPixmap(image)
