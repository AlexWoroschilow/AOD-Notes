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
import sys
import inject
import unittest
from PyQt5 import QtWidgets

from modules.storage import module

 
class ModuleTestCase(unittest.TestCase):
    loader = module.Loader({}, [])

    def __configure(self, binder):
    
        class Config(object):
    
            def get(self, name):
                return name
            
        binder.bind('config', Config())

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.application = QtWidgets.QApplication(sys.argv)
        inject.clear_and_configure(self.__configure)

    def tearDown(self):
        self.application.exit()
        unittest.TestCase.tearDown(self)

    def test__storage_should_return_correct_instance(self):
        storage = self.loader._storage()
        self.assertTrue(isinstance(storage, QtWidgets.QFileSystemModel))

    def test__encryptor_should_return_correct_instance(self):
        storage = self.loader._encryptor()
        self.assertTrue(isinstance(storage, object))

    def test_enabled_should_return_true(self):
        self.assertTrue(self.loader.enabled)
