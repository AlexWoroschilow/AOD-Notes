# -*- coding: utf-8 -*-

# PYQT5 PyQt4’s QtGui module has been split into PyQt5’s QtGui, QtPrintSupport and QtWidgets modules
import inject
from PyQt5.QtCore import Qt

from PyQt5 import QtGui
from PyQt5 import QtPrintSupport
from PyQt5 import QtWidgets


class SearchField(QtWidgets.QLineEdit):
    def __init__(self, parent=None):
        """

        :param parent: 
        """
        super(SearchField, self).__init__(parent)
        self.setPlaceholderText('Enter the search string...')
        self.setContentsMargins(20, 15, 20, 0)
        self.setClearButtonEnabled(False)

        font = self.font()
        font.setPixelSize(24)
        self.setFont(font)
