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
import configparser


class ConfigFile(object):
    parser = configparser.ConfigParser()
    file = None

    def __init__(self, file=None):
        if file is None:
            return None
        
        self.file = file
        if os.path.exists(self.file):
            self.parser.read(self.file)
            return None
                    
        folder = os.path.dirname(self.file)
        if not os.path.exists(folder):
            os.makedirs(folder)

        with open(self.file, 'w') as stream:
            self.parser.add_section('window')
            self.parser.set('window', 'width', '950')
            self.parser.set('window', 'height', '600')

            self.parser.add_section('folders')
            self.parser.set('folders', 'toolbar', '1')
            self.parser.set('folders', 'keywords', '1')

            self.parser.add_section('editor')
            self.parser.set('editor', 'leftbar', '1')
            self.parser.set('editor', 'formatbar', '1')
            self.parser.set('editor', 'rightbar', '1')
            self.parser.set('editor', 'current', '')

            self.parser.add_section('storage')
            self.parser.set('storage', 'location', '~/owncloud/CloudNotes/')

            self.parser.add_section('cryptography')
            self.parser.set('cryptography', 'password', '')
            
            self.parser.write(stream)
            stream.close()
            
        self.parser.read(self.file)
        return None

    def get(self, name, default=None):
        if not self.has(name):
            return self.set(name, default)

        section, option = name.split('.', 1)
        if not self.parser.has_section(section):
            return None

        if self.parser.has_option(section, option):
            return self.parser.get(section, option)
        return None

    def set(self, name, value=None):
        section, option = name.split('.', 1)

        if not self.parser.has_section(section):
            self.parser.add_section(section)

        self.parser.set(section, option, '%s' % value)
        with open(self.file, 'w') as stream:
            self.parser.write(stream)
            stream.close()
        return value

    def has(self, name):
        section, option = name.split('.', 1)

        if self.parser.has_section(section):
            return self.parser.has_option(section, option)

        return False
