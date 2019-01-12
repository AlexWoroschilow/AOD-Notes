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
    def _widget_editor(self, kernel, config):
        
        widget = TextEditorWidget()
        
        widget.leftbar.setVisible(int(config.get('editor.leftbar')))
        widget.formatbar.setVisible(int(config.get('editor.formatbar')))
        widget.rightbar.setVisible(int(config.get('editor.rightbar')))
        
        kernel.dispatch('window.notepad.leftbar', (widget, widget.leftbar))
        kernel.dispatch('window.notepad.rightbar', (widget, widget.rightbar))
        kernel.dispatch('window.notepad.formatbar', (widget, widget.formatbar))

        action = functools.partial(self.actions.onActionSave, widget=widget)
        widget.save.connect(action)
        
        action = functools.partial(self.actions.onActionFullScreen, widget=widget)
        widget.fullscreen.connect(action)

        action = functools.partial(self.actions.onActionConfigUpdatedEditor, widget=widget)
        kernel.listen('config_updated', action)

        return widget

    @inject.params(kernel='kernel', storage='storage')
    def _widget(self, kernel, storage):
        
        widget = FolderList(self.actions)
        
        action = functools.partial(self.actions.onActionNoteEdit, widget=widget)
        widget.edit.connect(action)

        action = functools.partial(self.actions.onActionCopy, widget=widget)
        widget.clone.connect(action)

        action = functools.partial(self.actions.onActionDelete, widget=widget)
        widget.delete.connect(action)

        action = functools.partial(self.actions.onActionFileRenamed, widget=widget)
        storage.fileRenamed.connect(action)

        action = functools.partial(self.actions.onActionContextMenu, widget=widget)
        widget.tree.customContextMenuRequested.connect(action)
        
        action = functools.partial(self.actions.onActionNoteSelect, widget=widget)
        widget.tree.clicked.connect(action)
        
        action = functools.partial(self.actions.onActionClone, widget=widget)
        widget.toolbar.copyAction.clicked.connect(action)

        action = functools.partial(self.actions.onActionExpand, widget=widget)
        widget.toolbar.expandAction.clicked.connect(action)

        action = functools.partial(self.actions.onActionCollaps, widget=widget)
        widget.toolbar.collapseAction.clicked.connect(action)

        action = functools.partial(self.actions.onActionRemove, widget=widget)
        widget.toolbar.removeAction.clicked.connect(action)

        action = functools.partial(self.actions.onActionConfigUpdated, widget=widget)
        kernel.listen('config_updated', action)

        return widget
