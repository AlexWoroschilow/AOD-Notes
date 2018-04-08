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
        self.setObjectName('searchSearchField')
