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

        action = functools.partial(self.onActionFolderCreate, widget=widget)
        widget.triggered.connect(action)

        return widget

    @inject.params(config='config')
    def _constructor_create_note(self, config=None):

        widget = QtWidgets.QAction(QtGui.QIcon("icons/plus.svg"), 'Create document')

        action = functools.partial(self.onActionNoteCreate, widget=widget)
        widget.triggered.connect(action)

        return widget

    @inject.params(config='config')
    def _constructor_import_note(self, config=None):

        widget = QtWidgets.QAction(QtGui.QIcon("icons/import.svg"), 'Import document')

        action = functools.partial(self.onActionNoteImport, widget=widget)
        widget.triggered.connect(action)

        return widget

    @inject.params(config='config')
    def _constructor_settings(self, config=None):

        widget = QtWidgets.QAction(QtGui.QIcon("icons/settings.svg"), None)

        return widget

    @property
    def enabled(self):
        return True

    def config(self, binder=None):
        binder.bind_to_constructor('widget.search', self._constructor_search)
        binder.bind_to_constructor('widget.create_folder', self._constructor_create_folder)
        binder.bind_to_constructor('widget.create_note', self._constructor_create_note)
        binder.bind_to_constructor('widget.import_note', self._constructor_import_note)
        binder.bind_to_constructor('widget.settings', self._constructor_settings)

    @inject.params(dispatcher='event_dispatcher')
    def boot(self, options=None, args=None, dispatcher=None):
        dispatcher.add_listener('header_content', self.onActionHeader)

    @inject.params(widget_search='widget.search', widget_create_folder='widget.create_folder', widget_create_note='widget.create_note', widget_import_note='widget.import_note', widget_settings='widget.settings')
    def onActionHeader(self, event=None, widget_search=None, widget_create_folder=None, widget_create_note=None, widget_import_note=None, widget_settings=None):
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
        self._container.addAction(widget_settings)

    @inject.params(kernel='kernel')
    def onActionSearchRequest(self, event=None, kernel=None, widget=None):
        kernel.dispatch('search_request', widget.text())

    def onActionSearchShortcut(self, event=None, widget=None):
        if widget is None:
            return None
        widget.setFocusPolicy(Qt.StrongFocus)
        widget.setFocus()

    @inject.params(storage='storage')
    def _onNotepadFolderNew(self, event=None, dispather=None, storage=None):
        name, description = event.data
        storage.addFolder(name, description)

    @inject.params(kernel='kernel')
    def onActionFolderCreate(self, event, kernel=None, widget=None):
        event = (('New folder', 'New folder description'), self)
        kernel.dispatch('folder_new', event)

    @inject.params(kernel='kernel', folders='folders')
    def onActionNoteCreate(self, event, kernel=None, folders=None, widget=None):
        event = ('New note', 'New description', folders.selected) 
        kernel.dispatch('note_new', event)

    @inject.params(kernel='kernel', folders='folders')
    def onActionNoteImport(self, event, kernel=None, folders=None, widget=None):
        selector = QtWidgets.QFileDialog()
        if not selector.exec_():
            return None

        for path in selector.selectedFiles():
            if not os.path.exists(path):
                continue

            size = os.path.getsize(path) / 1000000 
            if size and size >= 1: 
                message = widget.tr("The file  '%s' is about %.2f Mb, are you sure?" % (path, size))
                reply = QtWidgets.QMessageBox.question(self._widget, 'Message', message, QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.No:
                    continue
            with open(path, 'r') as stream:
                event = (os.path.basename(path), stream.read(), folders.selected)
                kernel.dispatch('note_new', event)
                stream.close()

