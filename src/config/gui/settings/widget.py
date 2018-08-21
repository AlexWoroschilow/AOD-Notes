# -*- coding: utf-8 -*-

# PYQT5 PyQt4’s QtGui module has been split into PyQt5’s QtGui, QtPrintSupport and QtWidgets modules
import inject
from PyQt5.QtCore import Qt

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore

from .text import TextEditor


class WidgetSettings(QtWidgets.QWidget):

    def __init__(self, config=None):
        super(WidgetSettings, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding);

        self.setStyleSheet('margin: 2px 50px; padding: 10px 20px;')

    
        self.layout = QtWidgets.QGridLayout()

        label = QtWidgets.QLabel('Storage settings')
        label.setStyleSheet('QLabel { font-size: 26px;}')

        self.layout.addWidget(label, 0, 0, 1, 3)

        spacer = QtWidgets.QWidget();
        spacer.setObjectName('spacer')
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding);
        self.layout.addWidget(spacer, 1, 0, 8, 4)

        
        folders = QtWidgets.QCheckBox('Show toolbar at the folder panel')
        folders.setChecked(bool(config.get('folders.leftbar')))
        # folders.clicked.connect(self.exportData)

        self.layout.addWidget(folders, 2, 0)

        folders = QtWidgets.QCheckBox('Show toolbar at the notes panel')
        folders.setChecked(bool(config.get('notes.leftbar')))
        # folders.clicked.connect(self.exportData)

        self.layout.addWidget(folders, 3, 0)

        folders = QtWidgets.QCheckBox('Show left toolbar at the editor panel')
        folders.setChecked(bool(config.get('editor.leftbar')))
        # folders.clicked.connect(self.exportData)

        self.layout.addWidget(folders, 4, 0)

        folders = QtWidgets.QCheckBox('Show format-bar at the editor panel')
        folders.setChecked(bool(config.get('editor.formatbar')))
        # folders.clicked.connect(self.exportData)

        self.layout.addWidget(folders, 5, 0)

        folders = QtWidgets.QCheckBox('Show right toolbar at the editor panel')
        folders.setChecked(bool(config.get('editor.rightbar')))
        # folders.clicked.connect(self.exportData)

        self.layout.addWidget(folders, 6, 0)

        self.setLayout(self.layout)

        self.show()

