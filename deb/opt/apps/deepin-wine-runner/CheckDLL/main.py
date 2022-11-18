import os
import sys
import json
import traceback
import subprocess
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets
# 加入路径
import os
import sys
programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
sys.path.append(f"{programPath}/../")
from Model import *
finding = False
def ReadNeedDll(lists):
    nmodel = QtGui.QStandardItemModel(window)
    if not len(lists):
        item = QtGui.QStandardItem("无")
        nmodel.appendRow(item)
    for i in lists:
        item = QtGui.QStandardItem(i)
        nmodel.appendRow(item)
    needDllList.setModel(nmodel)

def ReadBadNeedDll(lists):
    global finding
    nmodel = QtGui.QStandardItemModel(window)
    if not len(lists):
        item = QtGui.QStandardItem("无")
        nmodel.appendRow(item)
    for i in lists:
        item = QtGui.QStandardItem(i)
        nmodel.appendRow(item)
    badDllList.setModel(nmodel)   
    finding = True

def ErrorMsg(message):
    QtWidgets.QMessageBox.critical(window, "错误", message)

class ReadDll(QtCore.QThread):
    readNeed = QtCore.pyqtSignal(list)
    readBad = QtCore.pyqtSignal(list)
    error = QtCore.pyqtSignal(str)
    def __init__(self) -> None:
        super().__init__()

    def run(self):
        programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
        try:
            output = subprocess.getoutput(f"python3 '{programPath}/CheckCommand.py' '{sys.argv[1]}' --json")
            print(output)
            self.readNeed.emit(json.loads(output))
        except:
            traceback.print_exc()
            self.error.emit(traceback.format_exc())
        try:
            badoutput = subprocess.getoutput(f"python3 '{programPath}/CheckCommand.py' '{sys.argv[1]}' --json -w '{sys.argv[2]}' '{sys.argv[3]}'")
            print(badoutput)
            self.readBad.emit(json.loads(badoutput))
        except:
            traceback.print_exc()
            self.error.emit(traceback.format_exc())

def GetDll():
    global read
    read = ReadDll()
    read.readNeed.connect(ReadNeedDll)
    read.readBad.connect(ReadBadNeedDll)
    read.error.connect(ErrorMsg)
    read.start()

def Change():
    if not finding:
        return
    things = badDllList.selectionModel().selectedIndexes()[0].data().lower()
    repairButton.setEnabled(os.path.exists(f"{programPath}/bash/{things}.sh"))
    findButton.setEnabled(True)
    
def FindDll():
    global dllMap
    things = badDllList.selectionModel().selectedIndexes()[0].data().lower()
    try:
        dllMap["check"]
    except:
        try:
            with open(f"{programPath}/lists.json", "r") as file:
                dllMap = json.loads(file.read())
        except:
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(window, "错误", traceback.format_exc())
            return
    try:
        QtWidgets.QMessageBox.information(window, f"关于“{things}”", dllMap[things])
    except:
        QtWidgets.QMessageBox.information(window, f"关于“{things}”", "无此 Dll 的信息")

def RepairDll():
    things = badDllList.selectionModel().selectedIndexes()[0].data().lower()
    OpenTerminal(f"'{programPath}/../AutoShell/main.py' '{programPath}/bash/{things}.sh'") 

programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
iconPath = "{}/../deepin-wine-runner.svg".format(programPath)
app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QMainWindow()
widget = QtWidgets.QWidget()
layout = QtWidgets.QGridLayout()
badDllList = QtWidgets.QListView()
needDllList = QtWidgets.QListView()
badDllList.clicked.connect(Change)
findButton = QtWidgets.QPushButton("查询此 Dll 信息")
repairButton = QtWidgets.QPushButton("修复此 Dll")
findButton.setDisabled(True)
repairButton.setDisabled(True)
findButton.clicked.connect(FindDll)
repairButton.clicked.connect(RepairDll)
badDllList.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
needDllList.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
loadingTips = QtGui.QStandardItemModel(window)
loadingTipsItem = QtGui.QStandardItem("正在读取……")
loadingTips.appendRow(loadingTipsItem)
badDllList.setModel(loadingTips)
needDllList.setModel(loadingTips)
layout.addWidget(QtWidgets.QLabel("程序需要的 Dll(不太准)："), 0, 0, 1, 1)
layout.addWidget(QtWidgets.QLabel("程序缺失的 Dll(不太准)："), 0, 1, 1, 2)
layout.addWidget(needDllList, 1, 0)
layout.addWidget(badDllList, 1, 1, 1, 2)
layout.addWidget(findButton, 2, 1)
layout.addWidget(repairButton, 2, 2)
widget.setLayout(layout)
window.setCentralWidget(widget)
window.setWindowIcon(QtGui.QIcon(f"{programPath}/deepin-wine-runner.svg"))
window.setWindowTitle(f"查看程序“{os.path.basename(sys.argv[1])}”缺少的 DLL")
window.resize(int(window.frameGeometry().width() * 1.2), int(window.frameGeometry().height() * 1.1))
GetDll()
window.show()
app.exec_()