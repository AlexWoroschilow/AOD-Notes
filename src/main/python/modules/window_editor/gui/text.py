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


class PopupImageToolbar(QtWidgets.QWidget):
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


class ExamplePopup(QtWidgets.QDialog):
    sizeChanged = QtCore.pyqtSignal(object)

    def __init__(self, name, width, parent=None):
        super().__init__(parent)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.setMinimumSize(320, 240)

        self.image = QtGui.QPixmap(name)

        self.label = QtWidgets.QLabel(self)
        self.label.setBackgroundRole(QtGui.QPalette.Base)
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.label.setScaledContents(True)

        image = self.image.scaledToWidth(width)
        self.label.setFixedHeight(image.height())
        self.label.setFixedWidth(image.width())
        self.label.setPixmap(image)

        self.scrollArea = QtWidgets.QScrollArea(self)
        self.scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
        self.scrollArea.setWidget(self.label)
        self.layout().addWidget(self.scrollArea)

        self.toolbar = PopupImageToolbar(self.image.width(), width)
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


class TextEditor(QtWidgets.QTextEdit):

    def __init__(self, parent=None):
        super(TextEditor, self).__init__(parent)
        self.setWordWrapMode(QtGui.QTextOption.WordWrap)
        self.setViewportMargins(40, 20, 20, 20)
        self.setAcceptRichText(True)
        self.setAcceptDrops(True)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFrameShape(QtWidgets.QFrame.NoFrame)

        self._entity = None

    @property
    def entity(self):
        return self._entity

    @entity.setter
    def entity(self, value):
        self.entity = value

    def resizeImageEvent(self, size):
        cursor = self.textCursor()
        it = cursor.block().begin()
        while not it.atEnd():
            fragment = it.fragment()
            if not fragment.isValid() or not fragment.charFormat().isImageFormat():
                continue

            width, height = size

            newImageFormat = fragment.charFormat().toImageFormat()
            newImageFormat.setWidth(width)
            newImageFormat.setHeight(height)

            cursor.setPosition(fragment.position())
            cursor.setPosition(fragment.position() + fragment.length(), QtGui.QTextCursor.KeepAnchor)
            cursor.setCharFormat(newImageFormat)

            it += 1

    def mouseDoubleClickEvent(self, QMouseEvent):
        cursor = self.textCursor()
        it = cursor.block().begin()
        while not it.atEnd():
            fragment = it.fragment()
            if fragment.isValid() and fragment.charFormat().isImageFormat():
                image = fragment.charFormat().toImageFormat()
                popup = ExamplePopup(image.name(), 800 if not image.width() else image.width(), self)
                popup.sizeChanged.connect(self.resizeImageEvent)
                popup.setMinimumSize(200, 200)
                popup.show()

            it += 1

        # or (it = currentBlock.begin(); !(it.atEnd());
        # ++it)
        # {
        #
        #     QTextFragment
        # fragment = it.fragment();

        return super(TextEditor, self).mouseDoubleClickEvent(QMouseEvent)

    def wheelEvent(self, event):
        point = event.angleDelta()
        if event.modifiers() == QtCore.Qt.ControlModifier:
            if point.y() > 0:
                self.zoomIn(5)
            if point.y() < 0:
                self.zoomOut(5)
        return super(TextEditor, self).wheelEvent(event)

    def close(self):
        super(TextEditor, self).deleteLater()
        return super(TextEditor, self).close()
