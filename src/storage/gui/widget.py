# -*- coding: utf-8 -*-

# PYQT5 PyQt4’s QtGui module has been split into PyQt5’s QtGui, QtPrintSupport and QtWidgets modules
import inject
from PyQt5.QtCore import Qt

from PyQt5 import QtGui
from PyQt5 import QtWidgets


class WidgetSettings(QtWidgets.QWidget):

    def __init__(self):
        super(WidgetSettings, self).__init__()
        
        self.layout = QtWidgets.QVBoxLayout()
        
        self.layout.addWidget(QtWidgets.QLabel('Test'))

        self.setLayout(self.layout)
