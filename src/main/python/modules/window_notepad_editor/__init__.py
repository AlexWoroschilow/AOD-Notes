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

from .gui.editor.widget import TextEditorWidget
from .factory import ToolbarFactory


class Loader(object):
    actions = ModuleActions()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def enabled(self, options=None, args=None):
        return True

    @inject.params(config='config', factory_leftbar='toolbar_factory.leftbar', factory_rightbar='toolbar_factory.rightbar', factory_formatbar='toolbar_factory.formatbar')
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

        widget.fullscreen.connect(self.actions.onActionFullScreen)
        widget.save.connect(functools.partial(self.actions.onActionSave, widget=widget))

        return widget

    def configure(self, binder, options, args):

        binder.bind_to_provider('notepad.editor', self._notepad_editor)

        binder.bind('toolbar_factory.leftbar', ToolbarFactory())
        binder.bind('toolbar_factory.formatbar', ToolbarFactory())
        binder.bind('toolbar_factory.rightbar', ToolbarFactory())
