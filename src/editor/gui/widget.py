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

from .text import TextEditor
from .text import NameEditor
from .text import TextWriter

from .bar import ToolbarbarWidgetLeft
from .bar import ToolbarbarWidgetRight
from .bar import FormatbarWidget


class TextEditorWidget(QtWidgets.QWidget):
    @inject.params(dispatcher='event_dispatcher', storage='storage')
    def __init__(self, parent=None, dispatcher=None, storage=None):
        """
        
        :param parent: 
        :param dispatcher: 
        """
        super(TextEditorWidget, self).__init__(parent)

        dispatcher.add_listener('window.notepad.note_update', self._onWindowNoteEdit)

        self.changesSaved = True
        self.filename = ""
        self._index = None

        self.setStyleSheet(''' QTextEdit{ border: none; }
            QLineEdit{ border: none; }''')

        self.name = NameEditor()

        self.writer = TextWriter(self)
        self.writer.text.cursorPositionChanged.connect(self.cursorPosition)
        self.writer.text.textChanged.connect(self.changed)

        self.leftbar = ToolbarbarWidgetLeft()
        self.leftbar.saveAction.triggered.connect(self._onSaveEvent)
        self.leftbar.printAction.triggered.connect(self.printHandler)
        self.leftbar.previewAction.triggered.connect(self.preview)
        self.leftbar.cutAction.triggered.connect(self.writer.text.cut)
        self.leftbar.copyAction.triggered.connect(self.writer.text.copy)
        self.leftbar.pasteAction.triggered.connect(self.writer.text.paste)
        self.leftbar.undoAction.triggered.connect(self.writer.text.undo)
        self.leftbar.redoAction.triggered.connect(self.writer.text.redo)
        self.leftbar.fullscreenAction.triggered.connect(self._onFullScreenEvent)

        dispatcher.dispatch('window.notepad.leftbar', (
            self.writer, self.leftbar
        ))

        self.formatbar = FormatbarWidget()
        self.formatbar.bulletAction.triggered.connect(self.bulletList)
        # self.formatbar.fontBox.currentFontChanged.connect(lambda font: self.writer.text.setCurrentFont(font))
        self.formatbar.fontSize.valueChanged.connect(lambda size: self.writer.text.setFontPointSize(size))
        self.formatbar.numberedAction.triggered.connect(self.numberList)
        self.formatbar.alignLeft.triggered.connect(self.alignLeft)
        self.formatbar.alignCenter.triggered.connect(self.alignCenter)
        self.formatbar.alignRight.triggered.connect(self.alignRight)
        self.formatbar.alignJustify.triggered.connect(self.alignJustify)
        self.formatbar.indentAction.triggered.connect(self.indent)
        self.formatbar.dedentAction.triggered.connect(self.dedent)
        self.formatbar.imageAction.triggered.connect(self.insertImage)

        dispatcher.dispatch('window.notepad.formatbar', (
            self.writer, self.formatbar
        ))

        self.rightbar = ToolbarbarWidgetRight()
        self.rightbar.italicAction.triggered.connect(self.italic)
        self.rightbar.boldAction.triggered.connect(self.bold)
        self.rightbar.strikeAction.triggered.connect(self.strike)
        self.rightbar.superAction.triggered.connect(self.superScript)
        self.rightbar.subAction.triggered.connect(self.subScript)
        self.rightbar.backColor.triggered.connect(self.highlight)

        dispatcher.dispatch('window.notepad.rightbar', (
            self.writer, self.rightbar
        ))

        self.statusbar = QtWidgets.QLabel()
        self.statusbar.setText("Words: 12, Characters: 120")

        # layout1.setSpacing(5)


        layout3 = QtWidgets.QVBoxLayout()
        layout3.addWidget(self.formatbar)
        layout3.addWidget(self.writer)

        widget3 = QtWidgets.QWidget()
        widget3.setLayout(layout3)

        layout2 = QtWidgets.QHBoxLayout()
        layout2.addWidget(widget3)
        layout2.addWidget(self.rightbar)

        widget2 = QtWidgets.QWidget()
        widget2.setLayout(layout2)

        layout1 = QtWidgets.QVBoxLayout()
        layout1.addWidget(self.name)
        layout1.addWidget(widget2)
        layout1.addWidget(self.statusbar)

        widget1 = QtWidgets.QWidget()
        widget1.setLayout(layout1)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.leftbar)
        layout.addWidget(widget1)

        self.setLayout(layout)

    @property
    def entity(self):
        """
        
        :return: 
        """
        return self._entity

    @inject.params(dispatcher='event_dispatcher')
    def _onFullScreenEvent(self, event=None, dispatcher=None):
        """
        
        :param event: 
        :param dispatcher: 
        :return: 
        """
        if self._entity is None or dispatcher is None:
            return None

        dispatcher.dispatch('window.notepad.note_tab', self._entity)

    @inject.params(storage='storage')
    def _onWindowNoteEdit(self, event=None, dispatcher=None, storage=None):
        """

        :param event: 
        :param dispatcher: 
        :return: 
        """
        if storage is None or event.data is None:
            return None

        entity = event.data
        if self._entity.index not in [entity.index]:
            return None

        if self.writer.text is None or self.name is None:
            return None

        self.name.setText(entity.name)
        self.writer.text.setText(entity.text)

    @inject.params(dispatcher='event_dispatcher')
    def _onSaveEvent(self, event=None, dispatcher=None):
        """

        :param dispatcher: 
        :return: 
        """
        if self._entity is not None and dispatcher is not None:
            self._entity.name = self.name.text()
            self._entity.text = self.writer.text.toHtml()
            dispatcher.dispatch('window.notepad.note_update', self._entity)

    def edit(self, entity=None):
        """
        
        :param index: 
        :param name: 
        :param text: 
        :return: 
        """
        self._entity = entity
        self.name.setText(entity.name)
        if entity.folder is not None:
            self.formatbar.setFolder(entity.folder)
        self.writer.text.setText(entity.text)

    def changed(self):
        """
        
        :return: 
        """
        self.changesSaved = False

    def cursorPosition(self):
        """
        
        :return: 
        """

        cursor = self.writer.text.textCursor()

        # Mortals like 1-indexed things
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber()

        self.statusbar.setText("Line: {} | Column: {}".format(line, col))

    def toggleToolbar(self):
        """
        
        :return: 
        """
        state = self.leftbar.isVisible()
        self.leftbar.setVisible(not state)

    def toggleFormatbar(self):
        """
        
        :return: 
        """

        state = self.formatbar.isVisible()
        self.formatbar.setVisible(not state)

    def toggleStatusbar(self):
        """
        
        :return: 
        """
        # state = self.statusbar.isVisible()
        # self.statusbar.setVisible(not state)

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

    def cursorPosition(self):

        cursor = self.writer.text.textCursor()

        # Mortals like 1-indexed things
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber()

        self.statusbar.setText("Line: {} | Column: {}".format(line, col))

    def wordCount(self):
        """
        
        :return: 
        """
        # wc = wordcount.WordCount(self)
        #
        # wc.getText()
        #
        # wc.show()

    def insertImage(self):

        # Get image file name
        # PYQT5 Returns a tuple in PyQt5
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Insert image', ".", "Images (*.png *.xpm *.jpg *.bmp *.gif)")[0]

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
