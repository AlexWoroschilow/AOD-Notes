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
from bs4 import BeautifulSoup

from PyQt5 import QtGui

from .gui.button import ToolBarButton


class Loader(object):

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def enabled(self, options=None, args=None):
        return options.console is None

    @inject.params(factory='toolbar_factory.leftbar')
    def boot(self, options=None, args=None, factory=None):
        factory.addWidget(self._constructor, 80)

    def _constructor(self):
        widget = ToolBarButton()
        widget.setIcon(QtGui.QIcon("icons/cleanup"))
        widget.setToolTip(widget.tr("Cleanup the document formatting"))
        widget.clickedEvent = self.clickedEvent
        return widget

    def _strip_tags(self, html=None):
        if html is None:
            return None

        soup = BeautifulSoup(html, "html5lib")
        [x.extract() for x in soup.find_all('script')]
        [x.extract() for x in soup.find_all('style')]
        [x.extract() for x in soup.find_all('meta')]
        [x.extract() for x in soup.find_all('noscript')]
        [x.extract() for x in soup.find_all('iframe')]
        return soup.text

    def clickedEvent(self, event=None, widget=None):
        print(widget)
        content = widget.document().toRawText()
        widget.document().setPlainText(content)
