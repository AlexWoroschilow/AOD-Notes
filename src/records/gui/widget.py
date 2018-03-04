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


class QCustomQWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(QCustomQWidget, self).__init__(parent)
        self.textQVBoxLayout = QtWidgets.QVBoxLayout()
        self.textUpQLabel = QtWidgets.QLabel()
        self.textDownQLabel = QtWidgets.QLabel()
        self.textQVBoxLayout.addWidget(self.textUpQLabel)
        self.textQVBoxLayout.addWidget(self.textDownQLabel)
        self.allQHBoxLayout = QtWidgets.QHBoxLayout()
        self.iconQLabel = QtWidgets.QLabel()
        self.allQHBoxLayout.addWidget(self.iconQLabel, 0)
        self.allQHBoxLayout.addLayout(self.textQVBoxLayout, 1)
        self.setLayout(self.allQHBoxLayout)
        # setStyleSheet
        self.textUpQLabel.setStyleSheet('''
            color: rgb(0, 0, 255);
        ''')
        self.textDownQLabel.setStyleSheet('''
            color: rgb(255, 0, 0);
        ''')

    def setTextUp(self, text):
        self.textUpQLabel.setText(text)

    def getTextUp(self):
        return self.textUpQLabel.text()

    def setTextDown(self, text):
        self.textDownQLabel.setText(text)

    def getTextDown(self):
        return self.textDownQLabel.text()

    def setIcon(self, imagePath):
        self.iconQLabel.setPixmap(QtGui.QPixmap(imagePath))


class NoteItem(QtWidgets.QListWidgetItem):
    def __init__(self, index=None, name=None, text=None):
        """
        
        :param index: 
        :param name: 
        :param text: 
        """
        super(NoteItem, self).__init__()
        self._index = index
        self._name = name
        self._text = text

    @property
    def index(self):
        """
        
        :return: 
        """
        return self._index

    @property
    def name(self):
        """

        :return: 
        """
        return self._name

    @name.setter
    def name(self, value):
        """

        :return: 
        """
        self._name = value
        self.setText(value)

    @property
    def text(self):
        """

        :return: 
        """
        return self._text

    @text.setter
    def text(self, value):
        """

        :return: 
        """
        self._text = value


class ItemList(QtWidgets.QListWidget):
    def __init__(self, parent=None):
        """
        
        :param parent: 
        """
        super(ItemList, self).__init__(parent)

    def addLine(self, index=None, name=None, text=None):
        """
        
        :param name: 
        :param descrption: 
        :return: 
        """

        myQCustomQWidget = QCustomQWidget()
        myQCustomQWidget.setTextUp(name)
        myQCustomQWidget.setTextDown(text)

        item = NoteItem(index, name, text)
        item.setSizeHint(myQCustomQWidget.sizeHint())

        self.addItem(item)
        self.setItemWidget(item, myQCustomQWidget)


class RecordList(QtWidgets.QWidget):
    def __init__(self, parent=None):
        """
        
        :param parent: 
        """
        super(RecordList, self).__init__(parent)
        self.setContentsMargins(0, 10, 10, 0)

        self.list = ItemList()
        self.toolbar = ToolbarbarWidget()
        self.container = QtWidgets.QWidget()

        self.statusbar = QtWidgets.QLabel()
        self.statusbar.setText("Total amount of records: 12")

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(self.list)
        layout.addWidget(self.statusbar)

        self.container.setLayout(layout)
        layout1 = QtWidgets.QHBoxLayout()
        layout1.setContentsMargins(0, 0, 0, 0)
        layout1.setSpacing(0)
        layout1.addWidget(self.toolbar)
        layout1.addWidget(self.container)
        self.setLayout(layout1)

    def addLine(self, index=None, name=None, text=None):
        """
        
        :param name: 
        :param descrption: 
        :return: 
        """
        self.list.addLine(index, name, text)
