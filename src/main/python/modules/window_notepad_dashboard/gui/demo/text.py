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
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets


class DemoViewContainer(QtWidgets.QLabel):

    def __init__(self, parent=None):
        super(DemoViewContainer, self).__init__(parent)
        self.setWordWrap(True)

        with open('./template/hotkeys.html', 'r') as stream:
            self.setText(stream.read())


class TextView(QtWidgets.QScrollArea):

    def __init__(self, parent=None):
        super(TextView, self).__init__(parent)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setContentsMargins(0, 0, 0, 0)

        self.text = DemoViewContainer(self)
        self.setWidgetResizable(True)
        self.setWidget(self.text)
        
        self._entity = None

    def zoomIn(self, value):
        if self.text is None:
            return None
        self.text.zoomIn(value)
        
    def zoomOut(self, value):
        if self.text is None:
            return None
        self.text.zoomOut(value)
            
