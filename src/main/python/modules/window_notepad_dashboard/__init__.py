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

from .gui.dashboard import NotepadDashboard


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

    @inject.params(config='config', storage='storage')
    def _notepad_dashboard(self, config, storage, binder):
        widget = NotepadDashboard()
        widget.newNoteAction.connect(self.actions.onActionCreateNote)
        widget.newGroupAction.connect(self.actions.onActionCreateGroup)
        widget.fullscreenNoteAction.connect(self.actions.onActionFullScreen)
        widget.saveNoteAction.connect(self.actions.onActionSaveNote)
        widget.editNoteAction.connect(self.actions.onActionEditNote)
        widget.removeNoteAction.connect(self.actions.onActionRemove)
        widget.cloneNoteAction.connect(self.actions.onActionClone)
        widget.cloneNoteAction.connect(self.actions.onActionClone)
        widget.renameAction.connect(self.actions.onActionRename)
        widget.menuAction.connect(functools.partial(self.actions.onActionContextMenu, widget=widget))
        # widget.importNoteAction.connect(self.actions.onActionNoteImport)
        # widget.fullscreen.connect(functools.partial(self.actions.onActionFullScreen, widget=widget))
        # widget.storage_changed.connect(functools.partial(self.actions.onActionStorageChanged, widget=widget))
        # widget.note_new.connect(functools.partial(self.actions.onActionNoteCreate, widget=widget))
        # widget.note_import.connect(functools.partial(self.actions.onActionNoteImport, widget=widget))
        # widget.group_new.connect(functools.partial(self.actions.onActionFolderCreate, widget=widget))
        # widget.clone.connect(functools.partial(self.actions.onActionCopy, widget=widget))
        # widget.delete.connect(functools.partial(self.actions.onActionDelete, widget=widget))

        return widget

    def enabled(self, options=None, args=None):
        return options.console is None

    def configure(self, binder, options, args):
        binder.bind_to_provider('notepad', self._notepad_tab)
        binder.bind_to_constructor('notepad.dashboard', functools.partial(
            self._notepad_dashboard, binder=binder
        ))

    @inject.params(dashboard='notepad.dashboard')
    def boot(self, options=None, args=None, dashboard=None):
        pass
