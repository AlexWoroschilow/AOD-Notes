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


class ModuleActions(object):

    def onActionFileRenamed(self, source, old, new, widget):
        return self.onActionNoteSelect((source, old, new), widget=widget)

    def onActionNoteSelect(self, event=None, widget=None):
        return self.onActionNoteEdit(widget.current, widget=widget)

    def onActionClone(self, event=None, widget=None):
        return self.onActionCopy(widget.tree.current, widget=widget)

    def onActionRemove(self, event=None, widget=None):
        return self.onActionDelete(widget.tree.current, widget=widget)

    @inject.params(storage='storage', logger='logger')
    def onActionNoteEdit(self, index, storage, logger, widget):
        try:
            if storage.isDir(index):
                return widget.group(index)
            if storage.isFile(index):
                return widget.note(index)
            return widget.demo()
        except(Exception) as ex:
            logger.exception(ex)

    @inject.params(storage='storage', search='search', logger='logger')
    def onActionNoteCreate(self, event, widget, storage, search, logger):
        try:
            index = storage.touch(widget.current, 'New note')
            if index is None: return None
            # update search index only after
            # the update was successful
            name = storage.fileName(index)
            content = storage.fileContent(index) 
            path = storage.filePath(index)
            if search is None: return None
            search.append(name, path, content)
            
        except(Exception) as ex:
            logger.exception(ex)

    @inject.params(storage='storage', search='search', logger='logger')
    def onActionCopy(self, index, widget, storage, search, logger):
        try:
            # update search index only after
            # the update was successful
            index = storage.clone(index)
            if index is None: return None
            name = storage.fileName(index)
            content = storage.fileContent(index) 
            path = storage.filePath(index)
            if search is None: return None
            search.append(name, path, content)
                                
        except(Exception) as ex:
            logger.exception(ex)

    @inject.params(storage='storage', search='search', logger='logger')
    def onActionSave(self, event, storage, search, logger, widget):
        try:
            index, content = event 
            if index is None: return None
            index = storage.setFileContent(index, content)
            if index is None: return None
            # update search index only after
            # the update was successful
            if search is None: return None
            name = storage.fileName(index)
            path = storage.filePath(index)
            search.update(name, path, content)
                            
        except(Exception) as ex:
            logger.exception(ex)

    @inject.params(storage='storage', logger='logger')
    def onActionFolderCreate(self, event, widget, storage, logger):
        try:
            if widget.tree.current is not None:
                return storage.mkdir(widget.tree.current, 'New group')
            return storage.mkdir(storage.rootIndex(), 'New group')
        except(Exception) as ex:
            logger.exception(ex)

    @inject.params(window='window', editor='notepad.editor', storage='storage')
    def onActionFullScreen(self, event, widget, window, editor, storage):
        
        editor.index = widget.index

        name = storage.fileName(widget.index)
        window.tab.emit((editor, name))

    @inject.params(storage='storage', search='search', logger='logger')
    def onActionDelete(self, index, widget, storage, search, logger):
        
        message = widget.tr("Are you sure you want to remove this element: {} ?".format(
            storage.fileName(index)
        ))
        
        reply = QtWidgets.QMessageBox.question(widget, 'Remove folder', message, QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.No: return None
        
        try:
            path = storage.filePath(index)
            if not storage.remove(index): return None
            # update search index only after
            # the update was successful
            if search is None: return None
            search.remove(path)
        except(Exception) as ex:
            logger.exception(ex)

    @inject.params(logger='logger')
    def onActionExpand(self, event, widget, logger):
        try:
            widget.tree.expandAll()
        except(Exception) as ex:
            logger.exception(ex)

    @inject.params(logger='logger')
    def onActionCollaps(self, event, widget, logger):
        try:
            widget.tree.collapseAll()
        except(Exception) as ex:
            logger.exception(ex)

    @inject.params(config='config', logger='logger')
    def onActionConfigUpdated(self, event, config=None, widget=None, logger=None):

        try:        
            visible = int(config.get('folders.toolbar'))
            widget.toolbar.setVisible(visible)
        except (AttributeError) as ex:
            logger.exception(ex)

        self.onActionConfigUpdatedEditor(event, widget=widget.editor)

    @inject.params(config='config', logger='logger')
    def onActionConfigUpdatedEditor(self, event, widget, config, logger):

        try:        
            visible = int(config.get('editor.formatbar'))
            widget.formatbar.setVisible(visible)
        except (AttributeError) as ex:
            logger.exception(ex)

        try:        
            visible = int(config.get('editor.leftbar'))
            widget.leftbar.setVisible(visible)
        except (AttributeError) as ex:
            logger.exception(ex)
            
        try:        
            visible = int(config.get('editor.rightbar'))
            widget.rightbar.setVisible(visible)
        except (AttributeError) as ex:
            logger.exception(ex)

    @inject.params(storage='storage')
    def onActionContextMenu(self, event, widget, storage):

        menu = QtWidgets.QMenu()

        if widget.current and not storage.isDir(widget.current) and widget.editor:
            action = functools.partial(self.onActionFullScreen, event=None, widget=widget.editor)
            menu.addAction('Open in a new tab', action)
            menu.addSeparator()

        action = functools.partial(self.onActionNoteCreate, event=None, widget=widget)
        menu.addAction('Create new note', action)
        
        action = functools.partial(self.onActionFolderCreate, event=None, widget=widget)
        menu.addAction('Create new group', action)
        menu.addSeparator()

        if widget.current is not None and widget.current:
            
            action = functools.partial(self.onActionClone, event=None, widget=widget)
            menu.addAction('Clone selected element', action)

            action = functools.partial(self.onActionRemove, event=None, widget=widget)
            menu.addAction('Remove selected element', action)
        
        menu.exec_(widget.tree.mapToGlobal(event))
