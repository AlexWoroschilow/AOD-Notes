# -*- coding: utf-8 -*-

# PYQT5 PyQt4’s QtGui module has been split into PyQt5’s QtGui, QtPrintSupport and QtWidgets modules
import inject
from PyQt5.QtCore import Qt

from PyQt5 import QtGui
from PyQt5 import QtPrintSupport
from PyQt5 import QtWidgets
from .bar import ToolbarbarWidget, FormatbarWidget


# PYQT5 QMainWindow, QApplication, QAction, QFontComboBox, QSpinBox, QTextEdit, QMessageBox
# PYQT5 QFileDialog, QColorDialog, QDialog
# PYQT5 QPrintPreviewDialog, QPrintDialog

class TextEditorName(QtWidgets.QLineEdit):
    def __init__(self, parent=None):
        """

        :param parent: 
        """
        super(TextEditorName, self).__init__(parent)
        self.setPlaceholderText('Write a title here...')
        self.setClearButtonEnabled(True)

        font = self.font()
        font.setPixelSize(24)
        self.setFont(font)


class TextEditor(QtWidgets.QWidget):
    @inject.params(dispatcher='event_dispatcher', storage='storage')
    def __init__(self, parent=None, dispatcher=None, storage=None):
        """
        
        :param parent: 
        :param dispatcher: 
        """
        super(TextEditor, self).__init__(parent)
        dispatcher.add_listener('window.notepad.note_update', self._onWindowNoteEdit)

        self.changesSaved = True
        self.filename = ""
        self._index = None

        self.setStyleSheet(''' QTextEdit{ border: none; }
            QLineEdit{ border: none; }''')

        self.name = TextEditorName()

        self.text = QtWidgets.QTextEdit(self)
        self.text.textChanged.connect(self.changed)
        self.text.cursorPositionChanged.connect(self.cursorPosition)
        self.text.setTabStopWidth(33)

        self.toolbar = ToolbarbarWidget()
        self.toolbar.saveAction.triggered.connect(self._onSaveEvent)
        self.toolbar.printAction.triggered.connect(self.printHandler)
        self.toolbar.previewAction.triggered.connect(self.preview)
        self.toolbar.cutAction.triggered.connect(self.text.cut)
        self.toolbar.copyAction.triggered.connect(self.text.copy)
        self.toolbar.pasteAction.triggered.connect(self.text.paste)
        self.toolbar.undoAction.triggered.connect(self.text.undo)
        self.toolbar.redoAction.triggered.connect(self.text.redo)
        self.toolbar.fullscreenAction.triggered.connect(self._onFullScreenEvent)

        self.formatbar = FormatbarWidget()
        self.formatbar.fontColor.triggered.connect(self.fontColorChanged)
        self.formatbar.fontBox.currentFontChanged.connect(lambda font: self.text.setCurrentFont(font))
        self.formatbar.fontSize.valueChanged.connect(lambda size: self.text.setFontPointSize(size))
        self.formatbar.underlAction.triggered.connect(self.underline)
        self.formatbar.italicAction.triggered.connect(self.italic)
        self.formatbar.boldAction.triggered.connect(self.bold)
        self.formatbar.strikeAction.triggered.connect(self.strike)
        self.formatbar.superAction.triggered.connect(self.superScript)
        self.formatbar.subAction.triggered.connect(self.subScript)
        self.formatbar.backColor.triggered.connect(self.highlight)
        self.formatbar.bulletAction.triggered.connect(self.bulletList)
        self.formatbar.numberedAction.triggered.connect(self.numberList)
        self.formatbar.alignLeft.triggered.connect(self.alignLeft)
        self.formatbar.alignCenter.triggered.connect(self.alignCenter)
        self.formatbar.alignRight.triggered.connect(self.alignRight)
        self.formatbar.alignJustify.triggered.connect(self.alignJustify)
        self.formatbar.indentAction.triggered.connect(self.indent)
        self.formatbar.dedentAction.triggered.connect(self.dedent)
        self.formatbar.imageAction.triggered.connect(self.insertImage)

        layout1 = QtWidgets.QVBoxLayout()
        layout1.setSpacing(5)

        self.statusbar = QtWidgets.QLabel()
        self.statusbar.setText("Words: 12, Characters: 120")

        layout1.addWidget(self.name)
        layout1.addWidget(self.formatbar)
        layout1.addWidget(self.text)
        layout1.addWidget(self.statusbar)

        widget = QtWidgets.QWidget()
        widget.setLayout(layout1)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(widget)

        self.setLayout(layout)

    @inject.params(dispatcher='event_dispatcher')
    def _onFullScreenEvent(self, event=None, dispatcher=None):
        """
        
        :param event: 
        :param dispatcher: 
        :return: 
        """
        if dispatcher is None:
            return None

        dispatcher.dispatch('window.notepad.note_tab', (
            self._index, self.name.text(), self.text.toHtml()
        ))

    @inject.params(storage='storage')
    def _onWindowNoteEdit(self, event=None, dispatcher=None, storage=None):
        """

        :param event: 
        :param dispatcher: 
        :return: 
        """
        if storage is None:
            return None

        if event.data is None:
            return None

        index, name, text = event.data
        if self._index not in [index]:
            return None

        if self.name is None:
            return None

        if self.text is None:
            return None

        self.name.setText(name)
        self.text.setText(text)

    @inject.params(dispatcher='event_dispatcher')
    def _onSaveEvent(self, event=None, dispatcher=None):
        """

        :param dispatcher: 
        :return: 
        """
        dispatcher.dispatch('window.notepad.note_update', (
            self._index, self.name.text(), self.text.toHtml()
        ))

    def edit(self, index=None, name=None, text=None):
        """
        
        :param index: 
        :param name: 
        :param text: 
        :return: 
        """
        self._index = index
        self.name.setText(name)
        self.text.setText(text)

    def changed(self):
        """
        
        :return: 
        """
        self.changesSaved = False

    def cursorPosition(self):
        """
        
        :return: 
        """

        cursor = self.text.textCursor()

        # Mortals like 1-indexed things
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber()

        self.statusbar.setText("Line: {} | Column: {}".format(line, col))

    def toggleToolbar(self):
        """
        
        :return: 
        """
        state = self.toolbar.isVisible()
        self.toolbar.setVisible(not state)

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
        preview.paintRequested.connect(lambda p: self.text.print_(p))

        preview.exec_()

    def printHandler(self):

        # Open printing dialog
        dialog = QtPrintSupport.QPrintDialog()

        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.text.document().print_(dialog.printer())

    def cursorPosition(self):

        cursor = self.text.textCursor()

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

                cursor = self.text.textCursor()

                cursor.insertImage(image, filename)

    def fontColorChanged(self):

        # Get a color from the text dialog
        color = QtWidgets.QColorDialog.getColor()

        # Set it as the new text color
        self.text.setTextColor(color)

    def highlight(self):

        color = QtWidgets.QColorDialog.getColor()

        self.text.setTextBackgroundColor(color)

    def bold(self):

        if self.text.fontWeight() == QtGui.QFont.Bold:

            self.text.setFontWeight(QtGui.QFont.Normal)

        else:

            self.text.setFontWeight(QtGui.QFont.Bold)

    def italic(self):

        state = self.text.fontItalic()

        self.text.setFontItalic(not state)

    def underline(self):

        state = self.text.fontUnderline()

        self.text.setFontUnderline(not state)

    def strike(self):

        # Grab the text's format
        fmt = self.text.currentCharFormat()

        # Set the fontStrikeOut property to its opposite
        fmt.setFontStrikeOut(not fmt.fontStrikeOut())

        # And set the next char format
        self.text.setCurrentCharFormat(fmt)

    def superScript(self):

        # Grab the current format
        fmt = self.text.currentCharFormat()

        # And get the vertical alignment property
        align = fmt.verticalAlignment()

        # Toggle the state
        if align == QtGui.QTextCharFormat.AlignNormal:

            fmt.setVerticalAlignment(QtGui.QTextCharFormat.AlignSuperScript)

        else:

            fmt.setVerticalAlignment(QtGui.QTextCharFormat.AlignNormal)

        # Set the new format
        self.text.setCurrentCharFormat(fmt)

    def subScript(self):

        # Grab the current format
        fmt = self.text.currentCharFormat()

        # And get the vertical alignment property
        align = fmt.verticalAlignment()

        # Toggle the state
        if align == QtGui.QTextCharFormat.AlignNormal:

            fmt.setVerticalAlignment(QtGui.QTextCharFormat.AlignSubScript)

        else:

            fmt.setVerticalAlignment(QtGui.QTextCharFormat.AlignNormal)

        # Set the new format
        self.text.setCurrentCharFormat(fmt)

    def alignLeft(self):
        self.text.setAlignment(Qt.AlignLeft)

    def alignRight(self):
        self.text.setAlignment(Qt.AlignRight)

    def alignCenter(self):
        self.text.setAlignment(Qt.AlignCenter)

    def alignJustify(self):
        self.text.setAlignment(Qt.AlignJustify)

    def indent(self):

        # Grab the cursor
        cursor = self.text.textCursor()

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

        cursor = self.text.textCursor()

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

        cursor = self.text.textCursor()

        # Insert bulleted list
        cursor.insertList(QtGui.QTextListFormat.ListDisc)

    def numberList(self):

        cursor = self.text.textCursor()

        # Insert list with numbers
        cursor.insertList(QtGui.QTextListFormat.ListDecimal)
