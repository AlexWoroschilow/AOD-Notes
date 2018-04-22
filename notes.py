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

import sys
import inject
import logging
import optparse

from PyQt5 import QtGui, QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from lib.kernel import Kernel

import os

abspath = os.path.abspath(__file__)
os.chdir(os.path.dirname(abspath))


class Application(QtWidgets.QApplication):

    def __init__(self, options=None, args=None):
        self.kernel = Kernel(options, args)
        self.window = None

        QtWidgets.QApplication.__init__(self, sys.argv)

    @inject.params(dispatcher='event_dispatcher', logger='logger')
    def exec_(self, dispatcher=None, logger=None):
        dispatcher.add_listener('application.start', self.onWindowToggle)
        dispatcher.add_listener('window.toggle', self.onWindowToggle)
        dispatcher.add_listener('window.exit', self.exit)

        dispatcher.dispatch('application.start', self)

        return super(Application, self).exec_()

    def onWindowToggle(self, event=None, dispatcher=None):
        if self.window is None:
            self.window = MainWindow()
            return self.window.show()

        self.window.close()
        self.window = None
        return None


class WindowHeader(QtWidgets.QWidget):

    @inject.params(dispatcher='event_dispatcher', logger='logger')
    def __init__(self, parent=None, dispatcher=None, logger=None):
        super(WindowHeader, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
            
        toolbar = parent.addToolBar('main')
        toolbar.setIconSize(QtCore.QSize(20, 20))
        toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        toolbar.setFloatable(False)
        toolbar.setMovable(False)
        # fill tabs with widgets from different modules
        dispatcher.dispatch('window.header.content', (
            toolbar, self
        ))

        self.setLayout(layout)


class WindowContent(QtWidgets.QTabWidget):

    @inject.params(kernel='kernel', logger='logger')
    def __init__(self, parent=None, kernel=None, logger=None):
        super(WindowContent, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        
        self.setTabPosition(QtWidgets.QTabWidget.West)
        self.tabCloseRequested.connect(self._onTabClose)

        self.addTab(Dashboard(parent), self.tr('Notes'))
        self.setTabsClosable(True)

        kernel.listen('window.tab', self._onTabNew)

    def _onTabNew(self, event=None, dispatcher=None):
        widget, entity = event.data
        if widget is None or entity is None:
            return None

        self.addTab(widget, entity.name)
        self.setCurrentIndex(self.indexOf(widget))

    def _onTabClose(self, index=None):
        if index in [0]:
            return None
        widget = self.widget(index)
        if widget is not None:
            widget.deleteLater()
        self.removeTab(index)


class Dashboard(QtWidgets.QWidget):

    @inject.params(kernel='kernel', logger='logger')
    def __init__(self, parent=None, kernel=None, logger=None):
        super(Dashboard, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setObjectName('dashboard')
        
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.content = QtWidgets.QSplitter()
        self.content.setContentsMargins(0, 0, 0, 0)

        # fill tabs with widgets from different modules
        kernel.dispatch('window.dashboard.content', (
            self.content, parent
        ))

        layout.addWidget(self.content)

        self.setLayout(layout)


class MainWindow(QtWidgets.QMainWindow):

    @inject.params(dispatcher='event_dispatcher', logger='logger')
    def __init__(self, parent=None, dispatcher=None, logger=None):
        super(MainWindow, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)

        with open("css/stylesheet.qss") as stream:
            self.setStyleSheet(stream.read())

        self.setWindowIcon(QtGui.QIcon("icons/icon.svg"))
        self.setWindowTitle('Cloud notepad')

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(WindowHeader(self))
        layout.addWidget(WindowContent(self))

        content = QtWidgets.QWidget()
        content.setLayout(layout)

        spacer = QtWidgets.QWidget();
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred);
        self.statusBar().addWidget(spacer);
        self.statusBar().addWidget(QtWidgets.QLabel("Message in statusbar"));
        self.setCentralWidget(content)

    @inject.params(dispatcher='event_dispatcher', logger='logger')
    def closeEvent(self, event, dispatcher=None, logger=None):
        dispatcher.dispatch('window.toggle')


if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-t", "--tray", action="store_true", default=False, dest="tray",
                      help="enable grafic user interface")
    parser.add_option("-g", "--gui", action="store_true", default=True, dest="gui", help="enable grafic user interface")

    (options, args) = parser.parse_args()

    log_format = '[%(relativeCreated)d][%(name)s] %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=log_format)

    application = Application(options, args)
    sys.exit(application.exec_())
