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
        
    @inject.params(config='config', storage='storage', kernel='kernel', widget='notepad')
    def note(self, index, config, storage, widget, kernel):
        for i in range(self.container.layout().count()): 
            self.container.layout().itemAt(i).widget().close()            

        if not storage.isFile(index):
            self.container.layout().addWidget(DemoWidget())
            return self
            
        self.editor = TextEditorWidget()
        self.editor.formatbar.setVisible(int(config.get('editor.formatbar')))
        self.editor.rightbar.setVisible(int(config.get('editor.rightbar')))
        self.editor.leftbar.setVisible(int(config.get('editor.leftbar')))
        
        kernel.dispatch('window.notepad.rightbar', (self.editor, self.editor.rightbar))
        kernel.dispatch('window.notepad.formatbar', (self.editor, self.editor.formatbar))
        kernel.dispatch('window.notepad.leftbar', (self.editor, self.editor.leftbar))
        
        action = functools.partial(self.actions.onActionSave, widget=widget)
        self.editor.leftbar.saveAction.clicked.connect(action)
        
        action = functools.partial(self.actions.onActionFullScreen, widget=widget)
        self.editor.leftbar.fullscreenAction.clicked.connect(action)
        
        self.editor.insertHtml(storage.fileContent(index))
        
        self.container.layout().addWidget(self.editor)
        return self

    @inject.params(storage='storage')
    def group(self, index, storage):
        for i in range(self.container.layout().count()): 
            self.container.layout().itemAt(i).widget().close()            

        widget = FolderViewWidget()
        for entity in storage.entities(index):
            content = storage.fileContent(entity)
            name = storage.fileName(entity)
            widget.addPreview(name, content)
        
        self.container.layout().addWidget(widget)
        return self
 
    def demo(self):
        for i in range(self.container.layout().count()): 
            self.container.layout().itemAt(i).widget().close()            
        self.container.layout().addWidget(DemoWidget())
        return self
 
