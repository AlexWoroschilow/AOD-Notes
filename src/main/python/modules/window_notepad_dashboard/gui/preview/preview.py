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
    fullscreenNoteAction = QtCore.pyqtSignal(object)
    editNoteAction = QtCore.pyqtSignal(object)
    removeNoteAction = QtCore.pyqtSignal(object)
    cloneNoteAction = QtCore.pyqtSignal(object)

    def __init__(self, entity):
        super(NotePreviewDescription, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setContentsMargins(0, 0, 0, 0)
        self.setMaximumWidth(550)

        self.layout = QtWidgets.QGridLayout()
        self.layout.setAlignment(Qt.AlignTop)

        title = Title(entity.name)
        self.layout.addWidget(title, 0, 0, 1, 30)

        self.description = Description(entity.content)
        self.description.setFixedHeight(self.height() * 0.85)
        self.layout.addWidget(self.description, 1, 0, 20, 30)

        self.buttonClone = PictureButtonFlat(QtGui.QIcon("icons/copy"))
        self.buttonClone.clicked.connect(lambda x: self.cloneNoteAction.emit(entity))
        self.layout.addWidget(self.buttonClone, 1, 30)

        self.buttonDelete = PictureButtonFlat(QtGui.QIcon("icons/trash"))
        self.buttonDelete.clicked.connect(lambda x: self.removeNoteAction.emit(entity))
        self.layout.addWidget(self.buttonDelete, 2, 30)

        self.setLayout(self.layout)

        effect = QtWidgets.QGraphicsDropShadowEffect()
        effect.setBlurRadius(10)
        effect.setOffset(0)
        self.setGraphicsEffect(effect)

        self.entity = entity

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
            self.fullscreenNoteAction.emit(self.entity)

        if QEvent.type() == QtCore.QEvent.MouseButtonRelease:
            self.editNoteAction.emit(self.entity)

            effect = QtWidgets.QGraphicsDropShadowEffect()
            effect.setColor(QtGui.QColor('#6cccfc'))
            effect.setBlurRadius(20)
            effect.setOffset(0)

        return super(NotePreviewDescription, self).event(QEvent)

    def close(self):
        super(NotePreviewDescription, self).deleteLater()
        return super(NotePreviewDescription, self).close()
