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
from .gui.tab import Notepad


class Loader(object):
    actions = ModuleActions()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    @inject.params(dashboard='notepad.dashboard')
    def _notepad_tab(self, dashboard=None):
        widget = Notepad()
        widget.addTab(dashboard, 'Dashboard')

        return widget

    def _notepad_dashboard(self, binder):
        widget = NotepadDashboard()
        widget.newNoteAction.connect(self.actions.onActionCreateNote)
        widget.importNoteAction.connect(self.actions.onActionNoteImport)
        widget.newGroupAction.connect(self.actions.onActionCreateGroup)
        widget.groupAction.connect(self.actions.onActionGroup)
        widget.fullscreenNoteAction.connect(self.actions.onActionFullScreen)
        widget.saveNoteAction.connect(self.actions.onActionSaveNote)
        widget.selectNoteAction.connect(self.actions.onActionSelectNote)
        widget.editNoteAction.connect(self.actions.onActionEditNote)
        widget.removeNoteAction.connect(self.actions.onActionRemove)
        widget.renameNoteAction.connect(self.actions.onActionRename)
        widget.cloneNoteAction.connect(self.actions.onActionClone)
        widget.cloneNoteAction.connect(self.actions.onActionClone)
        widget.renameAction.connect(self.actions.onActionRename)
        widget.moveNoteAction.connect(self.actions.onActionMoveNote)
        widget.menuAction.connect(self.actions.onActionContextMenu)
        widget.moveAction.connect(self.actions.onActionMove)
        widget.updateAction.connect(self.actions.onActionUpdate)
        widget.searchAction.connect(self.actions.onActionSearch)

        return widget

    def enabled(self, options=None, args=None):
        return options.console is None

    def configure(self, binder, options, args):
        binder.bind_to_provider('notepad', self._notepad_tab)
        binder.bind_to_constructor('notepad.dashboard', functools.partial(
            self._notepad_dashboard, binder=binder
        ))

    @inject.params(store='store', dashboard='notepad.dashboard')
    def boot(self, options=None, args=None, store=None, dashboard=None):
        store.subscribe(dashboard.updateAction.emit)
