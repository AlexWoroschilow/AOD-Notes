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

from PyQt5 import QtPrintSupport
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui

from .bar import ToolbarWidgetLeft
from .bar import ToolBarWidgetRight
from .bar import FormatbarWidget

from .scroll import TextWriter


class TextEditorWidget(QtWidgets.QWidget):
    fullscreen = QtCore.pyqtSignal(object)
    save = QtCore.pyqtSignal(object)
    update = QtCore.pyqtSignal(object)

    fullscreenAction = QtCore.pyqtSignal(object)

    def __init__(self):
        super(TextEditorWidget, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)

        self._index = None

        self.writer = TextWriter(self)
        self.writer.text.cursorPositionChanged.connect(self.cursorPosition)

        self.statusbar = QtWidgets.QLabel()
        self.statusbar.setAlignment(Qt.AlignCenter)

        self.leftbar = ToolbarWidgetLeft()

        self.leftbar.printAction.clicked.connect(self.onActionPrint)
        self.leftbar.previewAction.clicked.connect(self.onActionPreview)
        self.leftbar.cutAction.clicked.connect(self.writer.text.cut)
        self.leftbar.copyAction.clicked.connect(self.writer.text.copy)
        self.leftbar.pasteAction.clicked.connect(self.writer.text.paste)
        self.leftbar.undoAction.clicked.connect(self.writer.text.undo)
        self.leftbar.redoAction.clicked.connect(self.writer.text.redo)

        self.leftbar.saveAction.clicked.connect(lambda x: self.save.emit((self.index, self.writer.document())))
        # self.leftbar.saveAction.clicked.connect(lambda x: self.update.emit(self.writer.document()))
        self.leftbar.fullscreenAction.clicked.connect(
            lambda x: self.fullscreen.emit((self.index, self.writer.document())))

        self.formatbar = FormatbarWidget()
        self.formatbar.fontSize.valueChanged.connect(lambda size: self.writer.text.setFontPointSize(size))
        self.formatbar.bulletAction.clicked.connect(self.onActionBulletList)
        self.formatbar.numberedAction.clicked.connect(self.onActionNumberList)
        self.formatbar.alignLeft.clicked.connect(self.onActionAlignLeft)
        self.formatbar.alignCenter.clicked.connect(self.onActionAlignCenter)
        self.formatbar.alignRight.clicked.connect(self.onActionAlignRight)
        self.formatbar.alignJustify.clicked.connect(self.onActionAlignJustify)
        self.formatbar.indentAction.clicked.connect(self.onActionIndent)
        self.formatbar.dedentAction.clicked.connect(self.onActionDedent)
        self.formatbar.imageAction.clicked.connect(self.onActionInsertImage)

        self.rightbar = ToolBarWidgetRight()
        self.rightbar.italicAction.clicked.connect(self.onActionItalic)
        self.rightbar.superAction.clicked.connect(self.onActionSuperScript)
        self.rightbar.strikeAction.clicked.connect(self.onActionStrike)
        self.rightbar.fontColor.clicked.connect(self.onActionFontColor)
        self.rightbar.backColor.clicked.connect(self.onActionHighlight)
        self.rightbar.subAction.clicked.connect(self.onActionSubScript)
        self.rightbar.boldAction.clicked.connect(self.onActionBold)

        layout = QtWidgets.QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.leftbar, 0, 0, 5, 1)
        layout.addWidget(self.rightbar, 1, 2, 3, 1)
        layout.addWidget(self.formatbar, 1, 1)
        layout.addWidget(self.writer, 2, 1)
        layout.addWidget(self.statusbar, 3, 1)

        self.setLayout(layout)

    def index(self):
        return self._index

    def setIndex(self, index=None):
        if index is None:
            return None
        self._index = index

    def document(self):
        if self.writer is None:
            return None

        return self.writer.document()

    def setDocument(self, document=None):
        if document is None:
            return None
        if self.writer is None:
            return None

        self.writer.setDocument(document)

        return None

    def focus(self):
        if self.writer is None: return self
        cursor = self.writer.text.textCursor()
        if cursor is None: return self
        cursor.setPosition(0)
        self.writer.text.setTextCursor(cursor)
        self.writer.focus()

        return self

    @property
    def index(self):
        return self._index

    @index.setter
    @inject.params(storage='storage')
    def index(self, value, storage):
        pass
        # self._index = value
        # content = storage.fileContent(value)
        # self.insertHtml(content)

    def clean(self):
        self.writer.text.setHtml('')
        self._index = None
        return self

    def zoomIn(self, value):
        if self.writer is None:
            return None
        self.writer.zoomIn(value)

    def zoomOut(self, value):
        if self.writer is None:
            return None
        self.writer.zoomOut(value)

    def cursorPosition(self):
        cursor = self.writer.text.textCursor()
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber()
        self.statusbar.setText("Line: {}, Column: {}".format(line, col))

    def onActionPreview(self):
        preview = QtPrintSupport.QPrintPreviewDialog()
        preview.paintRequested.connect(lambda p: self.writer.text.print_(p))
        preview.exec_()

    def onActionPrint(self):
        dialog = QtPrintSupport.QPrintDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.writer.text.document().print_(dialog.printer())

    def onActionInsertImage(self):
        filename = \
            QtWidgets.QFileDialog.getOpenFileName(self, 'Insert image', ".", "Images (*.png *.xpm *.jpg *.bmp *.gif)")[
                0]
        if filename:
            image = QtGui.QImage(filename)
            if image.isNull():
                popup = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                                              "Image load error",
                                              "Could not load image file!",
                                              QtWidgets.QMessageBox.Ok,
                                              self)
                popup.show()
            else:
                cursor = self.writer.text.textCursor()
                image = image.scaled(800, 600, Qt.KeepAspectRatio)
                cursor.insertImage(image, filename)

    def getHtml(self):
        return self.writer.text.toHtml()

    def insertHtml(self, html=None):
        if self.writer is not None and html is not None:
            self.writer.text.setHtml(html)

    def appendHtml(self, html=None):
        if self.writer is not None and html is not None:
            self.writer.text.insertHtml(html)

    def setTextColor(self, color=None):
        if self.writer is not None and color is not None:
            self.writer.text.setTextColor(color)

    def setFontPointSize(self, size=None):
        if self.writer is not None and size is not None:
            self.writer.text.setFontPointSize(size)

    def onActionFontColor(self):
        self.setTextColor(QtWidgets.QColorDialog.getColor())

    def onActionHighlight(self):
        color = QtWidgets.QColorDialog.getColor()
        self.writer.text.setTextBackgroundColor(color)

    def onActionBold(self):
        if self.writer.text.fontWeight() == QtGui.QFont.Bold:
            self.writer.text.setFontWeight(QtGui.QFont.Normal)
        else:
            self.writer.text.setFontWeight(QtGui.QFont.Bold)

    def onActionItalic(self):
        state = self.writer.text.fontItalic()
        self.writer.text.setFontItalic(not state)

    def onActionUnderline(self):
        state = self.writer.text.fontUnderline()
        self.writer.text.setFontUnderline(not state)

    def onActionStrike(self):
        fmt = self.writer.text.currentCharFormat()
        fmt.setFontStrikeOut(not fmt.fontStrikeOut())
        self.writer.text.setCurrentCharFormat(fmt)

    def onActionSuperScript(self):
        fmt = self.writer.text.currentCharFormat()
        align = fmt.verticalAlignment()
        if align == QtGui.QTextCharFormat.AlignNormal:
            fmt.setVerticalAlignment(QtGui.QTextCharFormat.AlignSuperScript)
        else:
            fmt.setVerticalAlignment(QtGui.QTextCharFormat.AlignNormal)
        self.writer.text.setCurrentCharFormat(fmt)

    def onActionSubScript(self):
        fmt = self.writer.text.currentCharFormat()
        align = fmt.verticalAlignment()
        if align == QtGui.QTextCharFormat.AlignNormal:
            fmt.setVerticalAlignment(QtGui.QTextCharFormat.AlignSubScript)
        else:
            fmt.setVerticalAlignment(QtGui.QTextCharFormat.AlignNormal)
        self.writer.text.setCurrentCharFormat(fmt)

    def onActionAlignLeft(self):
        self.writer.text.setAlignment(Qt.AlignLeft)

    def onActionAlignRight(self):
        self.writer.text.setAlignment(Qt.AlignRight)

    def onActionAlignCenter(self):
        self.writer.text.setAlignment(Qt.AlignCenter)

    def onActionAlignJustify(self):
        self.writer.text.setAlignment(Qt.AlignJustify)

    def onActionIndent(self):
        cursor = self.writer.text.textCursor()
        if cursor.hasSelection():
            temp = cursor.blockNumber()
            cursor.setPosition(cursor.anchor())
            diff = cursor.blockNumber() - temp
            direction = QtGui.QTextCursor.Up if diff > 0 else QtGui.QTextCursor.Down
            for n in range(abs(diff) + 1):
                cursor.movePosition(QtGui.QTextCursor.StartOfLine)
                cursor.insertText("\t")
                cursor.movePosition(direction)
        else:
            cursor.insertText("\t")

    def handleDedent(self, cursor):
        cursor.movePosition(QtGui.QTextCursor.StartOfLine)
        line = cursor.block().text()
        if line.startswith("\t"):
            cursor.deleteChar()
        else:
            for char in line[:8]:
                if char != " ":
                    break
                cursor.deleteChar()

    def onActionDedent(self):
        cursor = self.writer.text.textCursor()
        if cursor.hasSelection():
            temp = cursor.blockNumber()
            cursor.setPosition(cursor.anchor())
            diff = cursor.blockNumber() - temp
            direction = QtGui.QTextCursor.Up if diff > 0 else QtGui.QTextCursor.Down
            for n in range(abs(diff) + 1):
                self.handleDedent(cursor)
                cursor.movePosition(direction)
        else:
            self.handleDedent(cursor)

    def onActionBulletList(self):
        cursor = self.writer.text.textCursor()
        cursor.insertList(QtGui.QTextListFormat.ListDisc)

    def onActionNumberList(self):
        cursor = self.writer.text.textCursor()
        cursor.insertList(QtGui.QTextListFormat.ListDecimal)

    def close(self):
        super(TextEditorWidget, self).deleteLater()
        return super(TextEditorWidget, self).close()
