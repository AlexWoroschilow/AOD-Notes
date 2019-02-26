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
from .factory import ToolbarFactory


class Loader(Loader):
    
    actions = ModuleActions()

    @property
    def enabled(self):
        return True

    def config(self, binder=None):
        binder.bind('toolbar_factory.leftbar', ToolbarFactory())
        binder.bind('toolbar_factory.formatbar', ToolbarFactory())
        binder.bind('toolbar_factory.rightbar', ToolbarFactory())

        binder.bind_to_constructor('notepad', self._notepad)
        binder.bind_to_provider('editor', self._editor)

    @inject.params(config='config', storage='storage', notepad='notepad')
    def boot(self, options=None, args=None, config=None, storage=None, notepad=None):
        if not len(config.get('editor.current')):
            return notepad.note(storage.first())
        # get last edited document from the confnig
        # and open this document in the editor by default
        index = storage.index(config.get('editor.current'))
        if index is not None and storage.isDir(index):
            return notepad.group(index)
        
        if index is not None and storage.isFile(index):
            return notepad.note(index)

    @inject.params(kernel='kernel', config='config', factory_leftbar='toolbar_factory.leftbar', factory_rightbar='toolbar_factory.rightbar', factory_formatbar='toolbar_factory.formatbar')
    def _editor(self, kernel=None, config=None, factory_leftbar=None, factory_rightbar=None, factory_formatbar=None):
        
        widget = TextEditorWidget()

        for plugin in factory_leftbar.widgets:
            plugin.clicked.connect(functools.partial(plugin.clickedEvent, widget=widget))
            widget.leftbar.addWidget(plugin)
        widget.leftbar.setVisible(int(config.get('editor.leftbar')))
        
        for plugin in factory_formatbar.widgets:
            plugin.clicked.connect(functools.partial(plugin.clickedEvent, widget=widget))
            widget.formatbar.addWidget(plugin)
        widget.formatbar.setVisible(int(config.get('editor.formatbar')))

        for plugin in factory_rightbar.widgets:
            plugin.clicked.connect(functools.partial(plugin.clickedEvent, widget=widget))
            widget.rightbar.addWidget(plugin)
        widget.rightbar.setVisible(int(config.get('editor.rightbar')))
        
        action = functools.partial(self.actions.onActionSave, widget=widget)
        widget.save.connect(action)
        
        action = functools.partial(self.actions.onActionFullScreen, widget=widget)
        widget.fullscreen.connect(action)

        action = functools.partial(self.actions.onActionConfigUpdatedEditor, widget=widget)
        kernel.listen('config_updated', action)

        return widget

    @inject.params(kernel='kernel', storage='storage')
    def _notepad(self, kernel, storage):
        
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
