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
        # font.setPixelSize(12)
        self.setFont(font)

    def setText(self, value=None):
        """
        
        :param value: 
        :return: 
        """

        def remove_extra_spaces(data):
            p = re.compile(r'\s+')
            return p.sub(' ', data)

        def remove_html_tags(data):
            p = re.compile(r'<.*?>')
            return remove_extra_spaces(p.sub('', data))

        return super(LabelBottom, self).setText(remove_html_tags(value))


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
        return self.textDownQLabel.text()

    def setIcon(self, imagePath):
        self.iconQLabel.setPixmap(QtGui.QPixmap(imagePath))


class NoteItem(QtWidgets.QListWidgetItem):
    def __init__(self, index=None, widget=None):
        """
        
        :param index: 
        :param name: 
        :param text: 
        """
        super(NoteItem, self).__init__()
        self._widget = widget
        self._index = index
        self._name = None
        self._text = None

    @property
    def widget(self):
        """

        :return: 
        """
        return self._widget

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
        self.widget.setTextUp(value)
        self._name = value

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
        self.widget.setTextDown(value)
        self._text = value


class ItemList(QtWidgets.QListWidget):
    def __init__(self, parent=None):
        """
        
        :param parent: 
        """
        super(ItemList, self).__init__(parent)
        self.setStyleSheet('''
            QListWidget::item{ background-color: #fcf9f6; border: none; }
            QListWidget::item:selected{ background-color: #fdfcf9 }
        ''')

    def addLine(self, index=None, name=None, text=None):
        """
        
        :param name: 
        :param descrption: 
        :return: 
        """

        item = NoteItem(index, QCustomQWidget())
        item.setSizeHint(item.widget.sizeHint())
        item.name = name
        item.text = text

        self.addItem(item)
        self.setItemWidget(item, item.widget)


class RecordList(QtWidgets.QWidget):
    def __init__(self, parent=None):
        """
        
        :param parent: 
        """
        super(RecordList, self).__init__(parent)
        self.setStyleSheet(''' QListWidget::item{ background-color: #fcf9f6; border: none; }
            QListWidget::item:selected{ background-color: #fdfcf9 } ''')
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
        layout1.setContentsMargins(10, 0, 0, 10)
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
