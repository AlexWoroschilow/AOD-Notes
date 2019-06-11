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
import glob

from .actions import ModuleActions

from lib.plugin import Loader


class Loader(Loader):
    actions = ModuleActions()

    def enabled(self, options=None, args=None):
        return True

    def config(self, binder=None):
        binder.bind_to_constructor('storage', self._storage)

    def _storage_default(self):
        pool = [
            '~/Dropbox', '~/DropBox', '~/dropbox', '~/dropbox',
            '~/Own Cloud', '~/Owncloud', '~/OwnCloud', '~/ownCloud', '~/owncloud',
            '~/Next Cloud', '~/Nextcloud', '~/NextCloud', '~/nextCloud', '~/nextcloud',
            '~/Google Drive', '~/GoogleDrive', '~/googleDrive', '~/googledrive',
            '~/One Drive', '~/Onedrive', '~/OneDrive', '~/oneDrive', '~/onedrive',
        ]

        for candidate in pool:
            if not os.path.exists(candidate):
                continue
            if not os.path.isdir(candidate):
                continue
            return candidate

        return os.path.expanduser('~/AOD-Notepad')

    @inject.params(config='config')
    def _storage(self, config=None):
        location = config.get('storage.location', self._storage_default())

        if len(location) and location.find('~') != -1:
            location = os.path.expanduser(location)

        if not os.path.exists(location):
            if not os.path.exists(location):
                os.makedirs(location)

        from .service.storage import FilesystemStorage
        storage = FilesystemStorage(location)
        if storage.first() is None or not storage.first():
            index = storage.index(location)
            if index is None: return storage
            index = storage.mkdir(index, 'Example group')
            if index is None: return storage
            index = storage.touch(index, 'Example note')
            if index is None: return storage

        return storage

    @inject.params(config='config')
    def _widget_settings_storage(self, config=None):
        if config is None:
            return None

        from .gui.settings.storage import WidgetSettingsStorage

        widget = WidgetSettingsStorage()
        widget.location.setText(config.get('storage.location'))
        action = functools.partial(self.actions.onActionStorageLocationChange, widget=widget)
        widget.location.clicked.connect(action)

        return widget

    @inject.params(config='config', factory='settings_factory')
    def boot(self, options=None, args=None, config=None, factory=None):
        if options is None or args is None or factory is None:
            return None

        factory.addWidget(self._widget_settings_storage)
