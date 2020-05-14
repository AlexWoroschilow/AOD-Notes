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


class ModuleActions(QtCore.QObject):
    progressAction = QtCore.pyqtSignal(object)

    @inject.params(store='store')
    def onActionIndexation(self, event, store):
        store.dispatch({
            'type': '@@app/search/index/rebuild',
        })

    @inject.params(store='store', window='window')
    def onActionSelect(self, entity, store, window):
        window.switchTabAction.emit(0)

        store.dispatch({
            'type': '@@app/storage/resource/found/document',
            'entity': entity
        })
