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

from PyQt5 import QtWidgets

from .bar import ToolBarWidget

from .tags import TagsEditor
from .folders import FolderTree
from .demo.widget import DemoWidget
from .folder.widget import FolderViewWidget
from .editor.widget import TextEditorWidget


class FolderList(QtWidgets.QSplitter):

    @inject.params(config='config')
    def __init__(self, actions, config):
        super(FolderList, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.setObjectName('FolderList')
        
        containerLayout = QtWidgets.QGridLayout()
        containerLayout.setContentsMargins(0, 0, 0, 0)
        containerLayout.setSpacing(0)

        self.toolbar = ToolBarWidget(self)
        containerLayout.addWidget(self.toolbar, 0, 0, 3, 1)
        
        self.tree = FolderTree()
        self.tree.expandAll()

        containerLayout.addWidget(self.tree, 0, 1)

        self.tags = TagsEditor()
        self.tags.setVisible(int(config.get('folders.keywords')))
        containerLayout.addWidget(self.tags, 1, 1)

        container = QtWidgets.QWidget()
        container.setContentsMargins(0, 0, 0, 0)

        container.setLayout(containerLayout)
        self.addWidget(container)

        self.container = QtWidgets.QWidget()
        self.container.setLayout(QtWidgets.QVBoxLayout())
        self.container.layout().addWidget(DemoWidget())

        self.addWidget(self.container)
        
        self.setCollapsible(0, True)
        self.setCollapsible(1, False)
        self.setCollapsible(2, False)

        self.setStretchFactor(0, 4)
        self.setStretchFactor(1, 5)
        
        self.actions = actions
        self.test = None
        
    @inject.params(config='config', kernel='kernel', widget='notepad')
    def entity(self, entity, config, kernel, widget):
        for i in range(self.container.layout().count()): 
            self.container.layout().itemAt(i).widget().close()            

        if (entity.__class__.__name__ == 'Note'):
            self.editor = TextEditorWidget()
            self.editor.name.setVisible(int(config.get('editor.name')))
            self.editor.formatbar.setVisible(int(config.get('editor.formatbar')))
            self.editor.rightbar.setVisible(int(config.get('editor.rightbar')))
            self.editor.leftbar.setVisible(int(config.get('editor.leftbar')))

            kernel.dispatch('window.notepad.rightbar', (self.editor, self.editor.rightbar))
            self.editor.leftbar.saveAction.clicked.connect(functools.partial(
                self.actions.onActionSave, widget=self.editor
            ))
            kernel.dispatch('window.notepad.formatbar', (self.editor, self.editor.formatbar))
            self.editor.leftbar.fullscreenAction.clicked.connect(functools.partial(
                self.actions.onActionFullScreen, widget=widget
            ))
            kernel.dispatch('window.notepad.leftbar', (self.editor, self.editor.leftbar))

            self.editor.note = entity

            self.container.layout().addWidget(self.editor)
            return self

        if (entity.__class__.__name__ == 'Folder'):
            self.container.layout().addWidget(FolderViewWidget(entity))
            return self

        self.container.layout().addWidget(DemoWidget())
        return self
