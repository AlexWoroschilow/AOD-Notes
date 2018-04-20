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
import logging
import optparse

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore

import dbus


class Client(object):
    def check(self, user, password):
        bus = dbus.SystemBus()
        system = bus.get_object("com.deepin.dde.LockService", "/com/deepin/dde/LockService")

        method = system.get_dbus_method('UnlockCheck', 'com.deepin.dde.LockService')

        return method(user, password)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, width=None, height=None):
        """

        :param parent: 
        :param dispatcher: 
        :param logger: 
        """

        super(MainWindow, self).__init__()
        # self.setWindowFlags(QtCore.Qt.SplashScreen | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.X11BypassWindowManagerHint)
        self.setFixedWidth(width)
        self.setFixedHeight(height)

        sImage = QtGui.QImage("background.jpeg")
        sImage = sImage.scaled(QtCore.QSize(width, height))  # resize Image to widgets size
        palette = QtGui.QPalette()
        palette.setBrush(10, QtGui.QBrush(sImage))
        self.setPalette(palette)

        client = Client()
        print(client.check('sensey', '6IKSyAVB'))

        self.showFullScreen()

    def keyPressEvent(self, event=None):
        """

        :param event:
        :return:
        """
        print(event.key())
        event.ignore()


class Application(QtWidgets.QApplication):
    def __init__(self, options=None, args=None, dispatcher=None):
        """

        :param options: 
        :param args: 
        """

        QtWidgets.QApplication.__init__(self, sys.argv)

    def exec_(self):
        resolution = self.desktop().screenGeometry()
        self.window = MainWindow(resolution.width(), resolution.height())
        self.window.show()

        return super(Application, self).exec_()

    def onWindowExit(self, event=None, dispatcher=None):
        """
        
        :param event: 
        :param dispatcher: 
        :return: 
        """
        self.exit()


if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-t", "--tray", action="store_true", default=False, dest="tray", help="enable grafic user interface")
    parser.add_option("-g", "--gui", action="store_true", default=True, dest="gui", help="enable grafic user interface")

    (options, args) = parser.parse_args()

    log_format = '[%(relativeCreated)d][%(name)s] %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=log_format)

    application = Application(options, args)
    sys.exit(application.exec_())
