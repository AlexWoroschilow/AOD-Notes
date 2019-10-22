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
import os
import inject
import functools
from logging import getLogger

from PyQt5 import QtWidgets
from PyQt5 import QtGui
import platform


class ModuleActions(object):

    @inject.params(storage='storage', dashboard='notepad.dashboard', status='status')
    def onActionSave(self, event, storage, dashboard, status, widget):
        try:

            index, document = event
            if index is None:
                return None

            index = storage.setFileContent(index, document.toHtml())
            if index is None:
                return None

            dashboard.updated.emit(index)

        except Exception as ex:
            getLogger('app').exception(ex)
            status.error(ex.__str__())

    @inject.params(window='window', storage='storage')
    def onActionFullScreen(self, event, window, storage):
        try:
            index, document = event
            editor = inject.instance('notepad.editor')
            editor.setIndex(index)
            editor.setDocument(document)

            window.tab.emit((editor, storage.fileName(index)))

        except Exception as ex:
            getLogger('app').exception(ex)
