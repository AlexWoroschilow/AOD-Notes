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


class FolderListWidgetItem(QtWidgets.QListWidgetItem):
    def __init__(self, parent=None, folder=None):
        """

        :param parent: 
        """
        super(FolderListWidgetItem, self).__init__(parent)
        self._folder = folder

    @property
    def folder(self):
        """
        
        :return: 
        """
        return self._folder


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

        myQCustomQWidget = QCustomQWidget()
        myQCustomQWidget.setTextUp(folder.name)
        myQCustomQWidget.setTextDown(folder.text)

        item = FolderListWidgetItem(self, folder)
        item.setSizeHint(myQCustomQWidget.sizeHint())

        self.addItem(item)
        self.setItemWidget(item, myQCustomQWidget)


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

        self.list = ItemList()

        # items = ['aa', 'bb', 'cc']
        # self.list = QtWidgets.QTreeWidget()
        # self.list.setHeaderHidden(True)
        # font = self.list.font()
        # font.setPixelSize(18)
        # self.list.setFont(font)
        #
        # for item in items:
        #     root = QtWidgets.QTreeWidgetItem(self.list, [item])
        #     # root.setIcon(0, app.style().standardIcon(QtWidgets.QStyle.SP_ArrowUp))
        #     for i in range(3):
        #         sub_item = QtWidgets.QTreeWidgetItem(root, ["sub %s %s" % (item, i)])

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

    def addLine(self, folder=None):
        """
        
        :param name: 
        :param descrption: 
        :return: 
        """
        self.list.addLine(folder)
