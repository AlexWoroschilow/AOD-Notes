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
from .combo import FolderBomboBox


class ToolBarbarButton(QtWidgets.QPushButton):

    def __init__(self, parent=None, dispatcher=None):
        super(ToolBarbarButton, self).__init__()
        self.setIconSize(QtCore.QSize(20, 20))
        self.setFlat(True)


class ToolBarWidget(QtWidgets.QToolBar):

    @inject.params(kernel='kernel')
    def __init__(self, parent=None, kernel=None):
        super(ToolBarWidget, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.setOrientation(Qt.Vertical)
        self.setMaximumWidth(35)

        self.newAction = ToolBarbarButton()
        self.newAction.setIcon(QtGui.QIcon("icons/new.svg"))
        self.newAction.setToolTip("Create a new document.")
        self.newAction.setShortcut("Ctrl+N")

        self.copyAction = ToolBarbarButton()
        self.copyAction.setIcon(QtGui.QIcon("icons/copy.svg"))
        self.copyAction.setToolTip("Copy text to clipboard")

        self.removeAction = ToolBarbarButton()
        self.removeAction.setIcon(QtGui.QIcon("icons/remove.svg"))
        self.removeAction.setToolTip("Remove selected document")

        self.refreshAction = ToolBarbarButton()
        self.refreshAction.setIcon(QtGui.QIcon("icons/refresh.svg"))
        self.refreshAction.setToolTip("Refresh list")

        self.addWidget(self.newAction)
        self.addWidget(self.copyAction)
        self.addWidget(self.removeAction)
        self.addWidget(self.refreshAction)

        kernel.dispatch('window.notelist.toolbar', (
            parent, self
        ))


class ToolbarWidgetLeft(QtWidgets.QToolBar):

    @inject.params(kernel='kernel')
    def __init__(self, parent=None, kernel=None):
        super(ToolbarWidgetLeft, self).__init__()
        self.setObjectName('editorToolbarWidgetLeft')
        self.setContentsMargins(0, 0, 0, 0)
        self.setOrientation(Qt.Vertical)
        self.setMaximumWidth(35)

        self.saveAction = ToolBarbarButton()
        self.saveAction.setIcon(QtGui.QIcon("icons/save.svg"))
        self.saveAction.setToolTip("Save document")
        self.saveAction.setShortcut("Ctrl+S")

        self.printAction = ToolBarbarButton()
        self.printAction.setIcon(QtGui.QIcon("icons/print.svg"))
        self.printAction.setToolTip("Print document")
        self.printAction.setShortcut("Ctrl+P")

        self.previewAction = ToolBarbarButton()
        self.previewAction.setIcon(QtGui.QIcon("icons/preview.svg"))
        self.previewAction.setToolTip("Preview page before printing")
        self.previewAction.setShortcut("Ctrl+Shift+P")

        self.cutAction = ToolBarbarButton()
        self.cutAction.setIcon(QtGui.QIcon("icons/cut.svg"))
        self.cutAction.setToolTip("Cut to clipboard")
        self.cutAction.setShortcut("Ctrl+X")

        self.copyAction = ToolBarbarButton()
        self.copyAction.setIcon(QtGui.QIcon("icons/copy.svg"))
        self.copyAction.setToolTip("Copy text to clipboard")
        self.copyAction.setShortcut("Ctrl+C")

        self.pasteAction = ToolBarbarButton()
        self.pasteAction.setIcon(QtGui.QIcon("icons/paste.svg"))
        self.pasteAction.setToolTip("Paste text from clipboard")
        self.pasteAction.setShortcut("Ctrl+V")

        self.undoAction = ToolBarbarButton()
        self.undoAction.setIcon(QtGui.QIcon("icons/undo.svg"))
        self.undoAction.setToolTip("Undo last action")
        self.undoAction.setShortcut("Ctrl+Z")

        self.redoAction = ToolBarbarButton()
        self.redoAction.setIcon(QtGui.QIcon("icons/redo.svg"))
        self.redoAction.setToolTip("Redo last undone thing")
        self.redoAction.setShortcut("Ctrl+Y")

        self.fullscreenAction = ToolBarbarButton()
        self.fullscreenAction.setIcon(QtGui.QIcon("icons/fullscreen.svg"))
        self.fullscreenAction.setToolTip("Open editor in a new tab")

        self.addWidget(self.saveAction)
        self.addWidget(self.undoAction)
        self.addWidget(self.redoAction)
        self.addWidget(self.copyAction)
        self.addWidget(self.cutAction)
        self.addWidget(self.pasteAction)
        self.addWidget(self.printAction)
        self.addWidget(self.previewAction)
        self.addWidget(self.fullscreenAction)

        kernel.dispatch('window.notepad.leftbar', (
            parent, self
        ))


class ToolBarWidgetRight(QtWidgets.QToolBar):

    @inject.params(kernel='kernel')
    def __init__(self, parent=None, kernel=None):
        super(ToolBarWidgetRight, self).__init__()
        self.setObjectName('editorToolBarWidgetRight')
        self.setOrientation(Qt.Vertical)
        self.setContentsMargins(0, 0, 0, 0)
        self.setMaximumWidth(35)

        self.boldAction = ToolBarbarButton()
        self.boldAction.setIcon(QtGui.QIcon("icons/bold.svg"))
        self.boldAction.setToolTip("Bold")

        self.italicAction = ToolBarbarButton()
        self.italicAction.setIcon(QtGui.QIcon("icons/italic.svg"))
        self.italicAction.setToolTip("Italic")

        self.underlAction = ToolBarbarButton()
        self.underlAction.setIcon(QtGui.QIcon("icons/underline.svg"))
        self.underlAction.setToolTip("Underline")

        self.strikeAction = ToolBarbarButton()
        self.strikeAction.setIcon(QtGui.QIcon("icons/strike.svg"))
        self.strikeAction.setToolTip("Strike-out")

        self.superAction = ToolBarbarButton()
        self.superAction.setIcon(QtGui.QIcon("icons/superscript.svg"))
        self.superAction.setToolTip("Print document")

        self.subAction = ToolBarbarButton()
        self.subAction.setIcon(QtGui.QIcon("icons/subscript.svg"))
        self.subAction.setToolTip("Subscript")

        self.fontColor = ToolBarbarButton()
        self.fontColor.setIcon(QtGui.QIcon("icons/font-color.png"))
        self.fontColor.setToolTip("Change font color")

        self.backColor = ToolBarbarButton()
        self.backColor.setIcon(QtGui.QIcon("icons/highlight.png"))
        self.backColor.setToolTip("Print document")

        self.addWidget(self.boldAction)
        self.addWidget(self.italicAction)
        self.addWidget(self.underlAction)
        self.addWidget(self.strikeAction)
        self.addWidget(self.superAction)
        self.addWidget(self.subAction)
        self.addWidget(self.fontColor)
        self.addWidget(self.backColor)

        kernel.dispatch('window.notepad.rightbar', (
            parent, self
        ))


class FormatbarWidget(QtWidgets.QToolBar):

    @inject.params(kernel='kernel')
    def __init__(self, parent=None, kernel=None):
        super(FormatbarWidget, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.setObjectName('editorFormatBarWidget')

        self.folder = FolderBomboBox()

        self.fontSize = QtWidgets.QSpinBox(self)
        self.fontSize.setSuffix(" pt")
        self.fontSize.setValue(14)

        self.bulletAction = ToolBarbarButton()
        self.bulletAction.setIcon(QtGui.QIcon("icons/bullet.svg"))
        self.bulletAction.setToolTip("Insert bullet List")

        self.numberedAction = ToolBarbarButton()
        self.numberedAction.setIcon(QtGui.QIcon("icons/number.svg"))
        self.numberedAction.setToolTip("Insert numbered List")

        self.imageAction = ToolBarbarButton()
        self.imageAction.setIcon(QtGui.QIcon("icons/image.svg"))
        self.imageAction.setToolTip("Insert image")

        self.alignLeft = ToolBarbarButton()
        self.alignLeft.setIcon(QtGui.QIcon("icons/align-left.svg"))
        self.alignLeft.setToolTip("Align left")

        self.alignCenter = ToolBarbarButton()
        self.alignCenter.setIcon(QtGui.QIcon("icons/align-center.svg"))
        self.alignCenter.setToolTip("Align center")

        self.alignRight = ToolBarbarButton()
        self.alignRight.setIcon(QtGui.QIcon("icons/align-right.svg"))
        self.alignRight.setToolTip("Align right")

        self.alignJustify = ToolBarbarButton()
        self.alignJustify.setIcon(QtGui.QIcon("icons/align-justify.svg"))
        self.alignJustify.setToolTip("Align justify")

        self.indentAction = ToolBarbarButton()
        self.indentAction.setIcon(QtGui.QIcon("icons/indent.svg"))
        self.indentAction.setToolTip("Indent Area")

        self.dedentAction = ToolBarbarButton()
        self.dedentAction.setIcon(QtGui.QIcon("icons/outdent.svg"))
        self.dedentAction.setToolTip("Dedent Area")

        self.addWidget(self.folder)
        self.addWidget(self.fontSize)

        self.addWidget(self.alignLeft)
        self.addWidget(self.alignCenter)
        self.addWidget(self.alignRight)
        self.addWidget(self.alignJustify)

        self.addWidget(self.bulletAction)
        self.addWidget(self.numberedAction)

        self.addWidget(self.indentAction)
        self.addWidget(self.dedentAction)
        self.addWidget(self.imageAction)

        kernel.dispatch('window.notepad.formatbar', (
            parent, self
        ))

    def setFolder(self, value=None):
        self.folder.setFolder(int(value))
