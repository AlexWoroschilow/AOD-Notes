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
from PyQt5 import QtPrintSupport
from PyQt5 import QtWidgets
from PyQt5 import QtGui

from .bar import ToolbarWidgetLeft
from .bar import ToolBarWidgetRight
from .bar import FormatbarWidget


class TextWriter(QtWidgets.QScrollArea):

    def __init__(self, parent=None):
        super(TextWriter, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setObjectName('editorQScrollArea')

        self.text = TextEditor(self)

        self.setWidgetResizable(True)
        self.setWidget(self.text)

        # Align the scrollArea's widget in the center
        self.setAlignment(Qt.AlignHCenter)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)


class TextEditor(QtWidgets.QTextEdit):

    def __init__(self, parent=None):
        super(TextEditor, self).__init__(parent)
        self.setObjectName('editorTextEditor')
        self.setWordWrapMode(QtGui.QTextOption.WordWrap)
        self.setViewportMargins(40, 20, 20, 20)
        self.setAcceptRichText(True)
        self.setAcceptDrops(True)
        self.setFontPointSize(14)

        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self._entity = None
        
    @property
    def entity(self):
        return self._entity

    @entity.setter
    def entity(self, value):
        self.entity = value


class NameEditor(QtWidgets.QLineEdit):

    def __init__(self, parent=None):
        super(NameEditor, self).__init__(parent)
        self.setObjectName('editorNameEditor')


class TextEditorWidget(QtWidgets.QWidget):

    @inject.params(storage='storage', kernel='kernel')
    def __init__(self, parent=None, storage=None, kernel='kernel'):
        super(TextEditorWidget, self).__init__(parent)
        self.setObjectName('editorTextEditorWidget')
        self.setContentsMargins(0, 0, 0, 0)

        kernel.listen('window.notepad.note_update', self._onNoteUpdateEvent, 128)

        self.changesSaved = True
        self.filename = ""
        self._index = None

        self.name = NameEditor()

        self.writer = TextWriter(self)
        self.writer.text.cursorPositionChanged.connect(self.cursorPosition)
        self.writer.text.textChanged.connect(self.changed)

        self.leftbar = ToolbarWidgetLeft(self.writer)
        self.leftbar.saveAction.clicked.connect(self._onSaveEvent)
        self.leftbar.printAction.clicked.connect(self.printHandler)
        self.leftbar.previewAction.clicked.connect(self.preview)
        self.leftbar.cutAction.clicked.connect(self.writer.text.cut)
        self.leftbar.copyAction.clicked.connect(self.writer.text.copy)
        self.leftbar.pasteAction.clicked.connect(self.writer.text.paste)
        self.leftbar.undoAction.clicked.connect(self.writer.text.undo)
        self.leftbar.redoAction.clicked.connect(self.writer.text.redo)
        self.leftbar.fullscreenAction.clicked.connect(self._onFullScreenEvent)

        self.formatbar = FormatbarWidget(self.writer)
        self.formatbar.fontSize.valueChanged.connect(lambda size: self.writer.text.setFontPointSize(size))
        self.formatbar.bulletAction.clicked.connect(self.bulletList)
        self.formatbar.numberedAction.clicked.connect(self.numberList)
        self.formatbar.alignLeft.clicked.connect(self.alignLeft)
        self.formatbar.alignCenter.clicked.connect(self.alignCenter)
        self.formatbar.alignRight.clicked.connect(self.alignRight)
        self.formatbar.alignJustify.clicked.connect(self.alignJustify)
        self.formatbar.indentAction.clicked.connect(self.indent)
        self.formatbar.dedentAction.clicked.connect(self.dedent)
        self.formatbar.imageAction.clicked.connect(self.insertImage)

        self.rightbar = ToolBarWidgetRight(self.writer)
        self.rightbar.italicAction.clicked.connect(self.italic)
        self.rightbar.boldAction.clicked.connect(self.bold)
        self.rightbar.strikeAction.clicked.connect(self.strike)
        self.rightbar.superAction.clicked.connect(self.superScript)
        self.rightbar.subAction.clicked.connect(self.subScript)
        self.rightbar.backColor.clicked.connect(self.highlight)

        layout = QtWidgets.QGridLayout()
        layout.setContentsMargins(0, 10, 0, 0)

        layout.addWidget(self.leftbar, 0, 0, 5, 1)
        layout.addWidget(self.name, 0, 1, 1, 2)
        layout.addWidget(self.rightbar, 1, 2, 3, 1)
        layout.addWidget(self.formatbar, 1, 1)
        layout.addWidget(self.writer, 2, 1)

        self.setLayout(layout)

    def _onNoteUpdateEvent(self, event=None):
        if self._entity.index in [event.data.index]:
            self.setEntity(event.data)

    @property
    def entity(self):
        if self.writer is None:
            return None
        return self.writer.entity

    @entity.setter
    def entity(self, entity):
        self.writer.entity = entity
        if entity is None:
            self.writer.text.setText('')
            self.name.setText('')
            return None

        self.name.setText(entity.name)
        self.writer.text.setText(entity.text)

        if entity.folder is None:
            return None

        self.formatbar.setFolder(entity.folder)

    @inject.params(kernel='kernel')
    def _onFullScreenEvent(self, event=None, kernel=None):
        if self._entity is not None and kernel is not None:
            kernel.dispatch('window.notepad.note_tab', self._entity)

    @inject.params(storage='storage')
    def _onWindowNoteEdit(self, event=None, dispatcher=None, storage=None):
        if storage is None or event.data is None:
            return None

        entity = event.data
        if self._entity.index not in [entity.index]:
            return None

        if self.writer.text is None or self.name is None:
            return None

        self.name.setText(entity.name)
        self.writer.text.setText(entity.text)

    @inject.params(kernel='kernel')
    def _onSaveEvent(self, event=None, kernel=None):
        if self._entity is None or kernel is None:
            return None

        self._entity.name = self.name.text()
        self._entity.text = self.writer.text.toHtml()

        kernel.dispatch('window.notepad.note_update', self._entity)

    def setEntity(self, entity=None):
        self.entity = entity

    def changed(self):
        self.changesSaved = False

    def cursorPosition(self):
        cursor = self.writer.text.textCursor()

        # Mortals like 1-indexed things
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber()

    def toggleToolbar(self):
        state = self.leftbar.isVisible()
        self.leftbar.setVisible(not state)

    def toggleFormatbar(self):
        state = self.formatbar.isVisible()
        self.formatbar.setVisible(not state)

    def preview(self):

        # Open preview dialog
        preview = QtPrintSupport.QPrintPreviewDialog()

        # If a print is requested, open print dialog
        preview.paintRequested.connect(lambda p: self.writer.text.print_(p))

        preview.exec_()

    def printHandler(self):

        # Open printing dialog
        dialog = QtPrintSupport.QPrintDialog()

        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.writer.text.document().print_(dialog.printer())

    def insertImage(self):

        # Get image file name
        # PYQT5 Returns a tuple in PyQt5
        filename = \
        QtWidgets.QFileDialog.getOpenFileName(self, 'Insert image', ".", "Images (*.png *.xpm *.jpg *.bmp *.gif)")[0]

        if filename:

            # Create image object
            image = QtGui.QImage(filename)

            # Error if unloadable
            if image.isNull():

                popup = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                                              "Image load error",
                                              "Could not load image file!",
                                              QtWidgets.QMessageBox.Ok,
                                              self)
                popup.show()

            else:

                cursor = self.writer.text.textCursor()

                cursor.insertImage(image, filename)

    def fontColorChanged(self):

        # Get a color from the text dialog
        color = QtWidgets.QColorDialog.getColor()

        # Set it as the new text color
        self.writer.text.setTextColor(color)

    def highlight(self):

        color = QtWidgets.QColorDialog.getColor()

        self.writer.text.setTextBackgroundColor(color)

    def bold(self):

        if self.writer.text.fontWeight() == QtGui.QFont.Bold:
            self.writer.text.setFontWeight(QtGui.QFont.Normal)
        else:
            self.writer.text.setFontWeight(QtGui.QFont.Bold)

    def italic(self):

        state = self.writer.text.fontItalic()
        self.writer.text.setFontItalic(not state)

    def underline(self):

        state = self.writer.text.fontUnderline()

        self.writer.text.setFontUnderline(not state)

    def strike(self):

        # Grab the text's format
        fmt = self.writer.text.currentCharFormat()

        # Set the fontStrikeOut property to its opposite
        fmt.setFontStrikeOut(not fmt.fontStrikeOut())

        # And set the next char format
        self.writer.text.setCurrentCharFormat(fmt)

    def superScript(self):

        # Grab the current format
        fmt = self.writer.text.currentCharFormat()

        # And get the vertical alignment property
        align = fmt.verticalAlignment()

        # Toggle the state
        if align == QtGui.QTextCharFormat.AlignNormal:

            fmt.setVerticalAlignment(QtGui.QTextCharFormat.AlignSuperScript)

        else:

            fmt.setVerticalAlignment(QtGui.QTextCharFormat.AlignNormal)

        # Set the new format
        self.writer.text.setCurrentCharFormat(fmt)

    def subScript(self):

        # Grab the current format
        fmt = self.writer.text.currentCharFormat()

        # And get the vertical alignment property
        align = fmt.verticalAlignment()

        # Toggle the state
        if align == QtGui.QTextCharFormat.AlignNormal:
            fmt.setVerticalAlignment(QtGui.QTextCharFormat.AlignSubScript)
        else:
            fmt.setVerticalAlignment(QtGui.QTextCharFormat.AlignNormal)

        # Set the new format
        self.writer.text.setCurrentCharFormat(fmt)

    def alignLeft(self):
        self.writer.text.setAlignment(Qt.AlignLeft)

    def alignRight(self):
        self.writer.text.setAlignment(Qt.AlignRight)

    def alignCenter(self):
        self.writer.text.setAlignment(Qt.AlignCenter)

    def alignJustify(self):
        self.writer.text.setAlignment(Qt.AlignJustify)

    def indent(self):

        # Grab the cursor
        cursor = self.writer.text.textCursor()

        if cursor.hasSelection():

            # Store the current line/block number
            temp = cursor.blockNumber()

            # Move to the selection's end
            cursor.setPosition(cursor.anchor())

            # Calculate range of selection
            diff = cursor.blockNumber() - temp

            direction = QtGui.QTextCursor.Up if diff > 0 else QtGui.QTextCursor.Down

            # Iterate over lines (diff absolute value)
            for n in range(abs(diff) + 1):
                # Move to start of each line
                cursor.movePosition(QtGui.QTextCursor.StartOfLine)

                # Insert tabbing
                cursor.insertText("\t")

                # And move back up
                cursor.movePosition(direction)

        # If there is no selection, just insert a tab
        else:

            cursor.insertText("\t")

    def handleDedent(self, cursor):

        cursor.movePosition(QtGui.QTextCursor.StartOfLine)

        # Grab the current line
        line = cursor.block().text()

        # If the line starts with a tab character, delete it
        if line.startswith("\t"):

            # Delete next character
            cursor.deleteChar()

        # Otherwise, delete all spaces until a non-space character is met
        else:
            for char in line[:8]:

                if char != " ":
                    break

                cursor.deleteChar()

    def dedent(self):

        cursor = self.writer.text.textCursor()

        if cursor.hasSelection():

            # Store the current line/block number
            temp = cursor.blockNumber()

            # Move to the selection's last line
            cursor.setPosition(cursor.anchor())

            # Calculate range of selection
            diff = cursor.blockNumber() - temp

            direction = QtGui.QTextCursor.Up if diff > 0 else QtGui.QTextCursor.Down

            # Iterate over lines
            for n in range(abs(diff) + 1):
                self.handleDedent(cursor)

                # Move up
                cursor.movePosition(direction)

        else:
            self.handleDedent(cursor)

    def bulletList(self):

        cursor = self.writer.text.textCursor()

        # Insert bulleted list
        cursor.insertList(QtGui.QTextListFormat.ListDisc)

    def numberList(self):

        cursor = self.writer.text.textCursor()

        # Insert list with numbers
        cursor.insertList(QtGui.QTextListFormat.ListDecimal)
