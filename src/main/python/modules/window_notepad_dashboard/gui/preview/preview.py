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

from .button import PictureButtonFlat
from .text import Description
from .label import Title


class NotePreviewDescription(QtWidgets.QFrame):
    editAction = QtCore.pyqtSignal(object)
    fullscreenAction = QtCore.pyqtSignal(object)
    deleteAction = QtCore.pyqtSignal(object)
    cloneAction = QtCore.pyqtSignal(object)

    @inject.params(storage='storage')
    def __init__(self, index, storage):
        super(NotePreviewDescription, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setContentsMargins(0, 0, 0, 0)
        self.setFixedWidth(550)

        self.index = index

        self.layout = QtWidgets.QGridLayout()
        self.layout.setAlignment(Qt.AlignTop)

        title = Title(storage.fileName(index))
        self.layout.addWidget(title, 0, 0, 1, 30)

        self.description = Description(storage.fileContent(index))
        self.description.setFixedHeight(self.height() * 0.85)
        self.layout.addWidget(self.description, 1, 0, 20, 30)

        self.buttonClone = PictureButtonFlat(QtGui.QIcon("icons/copy"))
        self.buttonClone.clicked.connect(lambda x: self.cloneAction.emit(index))
        self.layout.addWidget(self.buttonClone, 1, 30)

        self.buttonDelete = PictureButtonFlat(QtGui.QIcon("icons/trash"))
        self.buttonDelete.clicked.connect(lambda x: self.deleteAction.emit(index))
        self.layout.addWidget(self.buttonDelete, 2, 30)

        self.setLayout(self.layout)

        effect = QtWidgets.QGraphicsDropShadowEffect()
        effect.setBlurRadius(10)
        effect.setOffset(0)
        self.setGraphicsEffect(effect)

    def document(self):
        return None

    def setDocument(self, document=None):
        return None

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

        if QEvent.type() == QtCore.QEvent.MouseButtonDblClick:
            self.fullscreenAction.emit((self.index, self.document()))

        if QEvent.type() == QtCore.QEvent.MouseButtonRelease:
            self.editAction.emit(self.index)

            effect = QtWidgets.QGraphicsDropShadowEffect()
            effect.setColor(QtGui.QColor('#6cccfc'))
            effect.setBlurRadius(20)
            effect.setOffset(0)

        return super(NotePreviewDescription, self).event(QEvent)

    def close(self):
        super(NotePreviewDescription, self).deleteLater()
        return super(NotePreviewDescription, self).close()
