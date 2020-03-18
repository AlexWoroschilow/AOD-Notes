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
import inject

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore


class MainWindow(QtWidgets.QMainWindow):
    newTabAction = QtCore.pyqtSignal(object)
    switchTabAction = QtCore.pyqtSignal(object)
    resize = QtCore.pyqtSignal(object)

    @inject.params(themes='themes')
    def __init__(self, parent=None, themes=None):
        self.content = None

        super(MainWindow, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setWindowTitle('AOD - Notepad')
        self.setStyleSheet(themes.get_stylesheet())

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.container = QtWidgets.QWidget()
        self.container.setLayout(layout)

        self.setCentralWidget(self.container)

        if not os.path.exists('icons/icon.svg'): return None
        self.setWindowIcon(QtGui.QIcon('icons/icon.svg'))

        self.switchTabAction.connect(self.onActionSwitchTab)
        self.newTabAction.connect(self.onActionNewTab)

    def resizeEvent(self, event):
        self.resize.emit(event)

    def clean(self):
        layout = self.container.layout()
        for i in range(0, layout.count()):
            item = layout.itemAt(i)
            if item is not None:
                widget = item.widget()
                if widget is not None:
                    widget.close()
            layout.takeAt(i)
        return True

    def setMainWidget(self, widget=None):

        if not self.clean():
            return None

        self.content = widget
        if hasattr(self.content, 'tabCloseRequested'):
            self.content.tabCloseRequested.connect(self.onActionTabClose)

        layout = self.container.layout()
        layout.addWidget(self.content)

    def onActionSwitchTab(self, index=None):
        if index is None: return None
        self.content.setCurrentIndex(index)

    def onActionNewTab(self, event=None):
        if event is None: return None
        widget, name = event
        if widget is None: return None
        if name is None: return None

        self.content.addTab(widget, name)
        index = self.content.indexOf(widget)
        if index is None: return None
        self.content.setCurrentIndex(index)

    def onActionTabClose(self, index=None):
        # Do not close the first one tab
        if index in [0]:
            return None

        if self.content is None: return None
        widget = self.content.widget(index)
        if widget is not None: widget.close()
        self.content.removeTab(index)
