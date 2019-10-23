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
from .menu.action import ImageResizeAction


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
        iterator = cursor.block().begin()
        while not iterator.atEnd():

            fragment = iterator.fragment()
            if fragment is None: break

            if not fragment.isValid() or not fragment.charFormat().isImageFormat():
                continue

            width, height = size
            if height is None: break
            if width is None: break

            image = fragment.charFormat().toImageFormat()
            if image is None: break

            image.setWidth(width)
            image.setHeight(height)

            cursor.setPosition(fragment.position())
            cursor.setPosition(fragment.position() + fragment.length(), QtGui.QTextCursor.KeepAnchor)
            cursor.setCharFormat(image)
            break

            iterator += 1

    def mouseDoubleClickEvent(self, event):
        cursor = self.textCursor()
        iterator = cursor.block().begin()
        while not iterator.atEnd():
            fragment = iterator.fragment()
            if fragment is None: return None

            if not fragment.isValid() or not fragment.charFormat().isImageFormat():
                continue

            image = fragment.charFormat().toImageFormat()
            if image is None: break

            width = 800 if not image.width() else image.width()
            if width is None: break

            popup = ImageResizeAction(self, image.name(), width)
            popup.sizeChanged.connect(self.resizeImageEvent)

            menu = QtWidgets.QMenu()
            menu.addAction(popup)
            menu.exec_(QtGui.QCursor.pos())
            break

            iterator += 1

        return super(TextEditor, self).mouseDoubleClickEvent(event)

    def imageInsertEvent(self):

        title = 'Insert image'
        formats = "Images (*.png *.xpm *.jpg *.bmp *.gif)"
        filename, formats = QtWidgets.QFileDialog.getOpenFileName(self, title, ".", formats)
        if filename is None: return None

        image = QtGui.QImage(filename)
        if image.isNull(): return None

        cursor = self.textCursor()
        cursor.insertImage(image.scaled(800, 600, Qt.KeepAspectRatio), filename)

        popup = ImageResizeAction(self, filename, 800)
        popup.sizeChanged.connect(self.resizeImageEvent)

        menu = QtWidgets.QMenu()
        menu.addAction(popup)
        menu.exec_(QtGui.QCursor.pos())

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
