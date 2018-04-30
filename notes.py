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
import os

abspath = os.path.abspath(__file__)
os.chdir(os.path.dirname(abspath))

import sys
import inject
import logging
import optparse

from PyQt5 import QtWidgets

from lib.kernel import Kernel
from lib.widget.window import MainWindow


class Application(QtWidgets.QApplication):
    _widget = None
    _kernel = None

    def __init__(self, options=None, args=None):
        QtWidgets.QApplication.__init__(self, sys.argv)
        self._kernel = Kernel(options, args)

    @inject.params(kernel='kernel', logger='logger')
    def exec_(self, kernel=None, logger=None):
        
        kernel.listen('window.toggle', self.onWindowToggle)
        kernel.listen('application.start', self.onWindowToggle)
        kernel.listen('window.exit', self.exit)
        
        kernel.dispatch('application.start')

        return super(Application, self).exec_()

    def onWindowToggle(self, event=None):
        if self._widget is not None:
            return self._widget.close()

        self._widget = MainWindow()
        return self._widget.show()


if __name__ == "__main__":
    parser = optparse.OptionParser()
    
    storage_default = '%s/.config/CloudNotes/storage.dhf' % os.environ.get('HOME')
    parser.add_option("--storage", default=storage_default, dest="storage", help="Select the storage destination")
    parser.add_option("--loglevel", default=logging.DEBUG, dest="loglevel", help="Loggin level")
    
    (options, args) = parser.parse_args()
    
    log_format = '[%(relativeCreated)d][%(name)s] %(levelname)s - %(message)s'
    logging.basicConfig(level=options.loglevel, format=log_format)

    application = Application(options, args)
    sys.exit(application.exec_())
