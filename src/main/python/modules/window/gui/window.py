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
import platform
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import Qt


class MainWindow(QtWidgets.QMainWindow):
    tab = QtCore.pyqtSignal(object)

    @inject.params(factory='window.header_factory')
    def __init__(self, parent=None, factory=None):
        super(MainWindow, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        container = QtWidgets.QWidget()
        container.setLayout(self.layout)

        self.setCentralWidget(container)

        spacer = QtWidgets.QWidget()
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.statusBar().addWidget(spacer)

        self.setWindowTitle('CryptoNotes')

        stylesheet = 'css/{}.qss'.format(platform.system().lower())
        if not os.path.exists(stylesheet): return None
        self.setStyleSheet(open(stylesheet).read())

        if not os.path.exists('icons/icon.svg'): return None
        self.setWindowIcon(QtGui.QIcon('icons/icon.svg'))

        self.tab.connect(self.onActionTabOpen)

        self.header = self.addToolBar('main')
        self.header.setObjectName('QToolBarTop')
        self.header.setIconSize(QtCore.QSize(20, 20))
        self.header.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.header.setFloatable(False)
        self.header.setMovable(False)

        for header_widget, priority in factory.widgets:
            if isinstance(header_widget, QtWidgets.QAction):
                self.header.addAction(header_widget)
            if isinstance(header_widget, QtWidgets.QWidget):
                self.header.addWidget(header_widget)

    def setMainWidget(self, widget=None):
        if self.layout is None: return None
        for index in range(0, self.layout.count()):
            item = self.layout.itemAt(index)
            if item is None: continue
            self.layout.removeItem(item)

        if widget is None: return None

        self.content = widget
        if hasattr(self.content, 'tabCloseRequested'):
            self.content.tabCloseRequested.connect(self.onActionTabClose)
        self.layout.addWidget(self.content)

    def onActionTabOpen(self, event=None):
        if event is None: return None
        widget, name = event
        if widget is None: return None
        if name is None: return None

        self.content.addTab(widget, name)
        index = self.content.indexOf(widget)
        if index is None: return None
        self.content.setCurrentIndex(index)

    def onActionTabClose(self, index=None):
        if self.content is None: return None
        # Do not close the first one tab 
        if index in [0]: return None
        widget = self.content.widget(index)
        if widget is None: widget.deleteLater()
        self.content.removeTab(index)
