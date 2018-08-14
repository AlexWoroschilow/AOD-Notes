# -*- coding: utf-8 -*-

# PYQT5 PyQt4’s QtGui module has been split into PyQt5’s QtGui, QtPrintSupport and QtWidgets modules
import inject
from PyQt5.QtCore import Qt

from PyQt5 import QtGui
from PyQt5 import QtWidgets


class WidgetSettingsFactory(object):

    def __init__(self):
        self.widgets = []

    def addWidget(self, widget):
        self.widgets.append(widget)

    @property
    def widget(self):
        widget = WidgetSettings()
        for constructor in self.widgets:
            widget.addWidget(constructor())
        return widget


class WidgetSettings(QtWidgets.QWidget):

    def __init__(self):
        super(WidgetSettings, self).__init__()
        
        self.layout = QtWidgets.QVBoxLayout()
        
        self.setLayout(self.layout)
        
    def addWidget(self, widget):
        self.layout.addWidget(widget)
        
        spacer = QtWidgets.QWidget();
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred);
        self.layout.addWidget(spacer)
        
