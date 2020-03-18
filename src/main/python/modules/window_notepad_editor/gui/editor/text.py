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
import os
import inject

from PyQt5.QtCore import Qt
from PyQt5 import QtPrintSupport
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui

from .menu.action import ImageResizeAction


class TextEditor(QtWidgets.QTextEdit):
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

    def __init__(self, parent=None):
        super(TextEditor, self).__init__(parent)
        self.setWordWrapMode(QtGui.QTextOption.WordWrap)
        self.setContentsMargins(0, 0, 0, 0)
        self.setMinimumWidth(500)

        self.setAcceptRichText(True)
        self.setAcceptDrops(True)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self._entity = None

        effect = QtWidgets.QGraphicsDropShadowEffect()
        effect.setBlurRadius(10)
        effect.setOffset(0)

        self.setGraphicsEffect(effect)

        self.printAction.connect(self.printEvent)
        self.previewAction.connect(self.previewEvent)
        self.cutAction.connect(self.cut)
        self.copyAction.connect(self.copy)
        self.pasteAction.connect(self.paste)
        self.undoAction.connect(self.undo)
        self.redoAction.connect(self.redo)

        self.bulletAction.connect(self.onActionBulletList)
        self.numberedAction.connect(self.onActionNumberList)
        self.alignLeftAction.connect(self.onActionAlignLeft)
        self.alignCenterAction.connect(self.onActionAlignCenter)
        self.alignRightAction.connect(self.onActionAlignRight)
        self.alignJustifyAction.connect(self.onActionAlignJustify)
        self.indentAction.connect(self.onActionIndent)
        self.dedentAction.connect(self.onActionDedent)
        self.imageAction.connect(self.imageInsertEvent)
        self.fontSizeAction.connect(self.setFontPointSize)

        self.italicAction.connect(self.onActionItalic)
        self.superAction.connect(self.onActionSuperScript)
        self.strikeAction.connect(self.onActionStrike)
        self.fontColorAction.connect(self.onActionFontColor)
        self.backColorAction.connect(self.onActionHighlight)
        self.subAction.connect(self.onActionSubScript)
        self.boldAction.connect(self.onActionBold)
        self.underlAction.connect(self.onActionUnderline)

        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+e"), self)
        shortcut.activatedAmbiguously.connect(self.setFocus)
        shortcut.activated.connect(self.setFocus)
        shortcut.setEnabled(True)

    @property
    def entity(self):
        return self._entity

    @entity.setter
    def entity(self, value):
        self.entity = value

    def onActionFontColor(self):
        self.setTextColor(QtWidgets.QColorDialog.getColor())

    def onActionHighlight(self):
        color = QtWidgets.QColorDialog.getColor()
        self.setTextBackgroundColor(color)

    def onActionBold(self):
        if self.fontWeight() == QtGui.QFont.Bold:
            return self.setFontWeight(QtGui.QFont.Normal)
        return self.setFontWeight(QtGui.QFont.Bold)

    def onActionItalic(self):
        state = self.fontItalic()
        self.setFontItalic(not state)

    def onActionUnderline(self):
        state = self.fontUnderline()
        self.setFontUnderline(not state)

    def onActionStrike(self):
        fmt = self.currentCharFormat()
        fmt.setFontStrikeOut(not fmt.fontStrikeOut())
        self.setCurrentCharFormat(fmt)

    def onActionSuperScript(self):
        fmt = self.currentCharFormat()
        align = fmt.verticalAlignment()
        if align == QtGui.QTextCharFormat.AlignNormal:
            fmt.setVerticalAlignment(QtGui.QTextCharFormat.AlignSuperScript)
        else:
            fmt.setVerticalAlignment(QtGui.QTextCharFormat.AlignNormal)
        self.setCurrentCharFormat(fmt)

    def onActionSubScript(self):
        fmt = self.currentCharFormat()
        align = fmt.verticalAlignment()
        if align == QtGui.QTextCharFormat.AlignNormal:
            fmt.setVerticalAlignment(QtGui.QTextCharFormat.AlignSubScript)
        else:
            fmt.setVerticalAlignment(QtGui.QTextCharFormat.AlignNormal)
        self.setCurrentCharFormat(fmt)

    def onActionIndent(self):
        cursor = self.textCursor()
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
        cursor = self.textCursor()
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

    def onActionAlignLeft(self):
        self.setAlignment(Qt.AlignLeft)

    def onActionAlignRight(self):
        self.setAlignment(Qt.AlignRight)

    def onActionAlignCenter(self):
        self.setAlignment(Qt.AlignCenter)

    def onActionAlignJustify(self):
        self.setAlignment(Qt.AlignJustify)

    def onActionBulletList(self):
        cursor = self.textCursor()
        cursor.insertList(QtGui.QTextListFormat.ListDisc)

    def onActionNumberList(self):
        cursor = self.textCursor()
        cursor.insertList(QtGui.QTextListFormat.ListDecimal)

    def previewEvent(self):
        preview = QtPrintSupport.QPrintPreviewDialog()
        preview.paintRequested.connect(lambda p: self.print_(p))
        preview.exec_()

    def printEvent(self):
        dialog = QtPrintSupport.QPrintDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.document().print_(dialog.printer())

    def resizeImageEvent(self, size):
        cursor = self.textCursor()
        iterator = cursor.block().begin()
        while not iterator.atEnd():

            fragment = iterator.fragment()
            if fragment is None: break

            if not fragment.isValid() or not fragment.charFormat().isImageFormat():
                continue

            width, height = size
            if height is None: break
            if width is None: break

            image = fragment.charFormat().toImageFormat()
            if image is None: break

            image.setWidth(width)
            image.setHeight(height)

            cursor.setPosition(fragment.position())
            cursor.setPosition(fragment.position() + fragment.length(), QtGui.QTextCursor.KeepAnchor)
            cursor.setCharFormat(image)
            break

            iterator += 1

    def mouseDoubleClickEvent(self, event):
        cursor = self.textCursor()
        iterator = cursor.block().begin()

        while not iterator.atEnd():
            fragment = iterator.fragment()
            if not fragment.isValid(): break

            if fragment.charFormat().isImageFormat():

                image = fragment.charFormat().toImageFormat()
                if image is None: break

                width = 800 if not image.width() else image.width()
                if width is None: break

                popup = ImageResizeAction(self, image.name(), width)
                popup.sizeChanged.connect(self.resizeImageEvent)

                menu = QtWidgets.QMenu()
                menu.addAction(popup)
                menu.setFocus()
                menu.exec_(QtGui.QCursor.pos())

            iterator += 1

        return super(TextEditor, self).mouseDoubleClickEvent(event)

    @inject.params(config='config')
    def imageInsertEvent(self, event, config=None):

        title = 'Insert image'
        formats = "Images (*.png *.xpm *.jpg *.bmp *.gif)"

        folder = config.get('editor.import_image', os.path.expanduser('~'))
        filename, formats = QtWidgets.QFileDialog.getOpenFileName(self, title, folder, formats)
        if filename is None: return None

        image = QtGui.QImage(filename)
        if image.isNull(): return None

        cursor = self.textCursor()
        cursor.insertImage(image.scaled(800, 600, Qt.KeepAspectRatio), filename)
        config.set('editor.import_image', os.path.dirname(filename))

        popup = ImageResizeAction(self, filename, 800)
        popup.sizeChanged.connect(self.resizeImageEvent)

        menu = QtWidgets.QMenu()
        menu.addAction(popup)
        menu.exec_(QtGui.QCursor.pos())

    def wheelEvent(self, event):
        point = event.angleDelta()
        if event.modifiers() == QtCore.Qt.ControlModifier:
            if point.y() > 0:
                self.zoomIn(5)
            if point.y() < 0:
                self.zoomOut(5)
        return super(TextEditor, self).wheelEvent(event)

    def event(self, QEvent):
        if QEvent.type() == QtCore.QEvent.Enter:
            effect = QtWidgets.QGraphicsDropShadowEffect()
            effect.setColor(QtGui.QColor('#6cccfc'))
            effect.setBlurRadius(20)
            effect.setOffset(0)

            self.setGraphicsEffect(effect)
        if QEvent.type() == QtCore.QEvent.Leave:
            effect = QtWidgets.QGraphicsDropShadowEffect()
            effect.setBlurRadius(10)
            effect.setOffset(0)
            self.setGraphicsEffect(effect)

        if QEvent.type() == QtCore.QEvent.MouseButtonRelease:
            effect = QtWidgets.QGraphicsDropShadowEffect()
            effect.setColor(QtGui.QColor('#6cccfc'))
            effect.setBlurRadius(20)
            effect.setOffset(0)

        return super(TextEditor, self).event(QEvent)

    def close(self):
        super(TextEditor, self).deleteLater()
        return super(TextEditor, self).close()
