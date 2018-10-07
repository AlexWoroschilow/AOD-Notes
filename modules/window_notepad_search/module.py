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
        """
        This is the core-functionaliry plugin,
        should be enabled by default
        """
        return True

    def config(self, binder=None):
        """
        Initialize the widget of this plugin as a service
        this widget will be used in the main window 
        """
        binder.bind_to_constructor('search', self._service)

    @inject.params(factory='window.header_factory', kernel='kernel')
    def boot(self, options=None, args=None, factory=None, kernel=None):

        widget_create_folder = QtWidgets.QAction(QtGui.QIcon("icons/plus.svg"), 'Create folder')
        widget_create_folder.triggered.connect(self.actions.onActionFolderCreate)

        widget_create_note = QtWidgets.QAction(QtGui.QIcon("icons/plus.svg"), 'Create document')
        widget_create_note.triggered.connect(self.actions.onActionNoteCreate)

        widget_import_document = QtWidgets.QAction(QtGui.QIcon("icons/import.svg"), 'Import document')
        widget_import_document.triggered.connect(self.actions.onActionNoteImport)
        
        widget_search_field = SearchField()
        widget_search_field.returnPressed.connect(functools.partial(
            self.actions.onActionSearchRequest, widget=widget_search_field
        ))

        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+f"), widget_search_field)
        shortcut.activated.connect(functools.partial(
            self.actions.onActionSearchShortcut, widget=widget_search_field
        ))

        factory.addWidget(widget_create_folder)
        factory.addWidget(widget_create_note)
        factory.addWidget(widget_import_document)

        spacer = QtWidgets.QWidget();
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred);
        factory.addWidget(spacer)
        
        factory.addWidget(widget_search_field)
        
        kernel.listen('note_created', self.actions.onActionNoteCreated)
        kernel.listen('note_udpated', self.actions.onActionNoteUpdated)
        kernel.listen('note_remove', self.actions.onActionNoteRemove)

    @inject.params(kernel='kernel', config='config', storage='storage')
    def _service(self, kernel, config, storage):
        from .service import Search
        
        destination = '%s/index' % os.path.dirname(kernel.options.config)
        
        service = Search()
        if service.exists(destination):
            return service.previous(destination)

        destination = config.get('storage.location')
        for entity in storage.entities(destination):
            service.append(entity)
        return service

