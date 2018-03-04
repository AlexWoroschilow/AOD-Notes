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

from PyQt5 import QtGui
from PyQt5 import QtWidgets

from lib.kernel import Kernel


class Application(QtWidgets.QApplication):
    def __init__(self, options=None, args=None, dispatcher=None, logger=None):
        """

        :param options: 
        :param args: 
        """
        self.kernel = Kernel(options, args)
        self.window = None

        QtWidgets.QApplication.__init__(self, sys.argv)

        dispatcher = self.kernel.get('event_dispatcher')
        dispatcher.add_listener('window.start', self.onWindowToggle)
        dispatcher.add_listener('window.toggle', self.onWindowToggle)
        dispatcher.add_listener('window.exit', self.onWindowExit)

    @inject.params(dispatcher='event_dispatcher', logger='logger')
    def exec_(self, dispatcher=None, logger=None):
        """

        :param dispather: 
        :param logger: 
        :return: 
        """
        dispatcher.dispatch('window.start', self)

        return super(Application, self).exec_()

    def onWindowToggle(self, event=None, dispatcher=None):
        """

        :param event: 
        :return: 
        """
        if self.window is None:
            self.window = MainWindow()
            return self.window.show()

        self.window.close()
        self.window = None
        return None

    def onWindowExit(self, event=None, dispatcher=None):
        """
        
        :param event: 
        :param dispatcher: 
        :return: 
        """
        self.exit()


class MainWindow(QtWidgets.QMainWindow):
    @inject.params(dispatcher='event_dispatcher', logger='logger')
    def __init__(self, parent=None, dispatcher=None, logger=None):
        """
        
        :param parent: 
        :param dispatcher: 
        :param logger: 
        """

        super(MainWindow, self).__init__(parent)
        self.setStyleSheet('QMainWindow{ background-color: #ffffff; }')
        self.setWindowIcon(QtGui.QIcon("icons/icon.svg"))
        self.setWindowTitle('Notepad')

        layout = QtWidgets.QHBoxLayout()
        layout.setSpacing(0)

        self.content = QtWidgets.QSplitter()
        self.content.setContentsMargins(0, 0, 0, 0)
        self.content.setLayout(layout)

        # fill tabs with widgets from different modules
        dispatcher.dispatch('window.first_tab.content', layout)

        self.content.setStretchFactor(0, 1)
        self.content.setStretchFactor(1, 4)
        self.content.setStretchFactor(2, 3)

        self.container = QtWidgets.QTabWidget(self)
        self.container.addTab(self.content, self.tr('Records'))

        self.setCentralWidget(self.container)
        self.setGeometry(100, 100, 1030, 800)

        self.show()

    @inject.params(dispatcher='event_dispatcher', logger='logger')
    def closeEvent(self, event, dispatcher=None, logger=None):
        """

        :param event: 
        :return: 
        """
        dispatcher.dispatch('window.toggle')

    def resizeEvent(self, event):
        """

        :param event: 
        :return: 
        """
        # self.tab.setFixedSize(event.size())


if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-t", "--tray", action="store_true", default=False, dest="tray", help="enable grafic user interface")
    parser.add_option("-g", "--gui", action="store_true", default=True, dest="gui", help="enable grafic user interface")

    (options, args) = parser.parse_args()

    log_format = '[%(relativeCreated)d][%(name)s] %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=log_format)

    application = Application(options, args)
    sys.exit(application.exec_())
