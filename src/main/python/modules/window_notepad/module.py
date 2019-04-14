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

        binder.bind_to_provider('notepad', self._notepad)
        binder.bind_to_provider('notepad.editor', self._notepad_editor)

        binder.bind_to_constructor('notepad.dashboard', self._notepad_dashboard)

    @inject.params(config='config', storage='storage', dashboard='notepad.dashboard')
    def boot(self, options=None, args=None, config=None, storage=None, dashboard=None):
        if config is None: return None
        if dashboard is None: return None
        if storage is None: return None

        current = config.get('editor.current')
        if not len(current): return dashboard.note(storage.first())
        # get last edited document from the confnig
        # and open this document in the editor by default
        index = storage.index(current)
        if index is None: return None

        if storage.isDir(index): return dashboard.group(index)
        if storage.isFile(index): return dashboard.note(index)

    @inject.params(config='config', dashboard='notepad.dashboard')
    def _notepad(self, config=None, dashboard=None):
        if not len(config.get('storage.location')): return None

        if dashboard is None: return None

        from .gui.dashboard import Notepad
        content = Notepad()
        content.addTab(dashboard, content.tr('Dashboard'))
        return content

    @inject.params(kernel='kernel', config='config', factory_leftbar='toolbar_factory.leftbar', factory_rightbar='toolbar_factory.rightbar', factory_formatbar='toolbar_factory.formatbar')
    def _notepad_editor(self, kernel=None, config=None, factory_leftbar=None, factory_rightbar=None, factory_formatbar=None):
        if not len(config.get('storage.location')): return None

        from .gui.editor.widget import TextEditorWidget

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

    @inject.params(kernel='kernel', config='config', storage='storage')
    def _notepad_dashboard(self, kernel, config, storage):
        if not len(config.get('storage.location')): return None

        from .gui.widget import NotepadDashboard

        widget = NotepadDashboard(self.actions)

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
