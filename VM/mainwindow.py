#!/usr/bin/env python3
import os
import sys
programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
sys.path.append(f"{programPath}/../")
sys.path.append(f"{programPath}/")
import json
import subprocess
import program_resources
import ui_mainwindow
import globalenv
from buildvbox import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

stopShowTime = False
m_cpuAll = 0
m_cpuFree = 0

def ShowCPUMessage():
    pass

def MainWindow():
    global cpuGet
    if (__name__ == "__main__"):
        ui.tabWidget.setTabPosition(QTabWidget.West)  # 标签靠左
    else:
        ui.tabWidget.setTabPosition(QTabWidget.East)  # 标签靠左
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
    '''if(os.system("which VBoxManage")):
        if(QMessageBox.question(this, ("提示"), "检测到您似乎没有安装 VirtualBox，立即安装？") == QMessageBox.Yes):
            os.system("xdg-open https:#www.virtualbox.org/wiki/Linux_Downloads")
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
        QMessageBox.critical(window, "错误", "无法读取版本号！")
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
    filePath = QFileDialog.getOpenFileName(this, "选择 ISO 文件", QDir.homePath(), "ISO 镜像文件(*.iso)所有文件(*.*)")[0]
    if(filePath != ""):
        ui.isoPath.setText(filePath)

def on_install_clicked():
    global stopShowTime
    if (ui.vmChooser.currentIndex() == 0):
        if(os.system("which qemu-system-x86_64")):
            if(QMessageBox.question(this, ("提示"), ("您似乎没有安装 Qemu，是否继续创建虚拟机？")) == QMessageBox.No):
                return
    elif (ui.vmChooser.currentIndex() == 1):
        if(os.system("which vboxmanage")):
            if(QMessageBox.question(this, ("提示"), ("您似乎没有安装 VBox，是否继续创建虚拟机？")) == QMessageBox.No):
                return
    elif (ui.vmChooser.currentIndex() == 8):
        if(os.system("which qemu-system-arm")):
            if(QMessageBox.question(this, ("提示"), ("无法检测到 qemu-system-arm，是否继续创建虚拟机？")) == QMessageBox.No):
                return
    elif (ui.vmChooser.currentIndex() == 9):
       if(os.system("which qemu-system-aarch64")):
           if(QMessageBox.question(this, ("提示"), ("无法检测到 qemu-system-aarch64，是否继续创建虚拟机？")) == QMessageBox.No):
               return
    file = QFile(QDir.homePath() + "/.config/deepin-wine-runner/QEMU-EFI")
    archFile = QFile(QDir.homePath() + "/.config/deepin-wine-runner/QEMU-ARCH")
    dir = QDir(QDir.homePath() + "/.config/deepin-wine-runner")
    archFile.open(QIODevice.WriteOnly)
    archFile.write("amd64".encode("utf-8"))
    archFile.close()
    if (ui.systemVersion.currentIndex() == 0):
        if(not QFile.exists(programPath + "/Windows7X86Auto.iso")):
            if(QMessageBox.question(this, ("提示"), ("似乎无法找到 Windows7X86Auto.iso，是否继续创建虚拟机？\n缺少该文件可能会导致虚拟机无法正常启动，尝试重新安装 Wine 运行器再试试？")) == QMessageBox.No):
                return
    elif (ui.systemVersion.currentIndex() == 1):
        if(not QFile.exists(programPath + "/Windows7X64Auto.iso")):
            if(QMessageBox.question(this, ("提示"), ("似乎无法找到 Windows7X64Auto.iso，是否继续创建虚拟机？\n缺少该文件可能会导致虚拟机无法正常启动，尝试重新安装 Wine 运行器再试试？")) == QMessageBox.No):
                return
    elif (ui.systemVersion.currentIndex() == 3):
        if(not QFile.exists("/usr/share/qemu/OVMF.fd") and not QFile.exists(programPath + "/OVMF.fd") and ui.vmChooser.currentIndex() == 0):
            if(QMessageBox.question(this, ("提示"), ("似乎无法找到 UEFI 固件，是否继续创建虚拟机？\nQemu 固件可以在“安装 Qemu”处安装")) == QMessageBox.No):
                return
            if(not dir.exists()):
                dir.mkpath(QDir.homePath() + "/.config/deepin-wine-runner")
            if(not QFile.exists(QDir.homePath() + "/.config/deepin-wine-runner/QEMU-EFI")):
                # 写入用于识别的空文件
                file.open(QIODevice.WriteOnly)
                file.write("1")
                file.close()
    elif (ui.systemVersion.currentIndex() == 4 or
          ui.systemVersion.currentIndex() == 5 or
          ui.systemVersion.currentIndex() == 6 or
          ui.systemVersion.currentIndex() == 7):
        if(ui.vmChooser.currentIndex() == 0):
            QMessageBox.warning(this, ("提示"), ("Qemu 不支持该选项！"))
            return
    elif (ui.systemVersion.currentIndex() == 8):
        if(ui.vmChooser.currentIndex() == 1):
            QMessageBox.warning(this, ("提示"), ("VirtualBox 不支持该选项！"))
            return
        archFile.open(QIODevice.WriteOnly)
        archFile.write("armhf")
        archFile.close()
    elif (ui.systemVersion.currentIndex() == 9):
        if(ui.vmChooser.currentIndex() == 1):
            QMessageBox.warning(this, ("提示"), ("VirtualBox 不支持该选项！"))
            return
        archFile.open(QIODevice.WriteOnly)
        archFile.write("aarch64")
        archFile.close()
    else:
        if(ui.vmChooser.currentIndex() == 0 and QFile.exists(QDir.homePath() + "/.config/deepin-wine-runner/QEMU-EFI")):
            QFile.remove(QDir.homePath() + "/.config/deepin-wine-runner/QEMU-EFI")
    buildvbox(ui.isoPath.text(), ui.systemVersion.currentIndex(), ui.vmChooser.currentIndex())
    ui.tabWidget.setCurrentIndex(1)
    stopShowTime = 1
    ui.CPUValue.showMessage(("提示：目前已经尝试开启虚拟机，如果在一段时间后依旧还没看到虚拟机窗口开启，请在菜单栏查看虚拟机日志"), 10000)
    return

def on_getvbox_clicked():
    QDesktopServices.openUrl(QUrl("https://www.virtualbox.org/wiki/Linux_Downloads"))

def on_getQemu_clicked():
    os.system(("python3 '" + programPath + "/../RunCommandWithTerminal.py' pkexec '" + programPath + "/../QemuSystemInstall.sh'"))

def on_vmChooser_currentIndexChanged(index: int):
    ui.qemuSetting.setDisabled(index)

# TODO
def on_qemuSetting_clicked():
    global show
    show = QemuSetting()
    show.show()

def on_addQemuDisk_triggered():
    if(QFile.exists(QDir.homePath() + "/Qemu/Windows/Windows.qcow2")):
        if(QMessageBox.question(this, ("提示"), ("磁盘文件已存在，是否覆盖？\n覆盖后将无法恢复！")) == QMessageBox.No):
            return
    path = QFileDialog.getOpenFileName(this, ("选择 Qemu 镜像"), QDir.homePath(), ("Qemu镜像(*.qcow2 *.img *.raw *.qcow *.qed *.vdi *.vhdx *.vmdk)所有文件(*.*)"))
    if(path == ""):
        return
    dir = QDir(QDir.homePath() + "/Qemu/Windows")
    if(not dir.exists()):
        dir.mkpath(QDir.homePath() + "/Qemu/Windows")
    if(QFile.exists(QDir.homePath() + "/Qemu/Windows/Windows.qcow2")):
        if(not QFile.remove(QDir.homePath() + "/Qemu/Windows/Windows.qcow2") or not QFile.copy(path, QDir.homePath() + "/Qemu/Windows/Windows.qcow2")):
            QMessageBox.critical(this, ("提示"), ("添加错误！"))
            return
    else:
        if(not QFile.copy(path, QDir.homePath() + "/Qemu/Windows/Windows.qcow2")):
            QMessageBox.critical(this, ("提示"), ("添加错误！"))
            return
    QMessageBox.information(this, ("提示"), ("添加完成！"))

def on_delQemuDisk_triggered():
    if(not QFile.exists(QDir.homePath() + "/Qemu/Windows/Windows.qcow2")):
        QMessageBox.information(this, ("提示"), ("不存在磁盘文件，无法导出"))
        return
    os.system(("xdg-open \"" + QDir.homePath() + "/Qemu/Windows/\""))

def on_addQemuDiskButton_clicked():
    on_addQemuDisk_triggered()

def on_saveQemuDiskButton_clicked():
    on_delQemuDisk_triggered()

def on_delQemuDiskButton_clicked():
    if(not QFile.exists(QDir.homePath() + "/Qemu/Windows/Windows.qcow2")):
        QMessageBox.information(this, ("提示"), ("不存在磁盘文件，无法移除"))
        return
    if(QMessageBox.question(this, ("提示"), ("是否删除？\n删除后将无法恢复！")) == QMessageBox.No):
        return
    if(not QFile.remove(QDir.homePath() + "/Qemu/Windows/Windows.qcow2")):
        QMessageBox.critical(this, ("提示"), ("移除失败"))
        return
    QMessageBox.information(this, ("提示"), ("移除成功"))

def on_kvmTest_clicked():
    if(os.system("which kvm-ok") and not QFile.exists(programPath + "/kvm-ok")):
        QMessageBox.critical(this, ("错误"), ("未识别到命令 kvm-ok\n可以使用命令 sudo apt install cpu-checker 安装"))
        return
    kvm_ok_path = "kvm-ok"
    if(not os.system("which kvm-ok")):
        kvm_ok_path = "kvm-ok"
    elif(QFile.exists(programPath + "/kvm-ok")):
        kvm_ok_path = programPath + "/kvm-ok"
    print(("使用"), kvm_ok_path)
    process = QProcess()
    process.start(kvm_ok_path)
    process.waitForStarted()
    process.waitForFinished()
    if(process.exitCode()):
        QMessageBox.critical(this, ("错误"), ("您的系统不支持使用 kvm：\n") + process.readAll())
        return
    QMessageBox.information(this, ("提示"), ("您的系统支持使用 kvm：\n") + process.readAll())

def on_actionVMRunlLog_triggered():
    if(not os.path.exists("/tmp/windows-virtual-machine-installer-for-wine-runner-run.log")):
        QMessageBox.information(this, ("提示"), ("没有日志文件"))
        return
    file = open("/tmp/windows-virtual-machine-installer-for-wine-runner-run.log")
    QInputDialog.getMultiLineText(this, ("运行日志"), ("虚拟机运行日志"),file.read())
    file.close()
    

def on_actionVMTest_triggered():
    # 运行 Demo
    if(QFile.exists(programPath + "/test.qcow2")):
        # 优先使用本地的磁盘
        os.system(("qemu-system-i386 --hda '" + programPath + "/test.qcow2' -rtc base=localtime > /tmp/windows-virtual-machine-installer-for-wine-runner-run.log 2>&1"))
        return
    # 写入 disk 文件
    file = QFile(":/TestDisk/test.qcow2")
    # 计算随机数
    writeFile = QFile("/tmp/indows-virtual-machine-installer-for-wine-runner-test-disk.qcow2")
    file.open(QIODevice.ReadOnly)
    writeFile.open(QIODevice.WriteOnly)
    writeFile.write(file.readAll())
    file.close()
    writeFile.close()
    os.system("qemu-system-i386 --hda /tmp/indows-virtual-machine-installer-for-wine-runner-test-disk.qcow2 -rtc base=localtime > /tmp/windows-virtual-machine-installer-for-wine-runner-run.log 2>&1")

def on_actionVMInstallLog_triggered():
    if(not os.path.exists("/tmp/windows-virtual-machine-installer-for-wine-runner-install.log")):
        QMessageBox.information(this, ("提示"), ("没有日志文件"))
        return
    file = open("/tmp/windows-virtual-machine-installer-for-wine-runner-install.log")
    QInputDialog.getMultiLineText(this, ("安装日志"), ("虚拟机安装日志"),file.read())
    file.close()

def on_action_StopVirtualBox_triggered():
    vmControl = vbox("")
    vmControl.Stop()


def on_action_StopQemu_triggered():
    vmControl = qemu("")
    vmControl.Stop()

def on_actionQemuDiskAddSpace_triggered():
    data = QInputDialog.getDouble(this, ("磁盘扩容"), "输入扩容多少GB\n注：1、扩容所需要的时间较长，程序可能会出现假死的情况，请不要关闭否则会导致虚拟磁盘损坏\n2、扩展后需要自行在虚拟机使用 Deepin Community Live CD、Live CD、Windows PE\n等工具调整系统分区大小才能使用")[0]
    if(data <= 0):
        return
    # 开始扩容
    result = qemu("").AddDiskSpace(QDir.homePath() + "/Qemu/Windows/Windows.qcow2", data)
    qDebug() << "Exit Code: " << result
    if(result):
        QMessageBox.critical(this, ("错误"), ("扩容失败！"))
        return
    QMessageBox.information(this, ("提示"), ("扩容完成！"))


def on_getDCLC_triggered():
    QDesktopServices.openUrl(QUrl("https://github.com/gfdgd-xi/deepin-community-live-cd/"))



programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
if (__name__ == "__main__"):
    app = QApplication(sys.argv)
else:
    app = globalenv.get_value("app")
this = window = QMainWindow()
ui = ui_mainwindow.Ui_MainWindow()
ui.setupUi(window)
MainWindow()
# 绑定信号
ui.browser.clicked.connect(on_browser_clicked)
ui.install.clicked.connect(on_install_clicked)
ui.getvbox.clicked.connect(on_getvbox_clicked)
ui.getQemu.clicked.connect(on_getQemu_clicked)
ui.vmChooser.currentIndexChanged.connect(on_vmChooser_currentIndexChanged)
ui.qemuSetting.clicked.connect(on_qemuSetting_clicked)
ui.addQemuDisk.triggered.connect(on_addQemuDisk_triggered)
ui.delQemuDisk.triggered.connect(on_delQemuDisk_triggered)
ui.addQemuDiskButton.clicked.connect(on_addQemuDiskButton_clicked)
ui.delQemuDiskButton.clicked.connect(on_delQemuDiskButton_clicked)
ui.saveQemuDiskButton.clicked.connect(on_saveQemuDiskButton_clicked)
ui.kvmTest.clicked.connect(on_kvmTest_clicked)
ui.actionVMRunlLog.triggered.connect(on_actionVMRunlLog_triggered)
ui.actionVMInstallLog.triggered.connect(on_actionVMInstallLog_triggered)
ui.actionVMTest.triggered.connect(on_actionVMTest_triggered)
ui.action_StopQemu.triggered.connect(on_action_StopQemu_triggered)
ui.action_StopVirtualBox.triggered.connect(on_action_StopVirtualBox_triggered)
ui.actionQemuDiskAddSpace.triggered.connect(on_actionQemuDiskAddSpace_triggered)
ui.getDCLC.triggered.connect(on_getDCLC_triggered)
window.show()
sys.exit(app.exec_())