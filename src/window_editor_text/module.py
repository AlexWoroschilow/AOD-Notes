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
        binder.bind_to_constructor('widget.editor', self._constructor_widget_editor)
        binder.bind_to_provider('widget.editor_provider', self._constructor_widget_editor)

    @inject.params(config='config', kernel='kernel')
    def _constructor_widget_editor(self, parent=None, config=None, kernel=None):

        widget = TextEditorWidget(parent, config)
        
        widget.leftbar.saveAction.clicked.connect(functools.partial(
            self.onActionSave, widget=widget
        ))
        
        widget.leftbar.fullscreenAction.clicked.connect(functools.partial(
            self.onActionFullScreen, widget=widget
        ))
        
        widget.formatbar.folderSelector.currentIndexChanged.connect(functools.partial(
            self.onActionFolderChange, widget=widget
        ))

        kernel.listen('folder_update', widget.formatbar.folderSelector.onFolderUpdate, 128)
        kernel.listen('folder_remove', widget.formatbar.folderSelector.onFolderRemove, 128)
        kernel.listen('folder_new', widget.formatbar.folderSelector.onFolderNew, 128)

        kernel.listen('note_update', functools.partial(
            self.onActionNoteUpdate, current=widget
        ), 128)
        
        return widget

    def onActionNoteUpdate(self, event=None, current=None):
        note, widget = event.data
        if widget == current or note is None :
            return None
        if current.note == note:
            current.note = note

    @inject.params(kernel='kernel')
    def onActionSave(self, event=None, widget=None, kernel=None):
        if widget.note is None:
            event = (widget.name, widget.text, widget.folder)
            return kernel.dispatch('note_new', event)

        widget.note.name = widget.name
        widget.note.description = widget.description
        widget.note.folder = widget.folder
        widget.note.text = widget.text

        event = (widget.note, widget)
        kernel.dispatch('note_update', event)
        
        if widget.note.id is not None and widget.note.id:
            kernel.dispatch('note_%s_update' % widget.note.id, event)
        
        folder = widget.note.folder
        if folder is None:
            return None

        if folder.id is not None and folder.id:
            event = (folder, widget)
            kernel.dispatch('folder_%s_update' % folder.id, event)

    @inject.params(kernel='kernel', widget_new='widget.editor_provider')
    def onActionFullScreen(self, event=None, widget=None, kernel=None, widget_new=None):
        if widget is None or widget_new is None:
            return None
        
        widget_new.note = widget.note
        event = (widget_new, widget.note)
        kernel.dispatch('window.tab', event)
        
    @inject.params(kernel='kernel')
    def onActionFolderChange(self, event=None, widget=None, kernel=None):
        if widget is None:
            return None
        
        cache = widget.note.folder
        folder = widget.folder
        
        widget.note.folder = widget.folder
        
        event = (widget.note, self)
        kernel.dispatch('note_update', event)
        if widget.note.id is not None and widget.note.id:
            kernel.dispatch('note_%s_update' % widget.note.id, event)

        if folder is None:
            return None

        event = (folder, self)
        kernel.dispatch('folder_%s_update' % folder.id, event)
        
        if cache is None:
            return None
        
        event = (cache, self)
        kernel.dispatch('folder_%s_update' % cache.id, event)
