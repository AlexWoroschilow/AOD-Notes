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
import os

from PyQt5 import QtGui
from PyQt5 import QtWidgets

from .header import WindowHeader
from .content import WindowContent


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        
        if os.path.exists('css/stylesheet.qss'):
            with open('css/stylesheet.qss') as stream:
                self.setStyleSheet(stream.read())

        if os.path.exists('icons/icon.svg'):
            icon = QtGui.QIcon('icons/icon.svg')
            self.setWindowIcon(icon)
        self.setWindowTitle('Cloud notepad')

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(WindowHeader(self))
        layout.addWidget(WindowContent(self))

        content = QtWidgets.QWidget()
        content.setLayout(layout)

        self.setCentralWidget(content)

