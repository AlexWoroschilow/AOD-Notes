####! /usr/bin/python3
#
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
import sys
import inject
import logging
import optparse

from PyQt5 import QtWidgets

from lib.kernel import Kernel

abspath = os.path.abspath(__file__)
os.chdir(os.path.dirname(abspath))

sys.path.append(os.path.join(os.getcwd(), 'lib'))
sys.path.append(os.path.join(os.getcwd(), 'modules'))
sys.path.append(os.path.join(os.getcwd(), 'plugins'))

from PyQt5 import QtCore


class Application(QtWidgets.QApplication):
    kernel = None

    def __init__(self, options=None, args=None):
        super(Application, self).__init__(sys.argv)
        self.setApplicationName('AOD - Notepad')
        self.kernel = Kernel(options, args)

    def exec_(self, options=None, args=None):
        container = inject.get_injector()
        if container is None: return None

        if options.console: return None

        window = container.get_instance('window')
        if window is None: return None

        config = container.get_instance('config')
        if config is None: return None

        window.show()

        width = int(config.get('window.width'))
        height = int(config.get('window.height'))

        animation = QtCore.QPropertyAnimation(window, b'size')
        animation.setEndValue(QtCore.QSize(width, height))
        animation.setStartValue(QtCore.QSize(800, 600))
        animation.setDuration(200)
        animation.start()

        return super(Application, self).exec_()


if __name__ == "__main__":
    parser = optparse.OptionParser()

    parser.add_option("--config", default='./notes.conf', dest="config", help="Config file location")
    parser.add_option("--console", action="store_true", dest="console", help="Start program in the console mode")
    parser.add_option("--console-export", default=None, dest="console_export", help="Start program in the console mode")
    parser.add_option("--logfile", default='./notes.log', dest="logfile", help="Logfile location")
    parser.add_option("--loglevel", default=logging.DEBUG, dest="loglevel", help="Logging level")

    (options, args) = parser.parse_args()

    log_format = '[%(relativeCreated)d][%(name)s] %(levelname)s - %(message)s'
    logging.basicConfig(level=options.loglevel, format=log_format)

    application = Application(options, args)
    sys.exit(application.exec_(options, args))
