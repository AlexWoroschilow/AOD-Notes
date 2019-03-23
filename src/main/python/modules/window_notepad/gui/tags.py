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


class TagsEditor(QtWidgets.QLabel):

    def __init__(self, parent=None):
        super(TagsEditor, self).__init__(parent)
        self.setObjectName('TagsEditor')
        self.setMaximumHeight(300)
        self.setWordWrap(True)
        
        tags = "Battery life still goes down while suspended, probably because the working method of suspend is just less efficient than the default, ideal, method that apparently isn't working properly, but it appears better than the default behaviour"
        self.setText(tags)
            