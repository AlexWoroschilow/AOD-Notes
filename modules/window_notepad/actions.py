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

from PyQt5 import QtWidgets


class ModuleActions(object):

    @inject.params(storage='storage')
    def onActionNoteRefresh(self, folder, old, new, storage, widget=None):
        """
        Reload the file into editor after the file name has been changed
        It crushed the application because somethimes the aditor 
        had not idea about the file name changs
        """
        return self.onActionNoteSelect(event=(folder,), widget=widget)

    @inject.params(storage='storage')
    def onActionNoteSelect(self, event, storage, widget=None):
        """
        Get the selected note from the tree and 
        open it in the text editor
        """
        if widget.tree is None:
            return None
        if widget.tree.selected is not None:
            widget.entity(storage.entity(
                widget.tree.selected                
            ))

    def onActionContextMenu(self, event, widget):

        menu = QtWidgets.QMenu()

        index = widget.tree.index 
        if index is not None:
            name = widget.tree.model().data(index)

            menu.addAction('Open in a new tab', functools.partial(
                self.onActionFullScreen, widget=widget
            ))
            menu.addSeparator()
            menu.addAction('Remove \'%s\'' % name, functools.partial(
                self.onActionFolderRemove, widget=widget
            ))
            menu.addAction('Clone \'%s\'' % name, functools.partial(
                self.onActionFolderCopy, widget=widget
            ))
            menu.addSeparator()

        menu.addAction('Create new document', functools.partial(
            self.onActionNoteCreate, widget=widget
        ))
        menu.addAction('Create new group', functools.partial(
            self.onActionFolderCreate, widget=widget
        ))
        
        menu.exec_(widget.tree.mapToGlobal(event))

    @inject.params(storage='storage', note='storage.note', kernel='kernel')
    def onActionNoteCreate(self, event, widget, storage, note, kernel):

        folder = storage.entity(widget.tree.selected)
        if folder is not None and folder:
            note.folder = folder
        
        if event.data is not None and event.data:
            note.name, note.text = event.data

        try:
            note = storage.create(note)
            kernel.dispatch('note_created', note)
        except(Exception) as ex:
            print(ex)

    @inject.params(storage='storage', folder='storage.folder')
    def onActionFolderCreate(self, event, widget, storage, folder):

        destination = storage.entity(widget.tree.selected)
        if destination is not None and destination:
            folder.folder = destination

        if event.data is not None and event.data:
            folder.name, folder.description = event.data
        
        try:
            storage.create(folder)
        except(Exception) as ex:
            print(ex)

    @inject.params(storage='storage')
    def onActionFolderCopy(self, event=None, widget=None, storage=None):
        if widget.tree is None:
            return None
        path = widget.tree.selected
        if path is not None:
            storage.clone(path)

    @inject.params(storage='storage')
    def onActionSave(self, event, widget, storage):
        note = widget._note
        note.name = widget.name.text() 
        note.text = widget._text.text.toHtml() 
        if note is not None:
            storage.update(note)
        
    @inject.params(kernel='kernel', storage='storage', editor='editor')
    def onActionFullScreen(self, event=None, widget=None, kernel=None, storage=None, editor=None):
        if widget.tree is None or editor is None:
            return None
        path = widget.tree.selected
        if path is None:
            return None
        
        note = storage.note(path)
        if note is None:
            return None
        
        editor.note = note

        kernel.dispatch('window.tab', (editor, note.name))

    @inject.params(storage='storage')
    def onActionFolderRemove(self, event=None, widget=None, storage=None):
        message = widget.tr("Are you sure you want to remove this Folder?")
        reply = QtWidgets.QMessageBox.question(widget, 'Remove folder', message, QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            path = widget.tree.selected
            if path is not None: 
                storage.delete(path)

    def onActionExpand(self, event=None, widget=None):
        if widget.tree is not None:
            widget.tree.expandAll()

    def onActionCollaps(self, event, widget):
        if widget.tree is not None:
            widget.tree.collapseAll()

    @inject.params(config='config', logger='logger')
    def onActionConfigUpdated(self, event, config=None, widget=None, logger=None):
        if widget is None or config is None:
            return None

        try:        
            visible = int(config.get('folders.toolbar'))
            widget.toolbar.setVisible(visible)
        except (AttributeError) as ex:
            logger.error(ex)

        try:        
            visible = int(config.get('folders.keywords'))
            widget.tags.setVisible(visible)
        except (AttributeError):
            pass
        
        self.onActionConfigUpdatedEditor(event, widget=widget.editor)

    @inject.params(config='config', logger='logger')
    def onActionConfigUpdatedEditor(self, event, widget=None, config=None, logger=None):

        try:        
            visible = int(config.get('editor.formatbar'))
            widget.formatbar.setVisible(visible)
        except (AttributeError):
            pass

        try:        
            visible = int(config.get('editor.leftbar'))
            widget.leftbar.setVisible(visible)
        except (AttributeError):
            pass
            
        try:        
            visible = int(config.get('editor.rightbar'))
            widget.rightbar.setVisible(visible)
        except (AttributeError):
            pass

        try:        
            visible = int(config.get('editor.name'))
            widget.name.setVisible(visible)
        except (AttributeError):
            pass

