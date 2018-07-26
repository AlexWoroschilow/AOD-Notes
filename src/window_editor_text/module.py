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

from .gui.widget import TextEditorWidget


class Loader(Loader):

    @property
    def enabled(self):
        return True
    
    def config(self, binder=None):
        binder.bind_to_constructor('widget.editor', self._constructor_editor)
        binder.bind_to_provider('widget.editor_provider', self._constructor_editor)

    @inject.params(config='config', kernel='kernel')
    def _constructor_editor(self, parent=None, config=None, kernel=None):

        widget = TextEditorWidget(parent, config)
        
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
        
        return widget

    @inject.params(kernel='kernel')
    def onActionSave(self, event=None, widget=None, kernel=None):
        if widget.note is None:
            event = (widget.name, widget.text, widget.folder)
            return kernel.dispatch('note_new', event)

        widget.note.name = widget.name
        widget.note.text = widget.text

        kernel.dispatch('note_update', widget.note)
        kernel.dispatch(widget.note.unique, widget.note)
        
        folder = widget.note.folder
        if folder is None:
            return None
        kernel.dispatch(folder.id, folder)

    @inject.params(kernel='kernel', widget_new='widget.editor_provider')
    def onActionFullScreen(self, event=None, widget=None, kernel=None, widget_new=None):
        if widget is None or widget_new is None:
            return None
        
        widget_new.note = widget.note
        kernel.dispatch('window.tab', (widget_new, widget.note.name))
