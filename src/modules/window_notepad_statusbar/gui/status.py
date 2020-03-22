#!/usr/bin/python3

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
from PyQt5.QtCore import Qt


class Status(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(Status, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)

        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.text = QtWidgets.QLabel('')
        self.addWidget(self.text)

        self.stack = []

    def error(self, text):
        text = '{}!'.format(text)
        self.text.setText(text)

    def info(self, text):
        self.stack.append(text)
        self.text.setText(text)

    def reset(self):
        pass

    def addWidget(self, widget):
        self.layout().addWidget(widget)
