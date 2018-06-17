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

from PyQt5 import QtWidgets


class WindowContentDashboard(QtWidgets.QWidget):

    @inject.params(kernel='kernel', logger='logger')
    def __init__(self, parent=None, kernel=None, logger=None):
        super(WindowContentDashboard, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setObjectName('dashboard')
        
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.content = QtWidgets.QSplitter()
        self.content.setContentsMargins(0, 0, 0, 0)

        # fill tabs with widgets from different modules
        kernel.dispatch('dashboard_content', (
            self.content, parent
        ))

        layout.addWidget(self.content)

        self.setLayout(layout)

    @property
    def entity(self):
        return None


class WindowContent(QtWidgets.QTabWidget):

    @inject.params(kernel='kernel', logger='logger')
    def __init__(self, parent=None, kernel=None, logger=None):
        super(WindowContent, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        
        self.setTabPosition(QtWidgets.QTabWidget.West)
        self.tabCloseRequested.connect(self._onTabClose)

        self.addTab(WindowContentDashboard(parent), self.tr('Dashboard'))
        self.setTabsClosable(True)

        kernel.listen('window.tab', self._onTabOpen)
        kernel.listen('note_update', self._onNoteUpdateEvent, 128)
        kernel.listen('folder_update', self._onNoteUpdateEvent, 128)

    def _onNoteUpdateEvent(self, event):
        entity, widget = event.data
        if entity is None or widget is None:
            return None 
        for index in range(0, self.count()):
            widget = self.widget(index)
            if widget.entity is None:
                continue
            if type(widget.entity) != type(entity):
                continue            
            if widget.entity != entity:
                continue
            self.setTabText(index, entity.name)

    def _onTabOpen(self, event=None, dispatcher=None):
        widget, entity = event.data
        if widget is None or entity is None:
            return None

        self.addTab(widget, entity.name)
        self.setCurrentIndex(self.indexOf(widget))

    def _onTabClose(self, index=None):
        if index in [0]:
            return None
        widget = self.widget(index)
        if widget is not None:
            widget.deleteLater()
        self.removeTab(index)
