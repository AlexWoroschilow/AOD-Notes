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
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.Qt import Qt

from lib.plugin import Loader
from .gui.widget import SearchField


class Loader(Loader):
    @property
    def enabled(self):
        """

        :return:
        """
        return True

    def config(self, binder=None):
        """

        :param binder:
        :return:
        """

    @inject.params(dispatcher='event_dispatcher')
    def boot(self, dispatcher=None):
        """

        :param dispatcher:.
        :return:.
        """
        dispatcher.add_listener('window.header.content', self._onWindowHeader)

    @inject.params(storage='storage')
    def _onNotepadFolderNew(self, event=None, dispather=None, storage=None):
        """

        :param event: 
        :param dispather: 
        :return: 
        """
        name, description = event.data
        storage.addFolder(name, description)

    @inject.params(storage='storage')
    def _onWindowHeader(self, event=None, dispather=None, storage=None):
        """

        :param event: 
        :param dispather: 
        :return: 

        """
        self._container, self._parent = event.data
        if self._container is None:
            return None

        self._widget = SearchField()
        self._widget.returnPressed.connect(self._OnSearchRequestEvent)

        self._action1 = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+f"), self._widget)
        self._action1.activated.connect(self._onShortcutSearchStart)

        # self.action2 = QtWidgets.QShortcut(QtGui.QKeySequence("ESC"), self._widget)
        # self.action2.activated.connect(self._onShortcutSearchClean)

        self._container.addWidget(self._widget)

    @inject.params(dispather='event_dispatcher')
    def _OnSearchRequestEvent(self, event=None, dispather=None):
        """

        :param event: 
        :return: 
        """
        dispather.dispatch('window.search.request', self._widget.text())

    @inject.params(dispather='event_dispatcher')
    def _onShortcutSearchStart(self, event=None, dispather=None):
        """

        :param event: 
        :return: 
        """
        if self._widget is None:
            return None

        self._widget.setFocusPolicy(Qt.StrongFocus)
        self._widget.setFocus()

    @inject.params(dispather='event_dispatcher')
    def _onShortcutSearchClean(self, event=None, dispather=None):
        """

        :return: 
        """
        if self._widget is None:
            return None

        self._widget.setText("")

        dispather.dispatch('window.search.request', self._widget.text())
