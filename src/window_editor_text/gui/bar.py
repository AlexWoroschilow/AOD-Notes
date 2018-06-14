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

from lib.widget.button import ToolBarButton
from .combo import FolderComboBox


class ToolbarWidgetLeft(QtWidgets.QToolBar):

    @inject.params(kernel='kernel')
    def __init__(self, parent=None, kernel=None):
        super(ToolbarWidgetLeft, self).__init__()
        self.setObjectName('editorToolbarWidgetLeft')
        self.setContentsMargins(0, 0, 0, 0)
        self.setOrientation(Qt.Vertical)
        self.setMaximumWidth(35)

        self.saveAction = ToolBarButton()
        self.saveAction.setIcon(QtGui.QIcon("icons/save.svg"))
        self.saveAction.setToolTip("Save document")
        self.saveAction.setShortcut("Ctrl+S")

        self.printAction = ToolBarButton()
        self.printAction.setIcon(QtGui.QIcon("icons/print.svg"))
        self.printAction.setToolTip("Print document")
        self.printAction.setShortcut("Ctrl+P")

        self.previewAction = ToolBarButton()
        self.previewAction.setIcon(QtGui.QIcon("icons/preview.svg"))
        self.previewAction.setToolTip("Preview page before printing")
        self.previewAction.setShortcut("Ctrl+Shift+P")

        self.cutAction = ToolBarButton()
        self.cutAction.setIcon(QtGui.QIcon("icons/cut.svg"))
        self.cutAction.setToolTip("Cut to clipboard")
        self.cutAction.setShortcut("Ctrl+X")

        self.copyAction = ToolBarButton()
        self.copyAction.setIcon(QtGui.QIcon("icons/copy.svg"))
        self.copyAction.setToolTip("Copy text to clipboard")
        self.copyAction.setShortcut("Ctrl+C")

        self.pasteAction = ToolBarButton()
        self.pasteAction.setIcon(QtGui.QIcon("icons/paste.svg"))
        self.pasteAction.setToolTip("Paste text from clipboard")
        self.pasteAction.setShortcut("Ctrl+V")

        self.undoAction = ToolBarButton()
        self.undoAction.setIcon(QtGui.QIcon("icons/undo.svg"))
        self.undoAction.setToolTip("Undo last action")
        self.undoAction.setShortcut("Ctrl+Z")

        self.redoAction = ToolBarButton()
        self.redoAction.setIcon(QtGui.QIcon("icons/redo.svg"))
        self.redoAction.setToolTip("Redo last undone thing")
        self.redoAction.setShortcut("Ctrl+Y")

        self.fullscreenAction = ToolBarButton()
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

        self.boldAction = ToolBarButton()
        self.boldAction.setIcon(QtGui.QIcon("icons/bold.svg"))
        self.boldAction.setToolTip("Bold")

        self.italicAction = ToolBarButton()
        self.italicAction.setIcon(QtGui.QIcon("icons/italic.svg"))
        self.italicAction.setToolTip("Italic")

        self.underlAction = ToolBarButton()
        self.underlAction.setIcon(QtGui.QIcon("icons/underline.svg"))
        self.underlAction.setToolTip("Underline")

        self.strikeAction = ToolBarButton()
        self.strikeAction.setIcon(QtGui.QIcon("icons/strike.svg"))
        self.strikeAction.setToolTip("Strike-out")

        self.superAction = ToolBarButton()
        self.superAction.setIcon(QtGui.QIcon("icons/superscript.svg"))
        self.superAction.setToolTip("Print document")

        self.subAction = ToolBarButton()
        self.subAction.setIcon(QtGui.QIcon("icons/subscript.svg"))
        self.subAction.setToolTip("Subscript")

        self.fontColor = ToolBarButton()
        self.fontColor.setIcon(QtGui.QIcon("icons/font-color.png"))
        self.fontColor.setToolTip("Change font color")

        self.backColor = ToolBarButton()
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

        self.folderSelector = FolderComboBox()

        self.fontSize = QtWidgets.QSpinBox(self)
        self.fontSize.setSuffix(" pt")
        self.fontSize.setValue(14)

        self.bulletAction = ToolBarButton()
        self.bulletAction.setIcon(QtGui.QIcon("icons/bullet.svg"))
        self.bulletAction.setToolTip("Insert bullet List")

        self.numberedAction = ToolBarButton()
        self.numberedAction.setIcon(QtGui.QIcon("icons/number.svg"))
        self.numberedAction.setToolTip("Insert numbered List")

        self.imageAction = ToolBarButton()
        self.imageAction.setIcon(QtGui.QIcon("icons/image.svg"))
        self.imageAction.setToolTip("Insert image")

        self.alignLeft = ToolBarButton()
        self.alignLeft.setIcon(QtGui.QIcon("icons/align-left.svg"))
        self.alignLeft.setToolTip("Align left")

        self.alignCenter = ToolBarButton()
        self.alignCenter.setIcon(QtGui.QIcon("icons/align-center.svg"))
        self.alignCenter.setToolTip("Align center")

        self.alignRight = ToolBarButton()
        self.alignRight.setIcon(QtGui.QIcon("icons/align-right.svg"))
        self.alignRight.setToolTip("Align right")

        self.alignJustify = ToolBarButton()
        self.alignJustify.setIcon(QtGui.QIcon("icons/align-justify.svg"))
        self.alignJustify.setToolTip("Align justify")

        self.indentAction = ToolBarButton()
        self.indentAction.setIcon(QtGui.QIcon("icons/indent.svg"))
        self.indentAction.setToolTip("Indent Area")

        self.dedentAction = ToolBarButton()
        self.dedentAction.setIcon(QtGui.QIcon("icons/outdent.svg"))
        self.dedentAction.setToolTip("Dedent Area")

        self.addWidget(self.folderSelector)
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

    @property
    def folder(self):
        if self.folderSelector is None:
            return None
        return self.folderSelector.entity

    @folder.setter
    def folder(self, entity=None):
        if self.folderSelector is None or entity is None:
            return None
        self.folderSelector.entity = entity

