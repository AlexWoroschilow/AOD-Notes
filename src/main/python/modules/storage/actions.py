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
import inject
from PyQt5 import QtWidgets


class ModuleActions(object):

    @inject.params(config='config', dashboard='notepad.dashboard')
    def onActionStorageLocationChange(self, event, config, dashboard):
        message = "Select Directory"
        destination = str(QtWidgets.QFileDialog.getExistingDirectory(dashboard, message, os.path.expanduser('~')))
        if destination is None or not len(destination):
            return None

        config.set('storage.location', destination)
        config.set('editor.current', destination)

        dashboard.storage_changed.emit(destination)
