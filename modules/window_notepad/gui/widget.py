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

from .bar import ToolBarWidget

from .tags import TagsEditor
from .folders import FolderTree
from .editor.widget import TextEditorWidget


class FolderList(QtWidgets.QSplitter):

    @inject.params(config='config')
    def __init__(self, config):
        super(FolderList, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)

        self.setObjectName('FolderList')

        containerLayout = QtWidgets.QGridLayout()
        containerLayout.setContentsMargins(0, 0, 0, 0)
        containerLayout.setSpacing(0)

        self.toolbar = ToolBarWidget(self)
        containerLayout.addWidget(self.toolbar, 0, 0, 3, 1)
        
        self.tree = FolderTree()
        containerLayout.addWidget(self.tree, 0, 1)

        self.tags = TagsEditor()
        self.tags.setVisible(int(config.get('folders.keywords')))
        containerLayout.addWidget(self.tags, 1, 1)

        container = QtWidgets.QWidget()
        container.setContentsMargins(0, 0, 0, 0)

        container.setLayout(containerLayout)
        self.addWidget(container)

        self.editor = TextEditorWidget()
        self.addWidget(self.editor)
        
        self.setCollapsible(0, True)
        self.setCollapsible(1, False)
        self.setCollapsible(2, False)
        
        self.setStretchFactor(0, 4)
        self.setStretchFactor(1, 5)
        
