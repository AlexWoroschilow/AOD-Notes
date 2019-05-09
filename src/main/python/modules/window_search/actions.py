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
import logging
from PyQt5 import QtWidgets

from .gui.preview.widget import PreviewScrollArea  


class ModuleActions(object):

    @inject.params(search='search', storage='storage', window='window')
    def onActionSearchRequest(self, widget=None, search=None, storage=None, window=None):
        if widget is None or window is None: return None
        
        text = widget.text()
        if text is None: return None
        if not len(text): return None

        preview = PreviewScrollArea(window)
        preview.edit.connect(self.onActionEditRequest)
# 
        result = search.search(text)
        result = [x['path'] for x in result]
        if result is None: return None
        if not len(result): return None
        
        for path in result:
            index = storage.index(path)
            if index is None: continue
            preview.addPreview(index)
        
        title = text if len(text) <= 25 else "{}...".format(text[0:22])
        window.tab.emit((preview, title))

    @inject.params(storage='storage', window='window', dashboard='notepad.dashboard')
    def onActionEditRequest(self, index, storage, window, dashboard):
        try:
            if storage.isDir(index):
                dashboard.group(index)
                window.tabSwitch.emit(0)
                return None            
            if storage.isFile(index):
                dashboard.note(index)
                window.tabSwitch.emit(0)                
                return None            
            return None            
        except(Exception) as ex:
            logger = logging.getLogger('search')
            logger.exception(ex)

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

