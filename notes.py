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
import functools

abspath = os.path.abspath(__file__)
os.chdir(os.path.dirname(abspath))

import sys
import inject       
import logging
import optparse

from PyQt5 import QtWidgets

from lib.kernel import Kernel


class Application(QtWidgets.QApplication):

    def __init__(self, options=None, args=None):
        QtWidgets.QApplication.__init__(self, sys.argv)
        self._kernel = Kernel(options, args)

    @inject.params(kernel='kernel', widget='window')
    def exec_(self, kernel=None, widget=None):
        
        kernel.listen('window_exit', self.exit)
        
        action = functools.partial(self.onWindowToggle, widget=widget)
        kernel.listen('window_toggle', action)
        
        action = functools.partial(self.onWindowToggle, widget=widget)
        kernel.listen('window_start', action)
        
        kernel.dispatch('window_start')

        return super(Application, self).exec_()
    
    def onWindowToggle(self, event=None, widget=None):
        if widget.isVisible():
            return widget.close()
        return widget.show()


if __name__ == "__main__":
    parser = optparse.OptionParser()
    
    parser.add_option("--loglevel", default=logging.DEBUG, dest="loglevel", help="Loggin level")
    config = os.path.expanduser('~/.config/CloudNotes/notes.conf')
    parser.add_option("--config", default=config, dest="config", help="Loggin level")
    
    (options, args) = parser.parse_args()
    
    log_format = '[%(relativeCreated)d][%(name)s] %(levelname)s - %(message)s'
    logging.basicConfig(level=options.loglevel, format=log_format)

    application = Application(options, args)
    sys.exit(application.exec_())
