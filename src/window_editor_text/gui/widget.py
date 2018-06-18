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

from PyQt5 import QtPrintSupport
from PyQt5 import QtWidgets
from PyQt5 import QtGui

from .bar import ToolbarWidgetLeft
from .bar import ToolBarWidgetRight
from .bar import FormatbarWidget

from .line import NameEditor
from .scroll import TextWriter


class TextEditorWidget(QtWidgets.QWidget):

    def __init__(self, parent=None, config=None):
        super(TextEditorWidget, self).__init__(parent)
        self.setObjectName('editorTextEditorWidget')
        self.setContentsMargins(0, 0, 0, 0)

        self._name = NameEditor()

        self._text = TextWriter(self)
        self._text.text.cursorPositionChanged.connect(self.cursorPosition)

        self.statusbar = QtWidgets.QLabel()
        self.statusbar.setAlignment(Qt.AlignCenter)

        self.leftbar = ToolbarWidgetLeft()
        self.leftbar.setVisible(bool(config.get('editor.leftbar')))
        
        self.leftbar.printAction.clicked.connect(self.printHandler)
        self.leftbar.previewAction.clicked.connect(self.preview)
        self.leftbar.cutAction.clicked.connect(self._text.text.cut)
        self.leftbar.copyAction.clicked.connect(self._text.text.copy)
        self.leftbar.pasteAction.clicked.connect(self._text.text.paste)
        self.leftbar.undoAction.clicked.connect(self._text.text.undo)
        self.leftbar.redoAction.clicked.connect(self._text.text.redo)

        self.formatbar = FormatbarWidget()
        self.formatbar.setVisible(bool(config.get('editor.formatbar')))
        self.formatbar.fontSize.valueChanged.connect(lambda size: self._text.text.setFontPointSize(size))
        self.formatbar.bulletAction.clicked.connect(self.bulletList)
        self.formatbar.numberedAction.clicked.connect(self.numberList)
        self.formatbar.alignLeft.clicked.connect(self.alignLeft)
        self.formatbar.alignCenter.clicked.connect(self.alignCenter)
        self.formatbar.alignRight.clicked.connect(self.alignRight)
        self.formatbar.alignJustify.clicked.connect(self.alignJustify)
        self.formatbar.indentAction.clicked.connect(self.indent)
        self.formatbar.dedentAction.clicked.connect(self.dedent)
        self.formatbar.imageAction.clicked.connect(self.insertImage)

        self.rightbar = ToolBarWidgetRight()
        self.rightbar.setVisible(bool(config.get('editor.rightbar')))
        self.rightbar.italicAction.clicked.connect(self.italic)
        self.rightbar.boldAction.clicked.connect(self.bold)
        self.rightbar.strikeAction.clicked.connect(self.strike)
        self.rightbar.superAction.clicked.connect(self.superScript)
        self.rightbar.subAction.clicked.connect(self.subScript)
        self.rightbar.backColor.clicked.connect(self.highlight)

        layout = QtWidgets.QGridLayout()
        layout.setContentsMargins(0, 10, 0, 0)

        layout.addWidget(self.leftbar, 0, 0, 5, 1)
        layout.addWidget(self._name, 0, 1, 1, 2)
        layout.addWidget(self.rightbar, 1, 2, 3, 1)
        layout.addWidget(self.formatbar, 1, 1)
        layout.addWidget(self._text, 2, 1)
        layout.addWidget(self.statusbar, 3, 1)

        self.setLayout(layout)
        
        self._note = None

    @property
    def name(self):
        if self._name is None:
            return None
        return self._name.text() 

    @property
    def text(self):
        if self._text is None:
            return None
        if self._text.text is None:
            return None
        return self._text.text.toHtml()

    @property
    def description(self):
        if self._text is None:
            return None
        if self._text.text is None:
            return None
        return self._text.text.toPlainText()

    @property
    def folder(self):
        if self.formatbar is None:
            return None
        return self.formatbar.folder

    @folder.setter
    def folder(self, folder=None):
        if self.formatbar is not None:
            self.formatbar.folder = folder 
        return self

    @property
    def note(self):
        if self._note is None:
            return None
        return self._note

    @note.setter
    def note(self, entity=None):
        self._note = entity
        if entity is None:
            self._text.text.setHtml('')
            self._name.setText('')
            return self
            
        if entity.folder is not None:
            self.folder = entity.folder
            
        self._name.setText(entity.name)
        self._text.text.setHtml(entity.text)
        
        return self

    @property
    def entity(self):
        return self.note

    @entity.setter
    def entity(self, entity=None):
        self.note = entity
        return self

    def cursorPosition(self):
        cursor = self._text.text.textCursor()
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber()
        self.statusbar.setText("Line: {}, Column: {}".format(line, col))

    def toggleToolbar(self):
        state = self.leftbar.isVisible()
        self.leftbar.setVisible(not state)

    def toggleFormatbar(self):
        state = self.formatbar.isVisible()
        self.formatbar.setVisible(not state)

    def preview(self):
        preview = QtPrintSupport.QPrintPreviewDialog()
        preview.paintRequested.connect(lambda p: self._text.text.print_(p))
        preview.exec_()

    def printHandler(self):
        dialog = QtPrintSupport.QPrintDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self._text.text.document().print_(dialog.printer())

    def insertImage(self):
        filename = \
        QtWidgets.QFileDialog.getOpenFileName(self, 'Insert image', ".", "Images (*.png *.xpm *.jpg *.bmp *.gif)")[0]
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
                cursor = self._text.text.textCursor()
                image = image.scaled(800, 600, Qt.KeepAspectRatio)
                cursor.insertImage(image, filename)

    def fontColorChanged(self):
        color = QtWidgets.QColorDialog.getColor()
        self._text.text.setTextColor(color)

    def highlight(self):
        color = QtWidgets.QColorDialog.getColor()
        self._text.text.setTextBackgroundColor(color)

    def bold(self):
        if self._text.text.fontWeight() == QtGui.QFont.Bold:
            self._text.text.setFontWeight(QtGui.QFont.Normal)
        else:
            self._text.text.setFontWeight(QtGui.QFont.Bold)

    def italic(self):
        state = self._text.text.fontItalic()
        self._text.text.setFontItalic(not state)

    def underline(self):
        state = self._text.text.fontUnderline()
        self._text.text.setFontUnderline(not state)

    def strike(self):
        fmt = self._text.text.currentCharFormat()
        fmt.setFontStrikeOut(not fmt.fontStrikeOut())
        self._text.text.setCurrentCharFormat(fmt)

    def superScript(self):
        fmt = self._text.text.currentCharFormat()
        align = fmt.verticalAlignment()
        if align == QtGui.QTextCharFormat.AlignNormal:
            fmt.setVerticalAlignment(QtGui.QTextCharFormat.AlignSuperScript)
        else:
            fmt.setVerticalAlignment(QtGui.QTextCharFormat.AlignNormal)
        self._text.text.setCurrentCharFormat(fmt)

    def subScript(self):
        fmt = self._text.text.currentCharFormat()
        align = fmt.verticalAlignment()
        if align == QtGui.QTextCharFormat.AlignNormal:
            fmt.setVerticalAlignment(QtGui.QTextCharFormat.AlignSubScript)
        else:
            fmt.setVerticalAlignment(QtGui.QTextCharFormat.AlignNormal)
        self._text.text.setCurrentCharFormat(fmt)

    def alignLeft(self):
        self._text.text.setAlignment(Qt.AlignLeft)

    def alignRight(self):
        self._text.text.setAlignment(Qt.AlignRight)

    def alignCenter(self):
        self._text.text.setAlignment(Qt.AlignCenter)

    def alignJustify(self):
        self._text.text.setAlignment(Qt.AlignJustify)

    def indent(self):
        cursor = self._text.text.textCursor()
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

    def dedent(self):
        cursor = self._text.text.textCursor()
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

    def bulletList(self):
        cursor = self._text.text.textCursor()
        cursor.insertList(QtGui.QTextListFormat.ListDisc)

    def numberList(self):
        cursor = self._text.text.textCursor()
        cursor.insertList(QtGui.QTextListFormat.ListDecimal)
