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
import inject
import functools

from PyQt5 import QtWidgets

from lib.plugin import Loader
from .gui.widget import FolderList
from .gui.text import TextEditor


class Loader(Loader):
    
    _search = None

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
        binder.bind_to_constructor('widget.folders', self._constructor_folders)

    @inject.params(kernel='kernel', config='config', storage='storage')
    def _constructor_folders(self, kernel=None, storage=None, config=None):
        
        widget = FolderList(storage)
        
        widget.toolbar.setVisible(bool(config.get('folders.leftbar')))
        
        action = functools.partial(self.onActionFolderCreate, widget=widget)
        widget.toolbar.newAction.clicked.connect(action)
        
        action = functools.partial(self.onActionFolderCopy, widget=widget)
        widget.toolbar.copyAction.clicked.connect(action)

        action = functools.partial(self.onActionRefresh, widget=widget)
        widget.toolbar.refreshAction.clicked.connect(action)

        action = functools.partial(self.onActionFolderRemove, widget=widget)
        widget.toolbar.removeAction.clicked.connect(action)

        action = functools.partial(self.onActionFolderOpen, widget=widget)
        widget.list.doubleClicked.connect(action)

        action = functools.partial(self.onActionFolderSelect, widget=widget)
        widget.list.clicked.connect(action)

        widget.tags.mouseDoubleClickEvent = functools.partial(
            self.onActionTagSelect, widget=widget.tags
        )
        
        # listen for the search request from the search module
        # the request string will be given as a data object to the event
        action = functools.partial(self.onActionSearchRequest, widget=widget)
        kernel.listen('search_request', action, 100)

        action = functools.partial(self.onActionRefresh, widget=widget)
        kernel.listen('folder_new', action, 128)

        action = functools.partial(self.onActionRefresh, widget=widget)
        kernel.listen('folders_refresh', action, 128)
        
        return widget

    @inject.params(kernel='kernel', logger='logger')
    def onActionFolderCreate(self, event=None, widget=None, kernel=None, logger=None):
        logger.debug('[folders] folder create event')
        kernel.dispatch('folder_new', ('New folder', 'New folder description'))
        widget.reload(self._search)

    @inject.params(kernel='kernel', logger='logger')
    def onActionFolderCopy(self, event=None, widget=None, kernel=None, logger=None):
        logger.debug('[folders] folder copy event: %s' % widget.selected.name)
        kernel.dispatch('folder_new', ("%s-copy" % widget.selected.name, 'New folder description'))
        widget.reload(self._search)

    @inject.params(kernel='kernel')
    def onActionFolderRemove(self, event=None, widget=None, kernel=None):
        message = widget.tr("Are you sure you want to remove this Folder?")
        reply = QtWidgets.QMessageBox.question(widget, 'Remove folder', message, QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            kernel.dispatch('folder_remove', widget.selected)
        widget.reload(self._search)

    @inject.params(kernel='kernel')
    def onActionRefresh(self, event=None, kernel=None, storage=None, widget=None):
        widget.reload(self._search)

    @inject.params(kernel='kernel', logger='logger')
    def onActionFolderOpen(self, event=None, selection=None, widget=None, kernel=None, logger=None):
        logger.debug('[folders] folder selected: %s' % widget.selected.name)
        kernel.dispatch('folder_gointo', widget.selected)

    @inject.params(kernel='kernel', logger='logger')
    def onActionFolderSelect(self, event=None, selection=None, widget=None, kernel=None, logger=None):
        logger.debug('[folders] folder selected: %s' % widget.selected.name)
        kernel.dispatch('folder_current', widget.selected)

    @inject.params(kernel='kernel', storage='storage')
    def onActionSearchRequest(self, event=None, kernel=None, storage=None, widget=None):
        self._search = event.data
        if self._search is not None:
            widget.reload(self._search)

    @inject.params(kernel='kernel')
    def onActionTagSelect(self, event, widget=None, kernel=None):
        super(TextEditor, widget).mouseDoubleClickEvent(event)
        
