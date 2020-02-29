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

from .text import TextEditor


class TextEditorWidget(QtWidgets.QFrame):
    fullscreenNoteAction = QtCore.pyqtSignal(object)
    saveNoteAction = QtCore.pyqtSignal(object)

    def __init__(self):
        super(TextEditorWidget, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)

        self.entity = None

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
        """
        Required for the plugins
        :return:
        """
        if self.writer is None:
            return None

        return self.writer.document()

    def open(self, entity=None):
        if entity is None: return self
        self.insertHtml(entity.content)
        self.entity = entity
        return self

    def focus(self):
        if self.writer is None: return self
        cursor = self.writer.textCursor()
        if cursor is None: return self
        cursor.setPosition(0)
        self.writer.setTextCursor(cursor)
        self.writer.setFocus()

        return self

    def clean(self):
        if self.writer is None: return self
        self.writer.text.setHtml('')
        self.entity = None
        return self

    def fullscreenEvent(self, event=None):
        self.fullscreenNoteAction.emit(self.entity)
        return self

    def saveEvent(self, event=None):
        if self.entity is None: return self
        self.entity.content = self.getHtml()
        self.saveNoteAction.emit(self.entity)
        return self

    def zoomIn(self, value):
        if self.writer is None: return None
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

    def insertHtml(self, content=None):
        if self.writer is None: return None
        if content is None: return None
        self.writer.setHtml(content)

    def appendHtml(self, html=None):
        if self.writer is None: return None
        if content is None: return None
        self.writer.insertHtml(content)

    def setTextColor(self, color=None):
        if self.writer is not None and color is not None:
            self.writer.setTextColor(color)

    def setFontPointSize(self, size=None):
        if self.writer is not None and size is not None:
            self.writer.setFontPointSize(size)

    def close(self):
        super(TextEditorWidget, self).deleteLater()
        return super(TextEditorWidget, self).close()
