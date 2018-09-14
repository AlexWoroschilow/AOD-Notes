# -*- coding: utf-8 -*-

# PYQT5 PyQt4’s QtGui module has been split into PyQt5’s QtGui, QtPrintSupport and QtWidgets modules

from PyQt5 import QtWidgets


class WidgetSettingsNavigator(QtWidgets.QWidget):

    def __init__(self):
        super(WidgetSettingsNavigator, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding);

        self.setStyleSheet('margin: 2px 50px; padding: 10px 20px;')
    
        self.layout = QtWidgets.QGridLayout()

        label = QtWidgets.QLabel('Navigator settings')
        label.setStyleSheet('QLabel { font-size: 26px;}')

        self.layout.addWidget(label, 0, 0, 1, 3)

        spacer = QtWidgets.QWidget();
        spacer.setObjectName('spacer')
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding);
        self.layout.addWidget(spacer, 1, 0, 8, 3)

        self.toolbar = QtWidgets.QCheckBox('Toolbar is visible')
        self.layout.addWidget(self.toolbar, 2, 0)

        self.keywords = QtWidgets.QCheckBox('Keywords are visible')
        self.layout.addWidget(self.keywords, 3, 0)

        self.setLayout(self.layout)

        self.show()


class WidgetSettingsEditor(QtWidgets.QWidget):

    def __init__(self):
        super(WidgetSettingsEditor, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding);

        self.setStyleSheet('margin: 2px 50px; padding: 10px 20px;')
    
        self.layout = QtWidgets.QGridLayout()

        label = QtWidgets.QLabel('Editor settings')
        label.setStyleSheet('QLabel { font-size: 26px;}')

        self.layout.addWidget(label, 0, 0, 1, 3)

        spacer = QtWidgets.QWidget();
        spacer.setObjectName('spacer')
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding);
        self.layout.addWidget(spacer, 1, 0, 8, 3)

        self.name = QtWidgets.QCheckBox('Record name is visible')
        self.layout.addWidget(self.name, 2, 0)

        self.formatbar = QtWidgets.QCheckBox('Formatting toolbar is visible')
        self.layout.addWidget(self.formatbar, 3, 0)

        self.rightbar = QtWidgets.QCheckBox('Toolbar at the rith side is visible')
        self.layout.addWidget(self.rightbar, 4, 0)

        self.leftbar = QtWidgets.QCheckBox('Toolbar at the left side is visible')
        self.layout.addWidget(self.leftbar, 5, 0)

        self.setLayout(self.layout)

        self.show()


class WidgetSettingsStorage(QtWidgets.QWidget):

    def __init__(self):
        super(WidgetSettingsStorage, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding);

        self.setStyleSheet('margin: 2px 50px; padding: 10px 20px;')
    
        self.layout = QtWidgets.QGridLayout()

        label = QtWidgets.QLabel('Storage settings')
        label.setStyleSheet('QLabel { font-size: 26px;}')

        self.layout.addWidget(label, 0, 0, 1, 3)

        spacer = QtWidgets.QWidget();
        spacer.setObjectName('spacer')
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding);
        self.layout.addWidget(spacer, 1, 0, 3, 3)

        self.location = QtWidgets.QLabel('...')
        self.layout.addWidget(self.location, 2, 0)

        self.locationChoice = QtWidgets.QPushButton('Change')
        self.locationChoice.setToolTip("Clone selected folder")
        self.locationChoice.setFlat(True)
        self.layout.addWidget(self.locationChoice, 2, 2)

        self.setLayout(self.layout)

        self.show()

