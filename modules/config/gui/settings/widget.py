# -*- coding: utf-8 -*-

# PYQT5 PyQt4’s QtGui module has been split into PyQt5’s QtGui, QtPrintSupport and QtWidgets modules

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from .text import TextEditor


class SettingsTitle(QtWidgets.QLabel):

    def __init__(self, text):
        super(SettingsTitle, self).__init__(text)


class WidgetSettings(QtWidgets.QGroupBox):

    def __init__(self):
        super(WidgetSettings, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.setMinimumHeight(200)

        effect = QtWidgets.QGraphicsDropShadowEffect()
        effect.setBlurRadius(10)
        effect.setOffset(0)

        self.setGraphicsEffect(effect)


class WidgetSettingsNavigator(WidgetSettings):

    def __init__(self):
        super(WidgetSettingsNavigator, self).__init__()

        self.layout = QtWidgets.QVBoxLayout()

        label = SettingsTitle('Navigator settings')
        self.layout.addWidget(label)

        self.toolbar = QtWidgets.QCheckBox('Toolbar is visible')
        self.layout.addWidget(self.toolbar)

        self.keywords = QtWidgets.QCheckBox('Keywords are visible')
        self.layout.addWidget(self.keywords)

        self.setLayout(self.layout)

        self.show()


class WidgetSettingsEditor(WidgetSettings):

    def __init__(self):
        super(WidgetSettingsEditor, self).__init__()

        self.layout = QtWidgets.QVBoxLayout()

        label = SettingsTitle('Editor settings')
        self.layout.addWidget(label)

        self.formatbar = QtWidgets.QCheckBox('Formatting toolbar is visible')
        self.layout.addWidget(self.formatbar)

        self.rightbar = QtWidgets.QCheckBox('Toolbar at the rith side is visible')
        self.layout.addWidget(self.rightbar)

        self.leftbar = QtWidgets.QCheckBox('Toolbar at the left side is visible')
        self.layout.addWidget(self.leftbar)

        self.setLayout(self.layout)

        self.show()


class WidgetSettingsStorage(WidgetSettings):

    def __init__(self):
        super(WidgetSettingsStorage, self).__init__()

        self.layout = QtWidgets.QVBoxLayout()

        label = SettingsTitle('Storage settings')
        self.layout.addWidget(label)
        
        self.layout.addSpacing(1)

        self.location = QtWidgets.QPushButton('Change')
        self.location.setToolTip("Clone selected folder")
        self.layout.setAlignment(Qt.AlignLeft)
        self.location.setFlat(True)
        self.layout.addWidget(self.location)
        
        self.layout.addSpacing(1)

        self.setLayout(self.layout)

        self.show()


class WidgetSettingsCryptography(WidgetSettings):

    def __init__(self):
        super(WidgetSettingsCryptography, self).__init__()

        self.layout = QtWidgets.QVBoxLayout()

        label = SettingsTitle('Cryptography settings')
        self.layout.addWidget(label)

        self.code = TextEditor('...')
        self.layout.addWidget(self.code)

        self.setLayout(self.layout)

        self.show()

