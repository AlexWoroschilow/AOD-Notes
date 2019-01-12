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

from lib.widget.button import ToolBarButton


class Button(QtWidgets.QPushButton):

    def __init__(self, parent=None):
        super(Button, self).__init__(parent)
        self.setIconSize(QtCore.QSize(20, 20))
        self.setMaximumWidth(40)
        self.setFlat(True)


class NotePreviewDescription(QtWidgets.QWidget):

    edit = QtCore.pyqtSignal(object)
    delete = QtCore.pyqtSignal(object)
    clone = QtCore.pyqtSignal(object)

    @inject.params(storage='storage')
    def __init__(self, index, storage):
        super(NotePreviewDescription, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)

        self.layout = QtWidgets.QGridLayout()
        self.layout.setAlignment(Qt.AlignTop)

        title = Title(storage.fileName(index))
        self.layout.addWidget(title, 0, 0, 1, 20)

        description = Description(storage.fileContent(index))
        self.layout.addWidget(description, 1, 0, 4, 20)

        self.buttonEdit = Button()
        self.buttonEdit.setIcon(QtGui.QIcon("icons/file-light.svg"))
        self.buttonEdit.clicked.connect(lambda x: self.edit.emit(index))
        
        self.layout.addWidget(self.buttonEdit, 0, 18, 1, 1)

        self.buttonClone = Button()
        self.buttonClone.setIcon(QtGui.QIcon("icons/copy-light.svg"))
        self.buttonClone.clicked.connect(lambda x: self.clone.emit(index))
        self.layout.addWidget(self.buttonClone, 0, 19, 1, 1)

        self.buttonDelete = Button()
        self.buttonDelete.setIcon(QtGui.QIcon("icons/remove-light.svg"))
        self.buttonDelete.clicked.connect(lambda x: self.delete.emit(index))
        self.layout.addWidget(self.buttonDelete, 0, 20, 1, 1)

        self.setLayout(self.layout)


class Title(QtWidgets.QLabel):

    def __init__(self, text):
        super(Title, self).__init__(text)
        font = self.font()
        font.setPixelSize(20)
        self.setFont(font)
        self.setWordWrap(True)


class Description(QtWidgets.QLabel):

    def __init__(self, parent=None):
        super(Description, self).__init__(parent)
        self.setWordWrap(True)

