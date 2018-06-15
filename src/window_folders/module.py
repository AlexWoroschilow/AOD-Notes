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


class Loader(Loader):
    _first = None
    _search = None
    _widget = None

    @inject.params(config='config')
    def _constructor_folders(self, config=None):
        
        widget = FolderList()
        
        widget.toolbar.setVisible(bool(config.get('folders.leftbar')))
        
        action = functools.partial(self.onActionFolderNew, widget=widget)
        widget.toolbar.newAction.clicked.connect(action)
        
        action = functools.partial(self.onActionFolderCopy, widget=widget)
        widget.toolbar.copyAction.clicked.connect(action)

        action = functools.partial(self.onActionRefresh, widget=widget)
        widget.toolbar.refreshAction.clicked.connect(action)

        action = functools.partial(self.onActionFolderRemove, widget=widget)
        widget.toolbar.removeAction.clicked.connect(action)

        action = functools.partial(self.onActionFolderOpen, widget=widget)
        widget.list.doubleClicked.connect(action)
        
        widget.list.selectionChanged = functools.partial(
            self.onActionFolderSelect, widget=widget
        )
        
        return widget

    @property
    def enabled(self):
        return True

    def config(self, binder=None):
        binder.bind_to_constructor('widget.folders', self._constructor_folders)
        binder.bind('folders', self)

    @inject.params(kernel='kernel', widget='widget.folders')
    def boot(self, options=None, args=None, kernel=None, widget=None):
        # listen for the search request from the search module
        # the request string will be given as a data object to the event
        action = functools.partial(self.onActionSearchRequest, widget=widget)
        kernel.listen('search_request', action, 100)

        action = functools.partial(self.onActionFirstTab, widget=widget)
        kernel.listen('dashboard_content', action, 100)

        action = functools.partial(self.onActionRefresh, widget=widget)
        kernel.listen('folder_new', action, 128)

    @inject.params(kernel='kernel', storage='storage')
    def onActionFirstTab(self, event=None, kernel=None, storage=None, widget=None):

        self._first = None
        widget.list.clear()
        for folder in storage.folders():
            if self._first is None:
                self._first = folder
            widget.addLine(folder)
        widget.list.setCurrentRow(0)

        container, parent = event.data
        if container is None or parent is None:
            return None
        
        container.addWidget(widget)

        if self._first is None:
            return None

        event = (widget.tr('%d folders found' % widget.list.count()), 10)
        kernel.dispatch('window.status', event)

        event = (self._first, self._search, None)
        kernel.dispatch('folder_select', event)
        
    @property
    @inject.params(widget='widget.folders')
    def selected(self, widget=None):
        if widget is None:
            return None
        return widget.selected

    @inject.params(kernel='kernel')
    def onActionFolderNew(self, event=None, widget=None, kernel=None):
        
        event = (('New folder', 'New folder description'), self)
        kernel.dispatch('folder_new', event)

    @inject.params(kernel='kernel')
    def onActionFolderCopy(self, event=None, widget=None, kernel=None):
        event = ((self.selected.name, 'New folder description'), self)
        kernel.dispatch('folder_new', event)

    @inject.params(kernel='kernel')
    def onActionFolderRemove(self, event=None, widget=None, kernel=None):
        message = widget.tr("Are you sure you want to remove this Folder?")
        reply = QtWidgets.QMessageBox.question(widget, 'Remove folder', message, QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.No:
            return None

        for index in widget.selectedIndexes():
            item = widget.itemFromIndex(index)
            if item is None and item.folder is None:
                continue

            folder = item.folder
            if folder is None:
                continue

            event = (folder, self)
            if folder.id is not None and folder.id:
                kernel.dispatch('folder_%s_remove' % folder.id, event)
            kernel.dispatch('folder_remove', event)

            widget.takeItem(index)
            
        event = (widget.tr('%d folders found' % widget.list.count()), None)
        kernel.dispatch('window.status', event)

    @inject.params(kernel='kernel', storage='storage')
    def onActionRefresh(self, event=None, kernel=None, storage=None, widget=None):
        current = widget.list.currentIndex()
        
        widget.list.clear()
        for entity in storage.folders():
            widget.addLine(entity)

        if widget.list.item(current.row()) not in [0]:
            widget.list.setCurrentIndex(current)

        event = (widget.tr('%d folders found' % widget.list.count()), None)
        kernel.dispatch('window.status', event)

    @inject.params(kernel='kernel')
    def onActionFolderOpen(self, event=None, selection=None, widget=None, kernel=None):
        event = (self.selected, self._search)
        kernel.dispatch('folder_open', event)

    @inject.params(kernel='kernel')
    def onActionFolderSelect(self, event=None, selection=None, widget=None, kernel=None):
        event = (self.selected, self._search, None)
        kernel.dispatch('folder_select', event)

    @inject.params(kernel='kernel', storage='storage')
    def onActionSearchRequest(self, event=None, kernel=None, storage=None, widget=None):
        self._search = event.data
        if self._search is None:
            return None

        self._first = None
        widget.list.clear()
        for entity in storage.folders(string=self._search):
            if self._first is None:
                self._first = entity
            widget.addLine(entity)
