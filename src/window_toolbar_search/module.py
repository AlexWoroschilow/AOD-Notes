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
import functools

from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.Qt import Qt

from lib.plugin import Loader
from .gui.widget import SearchField


class Loader(Loader):

    @property
    def enabled(self):
        return True

    def config(self, binder=None):
        binder.bind_to_constructor('widget.search', self._constructor_search)
        binder.bind_to_constructor('widget.create_folder', self._constructor_create_folder)
        binder.bind_to_constructor('widget.create_note', self._constructor_create_note)
        binder.bind_to_constructor('widget.import_note', self._constructor_import_note)

    @inject.params(dispatcher='event_dispatcher')
    def boot(self, options=None, args=None, dispatcher=None):
        dispatcher.add_listener('header_content', self.onActionHeader)

    @inject.params(config='config')
    def _constructor_search(self, config=None):
        widget = SearchField()

        action = functools.partial(self.onActionSearchRequest, widget=widget)
        widget.returnPressed.connect(action)

        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+f"), widget)
        action = functools.partial(self.onActionSearchShortcut, widget=widget)
        shortcut.activated.connect(action)

        return widget

    @inject.params(config='config')
    def _constructor_create_folder(self, config=None):
        widget = QtWidgets.QAction(QtGui.QIcon("icons/plus.svg"), 'Create folder')
        widget.triggered.connect(self.onActionFolderCreate)

        return widget

    @inject.params(config='config')
    def _constructor_create_note(self, config=None):

        widget = QtWidgets.QAction(QtGui.QIcon("icons/plus.svg"), 'Create document')
        widget.triggered.connect(self.onActionNoteCreate)

        return widget

    @inject.params(config='config')
    def _constructor_import_note(self, config=None):

        widget = QtWidgets.QAction(QtGui.QIcon("icons/import.svg"), 'Import document')
        widget.triggered.connect(self.onActionNoteImport)

        return widget

    @inject.params(widget_search='widget.search', widget_create_folder='widget.create_folder', widget_create_note='widget.create_note', widget_import_note='widget.import_note')
    def onActionHeader(self, event=None, widget_search=None, widget_create_folder=None, widget_create_note=None, widget_import_note=None):
        self._container, self._parent = event.data
        if self._container is None:
            return None

        self._container.addAction(widget_create_folder)
        self._container.addAction(widget_create_note)
        self._container.addAction(widget_import_note)

        spacer = QtWidgets.QWidget();
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred);
        self._container.addWidget(spacer)
        
        self._container.addWidget(widget_search)

    @inject.params(kernel='kernel')
    def onActionSearchRequest(self, event=None, kernel=None, widget=None):
        kernel.dispatch('search_request', widget.text())

    def onActionSearchShortcut(self, event=None, widget=None):
        widget.setFocusPolicy(Qt.StrongFocus)
        widget.setFocus()

    @inject.params(kernel='kernel')
    def onActionFolderCreate(self, event, kernel):
        kernel.dispatch('folder_new')

    @inject.params(kernel='kernel')
    def onActionNoteCreate(self, event, kernel=None):
        kernel.dispatch('note_new')

    @inject.params(kernel='kernel', logger='logger')
    def onActionNoteImport(self, event=None, kernel=None, logger=None):
        logger.debug('[search] document import event')

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
            with open(path, 'r') as stream:
                kernel.dispatch('note_new', (os.path.basename(path), stream.read()))
                stream.close()

