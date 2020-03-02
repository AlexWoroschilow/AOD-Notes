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
import pydux
import inject

from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from .preview import NotePreviewDescription


class NoteItem(QtWidgets.QListWidgetItem):

    def __init__(self, document=None):
        super(NoteItem, self).__init__()
        self.setSizeHint(QtCore.QSize(400, 550))
        self.setTextAlignment(Qt.AlignCenter)
        self.setData(0, document)


class PreviewScrollArea(QtWidgets.QListWidget):
    fullscreenNoteAction = QtCore.pyqtSignal(object)
    editNoteAction = QtCore.pyqtSignal(object)
    removeNoteAction = QtCore.pyqtSignal(object)
    cloneNoteAction = QtCore.pyqtSignal(object)

    def __init__(self, store=None, status=None):
        super(PreviewScrollArea, self).__init__()
        self.setDragEnabled(True)
        self.setViewMode(QtWidgets.QListView.IconMode)
        self.setResizeMode(QtWidgets.QListView.Adjust)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setMovement(QtWidgets.QListView.Static)

    def addItemRow(self, document):
        item = NoteItem(document)
        self.addItem(item)

        widget = NotePreviewDescription(document)
        self.setItemWidget(item, widget)

        widget.editNoteAction.connect(self.editNoteAction.emit)
        widget.fullscreenNoteAction.connect(self.fullscreenNoteAction.emit)
        widget.removeNoteAction.connect(self.removeNoteAction.emit)
        widget.cloneNoteAction.connect(self.cloneNoteAction.emit)

    def open(self, index_to_open=None):
        pass

    @inject.params(store='store')
    def itemClickedEvent(self, item, store=None):
        store.dispatch({
            'type': '@@app/storage/resource/selected/document',
            'entity': item.data(0)
        })
