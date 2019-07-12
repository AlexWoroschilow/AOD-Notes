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
import math
import inject

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import Qt

from .preview import NotePreviewDescription


class PreviewContainer(QtWidgets.QWidget):
    edit = QtCore.pyqtSignal(object)
    delete = QtCore.pyqtSignal(object)
    clone = QtCore.pyqtSignal(object)

    def __init__(self, parent):
        super(PreviewContainer, self).__init__(parent)

        layout = QtWidgets.QGridLayout()
        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)

    def close(self):
        super(PreviewContainer, self).deleteLater()
        return super(PreviewContainer, self).close()


class PreviewScrollArea(QtWidgets.QScrollArea):
    edit = QtCore.pyqtSignal(object)
    delete = QtCore.pyqtSignal(object)
    clone = QtCore.pyqtSignal(object)
    columns = 1

    def __init__(self, parent, collection):
        super(PreviewScrollArea, self).__init__(parent)
        self.collection = collection

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        self.preview = PreviewContainer(self)
        self.preview.edit.connect(self.edit.emit)
        self.preview.delete.connect(self.delete.emit)
        self.preview.clone.connect(self.clone.emit)

        self.setWidget(self.preview)

        self.show()

    def resizeEvent(self, event):
        columns = round(event.size().width() / 600)
        if columns and self.columns != columns:
            self.columns = columns if columns > 0 else 1
            self.show()
        return super(PreviewScrollArea, self).resizeEvent(event)

    @inject.params(status='status')
    def show(self, status):

        layout = self.preview.layout()
        for i in range(0, layout.count()):
            item = layout.itemAt(i)
            if item is None: layout.takeAt(i)
            widget = item.widget()
            if item is not None: widget.close()

        for current, index in enumerate(self.collection):
            widget = NotePreviewDescription(index)
            widget.edit.connect(self.edit.emit)
            widget.delete.connect(self.delete.emit)
            widget.clone.connect(self.clone.emit)
            widget.setFixedHeight(500)

            i = math.floor(current / self.columns)
            j = math.floor(current % self.columns)
            self.preview.layout().addWidget(widget, i, j)

        status.info('{} notes found'.format(len(self.collection)))

        return super(PreviewScrollArea, self).show()

    def close(self):
        super(PreviewScrollArea, self).deleteLater()
        return super(PreviewScrollArea, self).close()
