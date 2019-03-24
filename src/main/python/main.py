#! /usr/bin/python3
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
import math
import logging
import optparse
import inject
import glob
import pdfkit
import secrets
import configparser
import html
import importlib

import Crypto
from Crypto import Cipher
from Crypto import Random

from html import parser
from html.parser import HTMLParser

import whoosh
from whoosh import fields

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import Qt

from fbs_runtime.application_context import ApplicationContext

abspath = os.path.abspath(__file__)
os.chdir(os.path.dirname(abspath))

sys.path.append(os.path.join(os.getcwd(), 'lib'))
sys.path.append(os.path.join(os.getcwd(), 'modules'))
sys.path.append(os.path.join(os.getcwd(), 'plugins'))

from lib.kernel import Kernel


class ApplicationContainer(ApplicationContext):

    def run(self, options, args):
        self.app.setAttribute(Qt.AA_ShareOpenGLContexts)

        spec = importlib.util.find_spec('application')
        module = spec.loader.load_module()

        if module is None: return None

        self.application = module.Application(options, args)
        return self.application.exec_()


if __name__ == "__main__":
    parser = optparse.OptionParser()

    parser.add_option("--loglevel", default=logging.DEBUG, dest="loglevel", help="Logging level")
    parser.add_option("--logfile", default=os.path.expanduser('~/.config/CryptoNotes/notes.log'), dest="logfile", help="Logfile location")
    parser.add_option("--config", default=os.path.expanduser('~/.config/CryptoNotes/notes.conf'), dest="config", help="Config file location")

    (options, args) = parser.parse_args()

    log_format = '[%(relativeCreated)d][%(name)s] %(levelname)s - %(message)s'
    logging.basicConfig(level=options.loglevel, format=log_format)

    application = ApplicationContainer()
    sys.exit(application.run(options, args))
