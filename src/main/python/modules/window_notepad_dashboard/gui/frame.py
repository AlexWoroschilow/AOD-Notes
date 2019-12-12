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
from PyQt5 import QtWidgets


class NotepadDashboardTop(QtWidgets.QFrame):
    def __init__(self):
        super(NotepadDashboardTop, self).__init__()
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

    def addWidget(self, widget):
        self.layout().addWidget(widget)

    def clean(self):
        layout = self.layout()
        for i in range(0, layout.count()):
            item = layout.itemAt(i)
            if item is None:
                layout.takeAt(i)

            widget = item.widget()
            if item is not None:
                widget.close()


class NotepadDashboardLeft(QtWidgets.QFrame):
    def __init__(self):
        super(NotepadDashboardLeft, self).__init__()
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

    def addWidget(self, widget):
        self.layout().addWidget(widget)

    def clean(self):
        layout = self.layout()
        for i in range(0, layout.count()):
            item = layout.itemAt(i)
            if item is None:
                layout.takeAt(i)

            widget = item.widget()
            if item is not None:
                widget.close()


class NotepadDashboardRight(QtWidgets.QFrame):
    def __init__(self):
        super(NotepadDashboardRight, self).__init__()
        self.setLayout(QtWidgets.QVBoxLayout(self))
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

    def addWidget(self, widget):
        self.layout().addWidget(widget)

    def clean(self):
        layout = self.layout()
        for i in range(0, layout.count()):
            item = layout.itemAt(i)
            if item is None:
                layout.takeAt(i)

            widget = item.widget()
            if item is not None:
                widget.close()
