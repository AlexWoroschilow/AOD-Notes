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


class Button(QtWidgets.QPushButton):

    def __init__(self, parent=None):
        super(Button, self).__init__(parent)
        self.setMaximumWidth(40)
        self.setFlat(True)


class NotePreviewDescription(QtWidgets.QGroupBox):
    edit = QtCore.pyqtSignal(object)
    delete = QtCore.pyqtSignal(object)
    clone = QtCore.pyqtSignal(object)

    @inject.params(storage='storage')
    def __init__(self, index, storage):
        super(NotePreviewDescription, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Expanding);
        self.setContentsMargins(0, 0, 0, 0)
        self.setObjectName('preview')

        self.layout = QtWidgets.QGridLayout()
        self.layout.setAlignment(Qt.AlignTop)

        title = Title(storage.fileName(index))
        self.layout.addWidget(title, 0, 0, 1, 27)

        description = Description(storage.fileContent(index))
        self.layout.addWidget(description, 1, 0, 4, 30)

        self.buttonEdit = Button()
        self.buttonEdit.setIcon(QtGui.QIcon("icons/file"))
        self.buttonEdit.clicked.connect(lambda x: self.edit.emit(index))

        self.layout.addWidget(self.buttonEdit, 0, 27, 1, 1)

        self.buttonClone = Button()
        self.buttonClone.setIcon(QtGui.QIcon("icons/copy"))
        self.buttonClone.clicked.connect(lambda x: self.clone.emit(index))
        self.layout.addWidget(self.buttonClone, 0, 28, 1, 1)

        self.buttonDelete = Button()
        self.buttonDelete.setIcon(QtGui.QIcon("icons/file-remove"))
        self.buttonDelete.clicked.connect(lambda x: self.delete.emit(index))
        self.layout.addWidget(self.buttonDelete, 0, 29, 1, 1)

        self.setLayout(self.layout)

        effect = QtWidgets.QGraphicsDropShadowEffect()
        effect.setBlurRadius(10)
        effect.setOffset(0)

        self.setGraphicsEffect(effect)


class Title(QtWidgets.QLabel):

    def __init__(self, text):
        super(Title, self).__init__(text)
        font = self.font()
        font.setPixelSize(20)
        self.setFont(font)
        self.setWordWrap(True)


class Description(QtWidgets.QTextEdit):

    def __init__(self, text=None):
        super(Description, self).__init__()
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setEnabled(False)
        self.setHtml(text)
        self.show()

    def resizeEvent(self, *args, **kwargs):
        document = self.document()
        if document is None: return None
        size = document.size()
        if size is None: return None

        self.setFixedHeight(size.height())
        return QtWidgets.QTextEdit.resizeEvent(self, *args, **kwargs)
