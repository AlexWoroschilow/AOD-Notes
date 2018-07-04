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


class LabelTop(QtWidgets.QLabel):

    def __init__(self, parent=None):
        super(LabelTop, self).__init__(parent)
        self.setObjectName('notesLabelTop')
        self.setMaximumHeight(50)
        self.setWordWrap(True)


class LabelBottom(QtWidgets.QLabel):

    def __init__(self, parent=None):
        super(LabelBottom, self).__init__(parent)
        self.setObjectName('notesLabelBottom')
        self.setMaximumHeight(20)


class LabelDescription(QtWidgets.QLabel):

    def __init__(self, parent=None):
        super(LabelDescription, self).__init__(parent)
        self.setObjectName('notesLabelDescription')
        self.setMaximumWidth(100)
        self.setMaximumHeight(80)
        self.setWordWrap(True)
        
    def setText(self, text=None):
        super(LabelDescription, self).setText(text)
        
