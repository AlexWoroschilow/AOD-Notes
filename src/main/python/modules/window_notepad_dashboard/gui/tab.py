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
from PyQt5.QtCore import Qt
from PyQt5 import QtGui


class Notepad(QtWidgets.QTabWidget):

    def __init__(self):
        super(Notepad, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.setTabPosition(QtWidgets.QTabWidget.West)
        self.setTabsClosable(True)

    def event(self, event):
        if type(event) == QtGui.QKeyEvent:
            if event.key() == Qt.Key_Escape:
                index = self.currentIndex()
                if index is not None and index not in [0]:
                    widget = self.widget(index)
                    if widget is not None:
                        widget.close()
                    self.removeTab(index)

        return super(Notepad, self).event(event)

    def removeTab(self, p_int):
        inject.instance('status').reset()
        return super(Notepad, self).removeTab(p_int)

    def close(self):
        super(Notepad, self).deleteLater()
        return super(Notepad, self).close()
