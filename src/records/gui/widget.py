# -*- coding: utf-8 -*-

import sys

# PYQT5 PyQt4’s QtGui module has been split into PyQt5’s QtGui, QtPrintSupport and QtWidgets modules

import inject
from PyQt5 import QtWidgets
# PYQT5 QMainWindow, QApplication, QAction, QFontComboBox, QSpinBox, QTextEdit, QMessageBox
# PYQT5 QFileDialog, QColorDialog, QDialog

from PyQt5 import QtPrintSupport
# PYQT5 QPrintPreviewDialog, QPrintDialog

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from .bar import ToolbarbarWidget
from .editor import FolderName
import re
from bs4 import BeautifulSoup, NavigableString


class LabelTop(QtWidgets.QLabel):
    def __init__(self, parent=None):
        """
        
        :param parent: 
        """
        super(LabelTop, self).__init__(parent)
        self.setStyleSheet('QLabel{ color: #000000; }')
        font = self.font()
        font.setPixelSize(18)
        self.setFont(font)


class LabelBottom(QtWidgets.QLabel):
    def __init__(self, parent=None):
        """
        
        :param parent: 
        """
        super(LabelBottom, self).__init__(parent)
        self.setStyleSheet('QLabel{ color: #c0c0c0; }')
        font = self.font()
        self.setFont(font)

    def setText(self, value=None):
        """
        
        :param value: 
        :return: 
        """

        document = QtGui.QTextDocument()
        document.setHtml(value)

        text = re.sub(r'^$\n', ' ', document.toPlainText(), flags=re.MULTILINE)

        return super(LabelBottom, self).setText(text[0:150])


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

    def getTextUp(self):
        return self.textUpQLabel.text()

    def setTextDown(self, text=None):
        """
        
        :param text: 
        :return: 
        """
        self.textDownQLabel.setText(text)

    def getTextDown(self):
        """
        
        :return: 
        """
        return self.textDownQLabel.text()

    def setIcon(self, imagePath):
        """
        
        :param imagePath: 
        :return: 
        """
        self.iconQLabel.setPixmap(QtGui.QPixmap(imagePath))


class NoteItem(QtWidgets.QListWidgetItem):
    def __init__(self, entity=None, widget=None):
        """
        
        :param index: 
        :param name: 
        :param text: 
        """
        super(NoteItem, self).__init__()
        widget.setTextDown(entity.text)
        widget.setTextUp(entity.name)
        self._entity = entity
        self._widget = widget

    @property
    def widget(self):
        """
        
        :return: 
        """
        return self._widget

    @property
    def entity(self):
        """

        :return: 
        """
        return self._entity

    @entity.setter
    def entity(self, entity=None):
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
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet('''
            QListWidget{ border: none; }
            QListWidget::item{ background-color: #fcf9f6; padding: 0px 0px 0px 0px; }
            QListWidget::item:selected{ background-color: #fdfcf9 }
        ''')

    def addLine(self, entity=None):
        """
        
        :param name: 
        :param descrption: 
        :return: 
        """

        item = NoteItem(entity, QCustomQWidget())
        item.setSizeHint(item.widget.sizeHint())

        self.addItem(item)
        self.setItemWidget(item, item.widget)


class RecordList(QtWidgets.QWidget):
    @inject.params(dispatcher='event_dispatcher', storage='storage')
    def __init__(self, parent=None, dispatcher=None, storage=None):
        """
        
        :param parent: 
        """
        super(RecordList, self).__init__(parent)
        self._folder = None

        self.setStyleSheet(''' QListWidget::item{ background-color: #fcf9f6; border: none; }
            QListWidget::item:selected{ background-color: #fdfcf9 } ''')

        self.list = ItemList()
        self.folderEditor = FolderName()
        self.folderEditor.setText('Folder 1')
        self.toolbar = ToolbarbarWidget()

        dispatcher.dispatch('window.notelist.toolbar', (
            self, self.toolbar
        ))

        self.container = QtWidgets.QWidget()

        self.statusbar = QtWidgets.QLabel()
        self.statusbar.setText("Total amount of records: 12")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.folderEditor)
        layout.addWidget(self.list)
        layout.addWidget(self.statusbar)

        self.container.setLayout(layout)
        layout1 = QtWidgets.QHBoxLayout()
        layout1.addWidget(self.toolbar)
        layout1.addWidget(self.container)
        self.setLayout(layout1)

    @property
    def entity(self):
        """

        :return: 
        """
        for index in self.list.selectedIndexes():
            item = self.list.itemFromIndex(index)
            if item is not None and item.entity is not None:
                return item.entity
        return None

    @property
    def folder(self):
        """
        
        :return: 
        """
        return self._folder

    def addLine(self, entity=None):
        """
        
        :param name: 
        :param descrption: 
        :return: 
        """
        self.list.addLine(entity)

    def setFolder(self, folder=None):
        """
        
        :param folder: 
        :return: 
        """
        self._folder = folder
        self.folderEditor.setText(folder.name)

        self.statusbar.setText("%i records found" % self.list.count())

