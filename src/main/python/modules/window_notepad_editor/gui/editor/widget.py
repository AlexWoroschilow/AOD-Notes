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
from PyQt5.QtCore import Qt

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui

from .bar import ToolbarWidgetLeft
from .bar import ToolBarWidgetRight
from .bar import FormatbarWidget

from .scroll import TextWriter
from .text import TextEditor


class TextEditorWidget(QtWidgets.QWidget):
    fullscreen = QtCore.pyqtSignal(object)
    fullscreenAction = QtCore.pyqtSignal(object)
    save = QtCore.pyqtSignal(object)
    update = QtCore.pyqtSignal(object)

    def __init__(self):
        super(TextEditorWidget, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.setFixedWidth(500)

        self._index = None

        self.writer = TextEditor(self)
        self.writer.cursorPositionChanged.connect(self.cursorPosition)

        self.statusbar = QtWidgets.QLabel()
        self.statusbar.setAlignment(Qt.AlignCenter)

        self.leftbar = ToolbarWidgetLeft()
        self.leftbar.printAction.clicked.connect(self.writer.printAction.emit)
        self.leftbar.previewAction.clicked.connect(self.writer.previewAction.emit)
        self.leftbar.cutAction.clicked.connect(self.writer.cutAction.emit)
        self.leftbar.copyAction.clicked.connect(self.writer.copyAction.emit)
        self.leftbar.pasteAction.clicked.connect(self.writer.pasteAction.emit)
        self.leftbar.undoAction.clicked.connect(self.writer.undoAction.emit)
        self.leftbar.redoAction.clicked.connect(self.writer.redoAction.emit)
        self.leftbar.fullscreenAction.clicked.connect(self.writer.fullscreenAction.emit)
        self.leftbar.fullscreenAction.clicked.connect(self.fullscreenEvent)
        self.leftbar.saveAction.clicked.connect(self.writer.saveAction.emit)
        self.leftbar.saveAction.clicked.connect(self.saveEvent)

        self.formatbar = FormatbarWidget()
        self.formatbar.bulletAction.clicked.connect(self.writer.bulletAction.emit)
        self.formatbar.numberedAction.clicked.connect(self.writer.numberedAction.emit)
        self.formatbar.alignLeft.clicked.connect(self.writer.alignLeftAction.emit)
        self.formatbar.alignCenter.clicked.connect(self.writer.alignCenterAction.emit)
        self.formatbar.alignRight.clicked.connect(self.writer.alignRightAction.emit)
        self.formatbar.alignJustify.clicked.connect(self.writer.alignJustifyAction.emit)
        self.formatbar.indentAction.clicked.connect(self.writer.indentAction.emit)
        self.formatbar.dedentAction.clicked.connect(self.writer.dedentAction.emit)
        self.formatbar.imageAction.clicked.connect(self.writer.imageAction.emit)
        self.formatbar.fontSize.valueChanged.connect(self.writer.fontSizeAction.emit)

        self.rightbar = ToolBarWidgetRight()
        self.rightbar.italicAction.clicked.connect(self.writer.italicAction.emit)
        self.rightbar.superAction.clicked.connect(self.writer.superAction.emit)
        self.rightbar.underlAction.clicked.connect(self.writer.underlAction.emit)
        self.rightbar.strikeAction.clicked.connect(self.writer.strikeAction.emit)
        self.rightbar.fontColor.clicked.connect(self.writer.fontColorAction.emit)
        self.rightbar.backColor.clicked.connect(self.writer.backColorAction.emit)
        self.rightbar.subAction.clicked.connect(self.writer.subAction.emit)
        self.rightbar.boldAction.clicked.connect(self.writer.boldAction.emit)

        self.setLayout(QtWidgets.QGridLayout())

        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(self.leftbar, 0, 0, 5, 1)
        self.layout().addWidget(self.rightbar, 1, 2, 3, 1)
        self.layout().addWidget(self.formatbar, 1, 1)
        self.layout().addWidget(self.writer, 2, 1)
        self.layout().addWidget(self.statusbar, 3, 1)

    def document(self):
        if self.writer is None:
            return None

        return self.writer.document()

    @inject.params(storage='storage')
    def open(self, index=None, document=None, storage=None):
        if storage is None: return self
        if index is None: return self

        self.setIndex(index)

        if document is not None:
            self.writer.setDocument(document)
            return self

        content = storage.fileContent(index)
        if content is None: return self

        self.insertHtml(content)

        return self

    @inject.params(storage='storage')
    def setDocument(self, document=None, storage=None):
        if document is None and self.index is not None:
            content = storage.fileContent(self.index)
            return self.insertHtml(content)
        if self.writer is None:
            return None
        self.writer.setDocument(document)

        return None

    def focus(self):
        if self.writer is None: return self
        cursor = self.writer.textCursor()
        if cursor is None: return self
        cursor.setPosition(0)
        self.writer.setTextCursor(cursor)
        self.writer.setFocus()

        return self

    @property
    def index(self):
        return self._index

    def setIndex(self, index=None):
        if index is None:
            return None
        self._index = index

    def clean(self):
        self.writer.text.setHtml('')
        self._index = None
        return self

    def saveEvent(self, event=None):
        return self.save.emit((
            self.index, self.document()
        ))

    def fullscreenEvent(self, event=None):
        return self.fullscreen.emit((
            self.index, self.document()
        ))

    def zoomIn(self, value):
        if self.writer is None:
            return None
        self.writer.zoomIn(value)

    def zoomOut(self, value):
        if self.writer is None:
            return None
        self.writer.zoomOut(value)

    def cursorPosition(self):
        cursor = self.writer.textCursor()
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber()
        self.statusbar.setText("Line: {}, Column: {}".format(line, col))

    def getHtml(self):
        return self.writer.toHtml()

    def insertHtml(self, html=None):
        if self.writer is not None and html is not None:
            self.writer.setHtml(html)

    def appendHtml(self, html=None):
        if self.writer is not None and html is not None:
            self.writer.insertHtml(html)

    def setTextColor(self, color=None):
        if self.writer is not None and color is not None:
            self.writer.setTextColor(color)

    def setFontPointSize(self, size=None):
        if self.writer is not None and size is not None:
            self.writer.setFontPointSize(size)

    def close(self):
        super(TextEditorWidget, self).deleteLater()
        return super(TextEditorWidget, self).close()
