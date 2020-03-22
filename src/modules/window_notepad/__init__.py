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

from .gui.window import MainWindow
from .actions import ModuleActions


class Loader(object):
    actions = ModuleActions()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    @inject.params(store='store', notepad='notepad')
    def _constructor_window(self, store=None, notepad=None):
        widget = MainWindow()
        widget.resize.connect(self.actions.onActionWindowResize)
        widget.setMainWidget(notepad)

        store.subscribe(self.update)

        return widget

    def enabled(self, options=None, args=None):
        return options.console is None

    def configure(self, binder, options, args):
        binder.bind_to_constructor('window', self._constructor_window)

    @inject.params(store='store', window='window')
    def update(self, store=None, window=None):
        state = store.get_state()
        if state is None: return None
