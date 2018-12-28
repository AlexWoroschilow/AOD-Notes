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

    @inject.params(storage='storage', logger='logger')
    def onActionNoteSelect(self, event, storage, widget, logger):
        try:
            if storage.isDir(widget.tree.current):
                return widget.group(widget.tree.current)
            if storage.isFile(widget.tree.current):
                return widget.note(widget.tree.current)
            return widget.demo()
        except(Exception) as ex:
            logger.exception(ex.message)

    @inject.params(storage='storage', search='search', logger='logger')
    def onActionNoteCreate(self, event, widget, storage, search, logger):
        try:
            index = storage.touch(widget.current, 'New note')
            if index is None or not index:
                return None
            # update search index only after
            # the update was successful
            name = storage.fileName(index)
            content = storage.fileContent(index) 
            path = storage.filePath(index)
            if search is None or not search:
                return None
            search.append(name, path, content)
            
        except(Exception) as ex:
            logger.exception(ex.message)

    @inject.params(storage='storage', search='search', logger='logger')
    def onActionClone(self, event, widget, storage, search, logger):
        try:
            # update search index only after
            # the update was successful
            index = storage.clone(widget.tree.current)
            if index is None or not index:
                return None
            
            name = storage.fileName(index)
            content = storage.fileContent(index) 
            path = storage.filePath(index)
            if search is None or not search:
                return None
            search.append(name, path, content)
                                
        except(Exception) as ex:
            logger.exception(ex.message)

    @inject.params(storage='storage', search='search', logger='logger')
    def onActionSave(self, event, storage, search, logger):
        try:
            name, path, content = event 
            index = storage.index(path)
            if index is None or not index:
                return None
            index = storage.setFileContent(index, content)
            if index is None or not index:
                return None
            # update search index only after
            # the update was successful
            if search is None or not search:
                return None
            search.update(name, path, content)
                            
        except(Exception) as ex:
            logger.exception(ex.message)

    @inject.params(storage='storage', logger='logger')
    def onActionFolderCreate(self, event, widget, storage, logger):
        try:
            storage.mkdir(widget.tree.current, 'New group')
        except(Exception) as ex:
            logger.exception(ex.message)

    @inject.params(kernel='kernel', editor='editor')
    def onActionFullScreen(self, event, widget, kernel, editor):
        
        editor.name = widget.name
        editor.content = widget.content
        editor.path = widget.path
        editor.insertHtml(editor.content)

        kernel.dispatch('window.tab', (editor, editor.name))

    @inject.params(storage='storage', search='search', logger='logger')
    def onActionRemove(self, event, widget, storage, search, logger):
        
        message = widget.tr("Are you sure you want to remove this element: {} ?".format(
            storage.fileName(widget.tree.current)
        ))
        
        reply = QtWidgets.QMessageBox.question(widget, 'Remove folder', message, QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.No:
            return None
        
        try:
            index = widget.tree.current
            path = storage.filePath(index)
            if not storage.remove(index):
                return None
            # update search index only after
            # the update was successful
            if search is None or not search:
                return None
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

        try:        
            visible = int(config.get('folders.keywords'))
            widget.tags.setVisible(visible)
        except (AttributeError) as ex:
            logger.exception(ex)
        
        self.onActionConfigUpdatedEditor(event, widget=widget.editor)

    @inject.params(config='config', logger='logger')
    def onActionConfigUpdatedEditor(self, event, widget=None, config=None, logger=None):

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

        if widget.tree.index is not None:
            name = storage.data(widget.tree.index)

            if hasattr(widget, 'editor') and widget.editor is not None:
                action = functools.partial(self.onActionFullScreen, event=None, widget=widget.editor)
                menu.addAction('Open in a new tab', action)
                menu.addSeparator()
            
            action = functools.partial(self.onActionRemove, event=None, widget=widget)
            menu.addAction('Remove \'{}\''.format(name), action)
            
            action = functools.partial(self.onActionClone, event=None, widget=widget)
            menu.addAction('Clone \'{}\''.format(name), action)
            menu.addSeparator()

        action = functools.partial(self.onActionNoteCreate, event=None, widget=widget)
        menu.addAction('Create new document', action)
        
        action = functools.partial(self.onActionFolderCreate, event=None, widget=widget)
        menu.addAction('Create new group', action)
        
        menu.exec_(widget.tree.mapToGlobal(event))
