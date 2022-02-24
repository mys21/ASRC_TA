# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'small_gui.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(889, 682)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(90, 30, 651, 521))
        self.graphicsView.setObjectName("graphicsView")
        self.linesPerFrame = QtWidgets.QLineEdit(self.centralwidget)
        self.linesPerFrame.setGeometry(QtCore.QRect(240, 60, 113, 21))
        self.linesPerFrame.setText("")
        self.linesPerFrame.setObjectName("linesPerFrame")
        self.History = QtWidgets.QTextBrowser(self.centralwidget)
        self.History.setGeometry(QtCore.QRect(460, 70, 261, 191))
        self.History.setObjectName("History")
        self.runButton = QtWidgets.QPushButton(self.centralwidget)
        self.runButton.setGeometry(QtCore.QRect(110, 90, 151, 41))
        self.runButton.setObjectName("runButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(560, 50, 60, 16))
        self.label.setObjectName("label")
        self.linesPerFrameLabel = QtWidgets.QLabel(self.centralwidget)
        self.linesPerFrameLabel.setGeometry(QtCore.QRect(130, 60, 121, 16))
        self.linesPerFrameLabel.setObjectName("linesPerFrameLabel")
        self.pumpsOnPlot = PlotWidget(self.centralwidget)
        self.pumpsOnPlot.setGeometry(QtCore.QRect(100, 300, 301, 241))
        self.pumpsOnPlot.setObjectName("pumpsOnPlot")
        self.pumpsOffPlot = PlotWidget(self.centralwidget)
        self.pumpsOffPlot.setGeometry(QtCore.QRect(410, 300, 311, 241))
        self.pumpsOffPlot.setObjectName("pumpsOffPlot")
        self.pumpOnLabel = QtWidgets.QLabel(self.centralwidget)
        self.pumpOnLabel.setGeometry(QtCore.QRect(100, 270, 151, 20))
        self.pumpOnLabel.setObjectName("pumpOnLabel")
        self.pumpOffLabel = QtWidgets.QLabel(self.centralwidget)
        self.pumpOffLabel.setGeometry(QtCore.QRect(410, 270, 161, 20))
        self.pumpOffLabel.setObjectName("pumpOffLabel")
        self.stopButton = QtWidgets.QPushButton(self.centralwidget)
        self.stopButton.setGeometry(QtCore.QRect(270, 90, 151, 41))
        self.stopButton.setObjectName("stopButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 889, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.runButton.setText(_translate("MainWindow", "Run"))
        self.label.setText(_translate("MainWindow", "History:"))
        self.linesPerFrameLabel.setText(_translate("MainWindow", "Lines per frame:"))
        self.pumpOnLabel.setText(_translate("MainWindow", "Avg Pumps On"))
        self.pumpOffLabel.setText(_translate("MainWindow", "Avg Pumps Off"))
        self.exitCameraButton.setText(_translate("MainWindow", "Exit Camera"))
        self.stopButton.setText(_translate("MainWindow", "Stop"))

from pyqtgraph import PlotWidget
