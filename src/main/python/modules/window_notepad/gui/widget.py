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
from PyQt5 import QtCore

from .folders import FolderTree
from .demo.widget import DemoWidget
from .folder.widget import FolderViewWidget
from .bar import FolderTreeToolBar


class NotepadDashboard(QtWidgets.QSplitter):

    edit = QtCore.pyqtSignal(object)
    delete = QtCore.pyqtSignal(object)
    clone = QtCore.pyqtSignal(object)

    saveAction = QtCore.pyqtSignal(object)
    fullscreenAction = QtCore.pyqtSignal(object)
    editor = None

    @inject.params(config='config', storage='storage')
    def __init__(self, actions, config, storage):
        super(NotepadDashboard, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)
        
        containerLayout = QtWidgets.QGridLayout()
        containerLayout.setContentsMargins(0, 0, 0, 0)
        containerLayout.setSpacing(0)

        self.toolbar = FolderTreeToolBar(self)
        containerLayout.addWidget(self.toolbar, 0, 0, 3, 1)
        
        self.tree = FolderTree()
        self.tree.expandAll()

        containerLayout.addWidget(self.tree, 0, 1)

        container = QtWidgets.QWidget()
        
        container.setContentsMargins(0, 0, 0, 0)

        container.setLayout(containerLayout)
        self.addWidget(container)

        self.container = QtWidgets.QWidget()
        self.container.setObjectName('FolderListContainer')
        self.container.setLayout(QtWidgets.QVBoxLayout())

        self.addWidget(self.container)
        
        self.setCollapsible(0, True)
        self.setCollapsible(1, False)
        self.setCollapsible(2, False)

        self.setStretchFactor(1, 2)
        self.setStretchFactor(2, 3)
        
        self.actions = actions
        self.test = None
        
    @property
    def current(self):
        injector = inject.get_injector()
        storage = injector.get_instance('storage')
        if len(storage.filePath(self.tree.currentIndex())):
            return self.tree.currentIndex()
        return storage.rootIndex()
        
    @inject.params(storage='storage', editor='notepad.editor', config='config')
    def note(self, index, storage, editor, config=None):
        current = storage.filePath(index)
        config.set('editor.current', current)
        
        layout = self.container.layout()
        for i in range(layout.count()): 
            layout.itemAt(i).widget().close()            

        if not storage.isFile(index):
            layout.addWidget(DemoWidget())
            return self

        self.editor = editor            
        self.editor.index = index
        layout.addWidget(self.editor)
        
        if self.current == index: return self 
        # highlight the current note if the  
        # selected not and editable not are different
        # this happens of the edition was started programmatically
        # or in any other way except the folder tree view
        self.tree.setCurrentIndex(index)
        return self

    @inject.params(storage='storage', config='config')
    def group(self, index, storage, config):
        current = storage.filePath(index)
        config.set('editor.current', current)

        layout = self.container.layout()
        for i in range(layout.count()): 
            layout.itemAt(i).widget().close()            

        widget = FolderViewWidget()
        widget.edit.connect(self.edit.emit)
        widget.delete.connect(self.delete.emit)
        widget.delete.connect(lambda x: self.group(index))
        widget.clone.connect(self.clone.emit)
        widget.clone.connect(lambda x: self.group(index))
        
        for entity in storage.entities(index):
            if not storage.isDir(entity):
                widget.addPreview(entity)
        layout.addWidget(widget)
        return self
 
    def demo(self):
        layout = self.container.layout()
        for i in range(layout.count()): 
            layout.itemAt(i).widget().close()            
        layout.addWidget(DemoWidget())
        return self
 
    @inject.params(storage='storage')
    def toggle(self, collection=[], state=False, storage=None):
        for index in storage.entities():
            row, parent = (index.row(), index.parent())
            self.tree.setRowHidden(row, parent, state)
            if index not in collection:
                continue

            current = index
            while current != storage.rootIndex():
                row, parent = (current.row(), current.parent())
                self.tree.setRowHidden(row, parent, False)
                self.tree.expand(current)
                current = parent
            
        return True

