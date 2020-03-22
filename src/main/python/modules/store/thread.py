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

from PyQt5 import QtCore
from PyQt5 import QtGui


class SearchThread(QtCore.QThread):

    @inject.params(store='store', search='search', filesystem='store.filesystem')
    def run(self, store=None, search=None, filesystem=None):
        if not search.clean():
            return None

        store.dispatch({
            'type': '@@app/search/index/progress',
            'progress': 0
        })

        collection = filesystem.allDocuments()
        for progress, document in enumerate(collection, start=1):
            store.dispatch({
                'type': '@@app/search/index/progress',
                'progress': progress / len(collection) * 100
            })

            search.update(document.name, document.path, document.content)

        store.dispatch({
            'type': '@@app/search/index/progress',
            'progress': 100
        })
