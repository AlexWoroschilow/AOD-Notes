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


class LabelTop(QtWidgets.QLabel):
    def __init__(self, parent=None):
        """

        :param parent: 
        """
        super(LabelTop, self).__init__(parent)
        self.setStyleSheet('color: #000')
        font = self.font()
        font.setPixelSize(18)
        self.setFont(font)


class LabelBottom(QtWidgets.QLabel):
    def __init__(self, parent=None):
        """

        :param parent: 
        """
        super(LabelBottom, self).__init__(parent)
        self.setStyleSheet('color: #c0c0c0')
        font = self.font()
        # font.setPixelSize(12)
        self.setFont(font)


class QCustomQWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(QCustomQWidget, self).__init__(parent)
        self.textQVBoxLayout = QtWidgets.QVBoxLayout()

        self.textUpQLabel = LabelTop()
        self.textDownQLabel = LabelBottom()

        self.textQVBoxLayout.addWidget(self.textUpQLabel)
        self.textQVBoxLayout.addWidget(self.textDownQLabel)
        self.allQHBoxLayout = QtWidgets.QHBoxLayout()
        self.iconQLabel = QtWidgets.QLabel()
        self.allQHBoxLayout.addWidget(self.iconQLabel, 0)
        self.allQHBoxLayout.addLayout(self.textQVBoxLayout, 1)
        self.setLayout(self.allQHBoxLayout)

    def setTextUp(self, text):
        self.textUpQLabel.setText(text)

    def setTextDown(self, text):
        self.textDownQLabel.setText(text)

    def setIcon(self, imagePath):
        self.iconQLabel.setPixmap(QtGui.QPixmap(imagePath))


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
        # myQCustomQWidget.setIcon("icons/bold.svg")
        # Create QListWidgetItem
        item = QtWidgets.QListWidgetItem(self)
        item.setSizeHint(myQCustomQWidget.sizeHint())

        self.addItem(item)
        self.setItemWidget(item, myQCustomQWidget)


class FolderList(QtWidgets.QWidget):
    def __init__(self, parent=None):
        """
        
        :param parent: 
        """
        super(FolderList, self).__init__(parent)
        self.setStyleSheet('''QListWidget{ border: none; }
            QListWidget::item{ background-color: #fcf9f6; border: none; }
            QListWidget::item:selected{ background-color: #fdfcf9 }''')

        self.list = ItemList()
        self.toolbar = ToolbarbarWidget()
        self.container = QtWidgets.QWidget()

        self.statusbar = QtWidgets.QLabel()
        self.statusbar.setText("Total amount of folders: 12")

        layout = QtWidgets.QVBoxLayout()

        layout.addWidget(self.list)
        layout.addWidget(self.statusbar)

        self.container.setLayout(layout)
        layout1 = QtWidgets.QHBoxLayout()
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
