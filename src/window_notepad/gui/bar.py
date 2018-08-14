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

from PyQt5.Qt import Qt
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui

from lib.widget.button import ToolBarButton


class TestAction(QtWidgets.QWidgetAction):

    @inject.params(config='config')
    def __init__(self, parent, config):
        QtWidgets.QWidgetAction.__init__(self, parent)
        
        layout = QtWidgets.QGridLayout()

        self.clone = QtWidgets.QCheckBox('Show button "Clone" (restart required)')
        layout.addWidget(self.clone, 0, 1)
        
        self.expand = QtWidgets.QCheckBox('Show button "Expand" (restart required)')
        layout.addWidget(self.expand, 1, 1)
        
        self.collapse = QtWidgets.QCheckBox('Show button "Collapse" (restart required)')
        layout.addWidget(self.collapse, 2, 1)
        
        self.remove = QtWidgets.QCheckBox('Show button "Remove" (restart required)')
        layout.addWidget(self.remove, 3, 1)

        self.tags = QtWidgets.QCheckBox('Show keywords')
        layout.addWidget(self.tags, 4, 1)
        
        self.toolbar = QtWidgets.QCheckBox('Show toolbar')
        layout.addWidget(self.toolbar, 5, 1)
        
        container = QtWidgets.QWidget()
        container.setContentsMargins(0, 0, 0, 0)
        container.setLayout(layout)
        
        self.setDefaultWidget(container)


class ToolBarWidget(QtWidgets.QToolBar):

    @inject.params(config='config')
    def __init__(self, parent=None, config=None):
        self.parent = parent
        super(ToolBarWidget, self).__init__(parent)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.onActionContextMenu)
        
        self.setObjectName('ToolBarWidget')
        self.setContentsMargins(0, 0, 0, 0)
        self.setOrientation(Qt.Vertical)
        self.setMaximumWidth(35)

        self.setVisible(int(config.get('folders.toolbar')))
        
        self.copyAction = ToolBarButton()
        self.copyAction.setIcon(QtGui.QIcon("icons/copy-light.svg"))
        self.copyAction.setVisible(int(config.get('folders.buttonClone')))
        self.copyAction.setToolTip("Clone selected folder")
        self.copyAction.setShortcut("Ctrl+C")
        self.addWidget(self.copyAction)

        self.expandAction = ToolBarButton()
        self.expandAction.setIcon(QtGui.QIcon("icons/plus-light.svg"))
        self.expandAction.setVisible(int(config.get('folders.buttonExpand')))
        self.expandAction.setToolTip("Expand all folders")
        self.addWidget(self.expandAction)

        self.collapseAction = ToolBarButton()
        self.collapseAction.setIcon(QtGui.QIcon("icons/minus-light.svg"))
        self.collapseAction.setVisible(int(config.get('folders.buttonCollapse')))
        self.collapseAction.setToolTip("Collaps all folders")
        self.addWidget(self.collapseAction)

        self.removeAction = ToolBarButton()
        self.removeAction.setIcon(QtGui.QIcon("icons/remove-light.svg"))
        self.removeAction.setVisible(int(config.get('folders.buttonRemove')))
        self.removeAction.setToolTip("Remove selected folder")
        self.removeAction.setShortcut("Del")
        self.addWidget(self.removeAction)
        
    @inject.params(config='config')
    def onActionContextMenu(self, event, config):

        menu = QtWidgets.QMenu()

        widget = TestAction(menu)
        widget.clone.setChecked(int(config.get('folders.buttonClone')))
        widget.clone.stateChanged.connect(functools.partial(
            self.onActionToggle,
            property='folders.buttonClone',
            widget=self.copyAction
        ))

        widget.expand.setChecked(int(config.get('folders.buttonExpand')))
        widget.expand.stateChanged.connect(functools.partial(
            self.onActionToggle,
            property='folders.buttonExpand',
            widget=self.expandAction
        ))

        widget.collapse.setChecked(int(config.get('folders.buttonCollapse')))
        widget.collapse.stateChanged.connect(functools.partial(
            self.onActionToggle,
            property='folders.buttonCollapse',
            widget=self.collapseAction
        ))

        widget.remove.setChecked(int(config.get('folders.buttonRemove')))
        widget.remove.stateChanged.connect(functools.partial(
            self.onActionToggle,
            property='folders.buttonRemove',
            widget=self.removeAction
        ))

        widget.tags.setChecked(int(config.get('folders.toolbarTags')))
        widget.tags.stateChanged.connect(functools.partial(
            self.onActionToggle,
            property='folders.toolbarTags',
            widget=self.parent.tags
        ))

        widget.toolbar.setChecked(int(config.get('folders.toolbar')))
        widget.toolbar.stateChanged.connect(functools.partial(
            self.onActionToggle,
            property='folders.toolbar',
            widget=self
        ))
        
        menu.addAction(widget)
        menu.exec_(self.mapToGlobal(event))

    @inject.params(config='config')
    def onActionToggle(self, status, widget, property, config):
        config.set(property, '%s' % status)
        widget.setVisible(int(config.get(property)))
        
        self.removeAction.setHidden(True)
