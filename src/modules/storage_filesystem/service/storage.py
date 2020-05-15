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
import re
import pydux
import shutil
import inject
import functools

import glob

from .model import Group
from .model import Document


def natural_keys(text):
    def atoi(text):
        return int(text) if text.isdigit() else text

    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [atoi(c) for c in re.split('(\d+)', text.lower())]


class StoreFileSystem(object):

    def _groups(self, location):
        result = []
        for path in sorted(glob.iglob('{}/**'.format(location)), key=natural_keys, reverse=False):
            if not len(path) or os.path.isfile(path):
                continue
            result.append(Group(path, self._groups(path)))
        return result

    def _documents(self, location, recursive=False):
        result = []
        for filename in sorted(glob.iglob('{}/**'.format(location)), key=natural_keys, reverse=False):
            if not len(filename) or os.path.isdir(filename):
                continue
            result.append(Document(filename))
        return result

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
            if not os.path.exists(candidate): continue
            if not os.path.isdir(candidate): continue
            return candidate

        return os.path.expanduser('~/AOD-Notes')

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
            print(ex)
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

        if location is None or not len(location):
            return None

        if not os.path.exists(location):
            return None

        return Group(location, self._groups(location))

    @inject.params(config='config')
    def groups(self, group=None, config=None):
        location = group.path if group is not None \
            else config.get('storage.location', self.default)

        if location is None or not len(location):
            return []

        if not os.path.exists(location):
            return []

        return [Group(location, self._groups(location))]

    @inject.params(config='config')
    def document(self, document=None, config=None):
        location = document.path if document is not None \
            else config.get('storage.selected.document')

        if location is None or not os.path.exists(location):
            return None

        return Document(location)

    @inject.params(config='config')
    def documents(self, group=None, config=None):
        location = group.path if group is not None \
            else config.get('storage.selected.group')

        if location is None or not len(location):
            return []

        if not os.path.exists(location):
            return []

        return self._documents(location)

    @inject.params(config='config')
    def allDocuments(self, group=None, config=None):
        location = group.path if group is not None \
            else config.get('storage.location', self.default)

        if location is None or not len(location):
            return []

        if not os.path.exists(location):
            return []

        return self._documents(location, True)
