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

from lib.plugin import Loader

from .actions import ModuleActions
from .gui.widget import SearchField


class Loader(Loader):

    actions = ModuleActions()

    @property
    def enabled(self):
        return True

    def config(self, binder=None):
        binder.bind_to_constructor('search', self._service)

    @inject.params(kernel='kernel', config='config', storage='storage')
    def _service(self, kernel, config, storage):
        from .service import Search
        
        service = Search()
        
        destination = os.path.dirname(kernel.options.config)
        if service.exists('%s/index' % destination):
            return service.previous('%s/index' % destination)

        service.create('%s/index' % destination)
        for index in storage.entitiesByPath(config.get('storage.location')):
            
            name = storage.fileName(index)
            path = storage.filePath(index)
            text = storage.fileContent(index)

            service.append(name, path, text)
        return service

    @inject.params(factory='window.header_factory', notepad='notepad')
    def boot(self, options, args, factory, notepad):

        self.buttonGroup = QtWidgets.QAction(QtGui.QIcon("icons/plus.svg"), 'Create group')
        action = functools.partial(notepad.actions.onActionFolderCreate, widget=notepad)
        self.buttonGroup.triggered.connect(action)

        self.buttonNote = QtWidgets.QAction(QtGui.QIcon("icons/plus.svg"), 'Create note')
        action = functools.partial(notepad.actions.onActionNoteCreate, widget=notepad)
        self.buttonNote.triggered.connect(action)

        self.buttonImport = QtWidgets.QAction(QtGui.QIcon("icons/import.svg"), 'Import document')
        self.buttonImport.triggered.connect(self.actions.onActionNoteImport)
        
        self.search = SearchField()
        action = functools.partial(self.onSearchFocusIn, widget=self.search)
        self.search.focusInEvent = action
        
        action = functools.partial(self.onSearchFocusOut, widget=self.search)          
        self.search.focusOutEvent = action
        
        action = functools.partial(self.actions.onActionSearchRequest, widget=self.search)         
        self.search.returnPressed.connect(action)

        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+f"), self.search)
        action = functools.partial(self.actions.onActionSearchShortcut, widget=self.search)
        shortcut.activated.connect(action)

        self.spacer = QtWidgets.QWidget();
        self.spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred);

        factory.addWidget(self.buttonGroup)
        factory.addWidget(self.buttonNote)
        factory.addWidget(self.buttonImport)
        factory.addWidget(self.spacer)
        factory.addWidget(self.search)

    def onSearchFocusIn(self, event, widget):
        self.spacer.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum);
        self.spacer.setVisible(False)
        self.buttonGroup.setVisible(False)
        self.buttonNote.setVisible(False)
        self.buttonImport.setVisible(False)
    
    def onSearchFocusOut(self, event, widget):
        self.spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred);
        self.spacer.setVisible(True)
        self.buttonGroup.setVisible(True)
        self.buttonImport.setVisible(True)
        self.buttonNote.setVisible(True)
