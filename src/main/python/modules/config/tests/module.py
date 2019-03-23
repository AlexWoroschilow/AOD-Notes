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
import inject
import unittest
import collections
import os
import sys
from PyQt5 import QtWidgets

from modules.config import module


class ModuleTestCase(unittest.TestCase):
    loader = module.Loader({}, [])

    def __configure(self, binder):
        binder.bind_to_provider('settings_factory', lambda binder: None)
    
        Config = collections.namedtuple('Config', 'config')
        binder.bind('config', Config(config='/tmp/test.conf'))
    
        class Kernel(object):
            options = Config(config='/tmp/test.conf')
            
        binder.bind('kernel', Kernel())

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.application = QtWidgets.QApplication(sys.argv)
        inject.clear_and_configure(self.__configure)

    def tearDown(self):
        self.application.exit()
        unittest.TestCase.tearDown(self)

    @inject.params(kernel='kernel')
    def test__config(self, kernel):
        
        config = self.loader._config(kernel)
        self.assertEqual(config.file, kernel.options.config)
        self.assertTrue(isinstance(config.parser, object))
        self.assertTrue(isinstance(config, object))
        
        self.assertTrue(os.path.exists(kernel.options.config))

    @inject.params(kernel='kernel')
    def test__widget_settings_cryptography(self, kernel):
        
        config = self.loader._config(kernel)
        cryptography = self.loader._widget_settings_cryptography(config)
        self.assertTrue(isinstance(cryptography, QtWidgets.QWidget))

    @inject.params(kernel='kernel')
    def test__widget_settings_navigator(self, kernel):
        
        config = self.loader._config(kernel)
        cryptography = self.loader._widget_settings_navigator(config)
        self.assertTrue(isinstance(cryptography, QtWidgets.QWidget))

    @inject.params(kernel='kernel')
    def test__widget_settings_editor(self, kernel):
        
        config = self.loader._config(kernel)
        cryptography = self.loader._widget_settings_editor(config)
        self.assertTrue(isinstance(cryptography, QtWidgets.QWidget))

    @inject.params(kernel='kernel')
    def test__widget_settings_storage(self, kernel):
        
        config = self.loader._config(kernel)
        cryptography = self.loader._widget_settings_storage(config)
        self.assertTrue(isinstance(cryptography, QtWidgets.QWidget))

    def test_boot_should_not_produce_errors(self):
        
        class WidgetMock(object):
            widgets = []

            def addWidget(self, widget):
                self.widgets.append(widget)
        
        container = WidgetMock()
        self.loader.boot({}, [], container)
        self.assertEqual(4, len(container.widgets))

    def test_enabled_should_return_true(self):
        self.assertTrue(self.loader.enabled)
