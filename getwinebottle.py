#!/usr/bin/env python3
# 本来是用C++写的，但在非deepin/UOS编译/运行就是下载不了https文件，只能用python重写
#########################################################################
# 作者：gfdgd xi、为什么您不喜欢熊出没和阿布
# 版本：2.4.0
# 感谢：感谢 deepin-wine 团队，提供了 deepin-wine 给大家使用，让我能做这个程序
# 基于 Python3 的 PyQt5 构建
#########################################################################
#################
# 引入所需的库
#################
import os
import shutil
import random
import sys
import json
import traceback
import requests
programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
sys.path.append(f"{programPath}/../")
from Model import *
from PyQt5 import QtCore, QtGui, QtWidgets
programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
# UI 布局（自动生成）
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(693, 404)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.verticalLayout = QtWidgets.QGridLayout()
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.addButton = QtWidgets.QPushButton(self.centralWidget)
        self.addButton.setObjectName("addButton")
        self.verticalLayout.addWidget(self.addButton, 1, 0)
        self.internetWineList = QtWidgets.QListView(self.centralWidget)
        self.internetWineList.setObjectName("internetWineList")
        self.verticalLayout.addWidget(self.internetWineList, 0, 0)
        self.centralWidget.setLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralWidget)
        # 菜单栏
        _translate = QtCore.QCoreApplication.translate
        self.menu = MainWindow.menuBar()
        self.changeSources = self.menu.addMenu(_translate("MainWindow", "更换源"))
        self.gitlinkAction = QtWidgets.QAction(_translate("MainWindow", "Gitlink 源（推荐）"))
        self.ipv6Action = QtWidgets.QAction(_translate("MainWindow", "备用源（只支持 IPv6 用户）"))
        self.localAction = QtWidgets.QAction(_translate("MainWindow", "本地测试源（127.0.0.1）"))
        self.changeSources.addAction(self.gitlinkAction)
        self.changeSources.addAction(self.ipv6Action)
        self.changeSources.addAction(self.localAction)
        for i in [self.gitlinkAction, self.ipv6Action, self.localAction]:
            i.setCheckable(True)
        self.gitlinkAction.setChecked(True)
        self.changeSourcesGroup = QtWidgets.QActionGroup(MainWindow)
        self.changeSourcesGroup.addAction(self.gitlinkAction)
        self.changeSourcesGroup.addAction(self.ipv6Action)
        self.changeSourcesGroup.addAction(self.localAction)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "下载容器"))
        self.addButton.setText(_translate("MainWindow", "下载"))

def ChangeSources():
    global urlSources
    global internetWineSource
    sources = [ui.gitlinkAction, ui.ipv6Action, ui.localAction]
    for i in range(0, len(sources)):
        if sources[i].isChecked():
            urlSources = internetWineSourceList[i]
            internetWineSource = internetWineSourceList[i]
            # 读取信息
            ReadInternetInformation()
            break
    print(urlSources)

# 下面内容均翻译自 C++ 版本
def ReadInternetInformation():
    global internetJsonList
    # C++ 版本是用 curl 的，考虑到 Python 用 requests 反而方便，于是不用 curl
    try:
        internetJsonList = json.loads(requests.get(f"{internetWineSource}/information.json").text)
    except:
        QtWidgets.QMessageBox.critical(window, "错误", "无法连接服务器！")
        return
    nmodel = QtGui.QStandardItemModel(window)
    for i in internetJsonList:
        item = QtGui.QStandardItem(i[0])
        nmodel.appendRow(item)
    ui.internetWineList.setModel(nmodel)
    
class DownloadThread(QtCore.QThread):
    MessageBoxInfo = QtCore.pyqtSignal(str)
    MessageBoxError = QtCore.pyqtSignal(str)
    ChangeDialog = QtCore.pyqtSignal(QtWidgets.QProgressDialog, int, int, int)
    Finish = QtCore.pyqtSignal()
    def __init__(self, progressDialog: QtWidgets.QProgressDialog, 
        url: str, savePath: str, fileName: str, view: QtWidgets.QListView, deleteZip: bool, 
        unzip: bool, localList) -> None:
        self.dialog = progressDialog
        self.fileUrl = url
        self.fileSavePath = savePath
        self.fileSaveName = fileName
        self.localView = view
        self.downloadDeleteZip = deleteZip
        self.downloadUnzip = unzip
        self.localJsonList = localList
        super().__init__()

    def run(self):
        try:
            # 创建文件夹
            dir = QtCore.QDir()
            savePath = f"{programPath}/{self.fileSaveName}"
            # 文件下载
            timeout = 0
            f = requests.get(self.fileUrl, stream=True)
            allSize = int(f.headers["content-length"])  # 文件总大小
            bytesRead = 0
            with open(savePath, "wb") as filePart:
                for chunk in f.iter_content(chunk_size=1024):
                    if chunk:
                        #progressbar.update(int(part / show))
                        filePart.write(chunk)
                        bytesRead += 1024
                        self.ChangeDialog.emit(self.dialog, int(bytesRead / allSize * 100), int(bytesRead / 1024 / 1024), int(allSize / 1024 / 1024))
            # 写入配置文件
            rfile = open(f"{programPath}/winelist.json", "r")
            list = json.loads(rfile.read())
            rfile.close()
            # C++ 版注释：不直接用 readwrite 是因为不能覆盖写入
            file = open(f"{programPath}/winelist.json", "w")
            list.append(self.fileSaveName.replace(".7z", ""))
            file.write(json.dumps(list))
            file.close()
            # 读取配置文件
            self.ReadLocalInformation()
            self.localJsonList = list
            # 解压文件
            shellCommand = ""
            if self.downloadUnzip:
                path = f"{programPath}/{self.fileSaveName.replace('.7z', '')}"
                shellCommand += f"""mkdir -p \"{path}\"
7z x -y \"{savePath}\" -o\"{path}\"
"""
            if self.downloadDeleteZip:
                shellCommand += f"rm -rf \"{savePath}\"\n"
            shellFile = open("/tmp/depein-wine-runner-wine-install.sh", "w")
            shellFile.write(shellCommand)
            shellFile.close()
            #process = QtCore.QProcess()
            #command = ["deepin-terminal", "-e", "bash", "/tmp/depein-wine-runner-wine-install.sh"]
            #process.start(f"{programPath}/../launch.sh", command)
            #process.waitForFinished()
            OpenTerminal("bash /tmp/depein-wine-runner-wine-install.sh")
            self.Finish.emit()
        except:
            traceback.print_exc()
            self.MessageBoxError.emit(traceback.format_exc())

def MessageBoxInfo(info):
    QtWidgets.QMessageBox.information(window, "提示", info)

def MessageBoxError(info):
    QtWidgets.QMessageBox.critical(window, "错误", info)

def ChangeDialog(dialog: QtWidgets.QProgressDialog, value, downloadBytes, totalBytes):
    dialog.setValue(value)
    dialog.setLabelText(f"{downloadBytes}MB/{totalBytes}MB")

def DownloadFinish():
    ui.centralWidget.setEnabled(True)

class QT:
    thread = None

def on_addButton_clicked():
    choose = ui.internetWineList.currentIndex().row()
    if choose < 0:
        QtWidgets.QMessageBox.information(window, "提示", "您未选中任何项，无法继续")
        return
    downloadName = internetJsonList[choose][1]
    ReadLocalInformation()
    for i in localJsonList:
        if i == internetJsonList[choose][0]:
            QtWidgets.QMessageBox.information(window, "提示", "您已经安装了这个Wine了！无需重复安装！")
            return
    downloadUrl = internetWineSource + downloadName
    dialog = QtWidgets.QProgressDialog()
    cancel = QtWidgets.QPushButton("取消")
    cancel.setDisabled(True)
    dialog.setWindowIcon(QtGui.QIcon(f"{programPath}/../deepin-wine-runner.svg"))
    dialog.setCancelButton(cancel)
    dialog.setWindowTitle(f"正在下载“{internetJsonList[choose][0]}”")
    QT.thread = DownloadThread(
        dialog, 
        downloadUrl, 
        "", 
        internetJsonList[choose][1],
        ui.localWineList,
        ui.deleteZip.isChecked(),
        not ui.unzip.isChecked(),
        localJsonList
        )
    QT.thread.MessageBoxInfo.connect(MessageBoxInfo)
    QT.thread.MessageBoxError.connect(MessageBoxError)
    QT.thread.ChangeDialog.connect(ChangeDialog)
    QT.thread.Finish.connect(DownloadFinish)
    ui.centralWidget.setDisabled(True)
    QT.thread.start()

# 获取当前语言
def get_now_lang()->"获取当前语言":
    return os.getenv('LANG')

if __name__ == "__main__":
    internetJsonList = []
    internetWineSourceList = [
        "https://code.gitlink.org.cn/gfdgd_xi/wine-bottle-library/raw/branch/master/",
        "http://gfdgdxi.msns.cn/wine-bottle-library/", # 备用源，纯 IPv6 源
        "http://127.0.0.1/wine-bottle-library/"  # 本地测试源
        ]
    internetWineSource = internetWineSourceList[0]
    app = QtWidgets.QApplication(sys.argv)
    # 读取翻译
    if not get_now_lang() == "zh_CN.UTF-8":
        trans = QtCore.QTranslator()
        trans.load(f"{programPath}/../LANG/installwine-en_US.qm")
        app.installTranslator(trans)
    # 窗口构建
    window = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    window.setWindowIcon(QtGui.QIcon(f"{programPath}/../deepin-wine-runner.svg"))
    ui.setupUi(window)
    window.show()
    # 连接信号
    ui.addButton.clicked.connect(on_addButton_clicked)
    #ui.delButton.clicked.connect(on_delButton_clicked)
    #ui.addOtherWine.clicked.connect(InstallOtherWine)
    #ui.changeSourcesGroup.triggered.connect(ChangeSources)
    ## 加载内容
    # 设置列表双击不会编辑
    #ui.localWineList.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
    ui.internetWineList.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
    # 读取信息
    ReadInternetInformation()
    # 图标
    ui.centralWidget.setWindowIcon(QtGui.QIcon(f"{programPath}/../deepin-wine-runner.svg"))

    app.exec_()