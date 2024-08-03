#!/usr/bin/env python3
#   库的引用
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore

import os
import sys
import json
import welcome
import subprocess
import WindowModule

# 读取文本文档
def readtxt(path):
    f = open(path, "r") # 设置文件对象
    str = f.read()  # 获取内容
    f.close()  # 关闭文本对象
    return str  # 返回结果

def ProgramVersion():
    information = json.loads(readtxt(f"{programPath}/information.json"))
    return information["Version"]

#   创建界面
class Window(QtWidgets.QWidget):
    moduleMapList = {}

    def __init__(self):
        super().__init__()
        self.counter_a = 1
        self.counter_b = 1
        self.counter_c = 1
        self.widgetList = list()
        self.initUI()

    def initUI(self):
        self.setMinimumSize(800, 600)
        self.setWindowTitle("Wine 运行器 {}".format(ProgramVersion()))
        self.mainLayout = QtWidgets.QHBoxLayout()
        self.setLayout(self.mainLayout)

        #   左侧区域
        self.leftWidget = LeftWidget()
        self.mainLayout.addWidget(self.leftWidget)

        time = 0
        for i in WindowModule.moduleNameList.keys():
            self.moduleMapList[self.leftWidget.actionList[i].text()] = [i, WindowModule.moduleNameList[i]["Name"]]
            self.leftWidget.actionList[i].triggered.connect(lambda: self.add(self.sender().text()))

        #self.leftWidget.btn4.clicked.connect(self.delCurrent)
        self.leftWidget.list1.itemClicked.connect(self.switchWidget)

        #   右侧区域
        self.rightWidget = RightWidget()
        self.mainLayout.addWidget(self.rightWidget)

        self.addWelcome()

        # 判断运行器是否为第一次打开，如果不是则默认切换至 Wine 运行器主窗口
        # 默认为列表里的第一个控件
        if (os.path.exists(get_home() + "/.config/deepin-wine-runner")):
            self.add(self.leftWidget.actionList[list(WindowModule.moduleNameList.keys())[0]].text())
        self.ConfigureConfigFile()


    #   新增欢迎界面
    def addWelcome(self):
        self.newTab = "欢迎页面"
        self.leftWidget.list1.addItem(self.newTab)

        self.newWidget = welcome.WinWelcome()
        self.widgetList.append(self.newWidget)
        self.rightWidget.addWidget(self.newWidget)

    #   新增界面
    def add(self, actionName: str):
        self.newInfo = "{}#{}".format(self.moduleMapList[actionName][1], self.counter_a)
        self.newTab = ItemWidget(self.newInfo)
        self.newTab.btn.clicked.connect(self.delCurrent)
        self.counter_a += 1
        self.leftWidget.list1.addItem(self.newTab)
        self.leftWidget.list1.setItemWidget(self.newTab, self.newTab.widget)

        self.newWidget = WindowModule.RunnerWindow(app, self.moduleMapList[actionName][0]).Win()
        self.widgetList.append(self.newWidget)
        self.rightWidget.addWidget(self.newWidget)

        # 自动切换新打开的页面
        self.leftWidget.list1.setCurrentRow(self.leftWidget.list1.model().rowCount() - 1)  # 设置选择最后一项
        self.switchWidget()


    #   删除_本页面
    def delCurrent(self):
        self.length = self.leftWidget.list1.count()
        print(self.length)
        self.row = self.leftWidget.list1.currentRow()
        print(self.row)
        if self.row == 0:
            return 0
        self.leftWidget.list1.takeItem(self.row)
        self.rightWidget.removeWidget(self.widgetList[self.row])
        self.widgetList.pop(self.row)

        #   将新界面的关闭按钮设为可用
        if self.row == self.length - 1:
            if self.row == 1:
                return 0
            else:
                self.leftWidget.list1.item(self.row - 1).btnEnable()
        else:
            self.leftWidget.list1.item(self.row).btnEnable()

    #   切换页面
    def switchWidget(self):
        self.row = self.leftWidget.list1.currentRow()
        self.rightWidget.setCurrentIndex(self.row)
        
        #   将当前页的关闭按钮设为可用
        for i in range(self.leftWidget.list1.count()):
            if i == 0:
                continue
            else:
                self.leftWidget.list1.item(i).btnDisable()
        if self.row != 0:
            self.leftWidget.list1.currentItem().btnEnable()
            

    def ConfigureConfigFile(self):
        if not os.path.exists(get_home() + "/.config/"):  # 如果没有配置文件夹
            os.mkdir(get_home() + "/.config/")  # 创建配置文件夹
        if not os.path.exists(get_home() + "/.config/deepin-wine-runner"):  # 如果没有配置文件夹
            os.mkdir(get_home() + "/.config/deepin-wine-runner")  # 创建配置文件夹
        
#   左侧区域
class LeftWidget(QtWidgets.QWidget):
    actionList = {}
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setFixedWidth(120)
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.mainLayout)

        #   左侧标题
        self.lab1 = QtWidgets.QLabel("<h3>页面导航区</h3>")
        self.mainLayout.addWidget(self.lab1)

        #   新建页面面按钮
        self.btnAdd = QtWidgets.QPushButton("新建界面")
        self.mainLayout.addWidget(self.btnAdd)
        self.menuAdd = QtWidgets.QMenu()
        self.btnAdd.setMenu(self.menuAdd)

        for i in WindowModule.moduleNameList.keys():
            action = QtWidgets.QAction("新建{}".format(WindowModule.moduleNameList[i]["Name"]))
            self.actionList[i] = action
            self.menuAdd.addAction(action)

        #   左侧页面列表
        self.list1 = QtWidgets.QListWidget()
        self.mainLayout.addWidget(self.list1)

        #   删_页面按钮
        self.archLabel = QtWidgets.QLabel("系统架构：{}".format(subprocess.getoutput("dpkg --print-architecture")))
        self.mainLayout.addWidget(self.archLabel)

#   列表项目组件
class ItemWidget(QtWidgets.QListWidgetItem):
    def __init__(self, info):
        super().__init__()
        self.info = info
        self.initUI()

    def initUI(self):
        self.widget = QtWidgets.QWidget()
        self.mainLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.setContentsMargins(2, 0, 0, 0)
        self.widget.setLayout(self.mainLayout)

        #   文字标签
        self.lab = QtWidgets.QLabel(self.info)
        self.mainLayout.addWidget(self.lab)
        self.mainLayout.addStretch()

        #   关闭按钮
        self.btn = QtWidgets.QPushButton("x")
        #self.btn.setMaximumWidth(20)
        self.btn.setEnabled(False)
        self.mainLayout.addWidget(self.btn)

    #   将按钮设为可用
    def btnEnable(self):
        self.btn.setEnabled(True)

    #   将按钮设为不可用
    def btnDisable(self):
        self.btn.setEnabled(False)

#   右侧区域
class RightWidget(QtWidgets.QStackedWidget):
    def __init__(self):
        super().__init__()
        #self.initUI()

    #def initUI(self):

# 获取用户主目录
def get_home():
    return os.path.expanduser('~')

programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
iconPath = "{}/deepin-wine-runner.svg".format(programPath)

#   运行程序
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = Window()
    mainWindow.setWindowIcon(QtGui.QIcon(iconPath))
    mainWindow.show()
    mainWindow.resize(int(mainWindow.geometry().width() * 1.2), int(mainWindow.geometry().height() * 1.2))
    sys.exit(app.exec())