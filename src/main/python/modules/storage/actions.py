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

    @inject.params(config='config', storage='storage', search='search', notepad='notepad.dashboard')
    def onActionStorageLocationChange(self, event, config, widget, storage, search, notepad):
        message = "Select Directory"
        destination = str(QtWidgets.QFileDialog.getExistingDirectory(widget, message, os.path.expanduser('~')))
        if destination is None or not len(destination):
            return None

        widget.location.setText(destination)
        config.set('storage.location', destination)
        config.set('editor.current', destination)

        notepad.tree.setModel(storage)

        index = storage.setRootPath(destination)
        notepad.tree.setRootIndex(index)
        notepad.tree.expandAll()

        notepad.group(index)
