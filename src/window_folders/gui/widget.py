# -*- coding: utf-8 -*-

import sys
import re
from PyQt5 import QtWidgets
from PyQt5 import QtPrintSupport
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from .bar import ToolbarbarWidget


class LabelTop(QtWidgets.QLabel):

    def __init__(self, parent=None):
        """

        :param parent: 
        """
        super(LabelTop, self).__init__(parent)
        self.setObjectName('LabelTop')


class LabelBottom(QtWidgets.QLabel):

    def __init__(self, parent=None):
        """

        :param parent: 
        """
        super(LabelBottom, self).__init__(parent)
        self.setObjectName('LabelBottom')


class QCustomQWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(QCustomQWidget, self).__init__(parent)
        self.textQVBoxLayout = QtWidgets.QVBoxLayout()
        self.textQVBoxLayout.setContentsMargins(10, 10, 0, 10)
        self.textQVBoxLayout.setSpacing(0)

        self.textUpQLabel = LabelTop()
        self.textQVBoxLayout.addWidget(self.textUpQLabel)

        self.textDownQLabel = LabelBottom()
        self.textQVBoxLayout.addWidget(self.textDownQLabel)

        self.setLayout(self.textQVBoxLayout)

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
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setContentsMargins(0, 0, 0, 0)
        self.setObjectName('foldersList')

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


class FolderList(QtWidgets.QSplitter):

    def __init__(self, parent=None):
        super(FolderList, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setObjectName('foldersWidget')

        self.toolbar = ToolbarbarWidget()
        self.addWidget(self.toolbar)

        self.list = ItemList()
        self.list.setMinimumWidth(180)
        self.addWidget(self.list)
        
        self.setCollapsible(0, True)
        self.setCollapsible(1, False)

    def addLine(self, folder=None):
        self.list.addLine(folder)

    def selectedIndexes(self):
        return self.list.selectedIndexes()

    def itemFromIndex(self, index=None):
        if index is None:
            return None
        return self.list.itemFromIndex(index)

    def takeItem(self, index=None):
        if index is None:
            return None
        self.list.takeItem(index.row())

