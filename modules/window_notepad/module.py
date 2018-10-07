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

from lib.plugin import Loader
from .gui.widget import FolderList
from .gui.editor.widget import TextEditorWidget  

from .actions import ModuleActions


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

        widget.leftbar.saveAction.clicked.connect(functools.partial(
            self.actions.onActionSave, widget=widget
        ))
        
        widget.leftbar.fullscreenAction.clicked.connect(functools.partial(
            self.actions.onActionFullScreen, widget=widget
        ))

        kernel.listen('config_updated', functools.partial(
            self.actions.onActionConfigUpdatedEditor, widget=widget
        ))

        return widget

    @inject.params(kernel='kernel', config='config', storage='storage', factory='settings_factory')
    def _widget(self, kernel=None, config=None, storage=None, factory=None):
        
        widget = FolderList(self.actions)

        storage.fileRenamed.connect(functools.partial(
            self.actions.onActionNoteRefresh, widget=widget
        ))

        widget.tree.customContextMenuRequested.connect(functools.partial(
            self.actions.onActionContextMenu, widget=widget
        ))
        
        widget.tree.clicked.connect(functools.partial(
            self.actions.onActionNoteSelect, widget=widget
        ))
        
        widget.toolbar.copyAction.clicked.connect(functools.partial(
            self.actions.onActionClone, widget=widget
        ))

        widget.toolbar.expandAction.clicked.connect(functools.partial(
            self.actions.onActionExpand, widget=widget
        ))

        widget.toolbar.collapseAction.clicked.connect(functools.partial(
            self.actions.onActionCollaps, widget=widget
        ))

        widget.toolbar.removeAction.clicked.connect(functools.partial(
            self.actions.onActionRemove, widget=widget
        ))

        kernel.listen('note_new', functools.partial(
            self.actions.onActionNoteCreate, widget=widget
        ))

        kernel.listen('folder_new', functools.partial(
            self.actions.onActionFolderCreate, widget=widget
        ))

        kernel.listen('config_updated', functools.partial(
            self.actions.onActionConfigUpdated, widget=widget
        ))

        return widget
