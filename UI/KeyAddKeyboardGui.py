# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'KeyAddKeyboardGui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 195)
        icon = QtGui.QIcon.fromTheme("..")
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.addTips = QtWidgets.QLabel(self.centralwidget)
        self.addTips.setObjectName("addTips")
        self.verticalLayout.addWidget(self.addTips)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.localTips = QtWidgets.QLabel(self.centralwidget)
        self.localTips.setObjectName("localTips")
        self.horizontalLayout.addWidget(self.localTips)
        self.localKeyboardChoose = QtWidgets.QComboBox(self.centralwidget)
        self.localKeyboardChoose.setObjectName("localKeyboardChoose")
        self.horizontalLayout.addWidget(self.localKeyboardChoose)
        self.addTips_2 = QtWidgets.QLabel(self.centralwidget)
        self.addTips_2.setObjectName("addTips_2")
        self.horizontalLayout.addWidget(self.addTips_2)
        self.localKey = QtWidgets.QLineEdit(self.centralwidget)
        self.localKey.setObjectName("localKey")
        self.horizontalLayout.addWidget(self.localKey)
        self.wineTips = QtWidgets.QLabel(self.centralwidget)
        self.wineTips.setObjectName("wineTips")
        self.horizontalLayout.addWidget(self.wineTips)
        self.wineKeyboardChoose = QtWidgets.QComboBox(self.centralwidget)
        self.wineKeyboardChoose.setObjectName("wineKeyboardChoose")
        self.horizontalLayout.addWidget(self.wineKeyboardChoose)
        self.addTipsWine = QtWidgets.QLabel(self.centralwidget)
        self.addTipsWine.setObjectName("addTipsWine")
        self.horizontalLayout.addWidget(self.addTipsWine)
        self.wineKey = QtWidgets.QLineEdit(self.centralwidget)
        self.wineKey.setObjectName("wineKey")
        self.horizontalLayout.addWidget(self.wineKey)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.addButton = QtWidgets.QPushButton(self.centralwidget)
        self.addButton.setObjectName("addButton")
        self.horizontalLayout_2.addWidget(self.addButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "添加快捷键"))
        self.addTips.setText(_translate("MainWindow", "暂时只支持 Ctrl+Alt+? 和 Alt+? 的组合\n"
"文本框内的只能输入单字母"))
        self.localTips.setText(_translate("MainWindow", "本地映射："))
        self.addTips_2.setText(_translate("MainWindow", "+"))
        self.wineTips.setText(_translate("MainWindow", "Wine 容器映射内容："))
        self.addTipsWine.setText(_translate("MainWindow", "+"))
        self.addButton.setText(_translate("MainWindow", "添加快捷键"))

