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
import re
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from bs4 import BeautifulSoup


class Description(QtWidgets.QLabel):

    def __init__(self, text=None):
        super(Description, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.setWordWrap(True)
        self.setText(self._strip_tags(text))

        font = self.font()
        font.setPixelSize(10)
        self.setFont(font)

        self.show()

    def _strip_tags(self, html=None):
        if html is None:
            return None

        soup = BeautifulSoup(html, "html5lib")
        [x.extract() for x in soup.find_all('script')]
        [x.extract() for x in soup.find_all('style')]
        [x.extract() for x in soup.find_all('meta')]
        [x.extract() for x in soup.find_all('noscript')]
        [x.extract() for x in soup.find_all('iframe')]
        if soup.text is None: return None

        text = re.sub(r'\s', ' ', soup.text)
        return "{}...".format(text[:180])
