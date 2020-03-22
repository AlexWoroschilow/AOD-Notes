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
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import Qt

from .text import TextEditor


class TextWriter(QtWidgets.QScrollArea):
    printAction = QtCore.pyqtSignal(object)
    previewAction = QtCore.pyqtSignal(object)
    cutAction = QtCore.pyqtSignal(object)
    copyAction = QtCore.pyqtSignal(object)
    pasteAction = QtCore.pyqtSignal(object)
    undoAction = QtCore.pyqtSignal(object)
    redoAction = QtCore.pyqtSignal(object)
    saveAction = QtCore.pyqtSignal(object)
    fullscreenAction = QtCore.pyqtSignal(object)
    fontSizeAction = QtCore.pyqtSignal(object)
    bulletAction = QtCore.pyqtSignal(object)
    numberedAction = QtCore.pyqtSignal(object)
    alignLeftAction = QtCore.pyqtSignal(object)
    alignCenterAction = QtCore.pyqtSignal(object)
    alignRightAction = QtCore.pyqtSignal(object)
    alignJustifyAction = QtCore.pyqtSignal(object)
    indentAction = QtCore.pyqtSignal(object)
    dedentAction = QtCore.pyqtSignal(object)
    imageAction = QtCore.pyqtSignal(object)
    italicAction = QtCore.pyqtSignal(object)
    superAction = QtCore.pyqtSignal(object)
    strikeAction = QtCore.pyqtSignal(object)
    fontColorAction = QtCore.pyqtSignal(object)
    backColorAction = QtCore.pyqtSignal(object)
    subAction = QtCore.pyqtSignal(object)
    boldAction = QtCore.pyqtSignal(object)
    underlAction = QtCore.pyqtSignal(object)

    def __init__(self, parent=None, editor=None):
        super(TextWriter, self).__init__(parent)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setAlignment(Qt.AlignHCenter)
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(20, 20, 20, 20)
        self.layout().setAlignment(Qt.AlignHCenter)

        self.text = TextEditor(self)
        self.printAction.connect(self.text.printEvent)
        self.previewAction.connect(self.text.previewEvent)
        self.cutAction.connect(self.text.cut)
        self.copyAction.connect(self.text.copy)
        self.pasteAction.connect(self.text.paste)
        self.undoAction.connect(self.text.undo)
        self.redoAction.connect(self.text.redo)

        self.bulletAction.connect(self.text.onActionBulletList)
        self.numberedAction.connect(self.text.onActionNumberList)
        self.alignLeftAction.connect(self.text.onActionAlignLeft)
        self.alignCenterAction.connect(self.text.onActionAlignCenter)
        self.alignRightAction.connect(self.text.onActionAlignRight)
        self.alignJustifyAction.connect(self.text.onActionAlignJustify)
        self.indentAction.connect(self.text.onActionIndent)
        self.dedentAction.connect(self.text.onActionDedent)
        self.imageAction.connect(self.text.imageInsertEvent)
        self.fontSizeAction.connect(self.text.setFontPointSize)

        self.italicAction.connect(self.text.onActionItalic)
        self.superAction.connect(self.text.onActionSuperScript)
        self.strikeAction.connect(self.text.onActionStrike)
        self.fontColorAction.connect(self.text.onActionFontColor)
        self.backColorAction.connect(self.text.onActionHighlight)
        self.subAction.connect(self.text.onActionSubScript)
        self.boldAction.connect(self.text.onActionBold)
        self.underlAction.connect(self.text.onActionUnderline)

        self.setWidgetResizable(True)
        self.layout().addWidget(self.text)

        self._entity = None

    def document(self):
        if self.text is not None:
            return self.text.document()
        return None

    def setDocument(self, document=None):
        if self.text is None: return None
        if document is None: return None

        document.setParent(self.text)
        self.text.setDocument(document)
        self.focus()

        return None

    def focus(self):
        if self.text is not None:
            self.text.setFocus()
        return self

    def zoomIn(self, value):
        if self.text is None:
            return None
        self.text.zoomIn(value)

    def zoomOut(self, value):
        if self.text is None:
            return None
        self.text.zoomOut(value)

    def html(self):
        return self.text.toHtml()
