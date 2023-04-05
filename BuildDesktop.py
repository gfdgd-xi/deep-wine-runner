#!/usr/bin/env python3
# 使用系统默认的 python3 运行
#################################################################################################################
# 作者：gfdgd xi
# 版本：2.5.0
# 更新时间：2022年11月20日
# 感谢：感谢 wine、deepin-wine 以及星火团队，提供了 wine、deepin-wine、spark-wine-devel 给大家使用，让我能做这个程序
# 基于 Python3 的 PyQt5 构建
#################################################################################################################
#################
# 引入所需的库
#################
import os
import sys
import traceback
import updatekiller
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets

desktopList = []
desktopUsrList = []

def GetDesktopList(path):
    for i in os.listdir(path):
        if os.path.isdir(f"{path}/{i}"):
            GetDesktopList(f"{path}/{i}")
        if os.path.isfile(f"{path}/{i}"):
            try:
                desktop = {}
                with open(f"{path}/{i}") as file:
                    things = file.read()
                    for k in things.splitlines():
                        if not "=" in k:
                            continue
                        desktop[k[:k.index("=")].lower()] = k[k.index("=") + 1:]
                desktopList.append([desktop["Name".lower()], desktop["Icon".lower()], desktop["Exec".lower()], f"{path}/{i}"])
            except:
                traceback.print_exc()
    delButton.setEnabled(len(desktopList))

class DesktopList(QtCore.QThread):
    show = QtCore.pyqtSignal(int)
    def __init__(self) -> None:
        super().__init__()

    def run(self):
        if os.path.exists(f"{homePath}/.local/share/applications"):
            GetDesktopList(f"{homePath}/.local/share/applications")
        self.show.emit(0)

def ShowDesktop(temp):
    nmodel = QtGui.QStandardItemModel(window)
    if not len(desktopList):
        item = QtGui.QStandardItem("无")
        nmodel.appendRow(item)
    y = 0
    for i in desktopList:
        #item = QtGui.QStandardItem(QtGui.QIcon(i[1]), i[0])
        #nmodel.appendRow(item)
        if os.path.exists(i[1]):
            nmodel.setItem(y, 0, QtGui.QStandardItem(QtGui.QIcon(i[1]), i[0]))
        else:
            nmodel.setItem(y, 0, QtGui.QStandardItem(QtGui.QIcon.fromTheme(i[1]), i[0]))
        nmodel.setItem(y, 1, QtGui.QStandardItem(i[2]))
        nmodel.setItem(y, 2, QtGui.QStandardItem(i[3]))
        y += 1
    nmodel.setHeaderData(0, QtCore.Qt.Horizontal, "程序名")
    nmodel.setHeaderData(1, QtCore.Qt.Horizontal, "运行路径")
    nmodel.setHeaderData(2, QtCore.Qt.Horizontal, ".desktop 文件所在路径")
    nmodel.setColumnCount(3)
    desktopListView.setModel(nmodel)   

def GetDesktopThread():
    global desktop
    desktop = DesktopList()
    desktop.show.connect(ShowDesktop)
    desktop.start()

def DeleteButton():
    index = desktopListView.currentIndex().row()
    if index < 0:
        QtWidgets.QMessageBox.critical(window, "错误", "未选中任何项")
        return
    print(index)
    print(desktopList[index][3])
    #desktopListView.rowMoved(index)
    
    #desktopListView.removeRow(index)
    try:
        os.remove(desktopList[index][3])
        del desktopList[index]
        ShowDesktop(0)
    except:
        traceback.print_exc()
        QtWidgets.QMessageBox.critical(window, "错误", traceback.format_exc())


programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
homePath = os.getenv("HOME")
iconPath = "{}/deepin-wine-runner.svg".format(programPath)
#GetDesktopList(f"{homePath}/.local/share/applications")
#print(desktopList)
app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QMainWindow()
widget = QtWidgets.QWidget()
layout = QtWidgets.QGridLayout()
delButton = QtWidgets.QPushButton("删除指定图标")
delButton.clicked.connect(DeleteButton)
#desktopListView = QtWidgets.QListView()
desktopListView = QtWidgets.QTableView()
desktopListView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
desktopListView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)#(QAbstractItemView::SelectRows)
layout.addWidget(desktopListView, 0, 0, 1, 4)
layout.addWidget(delButton, 1, 3, 1, 1)
widget.setLayout(layout)
window.setCentralWidget(widget)
window.setWindowTitle("图标管理")
window.resize(int(window.frameGeometry().width() * 1.5), int(window.frameGeometry().height() * 1.2))
window.setWindowIcon(QtGui.QIcon(f"{programPath}/deepin-wine-runner.svg"))
window.show()
GetDesktopThread()
app.exec_()