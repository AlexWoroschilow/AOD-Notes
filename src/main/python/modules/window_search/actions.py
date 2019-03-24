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
from PyQt5.Qt import Qt


class ModuleActions(object):

    @inject.params(search='search', storage='storage', dashboard='notepad.dashboard')
    def onActionSearchRequest(self, widget=None, search=None, storage=None, dashboard=None):
        if widget is None: return None
        if search is None: return None
        if dashboard is None: return None
        if storage is None: return None

        text = widget.text()
        if text is None or not len(text):
            return dashboard.toggle([], False)

        result = search.search(text)
        collection = [storage.index(x['path']) for x in result]

        if collection is None or not len(collection):
            return dashboard.toggle([], False)

        return dashboard.toggle(collection, True)

    def onActionSearchShortcut(self, event=None, widget=None):
        if widget is None: return None
        widget.setFocusPolicy(Qt.StrongFocus)
        widget.setFocus()

    @inject.params(storage='storage', config='config', dashboard='notepad.dashboard')
    def onActionNoteImport(self, event=None, storage=None, config=None, dashboard=None):
        if dashboard is None or storage is None or config is None: return None

        currentwd = config.get('storage.lastimport', os.path.expanduser('~'))
        selector = QtWidgets.QFileDialog(None, 'Select file', currentwd)
        if not selector.exec_(): return None

        for path in selector.selectedFiles():
            if not os.path.exists(path) or os.path.isdir(path): continue
            config.set('storage.lastimport', os.path.dirname(path))

            if os.path.getsize(path) / 1000000 >= 1:
                message = "The file  '{}' is about {:>.2f} Mb, are you sure?".format(path, os.path.getsize(path) / 1000000)
                reply = QtWidgets.QMessageBox.question(self._widget, 'Message', message, QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.No: continue

            with open(path, 'r') as source:
                index = dashboard.current
                if index is None: return None

                index = storage.touch(index, os.path.basename(path))
                if index is None: return None

                storage.setFileContent(index, source.read())
                source.close()

