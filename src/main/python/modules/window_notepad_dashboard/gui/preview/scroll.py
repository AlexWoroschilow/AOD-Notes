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
from .widget import PreviewContainer


class PreviewScrollArea(QtWidgets.QScrollArea):
    edit = QtCore.pyqtSignal(object)
    delete = QtCore.pyqtSignal(object)
    fullscreen = QtCore.pyqtSignal(object)
    clone = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        super(PreviewScrollArea, self).__init__(parent)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)
        self.setMinimumWidth(400)

        self.hashmap_widgets = {}
        self.hashmap_positions = {}

        self.columns = self.getColumnNumber(self.size())
        self.container = PreviewContainer(self)
        self.setWidget(self.container)
        self.show()

    @inject.params(storage='storage')
    def open(self, collection=None, storage=None):
        if collection is None: return None
        self.hashmap_widgets = {}
        self.hashmap_positions = {}
        for position, index in enumerate(collection):
            path = storage.filePath(index)
            self.hashmap_positions[path] = (
                position, index
            )
        self.show()

    @inject.params(storage='storage')
    def getDocumentByIndex(self, index=None, storage=None):
        path = storage.filePath(index)
        if path not in self.hashmap_widgets.keys():
            return None
        widget = self.hashmap_widgets[path]
        return widget.document()

    def getColumnNumber(self, size=None):
        if size is None:
            return 1

        columns = round(size.width() / 600)
        return columns if columns > 0 else 1

    def resizeEvent(self, event):
        columns = self.getColumnNumber(event.size())
        if self.columns != columns and columns:
            self.columns = columns
            self.show()
        return super(PreviewScrollArea, self).resizeEvent(event)

    @inject.params(storage='storage')
    def scrollTo(self, event, storage):
        index, document = event
        path = storage.filePath(index)
        if path is None: return None

        scrollbar = self.verticalScrollBar()
        if path in self.hashmap_positions.keys():
            position, index = self.hashmap_positions[path]
            if position is None or position == 0:

                preview = self.hashmap_widgets[path]
                if preview is not None and index is not None:
                    preview.edit.emit((index, preview.document()))

                minimum = scrollbar.minimum()
                return scrollbar.setValue(minimum)

            total = len(self.hashmap_positions.keys())
            if total is not None and total > 0:

                preview = self.hashmap_widgets[path]
                if preview is not None and index is not None:
                    preview.edit.emit((index, preview.document()))

                maximum = scrollbar.maximum()
                position = position * maximum / (total - 1)
                return scrollbar.setValue(position)

    @inject.params(status='status', storage='storage')
    def show(self, status=None, storage=None):

        if not self.clear():
            return None

        for path in self.hashmap_positions.keys():
            position, index = self.hashmap_positions[path]

            preview = NotePreviewDescription(index)
            preview.fullscreen.connect(self.fullscreen.emit)
            preview.delete.connect(self.delete.emit)
            preview.clone.connect(self.clone.emit)
            preview.edit.connect(self.edit.emit)
            if self.columns is None or self.columns in [0, 1]:
                preview.setMinimumWidth(self.width() * 0.95)
            preview.setFixedHeight(500)

            i = math.floor(position / self.columns)
            j = math.floor(position % self.columns)

            self.container.layout().addWidget(preview, i, j)
            self.hashmap_widgets[path] = preview

        status.info('{} records found '.format(len(self.hashmap_widgets)))
        return super(PreviewScrollArea, self).show()

    def clear(self):
        layout = self.container.layout()
        for i in range(0, layout.count()):
            item = layout.itemAt(i)
            if item is None:
                layout.takeAt(i)

            widget = item.widget()
            if item is not None:
                widget.close()

        return True

    def close(self):
        super(PreviewScrollArea, self).deleteLater()
        return super(PreviewScrollArea, self).close()
