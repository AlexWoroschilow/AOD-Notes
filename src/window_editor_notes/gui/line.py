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

from PyQt5 import QtWidgets


class NameEditor(QtWidgets.QLineEdit):

    def __init__(self, parent=None):
        super(NameEditor, self).__init__(parent)
        self.setObjectName('editorNameEditor')

        self._entity = None

    @property
    def entity(self):
        return self._entity
    
    @entity.setter
    def entity(self, entity=None):
        self._entity = entity
        if self.text is not None and entity is not None:
            return self.setText(entity.name)
        return self.setText('') 

