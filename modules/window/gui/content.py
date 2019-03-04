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

from PyQt5 import QtWidgets


class WindowContentDashboard(QtWidgets.QWidget):

    @inject.params(notepad='notepad')
    def __init__(self, parent=None, notepad=None):
        super(WindowContentDashboard, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setObjectName('dashboard')
        
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.content = QtWidgets.QSplitter()
        self.content.setContentsMargins(0, 0, 0, 0)
        self.content.addWidget(notepad)

        layout.addWidget(self.content)

        self.setLayout(layout)


class WindowContent(QtWidgets.QTabWidget):

    def __init__(self, parent=None):
        super(WindowContent, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setTabPosition(QtWidgets.QTabWidget.West)
        self.addTab(WindowContentDashboard(parent), self.tr('Dashboard'))
        self.setTabsClosable(True)
