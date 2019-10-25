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

from .label import Title
from .text import Description
from .button import PictureButtonFlat


class NotePreviewDescription(QtWidgets.QGroupBox):
    edit = QtCore.pyqtSignal(object)

    @inject.params(storage='storage')
    def __init__(self, index, storage):
        super(NotePreviewDescription, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setContentsMargins(0, 0, 0, 0)
        self.index = index

        self.layout = QtWidgets.QGridLayout()
        self.layout.setAlignment(Qt.AlignTop)

        title = Title(storage.fileName(index))
        self.layout.addWidget(title, 0, 0, 1, 27)

        description = Description(storage.fileContent(index))
        self.layout.addWidget(description, 1, 0, 4, 30)

        self.buttonEdit = PictureButtonFlat(QtGui.QIcon("icons/note"))
        self.buttonEdit.clicked.connect(lambda x: self.edit.emit(index))
        self.layout.addWidget(self.buttonEdit, 0, 29, 1, 1)

        self.setLayout(self.layout)

    def event(self, QEvent):
        if QEvent.type() == QtCore.QEvent.Enter:
            effect = QtWidgets.QGraphicsDropShadowEffect()
            effect.setColor(QtGui.QColor('#6cccfc'))
            effect.setBlurRadius(20)
            effect.setOffset(0)

            self.setGraphicsEffect(effect)
        if QEvent.type() == QtCore.QEvent.Leave:
            self.setGraphicsEffect(None)

        if QEvent.type() == QtCore.QEvent.MouseButtonRelease:
            self.edit.emit(self.index)
        return super(NotePreviewDescription, self).event(QEvent)
