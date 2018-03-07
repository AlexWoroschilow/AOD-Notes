# -*- coding: utf-8 -*-

import sys

# PYQT5 PyQt4’s QtGui module has been split into PyQt5’s QtGui, QtPrintSupport and QtWidgets modules

from PyQt5 import QtWidgets
# PYQT5 QMainWindow, QApplication, QAction, QFontComboBox, QSpinBox, QTextEdit, QMessageBox
# PYQT5 QFileDialog, QColorDialog, QDialog

from PyQt5 import QtPrintSupport
# PYQT5 QPrintPreviewDialog, QPrintDialog

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from .bar import ToolbarbarWidget
import re


class FolderName(QtWidgets.QLineEdit):
    def __init__(self, parent=None):
        """

        :param parent: 
        """
        super(FolderName, self).__init__(parent)

        self.setStyleSheet('''QLineEdit{ border: none; }''')

        font = self.font()
        font.setPixelSize(24)
        self.setFont(font)
