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
from PyQt5 import QtGui
from PyQt5.Qt import Qt

from lib.plugin import Loader
from .gui.widget import SearchField


class Loader(Loader):

    @property
    def enabled(self):
        return True

    @inject.params(dispatcher='event_dispatcher')
    def boot(self, options=None, args=None, dispatcher=None):
        dispatcher.add_listener('window.header.content', self._onWindowHeader)

    @inject.params(storage='storage')
    def _onWindowHeader(self, event=None, dispather=None, storage=None):
        self._container, self._parent = event.data
        if self._container is None:
            return None

        self._widget = SearchField()
        self._widget.returnPressed.connect(self._OnSearchRequestEvent)

        self._action1 = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+f"), self._widget)
        self._action1.activated.connect(self._onShortcutSearchStart)

        self._actionCreateFolder = QtWidgets.QAction(QtGui.QIcon("icons/plus.svg"), 'Create folder', self._container)
        self._actionCreateFolder.triggered.connect(self._onCreateFolder)
        self._container.addAction(self._actionCreateFolder)
        
        self._actionCreateNote = QtWidgets.QAction(QtGui.QIcon("icons/plus.svg"), 'Create document', self._container)
        self._actionCreateNote.triggered.connect(self._onCreateNote)
        self._container.addAction(self._actionCreateNote)

        self._actionImportNote = QtWidgets.QAction(QtGui.QIcon("icons/import.svg"), 'Import document', self._container)
        self._actionImportNote.triggered.connect(self._onImportNote)
        self._container.addAction(self._actionImportNote)

        spacer = QtWidgets.QWidget();
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred);
        self._container.addWidget(spacer)
        self._container.addWidget(self._widget)
        # self._container.addWidget(spacer)
        
        self._actionSettings = QtWidgets.QAction(QtGui.QIcon("icons/settings.svg"), None, self._container)
        self._container.addAction(self._actionSettings)

    @inject.params(dispather='event_dispatcher')
    def _OnSearchRequestEvent(self, event=None, dispather=None):
        dispather.dispatch('window.search.request', self._widget.text())

    @inject.params(dispather='event_dispatcher')
    def _onShortcutSearchStart(self, event=None, dispather=None):
        if self._widget is None:
            return None
        self._widget.setFocusPolicy(Qt.StrongFocus)
        self._widget.setFocus()

    @inject.params(storage='storage')
    def _onNotepadFolderNew(self, event=None, dispather=None, storage=None):
        name, description = event.data
        storage.addFolder(name, description)

    @inject.params(kernel='kernel')
    def _onCreateFolder(self, event, kernel=None):
        kernel.dispatch('window.notepad.folder_new', (
            ('New folder', 'New folder description'), self
        ))

    @inject.params(kernel='kernel', folders='folders')
    def _onCreateNote(self, event, kernel=None, folders=None):
        kernel.dispatch('window.notepad.note_new', (
            'New note', 'New description', folders.selected
        ))

    @inject.params(kernel='kernel', folders='folders')
    def _onImportNote(self, event, kernel=None, folders=None):
        selector = QtWidgets.QFileDialog()
        if not selector.exec_():
            return None

        for path in selector.selectedFiles():
            if not os.path.exists(path):
                continue

            size = os.path.getsize(path) / 1000000 
            if size and size >= 1: 
                message = self._widget.tr("The file  '%s' is about %.2f Mb, are you sure?" % (path, size))
                reply = QtWidgets.QMessageBox.question(self._widget, 'Message', message, QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.No:
                    continue
            with open(path, 'r') as stream:
                kernel.dispatch('window.notepad.note_new', (
                    os.path.basename(path), stream.read(), folders.selected
                ))
                stream.close()

