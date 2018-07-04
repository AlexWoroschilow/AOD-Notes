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
import json
import base64
import time


class SynchronisationService(object):

    def __init__(self, destination=None):
        self._destination = destination

    def dump(self, unique, json):
        timestamp = int(time.time())
        with open('%s/%s.v%i' % (self._destination, unique, timestamp), 'w') as dump:
            dump.write(json)
            dump.close
        print(json)
