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

from lib.plugin import Loader
from .gui.widget import FolderList
from .gui.editor.widget import TextEditorWidget  


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
        binder.bind_to_constructor('notepad', self._widget)
        """
        Initialize the widget of this plugin as a service
        this widget will be used in the main window 
        """
        binder.bind_to_provider('editor', self._widget_editor)

    @inject.params(kernel='kernel', config='config')
    def _widget_editor(self, kernel=None, config=None):
        widget = TextEditorWidget()
        widget.name.setVisible(int(config.get('editor.name')))
        widget.formatbar.setVisible(int(config.get('editor.formatbar')))
        widget.leftbar.setVisible(int(config.get('editor.leftbar')))
        widget.rightbar.setVisible(int(config.get('editor.rightbar')))

        event = (widget, widget.leftbar)
        kernel.dispatch('window.notepad.leftbar', event)

        event = (widget, widget.rightbar)
        kernel.dispatch('window.notepad.rightbar', event)

        event = (widget, widget.formatbar)
        kernel.dispatch('window.notepad.formatbar', event)

        action = functools.partial(self.onActionSave, widget=widget) 
        widget.leftbar.saveAction.clicked.connect(action)
        
        action = functools.partial(self.onActionFullScreen, widget=widget)
        widget.leftbar.fullscreenAction.clicked.connect(action)

        action = functools.partial(self.onActionConfigUpdatedEditor, widget=widget)
        kernel.listen('config_updated', action)

        return widget

    @inject.params(kernel='kernel', config='config', factory='settings_factory')
    def _widget(self, kernel=None, config=None, factory=None):
        
        widget = FolderList()
        widget.editor.name.setVisible(int(config.get('editor.name')))
        widget.editor.formatbar.setVisible(int(config.get('editor.formatbar')))
        widget.editor.leftbar.setVisible(int(config.get('editor.leftbar')))
        widget.editor.rightbar.setVisible(int(config.get('editor.rightbar')))

        event = (widget.editor, widget.editor.leftbar)
        kernel.dispatch('window.notepad.leftbar', event)

        event = (widget.editor, widget.editor.rightbar)
        kernel.dispatch('window.notepad.rightbar', event)

        event = (widget.editor, widget.editor.formatbar)
        kernel.dispatch('window.notepad.formatbar', event)

        action = functools.partial(self.onActionContextMenu, widget=widget)
        widget.tree.customContextMenuRequested.connect(action)
        
        action = functools.partial(self.onActionNoteSelect, widget=widget)
        widget.tree.clicked.connect(action)
        
        action = functools.partial(self.onActionFolderCopy, widget=widget)
        widget.toolbar.copyAction.clicked.connect(action)

        action = functools.partial(self.onActionExpand, widget=widget)
        widget.toolbar.expandAction.clicked.connect(action)

        action = functools.partial(self.onActionCollaps, widget=widget)
        widget.toolbar.collapseAction.clicked.connect(action)

        action = functools.partial(self.onActionFolderRemove, widget=widget)
        widget.toolbar.removeAction.clicked.connect(action)

        action = functools.partial(self.onActionSave, widget=widget.editor) 
        widget.editor.leftbar.saveAction.clicked.connect(action)
        
        action = functools.partial(self.onActionFullScreen, widget=widget)
        widget.editor.leftbar.fullscreenAction.clicked.connect(action)

        action = functools.partial(self.onActionNoteCreate, widget=widget)
        kernel.listen('note_new', action)

        action = functools.partial(self.onActionFolderCreate, widget=widget)
        kernel.listen('folder_new', action)

        action = functools.partial(self.onActionConfigUpdated, widget=widget)
        kernel.listen('config_updated', action)

        return widget

    def onActionContextMenu(self, event, widget):

        menu = QtWidgets.QMenu()

        index = widget.tree.index 
        if index is not None:
            name = widget.tree.model().data(index)

            action = functools.partial(self.onActionFullScreen, widget=widget)
            menu.addAction('Open note in new tab', action)
        
            action = functools.partial(self.onActionFolderCopy, widget=widget)
            menu.addAction('Clone \'%s\'' % name, action)
            
            action = functools.partial(self.onActionFolderRemove, widget=widget)
            menu.addAction('Remove \'%s\'' % name, action)

        action = functools.partial(self.onActionFolderCreate, widget=widget)
        menu.addAction('Create folder here', action)

        action = functools.partial(self.onActionNoteCreate, widget=widget)
        menu.addAction('Create note here', action)
        
        menu.exec_(widget.tree.mapToGlobal(event))

    @inject.params(storage='storage', config='config', note='storage.note')
    def onActionNoteCreate(self, event=None, widget=None, config=None, storage=None, note=None):
        if widget.editor is None:
            return None

        path = config.get('storage.location')
        if widget.tree.selected is not None:
            path = widget.tree.selected
            
        if os.path.isfile(path):
            path = os.path.dirname(path)

        note.name = 'New note'
        note.text = 'new note description'
        note.path = path
        
        if event is not None and event.data is not None:
            note.name, note.text = event.data
            
        storage.create(note)

    @inject.params(storage='storage', config='config', folder='storage.folder')
    def onActionFolderCreate(self, event=None, widget=None, config=None, storage=None, folder=None):
        if widget.editor is None:
            return None
        
        path = config.get('storage.location')
        if widget.tree.selected is not None:
            path = widget.tree.selected
            
        if os.path.isfile(path):
            path = os.path.dirname(path)
        
        folder.name = 'New folder'
        folder.path = path
        
        storage.create(folder)

    @inject.params(storage='storage')
    def onActionNoteSelect(self, event, widget, storage):
        if widget.tree is None:
            return None
        
        path = None
        if widget.tree.selected is not None:
            path = widget.tree.selected

        if path is None:
            return None

        note = storage.note(path)
        if note is None:
            return None
        
        widget.editor.note = note

    @inject.params(storage='storage')
    def onActionFolderCopy(self, event=None, widget=None, storage=None):
        if widget.tree is None:
            return None
        path = widget.tree.selected
        if path is not None:
            storage.clone(path)

    @inject.params(storage='storage')
    def onActionSave(self, event, widget, storage):
        note = widget._note
        note.name = widget.name.text() 
        note.text = widget._text.text.toHtml() 
        if note is not None:
            storage.update(note)
        
    @inject.params(kernel='kernel', storage='storage', editor='editor')
    def onActionFullScreen(self, event=None, widget=None, kernel=None, storage=None, editor=None):
        if widget.tree is None or editor is None:
            return None
        path = widget.tree.selected
        if path is None:
            return None
        
        note = storage.note(path)
        if note is None:
            return None
        
        editor.note = note

        event = (editor, note.name)
        kernel.dispatch('window.tab', event)

    @inject.params(storage='storage')
    def onActionFolderRemove(self, event=None, widget=None, storage=None):
        message = widget.tr("Are you sure you want to remove this Folder?")
        reply = QtWidgets.QMessageBox.question(widget, 'Remove folder', message, QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            path = widget.tree.selected
            if path is not None: 
                storage.delete(path)

    def onActionExpand(self, event=None, widget=None):
        if widget.tree is not None:
            widget.tree.expandAll()

    def onActionCollaps(self, event, widget):
        if widget.tree is not None:
            widget.tree.collapseAll()

    @inject.params(config='config', logger='logger')
    def onActionConfigUpdated(self, event, config=None, widget=None, logger=None):
        if widget is None or config is None:
            return None

        try:        
            visible = int(config.get('folders.toolbar'))
            widget.toolbar.setVisible(visible)
        except (AttributeError) as ex:
            logger.error(ex)

        try:        
            visible = int(config.get('folders.keywords'))
            widget.tags.setVisible(visible)
        except (AttributeError):
            pass
        
        self.onActionConfigUpdatedEditor(event, widget=widget.editor)

    @inject.params(config='config', logger='logger')
    def onActionConfigUpdatedEditor(self, event, widget=None, config=None, logger=None):

        try:        
            visible = int(config.get('editor.formatbar'))
            widget.formatbar.setVisible(visible)
        except (AttributeError):
            pass

        try:        
            visible = int(config.get('editor.leftbar'))
            widget.leftbar.setVisible(visible)
        except (AttributeError):
            pass
            
        try:        
            visible = int(config.get('editor.rightbar'))
            widget.rightbar.setVisible(visible)
        except (AttributeError):
            pass

        try:        
            visible = int(config.get('editor.name'))
            widget.name.setVisible(visible)
        except (AttributeError):
            pass

