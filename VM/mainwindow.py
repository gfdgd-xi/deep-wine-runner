#!/usr/bin/env python3
import os
import sys
import json
import subprocess
import ui_mainwindow
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

stopShowTime = False
m_cpuAll = 0
m_cpuFree = 0

def ShowCPUMessage():
    pass

def MainWindow():
    global cpuGet
    ui.tabWidget.setTabPosition(QTabWidget.West)  # 标签靠左
    #QApplication a(argc, argv)
    # 选择最优虚拟机
    if(not os.system("which qemu-system-x86_64")):
        ui.vmChooser.setCurrentIndex(0)
    if(not os.system("which vboxmanage")):
        ui.vmChooser.setCurrentIndex(1)
    if(not os.path.exists(programPath + "/../RunCommandWithTerminal.py")):
        ui.getQemu.setDisabled(True)
    # 允许输出 qDebug 信息
    #QLoggingCategory.defaultCategory().setEnabled(QLoggingCategory.QtDebugMsg, True)
    # 判断是否安装 vbox（无需判断）
    '''if(system("which VBoxManage")){
        if(QMessageBox.question(this, tr("提示"), "检测到您似乎没有安装 VirtualBox，立即安装？") == QMessageBox.Yes){
            system("xdg-open https:#www.virtualbox.org/wiki/Linux_Downloads")
        }
    }'''
    # QTimer
    cpuGet = QTimer(window)
    cpuGet.timeout.connect(ShowCPUMessage)
    cpuGet.setInterval(1000)
    cpuGet.start()
    ShowCPUMessage()
    # 读取程序版本号
    # / 版本号文件是否存在
    if (not os.path.exists(programPath + "/../information.json")):
        QMessageBox.critical(window, "错误", "无法读取版本号！");
        return
    with open(programPath + "/../information.json", "r") as file:
        fileinfo = file.read()
    versionObject = json.loads(fileinfo)
    buildTime = versionObject["Time"]
    versionValue = versionObject["Version"]
    thank = versionObject["Thank"]
    thankText = ""
    for i in range(0, len(thank)):
        thankText += "<p>" + thank[i] + "</p>\n"
        print(thank[i])
    # 设置程序标题
    this.setWindowTitle(("Wine 运行器虚拟机安装工具 ") + versionValue)
    # 读取谢明列表
    ui.textBrowser_2.setHtml(("<p>程序版本号：") + versionValue + ", " + subprocess.getoutput("arch") + ("</p><p>安装包构建时间：") + buildTime +  "</p>" + ui.textBrowser_2.toHtml() +
                               ("<hr/><h1>谢明列表</h1>") + thankText)
    ui.textBrowser_2.anchorClicked.connect(lambda link: QDesktopServices.openUrl(link))
    ui.textBrowser.anchorClicked.connect(lambda link: QDesktopServices.openUrl(link))
    ui.textBrowser_3.anchorClicked.connect(lambda link: QDesktopServices.openUrl(link))
    # 设置标签栏图标
    ui.tabWidget.setTabIcon(1, QIcon.fromTheme(f"{programPath}/application-vnd.oasis.opendocument.text.svg"))
    # 设置窗口图标
    this.setWindowIcon(QIcon(f"{programPath}/deepin-wine-runner.svg"))

def GetRunCommand(command: str):
    return subprocess.getoutput(command)

def on_browser_clicked():
    # 浏览镜像文件
    filePath = QFileDialog.getOpenFileName(this, "选择 ISO 文件", QDir.homePath(), "ISO 镜像文件(*.iso);;所有文件(*.*)");
    if(filePath != ""):
        ui.isoPath.setText(filePath)

programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
app = QApplication(sys.argv)
this = window = QMainWindow()
ui = ui_mainwindow.Ui_MainWindow()
ui.setupUi(window)
MainWindow()
window.show()
sys.exit(app.exec_())