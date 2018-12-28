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

    @inject.params(search='search', storage='storage', notepad='notepad')
    def onActionSearchRequest(self, widget, search, storage, notepad):
        text = widget.text()
        if text is None or not len(text):
            return notepad.toggle([], False)

        result = search.request(text)
        collection = [storage.index(x['path']) for x in result]
        
        if collection is None or not len(collection):
            return notepad.toggle([], False)

        return notepad.toggle(collection, True)

    def onActionSearchShortcut(self, event=None, widget=None):
        widget.setFocusPolicy(Qt.StrongFocus)
        widget.setFocus()

    @inject.params(kernel='kernel')
    def onActionFolderCreate(self, event, kernel):
        kernel.dispatch('folder_new')

        
    @inject.params(search='search')
    def onActionNoteCreated(self, event, search):
        return search.append(event.data)

    @inject.params(search='search')
    def onActionNoteUpdated(self, event, search):
        return search.update(event.data)

    @inject.params(search='search')
    def onActionNoteRemove(self, event, search):
        return search.remove(event.data)

    @inject.params(logger='logger', storage='storage', config='config')
    def onActionNoteImport(self, event, logger, storage, config):
        selector = QtWidgets.QFileDialog()
        if not selector.exec_():
            return None

        for path in selector.selectedFiles():
            if not os.path.exists(path):
                continue

            size = os.path.getsize(path) / 1000000 
            if size and size >= 1: 
                message = "The file  '%s' is about %.2f Mb, are you sure?" % (path, size)
                reply = QtWidgets.QMessageBox.question(self._widget, 'Message', message, QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.No:
                    continue
            with open(path, 'r') as source:
                index = storage.index(config.get('storage.location'))
                if index is None or not index:
                    return None
                
                index = storage.touch(index, os.path.basename(path))
                if index is None or not index:
                    return None
                
                storage.setFileContent(index, source.read())
                source.close()

