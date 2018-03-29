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

    def setTextUp(self, text=None):
        """
        
        :param text: 
        :return: 
        """
        self.textUpQLabel.setText(text)

    def setTextDown(self, text=None):
        """
        
        :param text: 
        :return: 
        """
        self.textDownQLabel.setText(text)

    def setIcon(self, imagePath=None):
        """
        
        :param imagePath: 
        :return: 
        """
        self.iconQLabel.setPixmap(QtGui.QPixmap(imagePath))


class FolderItem(QtWidgets.QListWidgetItem):
    def __init__(self, entity=None, widget=None):
        """

        :param parent: 
        """
        super(FolderItem, self).__init__()
        widget.setTextDown(entity.text)
        widget.setTextUp(entity.name)
        self._entity = entity
        self._widget = widget
        self._folder = entity

    @property
    def widget(self):
        """

        :return: 
        """
        return self._widget

    @property
    def folder(self):
        """
        
        :return: 
        """
        return self._folder

    @folder.setter
    def folder(self, entity=None):
        """

        :return:
        """
        self._widget.setTextUp(entity.name)
        self._widget.setTextDown(entity.text)
        self._entity = entity


class ItemList(QtWidgets.QListWidget):
    def __init__(self, parent=None):
        """
        
        :param parent: 
        """
        super(ItemList, self).__init__(parent)

    def addLine(self, folder=None):
        """
        
        :param name: 
        :param descrption: 
        :return: 
        """

        item = FolderItem(folder, QCustomQWidget())
        item.setSizeHint(item.widget.sizeHint())

        self.addItem(item)
        self.setItemWidget(item, item.widget)


class FolderList(QtWidgets.QWidget):
    def __init__(self, parent=None):
        """
        
        :param parent: 
        """
        super(FolderList, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet('''QListWidget{ border: none; }
            QListWidget::item{ background-color: #fcf9f6; border: none; }
            QListWidget::item:selected{ background-color: #fdfcf9 }''')


        self.toolbar = ToolbarbarWidget()
        self.list = ItemList()
        self.statusbar = QtWidgets.QLabel()
        self.statusbar.setText("...")

        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.toolbar, 0, 0, 3, 1)
        layout.addWidget(self.list, 0, 1)
        layout.addWidget(self.statusbar, 1, 1)
        self.setLayout(layout)


    def addLine(self, folder=None):
        """
        
        :param name: 
        :param descrption: 
        :return: 
        """
        self.list.addLine(folder)

        self.statusbar.setText("%i folders found" % self.list.count())

    def selectedIndexes(self):
        """
        
        :return: 
        """
        return self.list.selectedIndexes()

    def itemFromIndex(self, index=None):
        """
        
        :param index: 
        :return: 
        """
        if index is None:
            return None

        return self.list.itemFromIndex(index)

    def takeItem(self, index=None):
        """
        
        :param item: 
        :return: 
        """
        if index is None:
            return None

        self.list.takeItem(index.row())

        self.statusbar.setText("%i folders found" % self.list.count())
