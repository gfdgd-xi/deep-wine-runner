import os
import sys
import json
import traceback
import subprocess
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets

def ReadNeedDll(lists):
    nmodel = QtGui.QStandardItemModel(window)
    for i in lists:
        item = QtGui.QStandardItem(i)
        nmodel.appendRow(item)
    needDllList.setModel(nmodel)

def ReadBadNeedDll(lists):
    nmodel = QtGui.QStandardItemModel(window)
    for i in lists:
        item = QtGui.QStandardItem(i)
        nmodel.appendRow(item)
    badDllList.setModel(nmodel)   

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
    read.start()

app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QMainWindow()
widget = QtWidgets.QWidget()
layout = QtWidgets.QGridLayout()
badDllList = QtWidgets.QListView()
needDllList = QtWidgets.QListView()
badDllList.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
needDllList.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
loadingTips = QtGui.QStandardItemModel(window)
loadingTipsItem = QtGui.QStandardItem("正在读取……")
loadingTips.appendRow(loadingTipsItem)
badDllList.setModel(loadingTips)
needDllList.setModel(loadingTips)
layout.addWidget(needDllList, 0, 0)
layout.addWidget(badDllList, 0, 1)
widget.setLayout(layout)
window.setCentralWidget(widget)
window.resize(int(window.frameGeometry().width() * 1.2), int(window.frameGeometry().height() * 1.1))
GetDll()
window.show()
app.exec_()