# -*- coding: utf-8 -*-

# PYQT5 PyQt4’s QtGui module has been split into PyQt5’s QtGui, QtPrintSupport and QtWidgets modules
import inject
from PyQt5.QtCore import Qt

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets


class TextWriter(QtWidgets.QScrollArea):
    def __init__(self, parent=None):
        """

        :param parent: 
        """
        super(TextWriter, self).__init__(parent)

        self.text = TextEditor(self)

        doc = self.text.document()
        doc.setPageSize(QtCore.QSizeF(595, self.height()))
        rootFrame = doc.rootFrame()
        fmt = rootFrame.frameFormat()
        rootFrame.setFrameFormat(fmt)

        # Container widget that holds page
        container = QtWidgets.QWidget(self)

        container.setStyleSheet("background-color: #A0A0A0;")

        # Layout for container
        layout = QtWidgets.QGridLayout(self)

        # Empty widget for spacing
        layout.addWidget(QtWidgets.QWidget(), 0, 0)

        # Add QTextEdit to layout
        layout.addWidget(self.text, 1, 0)

        # Set layout to container
        container.setLayout(layout)

        self.setWidget(container)

        self.setWidgetResizable(True)

        # Align the scrollArea's widget in the center
        self.setAlignment(Qt.AlignHCenter)



class TextEditor(QtWidgets.QTextEdit):
    def __init__(self, parent=None):
        super(TextEditor, self).__init__(parent)

        self.setAcceptDrops(True)
        self.setAcceptRichText(True)
        self.setWordWrapMode(QtGui.QTextOption.WordWrap)
        self.setViewportMargins(50, 50, 20, 20)

        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.setStyleSheet("background-color: #FFFFFF;")
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setMinimumHeight(self.height())
        self.setFixedWidth(595)
        self.setTabStopWidth(33)


class NameEditor(QtWidgets.QLineEdit):
    def __init__(self, parent=None):
        """

        :param parent: 
        """
        super(NameEditor, self).__init__(parent)
        self.setPlaceholderText('Write a title here...')
        self.setClearButtonEnabled(True)

        font = self.font()
        font.setPixelSize(24)
        self.setFont(font)
