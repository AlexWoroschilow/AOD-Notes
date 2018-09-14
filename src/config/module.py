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

from lib.plugin import Loader

from .services import ConfigService


class Loader(Loader):

    @property
    def enabled(self):
        return True
    
    def config(self, binder=None):
        binder.bind_to_constructor('config', self._bind_config)

    @inject.params(kernel='kernel', factory='settings_factory')
    def _bind_config(self, kernel=None, factory=None):

        factory.addWidget(self._widget_settings_storage)
        factory.addWidget(self._widget_settings_navigator)
        factory.addWidget(self._widget_settings_editor)
        
        return ConfigService(kernel.options.config)

    @inject.params(config='config')
    def _widget_settings_navigator(self, config=None):
        
        from .gui.settings.widget import WidgetSettingsNavigator
        widget = WidgetSettingsNavigator()
        
        widget.toolbar.setChecked(int(config.get('folders.toolbar')))
        widget.toolbar.stateChanged.connect(functools.partial(
            self.onActionCheckboxToggle, variable='folders.toolbar'
        ))
        
        widget.keywords.setChecked(int(config.get('folders.keywords')))
        widget.keywords.stateChanged.connect(functools.partial(
            self.onActionCheckboxToggle, variable='folders.keywords'
        ))
        
        return widget

    @inject.params(config='config')
    def _widget_settings_editor(self, config=None):
        
        from .gui.settings.widget import WidgetSettingsEditor
        widget = WidgetSettingsEditor()
        
        widget.name.setChecked(int(config.get('editor.name')))
        widget.name.stateChanged.connect(functools.partial(
            self.onActionCheckboxToggle, variable='editor.name'
        ))

        widget.formatbar.setChecked(int(config.get('editor.formatbar')))
        widget.formatbar.stateChanged.connect(functools.partial(
            self.onActionCheckboxToggle, variable='editor.formatbar'
        ))

        widget.rightbar.setChecked(int(config.get('editor.rightbar')))
        widget.rightbar.stateChanged.connect(functools.partial(
            self.onActionCheckboxToggle, variable='editor.rightbar'
        ))
        
        widget.leftbar.setChecked(int(config.get('editor.leftbar')))
        widget.leftbar.stateChanged.connect(functools.partial(
            self.onActionCheckboxToggle, variable='editor.leftbar'
        ))
        
        return widget

    @inject.params(config='config')
    def _widget_settings_storage(self, config=None):
        from .gui.settings.widget import WidgetSettingsStorage
        widget = WidgetSettingsStorage()
        widget.location.setText(config.get('storage.location'))
        widget.locationChoice.clicked.connect(functools.partial(
            self.onActionStorageLocationChange, widget=widget
        ))
        
        return widget

    @inject.params(config='config', kernel='kernel')
    def onActionStorageLocationChange(self, event, config, widget, kernel):

        from PyQt5 import QtWidgets
        destination = str(QtWidgets.QFileDialog.getExistingDirectory(widget, "Select Directory"))
        if destination is not None and len(destination):
            config.set('storage.location', destination)
            widget.location.setText(destination)
            kernel.dispatch('config_updated')

    @inject.params(config='config', kernel='kernel')
    def onActionCheckboxToggle(self, status, variable, config, kernel):
        config.set(variable, '%s' % status)
        kernel.dispatch('config_updated')

