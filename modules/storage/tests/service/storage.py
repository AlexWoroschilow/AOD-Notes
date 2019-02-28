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
import unittest
import inject
import shutil
import os

from PyQt5 import QtWidgets

from modules.storage.service import storage
from modules.storage.service import cryptography

 
class StorageTestCase(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.application = QtWidgets.QApplication(sys.argv)
        inject.clear_and_configure(self.__configure)

    def __configure(self, binder):
        binder.bind('encryptor', cryptography.CryptoAES('1234567812345678'))

    def tearDown(self):
        self.application.exit()
        unittest.TestCase.tearDown(self)

    def test_mkdir_should_create_folder(self):
        folder = '/tmp/test'
        shutil.rmtree(folder, True)
        os.makedirs(folder)
            
        service = storage.FilesystemStorage(folder)
        service.mkdir(service.rootIndex(), 'test12')
        self.assertTrue(os.path.exists('{}/test12'.format(folder)))
        self.assertTrue(os.path.exists('{}/test12/.metadata'.format(folder)))
        
        shutil.rmtree(folder, True)
