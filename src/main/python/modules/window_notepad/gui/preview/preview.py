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
    edit = QtCore.pyqtSignal(object)
    delete = QtCore.pyqtSignal(object)
    clone = QtCore.pyqtSignal(object)

    @inject.params(storage='storage')
    def __init__(self, index, storage):
        super(NotePreviewDescription, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setContentsMargins(0, 0, 0, 0)

        self.layout = QtWidgets.QGridLayout()
        self.layout.setAlignment(Qt.AlignTop)

        title = Title(storage.fileName(index))
        self.layout.addWidget(title, 0, 0, 1, 27)

        description = Description(storage.fileContent(index))
        self.layout.addWidget(description, 1, 0, 4, 30)

        self.buttonEdit = PictureButtonFlat(QtGui.QIcon("icons/note"))
        self.buttonEdit.clicked.connect(lambda x: self.edit.emit(index))

        self.layout.addWidget(self.buttonEdit, 0, 27, 1, 1)

        self.buttonClone = PictureButtonFlat(QtGui.QIcon("icons/copy"))
        self.buttonClone.clicked.connect(lambda x: self.clone.emit(index))
        self.layout.addWidget(self.buttonClone, 0, 28, 1, 1)

        self.buttonDelete = PictureButtonFlat(QtGui.QIcon("icons/trash"))
        self.buttonDelete.clicked.connect(lambda x: self.delete.emit(index))
        self.layout.addWidget(self.buttonDelete, 0, 29, 1, 1)

        self.setLayout(self.layout)

    def close(self):
        super(NotePreviewDescription, self).deleteLater()
        return super(NotePreviewDescription, self).close()
