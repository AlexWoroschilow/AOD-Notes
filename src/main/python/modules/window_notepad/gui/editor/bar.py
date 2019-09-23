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


class ToolBarButton(QtWidgets.QPushButton):
    activate = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        super(ToolBarButton, self).__init__(parent)
        self.setFlat(True)

    def connected(self):
        try:
            receiversCount = self.receivers(self.clicked)
            return receiversCount > 0
        except (SyntaxError, RuntimeError) as err:
            return False

    def event(self, QEvent):
        if QEvent.type() == QtCore.QEvent.Enter:
            effect = QtWidgets.QGraphicsDropShadowEffect()
            effect.setColor(QtGui.QColor('#6cccfc'))
            effect.setBlurRadius(10)
            effect.setOffset(0)

            self.setGraphicsEffect(effect)
        if QEvent.type() == QtCore.QEvent.Leave:
            self.setGraphicsEffect(None)

        if QEvent.type() == QtCore.QEvent.MouseButtonRelease:
            effect = QtWidgets.QGraphicsDropShadowEffect()
            effect.setColor(QtGui.QColor('#6cccfc'))
            effect.setBlurRadius(10)
            effect.setOffset(0)

        return super(ToolBarButton, self).event(QEvent)


class ToolbarBase(QtWidgets.QToolBar):

    def __init__(self):
        super(ToolbarBase, self).__init__()


class ToolbarWidgetLeft(ToolbarBase):

    def __init__(self):
        super(ToolbarWidgetLeft, self).__init__()
        self.setObjectName('editorToolbarWidgetLeft')
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.setContentsMargins(0, 0, 0, 0)
        self.setOrientation(Qt.Vertical)

        self.saveAction = ToolBarButton()
        self.saveAction.setIcon(QtGui.QIcon("icons/save"))
        self.saveAction.setToolTip("Save document")
        self.saveAction.setShortcut("Ctrl+S")

        self.printAction = ToolBarButton()
        self.printAction.setIcon(QtGui.QIcon("icons/print"))
        self.printAction.setToolTip("Print document")
        self.printAction.setShortcut("Ctrl+P")

        self.previewAction = ToolBarButton()
        self.previewAction.setIcon(QtGui.QIcon("icons/preview"))
        self.previewAction.setToolTip("Preview page before printing")
        self.previewAction.setShortcut("Ctrl+Shift+P")

        self.cutAction = ToolBarButton()
        self.cutAction.setIcon(QtGui.QIcon("icons/cut"))
        self.cutAction.setToolTip("Cut to clipboard")
        self.cutAction.setShortcut("Ctrl+X")

        self.copyAction = ToolBarButton()
        self.copyAction.setIcon(QtGui.QIcon("icons/copy"))
        self.copyAction.setToolTip("Copy text to clipboard")
        self.copyAction.setShortcut("Ctrl+C")

        self.pasteAction = ToolBarButton()
        self.pasteAction.setIcon(QtGui.QIcon("icons/paste"))
        self.pasteAction.setToolTip("Paste text from clipboard")
        self.pasteAction.setShortcut("Ctrl+V")

        self.undoAction = ToolBarButton()
        self.undoAction.setIcon(QtGui.QIcon("icons/undo"))
        self.undoAction.setToolTip("Undo last action")
        self.undoAction.setShortcut("Ctrl+Z")

        self.redoAction = ToolBarButton()
        self.redoAction.setIcon(QtGui.QIcon("icons/redo"))
        self.redoAction.setToolTip("Redo last undone thing")
        self.redoAction.setShortcut("Ctrl+Y")

        self.fullscreenAction = ToolBarButton()
        self.fullscreenAction.setIcon(QtGui.QIcon("icons/fullscreen"))
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


class ToolBarWidgetRight(ToolbarBase):

    def __init__(self):
        super(ToolBarWidgetRight, self).__init__()
        self.setObjectName('editorToolBarWidgetRight')
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        self.setOrientation(Qt.Vertical)
        self.setContentsMargins(0, 0, 0, 0)
        self.setMaximumWidth(35)

        self.boldAction = ToolBarButton()
        self.boldAction.setIcon(QtGui.QIcon("icons/bold"))
        self.boldAction.setToolTip("Bold")

        self.italicAction = ToolBarButton()
        self.italicAction.setIcon(QtGui.QIcon("icons/italic"))
        self.italicAction.setToolTip("Italic")

        self.underlAction = ToolBarButton()
        self.underlAction.setIcon(QtGui.QIcon("icons/underline"))
        self.underlAction.setToolTip("Underline")

        self.strikeAction = ToolBarButton()
        self.strikeAction.setIcon(QtGui.QIcon("icons/strike"))
        self.strikeAction.setToolTip("Strike-out")

        self.superAction = ToolBarButton()
        self.superAction.setIcon(QtGui.QIcon("icons/superscript"))
        self.superAction.setToolTip("Print document")

        self.subAction = ToolBarButton()
        self.subAction.setIcon(QtGui.QIcon("icons/subscript"))
        self.subAction.setToolTip("Subscript")

        self.fontColor = ToolBarButton()
        self.fontColor.setIcon(QtGui.QIcon("icons/font-color"))
        self.fontColor.setToolTip("Change font color")

        self.backColor = ToolBarButton()
        self.backColor.setIcon(QtGui.QIcon("icons/highlight"))
        self.backColor.setToolTip("Print background color")

        self.addWidget(self.boldAction)
        self.addWidget(self.italicAction)
        self.addWidget(self.underlAction)
        self.addWidget(self.strikeAction)
        self.addWidget(self.superAction)
        self.addWidget(self.subAction)
        self.addWidget(self.fontColor)
        self.addWidget(self.backColor)


class FormatbarWidget(ToolbarBase):

    def __init__(self):
        super(FormatbarWidget, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.setObjectName('editorFormatBarWidget')
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        self.fontSize = QtWidgets.QSpinBox(self)
        self.fontSize.setSuffix(" pt")
        self.fontSize.setValue(14)

        self.bulletAction = ToolBarButton()
        self.bulletAction.setIcon(QtGui.QIcon("icons/bullet"))
        self.bulletAction.setToolTip("Insert bullet List")

        self.numberedAction = ToolBarButton()
        self.numberedAction.setIcon(QtGui.QIcon("icons/number"))
        self.numberedAction.setToolTip("Insert numbered List")

        self.imageAction = ToolBarButton()
        self.imageAction.setIcon(QtGui.QIcon("icons/image"))
        self.imageAction.setToolTip("Insert image")

        self.alignLeft = ToolBarButton()
        self.alignLeft.setIcon(QtGui.QIcon("icons/align-left"))
        self.alignLeft.setToolTip("Align left")

        self.alignCenter = ToolBarButton()
        self.alignCenter.setIcon(QtGui.QIcon("icons/align-center"))
        self.alignCenter.setToolTip("Align center")

        self.alignRight = ToolBarButton()
        self.alignRight.setIcon(QtGui.QIcon("icons/align-right"))
        self.alignRight.setToolTip("Align right")

        self.alignJustify = ToolBarButton()
        self.alignJustify.setIcon(QtGui.QIcon("icons/align-justify"))
        self.alignJustify.setToolTip("Align justify")

        self.indentAction = ToolBarButton()
        self.indentAction.setIcon(QtGui.QIcon("icons/indent"))
        self.indentAction.setToolTip("Indent Area")

        self.dedentAction = ToolBarButton()
        self.dedentAction.setIcon(QtGui.QIcon("icons/outdent"))
        self.dedentAction.setToolTip("Dedent Area")

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
