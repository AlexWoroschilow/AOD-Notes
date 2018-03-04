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
from PyQt5.Qt import Qt
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtSvg


class ToolbarbarWidget(QtWidgets.QToolBar):
    def __init__(self):
        super(ToolbarbarWidget, self).__init__()
        self.setOrientation(Qt.Vertical)
        self.setContentsMargins(0, 0, 0, 0)

        self.saveAction = QtWidgets.QAction(QtGui.QIcon("icons/save.svg"), "Save", self)
        self.saveAction.setStatusTip("Save document")
        self.saveAction.setShortcut("Ctrl+S")

        self.savePdf = QtWidgets.QAction(QtGui.QIcon("icons/pdf.svg"), "Save as pdf", self)
        self.savePdf.setStatusTip("Export document as PDF")
        self.savePdf.setShortcut("Ctrl+Shift+P")

        self.printAction = QtWidgets.QAction(QtGui.QIcon("icons/print.svg"), "Print document", self)
        self.printAction.setStatusTip("Print document")
        self.printAction.setShortcut("Ctrl+P")

        self.previewAction = QtWidgets.QAction(QtGui.QIcon("icons/preview.svg"), "Page view", self)
        self.previewAction.setStatusTip("Preview page before printing")
        self.previewAction.setShortcut("Ctrl+Shift+P")

        self.cutAction = QtWidgets.QAction(QtGui.QIcon("icons/cut.svg"), "Cut to clipboard", self)
        self.cutAction.setStatusTip("Delete and copy text to clipboard")
        self.cutAction.setShortcut("Ctrl+X")

        self.copyAction = QtWidgets.QAction(QtGui.QIcon("icons/copy.svg"), "Copy to clipboard", self)
        self.copyAction.setStatusTip("Copy text to clipboard")
        self.copyAction.setShortcut("Ctrl+C")

        self.pasteAction = QtWidgets.QAction(QtGui.QIcon("icons/paste.svg"), "Paste from clipboard", self)
        self.pasteAction.setStatusTip("Paste text from clipboard")
        self.pasteAction.setShortcut("Ctrl+V")

        self.undoAction = QtWidgets.QAction(QtGui.QIcon("icons/undo.svg"), "Undo last action", self)
        self.undoAction.setStatusTip("Undo last action")
        self.undoAction.setShortcut("Ctrl+Z")

        self.redoAction = QtWidgets.QAction(QtGui.QIcon("icons/redo.svg"), "Redo last undone thing", self)
        self.redoAction.setStatusTip("Redo last undone thing")
        self.redoAction.setShortcut("Ctrl+Y")

        self.addAction(self.saveAction)
        self.addAction(self.savePdf)

        self.addSeparator()

        self.addAction(self.printAction)
        self.addAction(self.previewAction)

        self.addSeparator()

        self.addAction(self.cutAction)
        self.addAction(self.copyAction)
        self.addAction(self.pasteAction)
        self.addAction(self.undoAction)
        self.addAction(self.redoAction)

class FormatbarWidget(QtWidgets.QToolBar):
    def __init__(self):
        super(FormatbarWidget, self).__init__()
        self.setOrientation(Qt.Horizontal)
        self.setContentsMargins(0, 0, 0, 0)

        self.fontBox = QtWidgets.QFontComboBox(self)

        self.fontSize = QtWidgets.QSpinBox(self)

        # Will display " pt" after each value
        self.fontSize.setSuffix(" pt")

        self.fontSize.setValue(14)

        self.fontColor = QtWidgets.QAction(QtGui.QIcon("icons/font-color.png"), "Change font color", self)
        self.boldAction = QtWidgets.QAction(QtGui.QIcon("icons/bold.svg"), "Bold", self)
        self.italicAction = QtWidgets.QAction(QtGui.QIcon("icons/italic.svg"), "Italic", self)
        self.underlAction = QtWidgets.QAction(QtGui.QIcon("icons/underline.svg"), "Underline", self)
        self.strikeAction = QtWidgets.QAction(QtGui.QIcon("icons/strike.svg"), "Strike-out", self)
        self.superAction = QtWidgets.QAction(QtGui.QIcon("icons/superscript.svg"), "Superscript", self)
        self.subAction = QtWidgets.QAction(QtGui.QIcon("icons/subscript.svg"), "Subscript", self)
        self.backColor = QtWidgets.QAction(QtGui.QIcon("icons/highlight.png"), "Change background color", self)

        self.bulletAction = QtWidgets.QAction(QtGui.QIcon("icons/bullet.svg"), "Insert bullet List", self)
        self.bulletAction.setStatusTip("Insert bullet list")
        self.bulletAction.setShortcut("Ctrl+Shift+B")

        self.numberedAction = QtWidgets.QAction(QtGui.QIcon("icons/number.svg"), "Insert numbered List", self)
        self.numberedAction.setStatusTip("Insert numbered list")
        self.numberedAction.setShortcut("Ctrl+Shift+L")

        self.imageAction = QtWidgets.QAction(QtGui.QIcon("icons/image.svg"), "Insert image", self)
        self.imageAction.setStatusTip("Insert image")
        self.imageAction.setShortcut("Ctrl+Shift+I")

        self.alignLeft = QtWidgets.QAction(QtGui.QIcon("icons/align-left.svg"), "Align left", self)
        self.alignCenter = QtWidgets.QAction(QtGui.QIcon("icons/align-center.svg"), "Align center", self)
        self.alignRight = QtWidgets.QAction(QtGui.QIcon("icons/align-right.svg"), "Align right", self)
        self.alignJustify = QtWidgets.QAction(QtGui.QIcon("icons/align-justify.svg"), "Align justify", self)
        self.indentAction = QtWidgets.QAction(QtGui.QIcon("icons/indent.svg"), "Indent Area", self)
        self.indentAction.setShortcut("Ctrl+Tab")
        self.dedentAction = QtWidgets.QAction(QtGui.QIcon("icons/outdent.svg"), "Dedent Area", self)
        self.dedentAction.setShortcut("Shift+Tab")

        self.addWidget(self.fontBox)
        self.addWidget(self.fontSize)

        self.addSeparator()

        self.addAction(self.boldAction)
        self.addAction(self.italicAction)
        self.addAction(self.underlAction)
        self.addAction(self.strikeAction)

        self.addSeparator()

        self.addAction(self.bulletAction)
        self.addAction(self.numberedAction)

        self.addAction(self.alignLeft)
        self.addAction(self.alignCenter)
        self.addAction(self.alignRight)
        self.addAction(self.alignJustify)

        self.addAction(self.indentAction)
        self.addAction(self.dedentAction)

        self.addSeparator()

        self.addAction(self.superAction)
        self.addAction(self.subAction)

        self.addSeparator()

        self.addAction(self.imageAction)
        self.addAction(self.fontColor)
        self.addAction(self.backColor)
