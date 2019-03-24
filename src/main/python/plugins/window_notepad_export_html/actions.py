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

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore


class ModuleActions(object):

    def onActionButtonPressed(self, widget):

        selector = QtWidgets.QFileDialog(None, 'Select where to export', os.path.expanduser('~'))
        if not selector.exec_(): return None

        for path in selector.selectedFiles():

            document = QtGui.QTextDocument()
            document.setHtml(widget.getHtml())
            encoding = QtCore.QByteArray(bytes('UTF8', 'utf-8'))

            if not os.path.exists(path):
                with open(path, 'w+') as stream:
                    stream.write(document.toHtml(encoding=encoding))
                    stream.close()
                continue

            message = widget.tr("Are you sure you want to overwrite the file '%s' ?" % path)
            reply = QtWidgets.QMessageBox.question(widget, 'Message', message, QtWidgets.QMessageBox.Yes,
                                                   QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.No:
                continue

            with open(path, 'w+') as stream:
                stream.write(document.toHtml(encoding=encoding))
                stream.close()
