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

from .actions import ModuleActions
from .factory import ToolbarFactory

from .gui.dashboard import NotepadDashboard
from .gui.editor.widget import TextEditorWidget


class Loader(object):
    actions = ModuleActions()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    @inject.params(config='config', dashboard='notepad.dashboard')
    def _notepad_tab(self, config=None, dashboard=None):
        if dashboard is None:
            return None

        from .gui.tab import Notepad

        content = Notepad()
        content.addTab(dashboard, content.tr('Dashboard'))

        return content

    @inject.params(config='config', factory_leftbar='toolbar_factory.leftbar',
                   factory_rightbar='toolbar_factory.rightbar', factory_formatbar='toolbar_factory.formatbar')
    def _notepad_editor(self, config=None, factory_leftbar=None, factory_rightbar=None, factory_formatbar=None):

        widget = TextEditorWidget()

        for plugin in factory_leftbar.widgets:
            if hasattr(plugin, 'clickedEvent') and callable(plugin.clickedEvent):
                plugin.clicked.connect(functools.partial(plugin.clickedEvent, widget=widget))
            widget.leftbar.addWidget(plugin)
        widget.leftbar.setVisible(int(config.get('editor.leftbar')))

        for plugin in factory_formatbar.widgets:
            if hasattr(plugin, 'clickedEvent') and callable(plugin.clickedEvent):
                plugin.clicked.connect(functools.partial(plugin.clickedEvent, widget=widget))
            widget.formatbar.addWidget(plugin)
        widget.formatbar.setVisible(int(config.get('editor.formatbar')))

        for plugin in factory_rightbar.widgets:
            if hasattr(plugin, 'clickedEvent') and callable(plugin.clickedEvent):
                plugin.clicked.connect(functools.partial(plugin.clickedEvent, widget=widget))
            widget.rightbar.addWidget(plugin)
        widget.rightbar.setVisible(int(config.get('editor.rightbar')))

        widget.fullscreen.connect(functools.partial(self.actions.onActionFullScreen, widget=widget))
        widget.save.connect(functools.partial(self.actions.onActionSave, widget=widget))

        return widget

    @inject.params(config='config', storage='storage')
    def _notepad_dashboard(self, config, storage, binder):

        widget = NotepadDashboard()
        widget.storage_changed.connect(functools.partial(self.actions.onActionStorageChanged, widget=widget))
        widget.note_new.connect(functools.partial(self.actions.onActionNoteCreate, widget=widget))
        widget.note_import.connect(functools.partial(self.actions.onActionNoteImport, widget=widget))
        widget.group_new.connect(functools.partial(self.actions.onActionFolderCreate, widget=widget))
        widget.clone.connect(functools.partial(self.actions.onActionCopy, widget=widget))
        widget.delete.connect(functools.partial(self.actions.onActionDelete, widget=widget))
        widget.menu.connect(functools.partial(self.actions.onActionContextMenu, widget=widget))

        return widget

    def enabled(self, options=None, args=None):
        return options.console is None

    def configure(self, binder, options, args):
        binder.bind('toolbar_factory.leftbar', ToolbarFactory())
        binder.bind('toolbar_factory.formatbar', ToolbarFactory())
        binder.bind('toolbar_factory.rightbar', ToolbarFactory())

        binder.bind_to_provider('notepad', self._notepad_tab)
        binder.bind_to_provider('notepad.editor', self._notepad_editor)

        binder.bind_to_constructor('notepad.dashboard', functools.partial(
            self._notepad_dashboard, binder=binder
        ))

    @inject.params(config='config', storage='storage', dashboard='notepad.dashboard')
    def boot(self, options=None, args=None, config=None, storage=None, dashboard=None):

        current = config.get('editor.current')
        if current is None or not len(current):
            return dashboard.note(storage.first())

        # get last edited document from the confnig
        # and open this document in the editor by default
        index = storage.index(current)
        if index is None: return None

        if storage.isDir(index):
            return dashboard.group(index)
        return dashboard.note(index)
