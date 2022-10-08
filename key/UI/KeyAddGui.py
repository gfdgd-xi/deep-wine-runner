# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'KeyAddGui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(692, 314)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tips = QtWidgets.QLabel(self.centralwidget)
        self.tips.setObjectName("tips")
        self.verticalLayout.addWidget(self.tips)
        self.keyBoardList = QtWidgets.QListView(self.centralwidget)
        self.keyBoardList.setObjectName("keyBoardList")
        self.verticalLayout.addWidget(self.keyBoardList)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.addButton = QtWidgets.QPushButton(self.centralwidget)
        self.addButton.setObjectName("addButton")
        self.horizontalLayout.addWidget(self.addButton)
        self.editButton = QtWidgets.QPushButton(self.centralwidget)
        self.editButton.setObjectName("editButton")
        self.horizontalLayout.addWidget(self.editButton)
        self.saveButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveButton.setObjectName("saveButton")
        self.horizontalLayout.addWidget(self.saveButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 692, 33))
        self.menuBar.setObjectName("menuBar")
        self.menu = QtWidgets.QMenu(self.menuBar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menuBar)
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")
        self.serverTips = QtWidgets.QAction(MainWindow)
        self.serverTips.setEnabled(False)
        self.serverTips.setObjectName("serverTips")
        self.startServer = QtWidgets.QAction(MainWindow)
        self.startServer.setObjectName("startServer")
        self.stopServer = QtWidgets.QAction(MainWindow)
        self.stopServer.setObjectName("stopServer")
        self.setAutoStart = QtWidgets.QAction(MainWindow)
        self.setAutoStart.setObjectName("setAutoStart")
        self.setUnautoStart = QtWidgets.QAction(MainWindow)
        self.setUnautoStart.setObjectName("setUnautoStart")
        self.menu.addAction(self.serverTips)
        self.menu.addSeparator()
        self.menu.addAction(self.startServer)
        self.menu.addAction(self.stopServer)
        self.menu.addSeparator()
        self.menu.addAction(self.setAutoStart)
        self.menu.addAction(self.setUnautoStart)
        self.menuBar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "编辑快捷键"))
        self.tips.setText(_translate("MainWindow", "<html><head/><body><p>此工具可以用于设置快捷键到 Wine 容器的映射，以便 Wine 程序可以正常的使用快捷键<br/>Deepin/UOS将会使用默认的快捷键服务，其它发行版将使用此运行器提供的快捷键服务<br>Deepin/UOS将只会提供快捷键添加功能，请在控制中心进行快捷键的修改管理</p></body></html>"))
        self.addButton.setText(_translate("MainWindow", "添加"))
        self.editButton.setText(_translate("MainWindow", "编辑"))
        self.saveButton.setText(_translate("MainWindow", "保存"))
        self.menu.setTitle(_translate("MainWindow", "设置快捷键服务"))
        self.action.setText(_translate("MainWindow", "关于"))
        self.serverTips.setText(_translate("MainWindow", "此内容只支持非Deepin/UOS发行版"))
        self.startServer.setText(_translate("MainWindow", "启动服务"))
        self.stopServer.setText(_translate("MainWindow", "停止服务"))
        self.setAutoStart.setText(_translate("MainWindow", "设置开机自启"))
        self.setUnautoStart.setText(_translate("MainWindow", "关闭开机自启动"))

