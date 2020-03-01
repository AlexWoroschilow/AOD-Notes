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
import pydux
import shutil
import inject
import functools

from .actions import ModuleActions
import glob


class Group(object):
    def __init__(self, path, children):
        self.children = children
        self.path = path

    @property
    def name(self):
        return os.path.basename(self.path)

    @name.setter
    def name(self, value, counter=1):
        if value == self.name:
            return self
        try:
            destination = "{}/{}".format(os.path.dirname(self.path), value)
            while os.path.exists(destination):
                destination = "{} ({})".format(destination, counter)
                counter += 1
            shutil.move(self.path, destination)
        except OSError as ex:
            return self
        return self


class Document(object):
    def __init__(self, path):
        self.path = path

    @property
    def name(self):
        return os.path.basename(self.path)

    @name.setter
    def name(self, value, counter=1):
        if value == self.name:
            return self
        try:
            destination = "{}/{}".format(os.path.dirname(self.path), value)
            while os.path.exists(destination):
                destination = "{} ({})".format(destination, counter)
                counter += 1
            shutil.move(self.path, destination)
        except OSError as ex:
            return self
        return self

    @property
    def content(self):
        try:
            return open(self.path, 'r').read()
        except OSError as ex:
            return ''

    @content.setter
    def content(self, value):
        return open(self.path, 'w').write(value)


class StoreFileSystem(object):

    @property
    def default(self):
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

    def _groups(self, location):
        result = []
        for path in glob.iglob('{}/**'.format(location)):
            if not len(path) or os.path.isfile(path):
                continue
            result.append(Group(path, self._groups(path)))
        return result

    def _documents(self, location):
        result = []
        for filename in glob.iglob('{}/**'.format(location)):
            if not len(filename) or os.path.isdir(filename):
                continue
            result.append(Document(filename))
        return result

    def clone(self, element, name='Copy', counter=1):
        """

        :param element:
        :param name:
        :param counter:
        :return:
        """
        location = "{} ({})".format(element.path, name)
        while os.path.exists(location):
            location = "{} ({} {})".format(element.path, name, counter)
            counter += 1

        try:

            if os.path.isfile(element.path):
                with open(element.path, 'r') as origin:
                    with open(location, 'w') as clone:
                        clone.write(origin.read())
                        clone.close()

                        return Document(location)

            if os.path.isdir(element.path):
                shutil.copytree(element.path, location)
                return Group(location, self._groups(location))

        except OSError as ex:
            pass

        return None

    def remove(self, element):
        """
        :param element:
        :return:
        """
        location = element.path
        if not os.path.exists(location):
            return False

        try:

            if os.path.isdir(location):
                shutil.rmtree(location)

            if os.path.isfile(location):
                os.remove(location)

            return not os.path.exists(location)

        except OSError as ex:
            return False

        return False

    def group_create(self, group, name='New Group', counter=1):
        """
        Create new note in the given folder
        :param group:
        :param name:
        :param counter:
        :return:
        """
        location = "{}/{}".format(group.path, name)
        while os.path.exists(location):
            location = "{}/{} ({})".format(group.path, name, counter)
            counter += 1

        try:
            os.mkdir(location)
            return Group(location, self._groups(location))

        except OSError as ex:
            return None

        return None

    def document_create(self, group, name='New Note', counter=1):
        """
        Create new note in the given folder
        :param group:
        :param name:
        :param counter:
        :return:
        """
        location = "{}/{}".format(group.path, name)
        print(location, group.path)
        while os.path.exists(location):
            location = "{}/{} ({})".format(group.path, name, counter)
            counter += 1

        with open(location, 'w') as stream:
            stream.write('')
            stream.close()

            return Document(location)

        return None

    @inject.params(config='config')
    def group(self, group=None, config=None):
        location = group.path if group is not None \
            else config.get('storage.selected.group')

        if not os.path.exists(location):
            return None
        return Group(location, self._groups(location))

    @inject.params(config='config')
    def groups(self, group=None, config=None):
        location = group.path if group is not None \
            else config.get('storage.location', self.default)

        if not os.path.exists(location):
            return None

        return self._groups(location)

    @inject.params(config='config')
    def document(self, document=None, config=None):
        location = document.path if document is not None \
            else config.get('storage.selected.document')

        if not os.path.exists(location):
            return None

        return Document(location)

    @inject.params(config='config')
    def documents(self, group=None, config=None):
        location = group.path if group is not None \
            else config.get('storage.selected.group')

        if not os.path.exists(location):
            return None

        return self._documents(location)


class Loader(object):
    actions = ModuleActions()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    @inject.params(config='config')
    def _storage(self, config=None):
        from .service.storage import FilesystemStorage
        location = config.get('storage.location')
        return FilesystemStorage(location)

    @inject.params(config='config')
    def _widget_settings_storage(self, config=None):
        from .gui.settings.storage import WidgetSettingsStorage

        widget = WidgetSettingsStorage()
        widget.location.clicked.connect(functools.partial(
            self.actions.onActionStorageLocationChange
        ))

        return widget

    def enabled(self, options=None, args=None):
        return True

    def configure(self, binder, options, args):
        binder.bind_to_constructor('storage', self._storage)
        binder.bind_to_constructor('store.filesystem', StoreFileSystem)

    @inject.params(config='config', factory='settings_factory', dashboard='notepad.dashboard', store='store')
    def boot(self, options, args, config, factory, dashboard, store):
        # dashboard.storage.connect(functools.partial(
        #     self.actions.onActionStorageLocationChange
        # ))
        #
        # factory.addWidget(functools.partial(
        #     self._widget_settings_storage
        # ))
        pass
