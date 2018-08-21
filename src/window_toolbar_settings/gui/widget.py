# -*- coding: utf-8 -*-

# PYQT5 PyQt4’s QtGui module has been split into PyQt5’s QtGui, QtPrintSupport and QtWidgets modules
import inject
from PyQt5.QtCore import Qt

from PyQt5 import QtGui
from PyQt5 import QtWidgets

from .scroll import SettingsScrollArea


class WidgetSettingsFactory(object):

    def __init__(self):
        self.widgets = []

    def addWidget(self, widget):
        self.widgets.append(widget)

    @property
    def widget(self):
        widget = SettingsScrollArea()
        for constructor in self.widgets:
            widget.addWidget(constructor())
        return widget

