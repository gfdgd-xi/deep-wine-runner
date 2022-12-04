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
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.localWineList = QtWidgets.QListView(self.centralWidget)
        self.localWineList.setObjectName("localWineList")
        self.horizontalLayout_2.addWidget(self.localWineList)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.addButton = QtWidgets.QPushButton(self.centralWidget)
        self.addButton.setObjectName("addButton")
        self.verticalLayout.addWidget(self.addButton)
        self.delButton = QtWidgets.QPushButton(self.centralWidget)
        self.delButton.setObjectName("delButton")
        self.verticalLayout.addWidget(self.delButton)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.internetWineList = QtWidgets.QListView(self.centralWidget)
        self.internetWineList.setObjectName("internetWineList")
        self.horizontalLayout_2.addWidget(self.internetWineList)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        #self.unzip = QtWidgets.QCheckBox(self.centralWidget)
        #self.unzip.setObjectName("unzip")
        #self.horizontalLayout.addWidget(self.unzip)
        #self.deleteZip = QtWidgets.QCheckBox(self.centralWidget)
        #self.deleteZip.setChecked(True)
        #self.deleteZip.setTristate(False)
        #self.deleteZip.setObjectName("deleteZip")
        #self.horizontalLayout.addWidget(self.deleteZip)
        #self.addOtherWine = QtWidgets.QPushButton(self.centralWidget)
        #self.horizontalLayout.addWidget(self.addOtherWine)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
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
        MainWindow.setWindowTitle(_translate("MainWindow", "下载 Qemu 镜像"))
        self.addButton.setText(_translate("MainWindow", "<<"))
        self.delButton.setText(_translate("MainWindow", ">>"))
        #self.unzip.setText(_translate("MainWindow", "不解压Wine资源文件"))
        #self.deleteZip.setText(_translate("MainWindow", "删除下载的资源包，只解压保留（两个选项都选相互抵消）"))
        #self.addOtherWine.setText(_translate("MainWindow", "导入自己的Wine"))

def ReadLocalInformation():
    try:
        global localJsonList
        file = open(f"{homePath}/.deepin-wine-runner-ubuntu-images/lists.json", "r")
        localJsonList = json.loads(file.read())
        nmodel = QtGui.QStandardItemModel(window)
        for i in localJsonList:
            item = QtGui.QStandardItem(i)
            nmodel.appendRow(item)
        ui.localWineList.setModel(nmodel)
        file.close()
    except:
        print("新建空列表")
        try:
            with open(f"{homePath}/.deepin-wine-runner-ubuntu-images/lists.json", "w") as file:
                file.write("[]")
        except:
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(window, "错误", traceback.format_exc())

def InstallOtherWine():
    path = QtWidgets.QFileDialog.getOpenFileName(window, "选择 Wine", os.getenv("~"), "wine(wine);;wine64(wine64);;全部文件(*.*)")
    if path[0] == "" or not path[1]:
        return
    try:
        # 写入配置文件
        rfile = open(f"{homePath}/.deepin-wine-runner-ubuntu-images/winelist.json", "r")
        list = json.loads(rfile.read())
        rfile.close()
        # 创建映射
        name = os.path.basename(os.path.dirname(os.path.dirname(path[0])))
        if name == "" or name == None:
            name = f"useradd-wine-{random.randint(0, 99999)}"
        #binPath = os.path.dirname(os.path.dirname(path[0]))
        os.makedirs(f"{programPath}/{name}/bin")
        if os.system(f"ln -s '{path[0]}' '{programPath}/{name}/bin/wine'") != 0:
            QtWidgets.QMessageBox.critical(window, "新建wine映射失败")
        # C++ 版注释：不直接用 readwrite 是因为不能覆盖写入
        file = open(f"{homePath}/.deepin-wine-runner-ubuntu-images/lists.json", "w")
        list.append(name)
        file.write(json.dumps(list))
        file.close()
    except:
        traceback.print_exc()
        QtWidgets.QMessageBox.critical(window, "错误", traceback.format_exc())
    ReadLocalInformation()

def ChangeSources():
    global urlSources
    global internetWineSource
    sources = [ui.gitlinkAction, ui.ipv6Action, ui.localAction]
    for i in range(0, len(sources)):
        if sources[i].isChecked():
            urlSources = internetWineSourceList[i]
            internetWineSource = internetWineSourceList[i]
            # 读取信息
            ReadLocalInformation()
            ReadInternetInformation()
            break
    print(urlSources)

# 下面内容均翻译自 C++ 版本
def ReadInternetInformation():
    global internetJsonList
    # C++ 版本是用 curl 的，考虑到 Python 用 requests 反而方便，于是不用 curl
    try:
        internetJsonList = json.loads(requests.get(f"{internetWineSource}/lists.json").text)
        internetJsonListNew = []
        for k in internetJsonList:
            archList = json.loads(requests.get(f"{internetWineSource}/{k}/lists.json").text)
            for e in archList:
                internetJsonListNew.append([e[0], e[1], k])
        internetJsonList = internetJsonListNew
    except:
        traceback.print_exc()
        QtWidgets.QMessageBox.critical(window, "错误", "无法连接服务器！")
        return
    print(internetJsonList)
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

    def ReadLocalInformation(self):
        global localJsonList
        try:
            file = open(f"{homePath}/.deepin-wine-runner-ubuntu-images/lists.json", "r")
            nmodel = QtGui.QStandardItemModel()
            localJsonList = json.loads(file.read())
            for i in localJsonList:
                nmodel.appendRow(QtGui.QStandardItem(i))
            self.localView.setModel(nmodel)
            file.close()
        except:
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(window, "错误", traceback.format_exc())

    def run(self):
        try:
            # 创建文件夹
            dir = QtCore.QDir()
            #savePath = f"{programPath}/{self.fileSaveName}"
            choose = ui.internetWineList.currentIndex().row()
            arch = internetJsonList[choose][2]
            savePath = f"{homePath}/.deepin-wine-runner-ubuntu-images/{arch}/{self.fileSaveName}"
            if not os.path.exists(os.path.dirname(savePath)):
                os.makedirs(os.path.dirname(savePath))
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
                        self.ChangeDialog.emit(self.dialog, bytesRead / allSize * 100, bytesRead / 1024 / 1024, allSize / 1024 / 1024)
            self.ChangeDialog.emit(self.dialog, 100, 100, 100)
            # 写入配置文件
            rfile = open(f"{homePath}/.deepin-wine-runner-ubuntu-images/lists.json", "r")
            list = json.loads(rfile.read())
            rfile.close()
            # C++ 版注释：不直接用 readwrite 是因为不能覆盖写入
            file = open(f"{homePath}/.deepin-wine-runner-ubuntu-images/lists.json", "w")
            list.append(self.fileSaveName.replace(".tar.gz", ""))
            file.write(json.dumps(list))
            file.close()
            # 读取配置文件
            self.ReadLocalInformation()
            self.localJsonList = list
            # 解压文件
            shellCommand = ""
            path = f"{homePath}/.deepin-wine-runner-ubuntu-images/{arch}/{self.fileSaveName.replace('.tar.gz', '')}/"
            #path = f"{programPath}/{self.fileSaveName.replace('.7z', '')}"
            shellCommand += f"""#!/bin/bash
mkdir -p \"{path}\"
tar -xvf \"{savePath}\" -C \"{path}\"
rm \"{savePath}\"
"""
            #if self.downloadDeleteZip:
            #    shellCommand += f"rm -rf \"{savePath}\"\n"
            shellFile = open("/tmp/depein-wine-runner-wine-install.sh", "w")
            shellFile.write(shellCommand)
            shellFile.close()
            process = QtCore.QProcess()
            command = ["deepin-terminal", "-e", "bash", "/tmp/depein-wine-runner-wine-install.sh"]
            process.start(f"{programPath}/../launch.sh", command)
            process.waitForFinished()
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
        if i.replace(".tar.gz", "") == internetJsonList[choose][0]:
            QtWidgets.QMessageBox.information(window, "提示", "您已经安装了这个镜像了！无需重复安装！")
            return
    #if(ui.deleteZip.isChecked() + ui.unzip.isChecked() == 2):
     #   ui.deleteZip.setChecked(False)
      #  ui.unzip.setChecked(False)
    arch = internetJsonList[choose][2]
    downloadUrl = f"{internetWineSource}/{arch}/{downloadName}"
    dialog = QtWidgets.QProgressDialog()
    cancel = QtWidgets.QPushButton("取消")
    cancel.setDisabled(True)
    dialog.setWindowIcon(QtGui.QIcon(f"{programPath}/deepin-wine-runner.svg"))
    dialog.setCancelButton(cancel)
    dialog.setWindowTitle(f"正在下载“{internetJsonList[choose][0]}”")
    QT.thread = DownloadThread(
        dialog, 
        downloadUrl, 
        "", 
        internetJsonList[choose][1],
        ui.localWineList,
        False,
        not True,
        localJsonList
        )
    QT.thread.MessageBoxInfo.connect(MessageBoxInfo)
    QT.thread.MessageBoxError.connect(MessageBoxError)
    QT.thread.ChangeDialog.connect(ChangeDialog)
    QT.thread.Finish.connect(DownloadFinish)
    ui.centralWidget.setDisabled(True)
    QT.thread.start()

def on_delButton_clicked():
    if os.path.exists("/tmp/deepin-wine-runner-qemu-lock"):
        if QtWidgets.QMessageBox.question(window, "提示", "检测到您的电脑已经运行了 Qemu/Chroot 容器，建议您重启电脑后再删除该容器，否则容易造成数据损失！\n是否取消操作？") == QtWidgets.QMessageBox.Yes:
            return
    if QtWidgets.QMessageBox.question(window, "提示", "你确定要删除吗？") == QtWidgets.QMessageBox.No:
        return
    if ui.localWineList.currentIndex().row() < 0:
        QtWidgets.QMessageBox.information(window, "提示", "您未选择任何项")
        return
    try:
        # {localJsonList[ui.localWineList.currentIndex().row()]}
        path = f"{homePath}/.deepin-wine-runner-ubuntu-images/"
        changed = False
        for i in os.listdir(path):
            if os.path.exists(f"{path}/{i}/{localJsonList[ui.localWineList.currentIndex().row()]}"):
                changed = True
                name = f"{path}/{i}/{localJsonList[ui.localWineList.currentIndex().row()]}".replace(".tar.gz", "")
        if not changed:
            name = f"{path}/i386/{localJsonList[ui.localWineList.currentIndex().row()]}".replace(".tar.gz", "")
        print(name)
        # 必须取消挂载目录才行
        os.system(f"bash '{programPath}/UnMount.sh' '{name}'")
        #name = f"{homePath}/.deepin-wine-runner-ubuntu-images/{localJsonList[ui.localWineList.currentIndex().row()]}"
        dir = QtCore.QDir(name)
        dir.removeRecursively()
        QtCore.QFile.remove(name + ".tar.gz")
        del localJsonList[ui.localWineList.currentIndex().row()]
        file = open(f"{homePath}/.deepin-wine-runner-ubuntu-images/lists.json", "w")
        file.write(json.dumps(localJsonList))
        file.close()
        ReadLocalInformation()
        QtWidgets.QMessageBox.information(window, "提示", "删除成功！")
    except:
        traceback.print_exc()
        QtWidgets.QMessageBox.critical(window, "错误", traceback.format_exc())

# 获取当前语言
def get_now_lang()->"获取当前语言":
    return os.getenv('LANG')

if __name__ == "__main__":
    homePath = os.getenv("HOME")
    localJsonList = []
    internetJsonList = []
    internetWineSourceList = [
        "https://code.gitlink.org.cn/gfdgd_xi/deepin-wine-runner-ubuntu-image/raw/branch/master/Sandbox",
        "http://gfdgdxi.msns.cn/deepin-wine-runner-ubuntu-image/Sandbox", # 备用源，纯 IPv6 源
        "http://127.0.0.1/deepin-wine-runner-ubuntu-image/Sandbox/"  # 本地测试源
        ]
    internetWineSource = internetWineSourceList[0]
    app = QtWidgets.QApplication(sys.argv)
    if os.system("which qemu-i386-static"):
        if QtWidgets.QMessageBox.question(None, "提示", "检测到您未安装 qemu-user-static，是否安装？") == QtWidgets.QMessageBox.Yes:
            OpenTerminal(f"pkexec bash '{programPath}/ShellList/InstallQemuUserStatic.sh'")
        exit()
    try:
        if not os.path.exists(f"{homePath}/.deepin-wine-runner-ubuntu-images/"):
            os.makedirs(f"{homePath}/.deepin-wine-runner-ubuntu-images/")
    except:
        traceback.print_exc()
        QtWidgets.QMessageBox.critical(None, "错误", traceback.format_exc())
        exit()
    # 读取翻译
    if not get_now_lang() == "zh_CN.UTF-8":
        trans = QtCore.QTranslator()
        trans.load(f"{programPath}/../LANG/installwine-en_US.qm")
        app.installTranslator(trans)
    # 窗口构建
    window = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    window.setWindowIcon(QtGui.QIcon(f"{programPath}/deepin-wine-runner.svg"))
    ui.setupUi(window)
    window.show()
    # 连接信号
    ui.addButton.clicked.connect(on_addButton_clicked)
    ui.delButton.clicked.connect(on_delButton_clicked)
    #ui.addOtherWine.clicked.connect(InstallOtherWine)
    ui.changeSourcesGroup.triggered.connect(ChangeSources)
    ## 加载内容
    # 设置列表双击不会编辑
    ui.localWineList.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
    ui.internetWineList.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
    # 读取信息
    ReadLocalInformation()
    ReadInternetInformation()
    # 图标
    ui.centralWidget.setWindowIcon(QtGui.QIcon(f"{programPath}/../deepin-wine-runner.svg"))

    app.exec_()
exit()
#!/usr/bin/env python3
import os
import sys
import json
import traceback
import req as requests
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets
from Model import *

sources = [
    "https://code.gitlink.org.cn/gfdgd_xi/deepin-wine-runner-ubuntu-image/raw/branch/master/Sandbox"
]
sourceIndex = 0

def ReadTXT(path: str) -> str:
    with open(path, "r") as file:
        things = file.read()
    return things

def WriteTXT(path: str, text: str) -> None:
    with open(path, "w") as file:
        file.write(text)

def CheckVersion(arch: str) -> bool:
    information = requests.get(f"{sources[sourceIndex]}/{arch}/lists.json").json()[0]
    if not os.path.exists(f"{homePath}/.deepin-wine-runner-ubuntu-images/{arch}"):
        return False
    localInformation = json.loads(ReadTXT(f"{homePath}/.deepin-wine-runner-ubuntu-images/lists.json"))
    try:
        if localInformation["arch"][0] == information[0]:
            print("版本相同")
            return True
        return False
    except:
        return False

if __name__ == "__main__":
    programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
    homePath = os.getenv("HOME")
    app = QtWidgets.QApplication(sys.argv)
    if os.system("which qemu-i386-static"):
        if QtWidgets.QMessageBox.question(None, "提示", "检测到您未安装 qemu-user-static，是否安装？") == QtWidgets.QMessageBox.Yes:
            OpenTerminal(f"pkexec bash '{programPath}/ShellList/InstallQemuUserStatic.sh'")
        exit()
    while True:
        archList = requests.get(f"{sources[sourceIndex]}/lists.json").json()
        choose = QtWidgets.QInputDialog.getItem(None, "选择", "选择要安装/更新的镜像对应的架构", archList, 0, False)
        if not choose[1]:
            QtWidgets.QMessageBox.information(None, "提示", "用户取消操作")
            break
        try:
            if CheckVersion(choose[0]):
                QtWidgets.QMessageBox.information(None, "提示", "最新版本，无需操作")
                continue

        except:
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(None, "出现错误", traceback.format_exc())
            continue