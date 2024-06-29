#!/usr/bin/env python3
# 使用系统默认的 python3 运行
#################################################################################################################
# 作者：gfdgd xi
# 版本：3.0.0
# 更新时间：2022年12月10日
# 感谢：感谢 wine、deepin-wine 以及星火团队，提供了 wine、deepin-wine、spark-wine-devel 给大家使用，让我能做这个程序
# 基于 Python3 的 PyQt5 构建
#################################################################################################################
#################
# 引入所需的库
#################
import os
import sys
import time
import json
import random
import base64
import shutil
import hashlib
import platform
import pyperclip
import threading
import traceback
import webbrowser
import updatekiller
import subprocess
import req as requests
import urllib.parse as parse
try:
    import PyQt5.QtGui as QtGui
except:
    os.system("python3 -m pip install --upgrade pyqt5 --trusted-host https://repo.huaweicloud.com -i https://repo.huaweicloud.com/repository/pypi/simple")
    os.system("python3 -m pip install --upgrade pyqt5 --trusted-host https://repo.huaweicloud.com -i https://repo.huaweicloud.com/repository/pypi/simple --break-system-packages")
    import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets
try:
    import PyQt5.QtWebEngineWidgets as QtWebEngineWidgets
    bad = False
except:
    threading.Thread(target=os.system, args=["python3 -m pip install --upgrade PyQtWebEngine --trusted-host https://repo.huaweicloud.com -i https://repo.huaweicloud.com/repository/pypi/simple"]).start()
    threading.Thread(target=os.system, args=["python3 -m pip install --upgrade PyQtWebEngine --trusted-host https://repo.huaweicloud.com -i https://repo.huaweicloud.com/repository/pypi/simple --break-system-packages"]).start()
    bad = True
from trans import *
from Model import *
from DefaultSetting import *

def PythonLower():
    app = QtWidgets.QApplication(sys.argv)
    QtWidgets.QMessageBox.critical(None, "错误", "Python 至少需要 3.6 及以上版本，目前版本：" + platform.python_version() + "")
    sys.exit(1)

# Python 版本检测，因为 f-string 格式化要至少 Python 3.6 及以上的版本，所以需要检测
# 判断主版本号
if sys.version_info[0] < 3:
    PythonLower()
if sys.version_info[1] < 6:
    PythonLower()

###################
# 程序所需事件
###################

def MiniMode(mode):
    for i in [sparkWineSetting, qemuMenu, installLib, log, safeWebsize,
              checkValue, virtualMachine, killProgram, killBottonProgram,
              fontAppStore, wineConfig, trasButton, button5,
              saveDesktopFileOnLauncher, label_r_2, combobox1,
              leftDown]:
        i.setVisible(not mode)

# 打开程序官网
def OpenProgramURL():
    webbrowser.open_new_tab(programUrl)

# 读取文本文档
def readtxt(path):
    f = open(path, "r") # 设置文件对象
    str = f.read()  # 获取内容
    f.close()  # 关闭文本对象
    return str  # 返回结果

# 写入文本文档
def write_txt(path, things):
    file = open(path, 'w', encoding='UTF-8')  # 设置文件对象
    file.write(things)  # 写入文本
    file.close()  # 关闭文本对象

# 获取用户桌面目录
def get_desktop_path():
    for line in open(get_home() + "/.config/user-dirs.dirs"):  # 以行来读取配置文件
        desktop_index = line.find("XDG_DESKTOP_DIR=\"")  # 寻找是否有对应项，有返回 0，没有返回 -1
        if desktop_index != -1:  # 如果有对应项
            break  # 结束循环
    if desktop_index == -1:  # 如果是提前结束，值一定≠-1，如果是没有提前结束，值一定＝-1
        return -1
    else:
        get = line[17:-2]  # 截取桌面目录路径
        get_index = get.find("$HOME")  # 寻找是否有对应的项，需要替换内容
        if get != -1:  # 如果有
            get = get.replace("$HOME", get_home())  # 则把其替换为用户目录（～）
        return get  # 返回目录

# 获取用户主目录
def get_home():
    return os.path.expanduser('~')

# 第一个浏览按钮事件
def liulanbutton():
    path = QtWidgets.QFileDialog.getExistingDirectory(widget, "选择 wine 容器", json.loads(readtxt(get_home() + "/.config/deepin-wine-runner/WineBotton.json"))["path"])
    if path != "" and path != "()":
        e1.setEditText(path)
        write_txt(get_home() + "/.config/deepin-wine-runner/WineBotton.json", json.dumps({"path": path}))  # 写入配置文件

# 第二个浏览按钮事件
def liulanexebutton():
    path = QtWidgets.QFileDialog.getOpenFileName(widget, "选择 exe 可执行文件", json.loads(readtxt(get_home() + "/.config/deepin-wine-runner/FindExe.json"))["path"], "exe 可执行文件(*.exe);;MSI 文件(*.msi);;所有文件(*.*)")
    if path != "" and path != "()":
        e2.setEditText(path[0])  # 显示路径
        write_txt(get_home() + "/.config/deepin-wine-runner/FindExe.json", json.dumps({"path": os.path.dirname(path[0])}))  # 写入配置文件
        
run = None
# 使用多线程运行可执行文件
def runexebutton(self):
    global run
    DisableButton(True)
    if not CheckProgramIsInstall(wine[o1.currentText()]) and not o1.currentText() in untipsWine:
        if QtWidgets.QMessageBox.question(widget, "提示", "检查到您未安装这个 wine，是否继续使用这个 wine 运行？") == QtWidgets.QMessageBox.No:
            DisableButton(False)
            return
    if e2.currentText() == "":  # 判断文本框是否有内容
        QtWidgets.QMessageBox.information(widget, "提示", "没有填写需要使用的 exe 应用")
        DisableButton(False)
        return
    returnText.setText("")
    run = Runexebutton_threading()
    run.signal.connect(QT.ShowWineReturn)
    run.showHistory.connect(QT.ShowHistory)
    run.start()

class QT:
    message = None
    def ShowWineReturn(things):
        returnText.insertPlainText(things)

    def ShowHistory(temp):
        e1.clear()
        e2.clear()
        e2.addItems(wineBottonHistory)
        e2.setEditText(wineBottonHistory[-1])
        e1.addItems(findExeHistory)
        e1.setEditText(findExeHistory[-1])

repairList = []
# Flag: 日志推断解决方案功能
class LogChecking():
    def ShowWindow():
        global logThread
        global logWindow
        global questionList
        global repairButton
        logWindow = QtWidgets.QWidget()
        logWindowLayout = QtWidgets.QGridLayout()
        questionList = QtWidgets.QListView()
        repairButton = QtWidgets.QPushButton("一键修复")
        repairButton.setDisabled(True)
        repairButton.clicked.connect(LogChecking.RepairButton)
        nmodel = QtGui.QStandardItemModel(window)
        item = QtGui.QStandardItem("正在分析中……")
        questionList.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        nmodel.appendRow(item)
        questionList.setModel(nmodel)
        logWindowLayout.addWidget(questionList, 0, 0, 3, 1)
        logWindowLayout.addWidget(repairButton, 0, 2, 1, 1)
        logWindow.setWindowTitle("分析日志")
        logWindow.setLayout(logWindowLayout)
        logThread = LogThreading()
        logThread.done.connect(LogChecking.Show)
        logThread.start()
        logWindow.setWindowIcon(QtGui.QIcon(f"{programPath}/deepin-wine-runner.svg"))
        logWindow.resize(int(logWindow.frameGeometry().width() * 1.2), int(logWindow.frameGeometry().height() * 1.2))
        logWindow.show()
    
    def RepairButton():
        index = questionList.currentIndex().row()
        lists = questionMap[index]
        print(f"{programPath}/CheckDLL/bash/{lists[1].lower()}.sh")
        if lists[0] == 1 and os.path.exists(f"{programPath}/CheckDLL/bash/{lists[1].lower()}.sh"):
            OpenTerminal(f"'{programPath}/AutoShell/main.py' '{programPath}/CheckDLL/bash/{lists[1].lower()}.sh'")
            return
        if lists[0] == 2:
            QtWidgets.QMessageBox.information(logWindow, "修复方法", "切换其它 Wine")
            return    
        if lists[0] == 4:
            QtWidgets.QMessageBox.information(logWindow, "修复方法", "如是 Deepin Wine 可以尝试切换 WineHQ，\n并且取消勾选运行器主页面菜单栏“程序”=>“设置Wine”，取消勾选“屏蔽 Wine 默认 Mono 和 Gecko 安装器”\n然后尝试在菜单栏的“Wine”=>“在指定 Wine、容器安装组件”=>“在指定 Wine、容器安装 Gecko”来安装 Gecko")
            return
        if lists[0] == 5:
            InstallMonoGecko("mono")
            return
        QtWidgets.QMessageBox.critical(logWindow, "错误", "无法修复该问题")

    def Show(lists):
        global questionMap
        nmodel = QtGui.QStandardItemModel(window)
        disbledButton = False
        print(lists)
        if not len(lists):
            nmodel.appendRow(QtGui.QStandardItem(f"√ 无法分析到错误"))
            disbledButton = True
        for i in lists:
            if i[0] == 0:
                nmodel.appendRow(QtGui.QStandardItem(f"√ 无法分析到错误"))
                disbledButton = True
                break
            if i[0] == 1:
                nmodel.appendRow(QtGui.QStandardItem(f"× 无法调用 Dll：{i[1]}"))
            if i[0] == 2:
                nmodel.appendRow(QtGui.QStandardItem(f"× 尝试用 Mono 运行非 .net 应用 {i[1]}？"))
            if i[0] == 3:
                nmodel.appendRow(QtGui.QStandardItem(f"！ 无法加载 Gecko，是被禁用或未安装？"))
            if i[0] == 4:
                nmodel.appendRow(QtGui.QStandardItem(f"× 无法更新 Wine 容器版本，是否还有 Wine 程序运行？"))
            if i[0] == 5:
                nmodel.appendRow(QtGui.QStandardItem(f"× Mono 禁用/未安装"))
        questionMap = lists[:]
        repairButton.setDisabled(disbledButton)
        questionList.setModel(nmodel)

class LogThreading(QtCore.QThread):
    done = QtCore.pyqtSignal(list)
    def __init__(self):
        super().__init__()

    def run(self):
        global logText
        repairList = []
        logText = returnText.toPlainText()
        print(logText.splitlines())
        for i in logText.splitlines():
            print(i)
            checkingText = i.lower()
            if "err:module:import_dll Library".lower() in checkingText:
                # Lose Dll
                repairList.append([1, i[i.index("Library") + 8: i.index("(")].strip()])
                continue
            if "err:module:fixup_imports_ilonly".lower() in checkingText:
                # Lose Dll
                repairList.append([1, i[i.index("_ilonly") + 8: i.index("not")].strip()])
                continue
            if "Cannot open assembly".lower() in checkingText and ": File does not contain a valid CIL image.".lower() in checkingText:
                # Mono
                repairList.append([2, i.replace(": File does not contain a valid CIL image.", "").replace("Cannot open assembly", "").strip()[1: -1]])
            if "Could not load wine-gecko. HTML rendering will be disabled.".lower() in checkingText and "Could not find Wine Gecko. HTML rendering will be disabled.".lower() in checkingText:
                # Disbled Gecko
                repairList.append([3, ""])
            if "Your wineserver binary was not upgraded correctly".lower() in checkingText:
                repairList.append([4, ""])
            if "Wine Mono is not installed".lower() in checkingText:
                repairList.append([5, ""])
        self.done.emit(repairList)
    

def DisableButton(things):
    button_r_6.setDisabled(things)
    button1.setDisabled(things)
    button2.setDisabled(things)
    button3.setDisabled(things)
    wineConfig.setDisabled(things)
    e1.setDisabled(things)
    e2.setDisabled(things)
    o1.setDisabled(things)
    #winetricksOpen.configure(state=a[things])
    getProgramIcon.setDisabled(things)
    uninstallProgram.setDisabled(things)
    trasButton.setDisabled(things)

def CheckProgramIsInstall(program):
    return not bool(os.system(f"which '{program}'"))
class Runexebutton_threading(QtCore.QThread):
    signal = QtCore.pyqtSignal(str)
    showHistory = QtCore.pyqtSignal(str)
    def __init__(self):
        super().__init__()

    def run(self):
        global lastRunCommand
        if e1.currentText() == "":
            wineBottonPath = setting["DefultBotton"]
        else:
            wineBottonPath = e1.currentText()
        option = ""
        if setting["Architecture"] != "Auto":
            option += f"WINEARCH={setting['Architecture']} "
        if setting["MonoGeckoInstaller"]:
            option += f"WINEDLLOVERRIDES=\"mscoree,mshtml=\" "
        if not setting["Debug"]:
            option += "WINEDEBUG=-all "
        else:
            option += "WINEDEBUG=FIXME,ERR,WARN,TRACE,Message "
        wineUsingOption = ""
        exePath = e2.currentText()
        # 禁用没什么用还一堆坑的参数识别问题
        if False:
            fileName = [".exe"]
            changePath = False
            for i in fileName:
                if i in exePath:
                    print(i)
                    print(exePath)
                    l = exePath.index(i)
                    exePath = f"{exePath[:l+4]}' {exePath[l+4:]} '"
                    print(l)
                    print(exePath)
                    changePath = True
                    break
            #if not changePath and not os.path.exists(changePath):
            if not changePath and not os.path.exists(exePath):
                # 删除前后无用空格以防止出现问题
                print(exePath)
                exePath = exePath.strip()
                # 有空格再说
                if " " in exePath:
                    l = exePath.index(" ")
                    exePath = f"{exePath[:l]}' {exePath[l:]} '"
                    print(l)
                    #print(i)
                print(exePath)
        if o1.currentText() == "基于 UOS exagear 的 deepin-wine6-stable" or o1.currentText() == "基于 UOS box86 的 deepin-wine6-stable":
            wineUsingOption = ""
        if o1.currentText() == "基于 UOS box86 的 deepin-wine6-stable" or o1.currentText() == "基于 UOS exagear 的 deepin-wine6-stable":
            if not os.path.exists(f"{programPath}/dlls-arm"):
                if os.system(f"7z x -y \"{programPath}/dlls-arm.7z\" -o\"{programPath}\""):
                    QtWidgets.QMessageBox.critical(widget, "错误", "无法解压资源")
                    return
                os.remove(f"{programPath}/dlls-arm.7z")
        if setting["TerminalOpen"]:
            res = ""
            if e2.currentText()[-4:] == ".msi" and os.path.exists(e2.currentText()):
                runCommand = "env WINEPREFIX='" + wineBottonPath + "' " + option + wine[o1.currentText()] + " msiexec /i '" + e2.currentText() + "' " + setting["WineOption"]
                OpenTerminal(runCommand)
            elif e2.currentText()[-4:] == ".bat" and os.path.exists(e2.currentText()):
                runCommand = "env WINEPREFIX='" + wineBottonPath + "' " + option + wine[o1.currentText()] + " wineconsole '" + e2.currentText() + "' " + setting["WineOption"]
                OpenTerminal(runCommand)
            else:
                runCommand = "env WINEPREFIX='" + wineBottonPath + "' " + option + wine[o1.currentText()] + " '" + exePath + "' " + setting["WineOption"]
                OpenTerminal(runCommand)
            #res = subprocess.Popen([f"'{programPath}/launch.sh' deepin-terminal -C \"WINEPREFIX='" + wineBottonPath + "' " + option + wine[o1.currentText()] + " '" + e2.currentText() + "' " + setting["WineOption"] + "\" --keep-open" + wineUsingOption], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        else:
            if e2.currentText()[-4:] == ".msi" and os.path.exists(e2.currentText()):
                runCommand = "WINEPREFIX='" + wineBottonPath + "' " + option + wine[o1.currentText()] + " msiexec /i '" + e2.currentText() + "' " + setting["WineOption"]
                res = subprocess.Popen([runCommand], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            elif e2.currentText()[-4:] == ".bat" and os.path.exists(e2.currentText()):
                runCommand = "WINEPREFIX='" + wineBottonPath + "' " + option + wine[o1.currentText()] + " wineconsole '" + e2.currentText() + "' " + setting["WineOption"]
                res = subprocess.Popen([runCommand], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            else:
                runCommand = "WINEPREFIX='" + wineBottonPath + "' " + option + wine[o1.currentText()] + " '" + exePath + "' " + setting["WineOption"]
                print(["WINEPREFIX='" + wineBottonPath + "' " + option + wine[o1.currentText()] + " '" + exePath + "' " + setting["WineOption"]])
                res = subprocess.Popen([runCommand], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # 实时读取程序返回
        #
        print(runCommand)
        lastRunCommand = runCommand
        if not setting["TerminalOpen"]:
            while res.poll() is None:
                try:
                    text = res.stdout.readline().decode("utf8")
                except:
                    text = ""
                self.signal.emit(text)
                print(text, end="")
        
        
        if len(findExeHistory) == 0 or findExeHistory[-1] != wineBottonPath:
            findExeHistory.append(wineBottonPath)  # 将记录写进数组
            write_txt(get_home() + "/.config/deepin-wine-runner/FindExeHistory.json", str(json.dumps(ListToDictionary(findExeHistory))))  # 将历史记录的数组转换为字典并写入
        if len(wineBottonHistory) == 0 or wineBottonHistory[-1] != e2.currentText():
            wineBottonHistory.append(e2.currentText())  # 将记录写进数组        
            write_txt(get_home() + "/.config/deepin-wine-runner/WineBottonHistory.json", str(json.dumps(ListToDictionary(wineBottonHistory))))  # 将历史记录的数组转换为字典并写入
        self.showHistory.emit("")
        # 针对 QQ、TIM 安装后不会生成 lnk 的问题，由程序读取以及自动创建
        # 判断是否安装了 QQ/TIM
        for i in iconListUnBuild:
            if os.path.exists(i[1].replace("wineBottonPath", wineBottonPath)):
                if not os.path.exists(f"{get_home()}/.local/share/applications/wine/{i[0]}-{os.path.basename(wineBottonPath)}.desktop"):
                    print("图标不存在，创建图标")
                    # 图标不存在
                    # 写入 .desktop 文件
                    try:
                        os.system(f"mkdir -p '{get_home()}/.local/share/applications/wine'")
                        name = i[0]
                        if setting["BuildByBottleName"]:
                            name = f"{i[0]}——{os.path.basename(wineBottonPath)}"
                        write_txt(f"{get_home()}/.local/share/applications/wine/{i[0]}-{os.path.basename(wineBottonPath)}.desktop", f'''[Desktop Entry]
Name={name}
Exec=env WINEPREFIX='{wineBottonPath}' {option} {wine[o1.currentText()]} '{i[1].replace("wineBottonPath", wineBottonPath)}' {setting["WineOption"]} {wineUsingOption}
Icon={programPath}/Icon/{i[0]}.svg
Type=Application
StartupNotify=true''')
                    except:
                        # 写入不进去就别写入了，当什么事情都没发生就行
                        traceback.print_exc()
        DisableButton(False)

class Temp:
    webWindow = None


        
    #QtCore.QUrl().url()

# 显示“关于这个程序”窗口
def about_this_program()->"显示“关于这个程序”窗口":
    global about
    global title
    global iconPath
    global clickIconTime
    clickIconTime = 0
    QT.message = QtWidgets.QMainWindow()  
    QT.message.setWindowIcon(QtGui.QIcon(iconPath))
    messageWidget = QtWidgets.QWidget()
    messageWidget.setObjectName("messageWidget")
    messageWidget.setStyleSheet(f"QWidget#messageWidget {{background: url({programPath}/Icon/Program/about-background.png) no-repeat;background-position: left bottom;}}")
    QT.message.setWindowTitle(f"关于 {title}")
    messageLayout = QtWidgets.QGridLayout()
    iconShow = QtWidgets.QLabel(f"<a href='https://www.gfdgdxi.top'><img width=256 src='{iconPath}'></a>")
    def ChangeIcon():
        global clickIconTime
        if clickIconTime >= 0:
            clickIconTime = clickIconTime + 1
        if clickIconTime > 0:
            clickIconTime = -1
            for k in ["", "Function", "Program"]:
                try:
                    for i in os.listdir(f"{programPath}/Icon/{k}"):
                        if i[-4:] == ".svg" or i[-4:] == ".png":
                            iconPathList.append(f"{programPath}/Icon/{k}/{i}")
                except:
                    traceback.print_exec()
        randomNumber = random.randint(0, len(iconPathList) - 1)
        iconShow.setText(f"<a href='https://www.gfdgdxi.top'><img width=256 src='{iconPathList[randomNumber]}'></a><p align='center'>{randomNumber + 1}/{len(iconPathList)}</p>")
    iconShow.linkActivated.connect(ChangeIcon)
    messageLayout.addWidget(iconShow, 0, 0, 1, 1, QtCore.Qt.AlignTop)
    aboutInfo = QtWidgets.QTextBrowser(messageWidget)
    aboutInfo.setFocusPolicy(QtCore.Qt.NoFocus)
    #aboutInfo.copyAvailable.connect(lambda: print("b"))
    aboutInfo.anchorClicked.connect(OpenUrl)
    aboutInfo.setOpenLinks(False)
    aboutInfo.setHtml(about)
    aboutInfo.setOpenExternalLinks(False)
    messageLayout.addWidget(aboutInfo, 0, 1, 1, 1)
    ok = QtWidgets.QPushButton(QtCore.QCoreApplication.translate("U", "确定"))
    ok.clicked.connect(QT.message.close)
    messageLayout.addWidget(ok, 1, 1, 1, 1, QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)
    messageWidget.setLayout(messageLayout)
    
    QT.message.setCentralWidget(messageWidget)
    QT.message.resize(int(messageWidget.frameGeometry().width() * 1.5), int(messageWidget.frameGeometry().height() * 1.5))
    QT.message.show()

# 显示“提示”窗口
def helps():
    global tips
    QtWidgets.QMessageBox.information(widget, "提示", tips)

# 显示更新内容窗口
def UpdateThings():
    QtWidgets.QMessageBox.information(widget, "更新内容", updateThings)

# 生成 desktop 文件在启动器
def make_desktop_on_launcher():
    try:
        if combobox1.currentText() == "" or e2.currentText() == "":  # 判断文本框是否有内容
            QtWidgets.QMessageBox.information(widget, "提示", "没有填写需要使用 exe 应用或保存的文件名")
            return
        if not CheckProgramIsInstall(wine[o1.currentText()]) and not o1.currentText() in untipsWine:
            if QtWidgets.QMessageBox.question(widget, "提示", "检查到您未安装这个 wine，是否继续使用这个 wine 写入？") == QtWidgets.QMessageBox.No:
                DisableButton(False)
                return
        else:  # 如果都有
            if os.path.exists(get_home() + "/.local/share/applications/" + combobox1.currentText() + ".desktop"): # 判断目录是否有该文件，如果有
                choose = QtWidgets.QMessageBox.question(widget, "提示", "文件已经存在，是否覆盖？") == QtWidgets.QMessageBox.Yes
                if choose:   # 如要覆盖
                    os.remove(get_home() + "/.local/share/applications/" + combobox1.currentText() + ".desktop")  # 删除该文件
                else:  # 如不覆盖
                    return  # 结束
            if e1.currentText() == "":
                wineBottonPath = setting["DefultBotton"]
            else:
                wineBottonPath = e1.currentText()
            option = ""
            if setting["Architecture"] != "Auto":
                option += f"WINEARCH={setting['Architecture']} "
            if not setting["Debug"]:
                option += "WINEDEBUG=-all "
            else:
                option += "WINEDEBUG=FIXME,ERR,WARN,TRACE,Message "
            wineUsingOption = ""
            if o1.currentText() == "基于 UOS box86 的 deepin-wine6-stable" or o1.currentText() == "基于 UOS exagear 的 deepin-wine6-stable":
                if not os.path.exists(f"{programPath}/dlls-arm"):
                    if os.system(f"7z x -y \"{programPath}/dlls-arm.7z\" -o\"{programPath}\""):
                        QtWidgets.QMessageBox.critical(widget, "错误", "无法解压资源")
                        return
                    os.remove(f"{programPath}/dlls-arm.7z")
            if o1.currentText() == "基于 UOS exagear 的 deepin-wine6-stable" or o1.currentText() == "基于 UOS box86 的 deepin-wine6-stable":
                wineUsingOption = ""
            value = ""
            if e2.currentText()[:2].upper() == "C:":
                value = f"{wineBottonPath}/drive_c/{e2.currentText()[2:]}".replace("\\", "/").replace("//", "/")
            print(value)
            iconPaths = iconPath
            for i in iconList:
                listValue = i[1].replace("wineBottonPath", wineBottonPath)
                if listValue == e2.currentText() or listValue == value:
                    # 如果路径相同，即可以用程序对应的图标
                    iconPaths = f"{programPath}/Icon/{i[0]}.svg"
                    # 读到了就不需要再读取了
                    break
            os.system(f"mkdir -p '{get_home()}/.local/share/applications/wine'")
            write_txt(get_home() + "/.local/share/applications/wine/" + combobox1.currentText() + ".desktop", f'''[Desktop Entry]
Name={combobox1.currentText()}
Exec=env WINEPREFIX='{wineBottonPath}' {option} {wine[o1.currentText()]} '{e2.currentText()}' {setting["WineOption"]} {wineUsingOption}
Icon={iconPaths}
Type=Application
StartupNotify=true''') # 写入文本文档
            if len(shellHistory) == 0 or shellHistory[-1] != combobox1.currentText():
                shellHistory.append(combobox1.currentText())  # 将记录写进数组
                write_txt(get_home() + "/.config/deepin-wine-runner/ShellHistory.json", str(json.dumps(ListToDictionary(shellHistory))))  # 将历史记录的数组转换为字典并写入
                combobox1.clear()
                combobox1.addItems(shellHistory)
            QtWidgets.QMessageBox.information(widget, "提示", "生成完成！")  # 显示完成对话框
    except:
        traceback.print_exc()
        QtWidgets.QMessageBox.critical(widget, "错误", f"快捷方式创建失败，错误如下：\n{traceback.format_exc()}")

def ConfigQemu():
    lists = []
    for i in qemuBottleList:
        lists.append(f"{i[0]}/{i[1]}")
    choose = QtWidgets.QInputDialog.getItem(window, "提示", "选择需要 Chroot 到里面的容器", lists, 0, False)
    if not choose[1]:
        return
    threading.Thread(target=OpenTerminal, args=[f"python3 '{programPath}/QemuRun.py' '{choose[0]}' '{int(setting['QemuUnMountHome'])}' "]).start()
    print(choose)

# 生成 desktop 文件在桌面
# （第四个按钮的事件）
def make_desktop_on_desktop():
    try:
        if combobox1.currentText() == "" or e2.currentText() == "":  # 判断文本框是否有内容
            QtWidgets.QMessageBox.information(widget, "提示", "没有填写需要使用 exe 应用或保存的文件名")
            return
        if not CheckProgramIsInstall(wine[o1.currentText()]) and not o1.currentText() in untipsWine:
            if QtWidgets.QMessageBox.question(widget, "提示", "检查到您未安装这个 wine，是否继续使用这个 wine 写入？") == QtWidgets.QMessageBox.No:
                DisableButton(False)
                return
        else:  # 如果都有
            if os.path.exists(get_desktop_path() + "/" + combobox1.currentText() + ".desktop"): # 判断目录是否有该文件，如果有
                choose = QtWidgets.QMessageBox.question(widget, "提示", "文件已经存在，是否覆盖？") == QtWidgets.QMessageBox.Yes
                if choose:   # 如要覆盖
                    os.remove(get_desktop_path() + "/" + combobox1.currentText() + ".desktop")  # 删除该文件
                else:  # 如不覆盖
                    return  # 结束
            if e1.currentText() == "":
                wineBottonPath = setting["DefultBotton"]
            else:
                wineBottonPath = e1.currentText()
            wineUsingOption = ""
            if o1.currentText() == "基于 UOS exagear 的 deepin-wine6-stable" or o1.currentText() == "基于 UOS box86 的 deepin-wine6-stable":
                wineUsingOption = ""
            if o1.currentText() == "基于 UOS box86 的 deepin-wine6-stable" or o1.currentText() == "基于 UOS exagear 的 deepin-wine6-stable":
                if not os.path.exists(f"{programPath}/dlls-arm"):
                    if os.system(f"7z x -y \"{programPath}/dlls-arm.7z\" -o\"{programPath}\""):
                        QtWidgets.QMessageBox.critical(widget, "错误", "无法解压资源")
                        return
                    os.remove(f"{programPath}/dlls-arm.7z")
            if not os.path.exists(get_desktop_path()):
                os.makedirs(get_home())
            os.mknod(get_desktop_path() + "/" + combobox1.currentText() + ".desktop")
            option = ""
            if setting["Architecture"] != "Auto":
                option += f"WINEARCH={setting['Architecture']} "
            if not setting["Debug"]:
                option += "WINEDEBUG=-all "
            value = ""
            if e2.currentText()[:2].upper() == "C:":
                value = f"{wineBottonPath}/drive_c/{e2.currentText()[2:]}".replace("\\", "/").replace("//", "/")
            print(value)
            iconPaths = iconPath
            for i in iconList:
                listValue = i[1].replace("wineBottonPath", wineBottonPath)
                if listValue == e2.currentText() or listValue == value:
                    # 如果路径相同，即可以用程序对应的图标
                    iconPaths = f"{programPath}/Icon/{i[0]}.svg"
                    # 读到了就不需要再读取了
                    break
            os.system(f"mkdir -p '{get_home()}/.local/share/applications/wine'")
            write_txt(get_desktop_path() + "/" + combobox1.currentText() + ".desktop", f'''[Desktop Entry]
Name={combobox1.currentText()}
Exec=env WINEPREFIX='{wineBottonPath}' {option} {wine[o1.currentText()]} '{e2.currentText()}' {setting["WineOption"]} {wineUsingOption}
Icon={iconPaths}
Type=Application
StartupNotify=true''') # 写入文本文档
            if len(shellHistory) == 0 or shellHistory[-1] != combobox1.currentText():
                shellHistory.append(combobox1.currentText())  # 将记录写进数组
                write_txt(get_home() + "/.config/deepin-wine-runner/ShellHistory.json", str(json.dumps(ListToDictionary(shellHistory))))  # 将历史记录的数组转换为字典并写入
                combobox1.clear()
                combobox1.addItems(shellHistory)
            QtWidgets.QMessageBox.information(widget, "提示", "生成完成！")  # 显示完成对话框
    except:
        traceback.print_exc()
        QtWidgets.QMessageBox.critical(widget, "错误", f"快捷方式创建失败，错误如下：\n{traceback.format_exc()}")

# 数组转字典
def ListToDictionary(list):
    dictionary = {}
    for i in range(len(list)):
        dictionary[i] = list[i]
    return dictionary

def CleanProgramHistory():
    if QtWidgets.QMessageBox.question(widget, "警告", "删除后将无法恢复，你确定吗？\n删除后软件将会自动重启。") == QtWidgets.QMessageBox.Yes:
        try:
            shutil.rmtree(get_home() + "/.config/deepin-wine-runner")
        except:
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(widget, "错误", traceback.format_exc())
        ReStartProgram()

def CleanProgramCache():
    try:
        shutil.rmtree(get_home() + "/.cache/deepin-wine-runner")
        QtWidgets.QMessageBox.information(widget, "提示", "缓存清理完毕！")
    except:
        traceback.print_exc()
        QtWidgets.QMessageBox.critical(widget, "错误", traceback.format_exc())

def SetFont(size):
    font = QtGui.QFont(defaultFont)
    if size == 1:
        app.setFont(defaultFont)    
        return
    font.setPixelSize(int(defaultFont.pixelSize() / size))
    font.setPointSize(int(defaultFont.pointSize() / size))
    app.setFont(font)

# 重启本应用程序
def ReStartProgram():
    python = sys.executable
    os.execl(python, python, * sys.argv)

def KillAllProgram():
    pass

def KillProgram():
    os.system(f"killall {wine[o1.currentText()]} -9")
    os.system("killall winedbg -9")
    exeName = os.path.basename(e2.currentText())
    os.system(f"killall {exeName} -9")

def InstallWine():
    threading.Thread(target=OpenTerminal, args=[f"'{programPath}/AllInstall.py'"]).start()

def InstallWineOnDeepin23():
    threading.Thread(target=OpenTerminal, args=[f"'{programPath}/InstallWineOnDeepin23.py'"]).start()

class DllWindow():
    def ShowWindow():
        global dllMessage
        global dllInfoMap
        global textInfo
        global dllName
        dllMessage = QtWidgets.QWidget()
        dllLayout = QtWidgets.QGridLayout()
        try:
            dllInfoMap["check"]
        except:
            try:
                with open(f"{programPath}/CheckDLL/lists.json", "r") as file:
                    dllInfoMap = json.loads(file.read())
            except:
                traceback.print_exc()
                QtWidgets.QMessageBox.critical(dllMessage, "错误", traceback.format_exc())
        # UI
        dllName = QtWidgets.QLineEdit()
        dllButton = QtWidgets.QPushButton("查询")
        textInfo = QtWidgets.QTextBrowser()
        dllButton.clicked.connect(DllWindow.Find)
        dllLayout.addWidget(QtWidgets.QLabel("Dll 名称："), 0, 0)
        dllLayout.addWidget(dllName, 0, 1)
        dllLayout.addWidget(dllButton, 0, 2)
        dllLayout.addWidget(textInfo, 1, 0, 1, 3)
        dllMessage.setWindowTitle(f"{title}——查询 Dll")
        dllMessage.setLayout(dllLayout)
        dllMessage.resize(int(dllMessage.frameGeometry().width() * 1.2), int(dllMessage.frameGeometry().height() * 1.1))
        dllMessage.setWindowIcon(QtGui.QIcon(f"{programPath}/deepin-wine-runner.svg"))
        dllMessage.show()

    def Find():
        dllNameText = dllName.text().strip().lower()
        if dllNameText[-4:] != ".dll":
            dllNameText += ".dll"
        try:
            textInfo.setText(dllInfoMap[dllNameText])
        except:
            textInfo.setText(f"未查询到有关 Dll '{dllNameText}' 有关的内容")

def InstallWineOnDeepin23Alpha():
    threading.Thread(target=OpenTerminal, args=[f"'{programPath}/InstallWineOnDeepin23Alpha.py'"]).start()

def InstallWineHQ():
    threading.Thread(target=OpenTerminal, args=[f"{programPath}/InstallNewWineHQ.sh"]).start()

def OpenWineBotton():
    if e1.currentText() == "":
        wineBottonPath = setting["DefultBotton"]
    else:
        wineBottonPath = e1.currentText()
    os.system("xdg-open \"" + wineBottonPath.replace("\'", "\\\'") + "\"")

def OpenWineFontPath():
    if e1.currentText() == "":
        wineBottonPath = setting["DefultBotton"]
    else:
        wineBottonPath = e1.currentText()
    QtWidgets.QMessageBox.information(widget, "提示", QtCore.QCoreApplication.translate("U", "如果安装字体？只需要把字体文件复制到此字体目录\n按下“OK”按钮可以打开字体目录"))
    os.system("xdg-open \"" + wineBottonPath.replace("\'", "\\\'") + "/drive_c/windows/Fonts\"")

def GetLoseDll():
    if e1.currentText() == "":
        wineBottonPath = setting["DefultBotton"]
    else:
        wineBottonPath = e1.currentText()
    option = ""
    if setting["MonoGeckoInstaller"]:
        option += f"WINEDLLOVERRIDES=\"mscoree,mshtml=\" "
    if setting["Architecture"] != "Auto":
        option += f"WINEARCH={setting['Architecture']} "
    if not setting["Debug"]:
        option += "WINEDEBUG=-all "
    wineUsingOption = ""
    if o1.currentText() == "基于 UOS exagear 的 deepin-wine6-stable":
        os.system(f"'{programPath}/deepin-wine-runner-create-botton.py' '{wineBottonPath}'")
    if o1.currentText() == "基于 UOS exagear 的 deepin-wine6-stable" or o1.currentText() == "基于 UOS box86 的 deepin-wine6-stable":
        wineUsingOption = ""
    if o1.currentText() == "基于 UOS box86 的 deepin-wine6-stable" or o1.currentText() == "基于 UOS exagear 的 deepin-wine6-stable":
        if not os.path.exists(f"{programPath}/dlls-arm"):
            if os.system(f"7z x -y \"{programPath}/dlls-arm.7z\" -o\"{programPath}\""):
                QtWidgets.QMessageBox.critical(widget, "错误", "无法解压资源")
                return
            os.remove(f"{programPath}/dlls-arm.7z")
    threading.Thread(target=os.system, args=[f"python3 '{programPath}/CheckDLL/main.py' '{e2.currentText()}' '{wineBottonPath}' '{wine[o1.currentText()]}'" + setting["WineOption"]]).start()

class RunWineProgramThread(QtCore.QThread):
    signal = QtCore.pyqtSignal(str)
    showHistory = QtCore.pyqtSignal(str)
    def __init__(self, wineProgram, history = False, Disbled = True):
        super().__init__()
        self.wineProgram = wineProgram
        self.history = history
        self.Disbled = Disbled

    def run(self):
        global lastRunCommand
        if e1.currentText() == "":
            wineBottonPath = setting["DefultBotton"]
        else:
            wineBottonPath = e1.currentText()
        option = ""
        if setting["MonoGeckoInstaller"]:
            option += f"WINEDLLOVERRIDES=\"mscoree,mshtml=\" "
        if setting["Architecture"] != "Auto":
            option += f"WINEARCH={setting['Architecture']} "
        if not setting["Debug"]:
            option += "WINEDEBUG=-all "
        wineUsingOption = ""
        if o1.currentText() == "基于 UOS exagear 的 deepin-wine6-stable":
            os.system(f"'{programPath}/deepin-wine-runner-create-botton.py' '{wineBottonPath}'")
        if o1.currentText() == "基于 UOS exagear 的 deepin-wine6-stable" or o1.currentText() == "基于 UOS box86 的 deepin-wine6-stable":
            wineUsingOption = ""
        if o1.currentText() == "基于 UOS box86 的 deepin-wine6-stable" or o1.currentText() == "基于 UOS exagear 的 deepin-wine6-stable":
            if not os.path.exists(f"{programPath}/dlls-arm"):
                if os.system(f"7z x -y \"{programPath}/dlls-arm.7z\" -o\"{programPath}\""):
                    QtWidgets.QMessageBox.critical(widget, "错误", "无法解压资源")
                    return
                os.remove(f"{programPath}/dlls-arm.7z")
        if setting["TerminalOpen"]:
            res = ""
            runCommand = f"env WINEPREFIX='" + wineBottonPath + "' " + option + wine[o1.currentText()] + " '" + self.wineProgram + "' " + setting["WineOption"] + " " + wineUsingOption
            OpenTerminal(runCommand)
            #res = subprocess.Popen([f"'{programPath}/launch.sh' deepin-terminal -C \"WINEPREFIX='" + wineBottonPath + "' " + option + wine[o1.currentText()] + " '" + self.wineProgram + "' " + setting["WineOption"] + " " + wineUsingOption + "\" --keep-open"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        else:
            runCommand = "WINEPREFIX='" + wineBottonPath + "' " + option + wine[o1.currentText()] + " '" + self.wineProgram + "' " + setting["WineOption"]
            res = subprocess.Popen([runCommand], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print(runCommand)
        lastRunCommand = runCommand
        # 实时读取程序返回
        if not setting["TerminalOpen"]:
            while res.poll() is None:
                try:
                    text = res.stdout.readline().decode("utf8")
                except:
                    text = ""
                self.signal.emit(text)
                print(text, end="")
        if self.history:
            if len(findExeHistory) == 0 or findExeHistory[-1] != wineBottonPath:
                findExeHistory.append(wineBottonPath)  # 将记录写进数组
                write_txt(get_home() + "/.config/deepin-wine-runner/FindExeHistory.json", str(json.dumps(ListToDictionary(findExeHistory))))  # 将历史记录的数组转换为字典并写入
            if len(wineBottonHistory) == 0 or wineBottonHistory[-1] != e2.currentText():
                wineBottonHistory.append(e2.currentText())  # 将记录写进数组
                write_txt(get_home() + "/.config/deepin-wine-runner/WineBottonHistory.json", str(json.dumps(ListToDictionary(wineBottonHistory))))  # 将历史记录的数组转换为字典并写入
            self.showHistory.emit("")
        if self.Disbled:
            DisableButton(False)

    
runProgram = None
def RunWineProgram(wineProgram, history = False, Disbled = True):
    global runProgram
    DisableButton(True)
    if not CheckProgramIsInstall(wine[o1.currentText()]) and o1.currentText() != "基于 linglong 的 deepin-wine6-stable（不推荐）" and o1.currentText() != "基于 UOS exagear 的 deepin-wine6-stable" and o1.currentText() != "基于 UOS box86 的 deepin-wine6-stable":
        if not CheckProgramIsInstall(wine[o1.currentText()]) and not o1.currentText() in untipsWine:
            if QtWidgets.QMessageBox.question(widget, "提示", "检查到您未安装这个 wine，是否继续使用这个 wine 运行？") == QtWidgets.QMessageBox.No:
                DisableButton(False)
                return
    returnText.setText("")
    runProgram = RunWineProgramThread(wineProgram, history, Disbled)
    runProgram.signal.connect(QT.ShowWineReturn)
    runProgram.showHistory.connect(QT.ShowHistory)
    runProgram.start()

class RunWinetricksThread(QtCore.QThread):
    signal = QtCore.pyqtSignal(str)
    bwrap = QtCore.pyqtSignal(str)
    def __init__(self, bwrap):
        self.bwrap = bwrap
        super().__init__()

    def run(self):
        wineBottonPath = setting["DefultBotton"]
        if not e1.currentText() == "":
            wineBottonPath = e1.currentText()
        option = ""
        if setting["Architecture"] != "Auto":
            option += f"WINEARCH={setting['Architecture']} "
        if not setting["Debug"]:
            option += "WINEDEBUG=-all "
        wineUsingOption = ""
        if o1.currentText() == "基于 UOS exagear 的 deepin-wine6-stable" or o1.currentText() == "基于 UOS box86 的 deepin-wine6-stable":
            wineUsingOption = ""
        if o1.currentText() == "基于 UOS box86 的 deepin-wine6-stable" or o1.currentText() == "基于 UOS exagear 的 deepin-wine6-stable":
            if not os.path.exists(f"{programPath}/dlls-arm"):
                if os.system(f"7z x -y \"{programPath}/dlls-arm.7z\" -o\"{programPath}\""):
                    QtWidgets.QMessageBox.critical(widget, "错误", "无法解压资源")
                    return
                os.remove(f"{programPath}/dlls-arm.7z")
        ## 获取 WineServer 路径
        wineServer = None
        winePath = wine[o1.currentText()]
        winePath = winePath.replace(f"bash '{programPath}/WineLib/run.sh'", "").strip()
        # 判断类似 xxx-server 的 WineServer
        if not os.system(f"{winePath}-server") >> 8:
            wineServer = f"{winePath}-server"
        # 判断类似 deepin-wine6-stable 的 WineServer
        elif os.path.exists(f"/opt/{winePath}/bin/wineserver"):
            wineServer = f"/opt/{winePath}/bin/wineserver"
        elif os.path.exists(winePath):
            wineServer = os.path.normpath(f"{winePath}/../wineserver")
        runtime = ""
        if self.bwrap:
            runtime = f"'{programPath}/WineLib/run.sh'"
        winetricksPath = "winetricks"
        if os.system("which winetricks") >> 8:
            winetricksPath = f"'{programPath}/winetricks'"
        print(wineServer)
        wineProgramP = wine[o1.currentText()].replace(f"bash '{programPath}/WineLib/run.sh'", "").strip()
        wineProgramP = subprocess.getoutput(f"which {wineProgramP}").strip()
        if setting["TerminalOpen"]:
            res = ""
            # 用终端开应该不用返回输出内容了
            if wineServer == None:
                OpenTerminal(f"WINEPREFIX='{wineBottonPath}' {option} WINE='{wineProgramP}' {runtime} {winetricksPath} --gui {wineUsingOption}")
            else:
                OpenTerminal(f"WINEPREFIX='{wineBottonPath}' {option} WINESERVER='{wineServer}' WINE='{wineProgramP}' {runtime} {winetricksPath} --gui {wineUsingOption}")
            #res = subprocess.Popen([f"'{programPath}/launch.sh' deepin-terminal -C \"WINEPREFIX='{wineBottonPath}' {option} WINE=" + subprocess.getoutput(f"which {wine[o1.currentText()]}").replace(" ", "").replace("\n", "") + f" winetricks --gui {wineUsingOption}\" --keep-open"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        else:    
            if wineServer == None:
                res = subprocess.Popen([f"WINEPREFIX='{wineBottonPath}' {option} WINE='{wineProgramP}' {runtime} {winetricksPath} --gui"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            else:
                res = subprocess.Popen([f"WINEPREFIX='{wineBottonPath}' {option} WINESERVER='{wineServer}' WINE='{wineProgramP}' {runtime} {winetricksPath} --gui"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # 实时读取程序返回
        while res.poll() is None:
            try:
                text = res.stdout.readline().decode("utf8")
            except:
                text = ""
            self.signal.emit(text)
            print(text, end="")
        
        
        DisableButton(False)

runWinetricks = None
def RunWinetricksWithWineLib():
    global runWinetricks
    DisableButton(True)
    if not CheckProgramIsInstall(wine[o1.currentText()]) and o1.currentText() != "基于 linglong 的 deepin-wine6-stable（不推荐）" and o1.currentText() != "基于 UOS exagear 的 deepin-wine6-stable" and o1.currentText() != "基于 UOS box86 的 deepin-wine6-stable":
        if not CheckProgramIsInstall(wine[o1.currentText()]) and not o1.currentText() in untipsWine:
            DisableButton(False)
            return
    if o1.currentText() == "基于 UOS box86 的 deepin-wine6-stable" or o1.currentText() == "基于 UOS exagear 的 deepin-wine6-stable":
        if not os.path.exists(f"{programPath}/dlls-arm"):
            if os.system(f"7z x -y \"{programPath}/dlls-arm.7z\" -o\"{programPath}\""):
                QtWidgets.QMessageBox.critical(widget, "错误", "无法解压资源")
                return
            os.remove(f"{programPath}/dlls-arm.7z")
    returnText.setText("")
    runWinetricks = RunWinetricksThread(False)
    runWinetricks.signal.connect(QT.ShowWineReturn)
    runWinetricks.start()

def RunWinetricks():
    global runWinetricks
    DisableButton(True)
    if not CheckProgramIsInstall(wine[o1.currentText()]) and o1.currentText() != "基于 linglong 的 deepin-wine6-stable（不推荐）" and o1.currentText() != "基于 UOS exagear 的 deepin-wine6-stable" and o1.currentText() != "基于 UOS box86 的 deepin-wine6-stable":
        if not CheckProgramIsInstall(wine[o1.currentText()]) and not o1.currentText() in untipsWine:
            DisableButton(False)
            return
    if o1.currentText() == "基于 UOS box86 的 deepin-wine6-stable" or o1.currentText() == "基于 UOS exagear 的 deepin-wine6-stable":
        if not os.path.exists(f"{programPath}/dlls-arm"):
            if os.system(f"7z x -y \"{programPath}/dlls-arm.7z\" -o\"{programPath}\""):
                QtWidgets.QMessageBox.critical(widget, "错误", "无法解压资源")
                return
            os.remove(f"{programPath}/dlls-arm.7z")
    returnText.setText("")
    runWinetricks = RunWinetricksThread(False)
    runWinetricks.signal.connect(QT.ShowWineReturn)
    runWinetricks.start()

def CleanWineBottonByUOS():
    if e1.currentText() == "":
        wineBottonPath = setting["DefultBotton"]
    else:
        wineBottonPath = e1.currentText()
    OpenTerminal(f"env WINE='{wine[o1.currentText()]}' '{programPath}/cleanbottle.sh' '{wineBottonPath}'")

def FontAppStore():
    if e1.currentText() == "":
        wineBottonPath = setting["DefultBotton"]
    else:
        wineBottonPath = e1.currentText()
    OpenTerminal(f"env WINE='{programPath}/launch.sh' '{programPath}/InstallFont.py' '{wineBottonPath}' {int(setting['RuntimeCache'])}")

def GetDllFromInternet():
    if e1.currentText() == "":
        wineBottonPath = setting["DefultBotton"]
    else:
        wineBottonPath = e1.currentText()
    OpenTerminal(f"env WINE='{programPath}/launch.sh' '{programPath}/InstallDll.py' '{wineBottonPath}' '{wine[o1.currentText()]}' {int(setting['RuntimeCache'])}")

def WineBottonAutoConfig():
    if e1.currentText() == "":
        wineBottonPath = setting["DefultBotton"]
    else:
        wineBottonPath = e1.currentText()
    option = ""
    if setting["Architecture"] != "Auto":
        option += f"WINEARCH={setting['Architecture']} "
    if setting["MonoGeckoInstaller"]:
        option += f"WINEDLLOVERRIDES=\"mscoree,mshtml=\" "
    if not setting["Debug"]:
        option += "WINEDEBUG=-all "
    else:
        option += "WINEDEBUG=FIXME,ERR,WARN,TRACE,Message "
    os.system(f"env WINEPREFIX='{wineBottonPath}' {option} WINE='{wine[o1.currentText()]}' '{programPath}/AutoConfig.py' '{wine[o1.currentText()]}' '{wineBottonPath}'")

def InstallMonoGecko(program):
    if e1.currentText() == "":
        wineBottonPath = setting["DefultBotton"]
    else:
        wineBottonPath = e1.currentText()
    OpenTerminal(f"'{programPath}/InstallMono.py' '{wineBottonPath}' '{wine[o1.currentText()]}' {program} {int(setting['RuntimeCache'])}")

def InstallNetFramework():
    if e1.currentText() == "":
        wineBottonPath = setting["DefultBotton"]
    else:
        wineBottonPath = e1.currentText()
    OpenTerminal(f"'{programPath}/InstallNetFramework.py' '{wineBottonPath}' '{wine[o1.currentText()]}' {int(setting['RuntimeCache'])}")

def InstallVB():
    if e1.currentText() == "":
        wineBottonPath = setting["DefultBotton"]
    else:
        wineBottonPath = e1.currentText()
    OpenTerminal(f"'{programPath}/InstallVisualBasicRuntime.py' '{wineBottonPath}' '{wine[o1.currentText()]}' {int(setting['RuntimeCache'])}")

def InstallFoxPro():
    if e1.currentText() == "":
        wineBottonPath = setting["DefultBotton"]
    else:
        wineBottonPath = e1.currentText()
    OpenTerminal(f"'{programPath}/InstallFoxpro.py' '{wineBottonPath}' '{wine[o1.currentText()]}' {int(setting['RuntimeCache'])}")

def InstallVisualStudioCPlusPlus():
    if e1.currentText() == "":
        wineBottonPath = setting["DefultBotton"]
    else:
        wineBottonPath = e1.currentText()
    OpenTerminal(f"'{programPath}/InstallVisualCPlusPlus.py' '{wineBottonPath}' '{wine[o1.currentText()]}' {int(setting['RuntimeCache'])}")

def InstallMSXML():
    if e1.currentText() == "":
        wineBottonPath = setting["DefultBotton"]
    else:
        wineBottonPath = e1.currentText()
    OpenTerminal(f"'{programPath}/InstallMsxml.py' '{wineBottonPath}' '{wine[o1.currentText()]}' {int(setting['RuntimeCache'])}")

def InstallDXVK():
    if not os.path.exists(f"{programPath}/dxvk"):
        if os.system(f"7z x -y \"{programPath}/dxvk.7z\" -o\"{programPath}\""):
            QtWidgets.QMessageBox.critical(widget, "错误", "无法解压资源")
            return
        os.remove(f"{programPath}/dxvk.7z")
    if e1.currentText() == "":
        wineBottonPath = setting["DefultBotton"]
    else:
        wineBottonPath = e1.currentText()
    OpenTerminal(f"env WINE='{wine[o1.currentText()]}' WINE64='{wine[o1.currentText()]}' WINEPREFIX='{wineBottonPath}' '{programPath}/dxvk/setup_dxvk.sh' uninstall")

def InstallVkd3d():
    if not os.path.exists(f"{programPath}/vkd3d-proton"):
        if os.system(f"7z x -y \"{programPath}/vkd3d-proton.7z\" -o\"{programPath}\""):
            QtWidgets.QMessageBox.critical(widget, "错误", "无法解压资源")
            return
        os.remove(f"{programPath}/vkd3d-proton.7z")
    if e1.currentText() == "":
        wineBottonPath = setting["DefultBotton"]
    else:
        wineBottonPath = e1.currentText()
    OpenTerminal(f"env WINE='{wine[o1.currentText()]}' WINE64='{wine[o1.currentText()]}' WINEPREFIX='{wineBottonPath}' '{programPath}/vkd3d-proton/setup_vkd3d_proton.sh' install")

def UninstallVkd3d():
    if not os.path.exists(f"{programPath}/vkd3d-proton"):
        if os.system(f"7z x -y \"{programPath}/vkd3d-proton.7z\" -o\"{programPath}\""):
            QtWidgets.QMessageBox.critical(widget, "错误", "无法解压资源")
            return
        os.remove(f"{programPath}/vkd3d-proton.7z")
    if e1.currentText() == "":
        wineBottonPath = setting["DefultBotton"]
    else:
        wineBottonPath = e1.currentText()
    OpenTerminal(f"env WINE='{wine[o1.currentText()]}' WINE64='{wine[o1.currentText()]}' WINEPREFIX='{wineBottonPath}' '{programPath}/vkd3d-proton/setup_vkd3d_proton.sh' uninstall")
    #process = QtCore.QProcess()
    #process.startDetached(f"{programPath}/launch.sh", ["deepin-terminal", "-e", 
            #"env", f"WINE={wine[o1.currentText()]}", f"WINE64={wine[o1.currentText()]}", f"WINEPREFIX={wineBottonPath}", "bash",
            #f"{programPath}/dxvk/setup_dxvk.sh", "install"])

def UninstallDXVK():
    if not os.path.exists(f"{programPath}/dxvk"):
        if os.system(f"7z x -y \"{programPath}/dxvk.7z\" -o\"{programPath}\""):
            QtWidgets.QMessageBox.critical(widget, "错误", "无法解压资源")
            return
        os.remove(f"{programPath}/dxvk.7z")
    if e1.currentText() == "":
        wineBottonPath = setting["DefultBotton"]
    else:
        wineBottonPath = e1.currentText()
    OpenTerminal(f"env WINE='{wine[o1.currentText()]}' WINE64='{wine[o1.currentText()]}' WINEPREFIX='{wineBottonPath}' '{programPath}/dxvk/setup_dxvk.sh' uninstall")
    #process = QtCore.QProcess()
    #process.startDetached(f"{programPath}/launch.sh", ["deepin-terminal", "-e", 
            #"env", f"WINE={wine[o1.currentText()]}", f"WINE64={wine[o1.currentText()]}", f"WINEPREFIX={wineBottonPath}",
            #f"{programPath}/dxvk/setup_dxvk.sh", "uninstall"])

def InstallOther():
    if e1.currentText()== "":
        wineBottonPath = setting["DefultBotton"]
    else:
        wineBottonPath = e1.currentText()
    OpenTerminal(f"'{programPath}/InstallOther.py' '{wineBottonPath}' '{wine[o1.currentText()]}' {int(setting['RuntimeCache'])}")

def BuildExeDeb():
    if e1.currentText() == "":
        wineBottonPath = setting["DefultBotton"]
    else:
        wineBottonPath = e1.currentText()
    threading.Thread(target=os.system, args=[f"python3 '{programPath}/deepin-wine-packager.py' '{wineBottonPath}' '{wine[o1.currentText()]}'"]).start()

def SetDeepinFileDialogDeepin():
    code = os.system(f"pkexec \"{programPath}/deepin-wine-venturi-setter.py\" deepin")
    if code != 0:
        if code == 1:
            QtWidgets.QMessageBox.critical(widget, "错误", "无法更新配置：配置不准重复配置")
            return
        QtWidgets.QMessageBox.critical(widget, "错误", "配置失败")
        return
    QtWidgets.QMessageBox.information(widget, "提示", "设置完成！")

def AddReg():
    path = QtWidgets.QFileDialog.getOpenFileName(window, "保存路径", get_home(), "reg文件(*.reg);;所有文件(*.*)")
    if path[0] == "" and not path[1]:
        return
    RunWineProgram(f"regedit' /S '{path[0]}' 'HKEY_CURRENT_USER\Software\Wine\DllOverrides")

def SaveDllList():
    path = QtWidgets.QFileDialog.getSaveFileName(window, "保存路径", get_home(), "reg文件(*.reg);;所有文件(*.*)")
    if path[0] == "" and not path[1]:
        return
    RunWineProgram(f"regedit' /E '{path[0]}' 'HKEY_CURRENT_USER\Software\Wine\DllOverrides")

def SetDeepinFileDialogDefult():
    code = os.system(f"pkexec \"{programPath}/deepin-wine-venturi-setter.py\" defult")
    if code != 0:
        if code == 1:
            QtWidgets.QMessageBox.critical(widget, "错误", "无法更新配置：配置不准重复配置")
            return
        QtWidgets.QMessageBox.critical(widget, "错误", "配置失败")
        return
    QtWidgets.QMessageBox.information(widget, "提示", "设置完成！")

def SetDeepinFileDialogRecovery():
    threading.Thread(target=OpenTerminal, args=[f"pkexec '{programPath}/deepin-wine-venturi-setter.py' recovery"]).start()

def DeleteDesktopIcon():
    if os.path.exists(f"{get_home()}/.local/share/applications/wine"):
        try:
            shutil.rmtree(f"{get_home()}/.local/share/applications/wine")
        except:
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(widget, "错误", traceback.format_exc())
            return
    QtWidgets.QMessageBox.information(widget, "提示", "删除完成")

def DeleteWineBotton():
    if QtWidgets.QMessageBox.question(widget, "提示", "你确定要删除容器吗？删除后将无法恢复！\n如果没有选择 wine 容器，将会自动删除默认的容器！") == QtWidgets.QMessageBox.No:
        return
    if e1.currentText() == "":
        wineBottonPath = setting["DefultBotton"]
    else:
        wineBottonPath = e1.currentText()
    try:
        shutil.rmtree(wineBottonPath)
        QtWidgets.QMessageBox.information(widget, "提示", "删除完毕！")
    except:
        traceback.print_exc()
        QtWidgets.QMessageBox.critical(widget, "错误", traceback.format_exc())

def ThankWindow():
    # 直接显示关于窗口，关于窗口已经添加
    about_this_program()

def InstallWineFont():
    # 筛选 apt
    if not os.system("which aptss"):
        threading.Thread(target=OpenTerminal, args=[f"sudo aptss install ms-core-fonts -y"]).start()
    elif not os.system("which ss-apt-fast"):
        threading.Thread(target=OpenTerminal, args=[f"sudo ss-apt-fast install ms-core-fonts -y"]).start()
    elif not os.system("which apt-fast"):
        threading.Thread(target=OpenTerminal, args=[f"sudo apt-fast install ms-core-fonts -y"]).start()
    else:
        threading.Thread(target=OpenTerminal, args=[f"sudo apt install ms-core-fonts -y"]).start()

def WineRunnerBugUpload():
    threading.Thread(target=os.system, args=[f"'{programPath}/deepin-wine-runner-update-bug'"]).start()

def SetHttpProxy():
    QtWidgets.QMessageBox.information(window, "提示", "请在下面的对话框正确输入内容以便设置代理")
    proxyServerAddress = QtWidgets.QInputDialog.getText(window, "提示", "请输入代理服务器地址")[0]
    port = QtWidgets.QInputDialog.getText(window, "提示", "请输入代理服务器端口")[0]
    if proxyServerAddress == "" or port == "":
        return
    RunWineProgram("reg' add 'HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings' /v ProxyEnable /t REG_DWORD /d 00000001 '/f")
    RunWineProgram(f"reg' add 'HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings' /v ProxyServer /d '{proxyServerAddress}:{port}' '/f")

def DisbledHttpProxy():
    RunWineProgram("reg' add 'HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings' /v ProxyEnable /t REG_DWORD /d 00000000 '/f")

def GetScreenSize():
    screenInformation = []
    # 使用 xrandr 进行筛选
    for i in subprocess.getoutput("xrandr").split('\n'):
        if not " connected " in i:  # 检测连接的显示器
            continue
        # 获取分辨率基本信息，如
        # DisplayPort-0 connected 1600x900+1280+0 (normal left inverted right x axis y axis) 434mm x 236mm
        # 先判断是否为主屏幕
        main = False
        if "primary" in i:
            main = True
        # 进行进一步筛选
        i = i[i.index("connected"):].replace("connected", "").replace("primary", "")
        # 进行初步筛选，如
        # 1600x900+1280+0 (normal left inverted right x axis y axis) 434mm x 236mm
        i = i[:i.index("(")].replace(" ", "")
        # 筛选为 1600x900+0+0 进行最后数值的提取
        screenInformation.append([
            int(i[:i.index("x")]),                     # 获取宽度
            int(i[i.index("x") + 1 :i.index("+")]),    # 获取高度
            int(i[i.index("+") + 1:].split('+')[0]),   # 获取显示屏 X 坐标
            int(i[i.index("+") + 1:].split('+')[1]),   # 获取显示屏 Y 坐标
            main                                       # 是否为主屏幕
        ])
    return screenInformation  # 返回结果

def UOSPackageScript():
    threading.Thread(target=os.system, args=[f"python3 '{programPath}/deepin-wine-packager-with-script.py'"]).start()

def RunVM():
    threading.Thread(target=os.system, args=[f"bash '{programPath}/RunVM.sh'"]).start()



class UpdateWindow():
    data = {}
    update = None
    def ShowWindow():
        UpdateWindow.update = QtWidgets.QMainWindow()
        updateWidget = QtWidgets.QWidget()
        updateWidgetLayout = QtWidgets.QGridLayout()
        versionLabel = QtWidgets.QLabel(f"当前版本：{version}\n最新版本：未知\n更新内容：")
        updateText = QtWidgets.QTextBrowser()
        updateText.anchorClicked.connect(OpenUrl)
        updateText.setOpenLinks(False)
        updateText.setOpenExternalLinks(False)
        ok = QtWidgets.QPushButton(QtCore.QCoreApplication.translate("U", "更新（更新时会自动关闭 Wine 运行器）"))
        ok.clicked.connect(UpdateWindow.Update)
        cancel = QtWidgets.QPushButton("取消")
        cancel.clicked.connect(UpdateWindow.update.close)
        url = "http://update.gfdgdxi.top/update.json"
        try:
            UpdateWindow.data = json.loads(requests.get(url).text)
            versionLabel = QtWidgets.QLabel(f"当前版本：{version}\n最新版本：{UpdateWindow.data['Version']}\n更新内容：")
            if UpdateWindow.data["Version"] == version:
                updateText.setText("此为最新版本，无需更新")
                ok.setDisabled(True)
            else:
                # 版本号读取（防止出现高版本号提示要“升级”到低版本号的问题）
                localVersionList = version.split(".")
                webVersionList = UpdateWindow.data['Version'].split(".")
                for i in range(len(localVersionList)):
                    local = int(localVersionList[i])
                    web = int(webVersionList[i])
                    if web < local:
                        updateText.setHtml(f"""<p>此为最新版本，无需更新，但似乎您当前使用的程序版本比云端版本还要高。</p>
<p>出现这个问题可能会有如下几种情况：</p>
<p>1、使用编译或者内测版本</p>
<p>2、自己修改了程序版本</p>
<p>3、作者忘记更新云端上的更新信息了</p>
<p>如果是第三种情况，请反馈到此：<a href='https://gitee.com/gfdgd-xi/deep-wine-runner/issues/I6T3FG'>https://gitee.com/gfdgd-xi/deep-wine-runner/issues/I6T3FG</a></p>
<p><img src='{programPath}/Icon/doge.png'></p>""")
                        ok.setDisabled(True)
                        break
                    if web > local:
                        updateText.setText(UpdateWindow.data["New"].replace("\\n", "\n"))
                        ok.setEnabled(True)
                        break
                
        except:
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(updateWidget, "错误", "无法连接服务器！")
        updateWidgetLayout.addWidget(versionLabel, 0, 0, 1, 1)
        updateWidgetLayout.addWidget(updateText, 1, 0, 1, 3)
        updateWidgetLayout.addWidget(ok, 2, 2, 1, 1)
        updateWidgetLayout.addWidget(cancel, 2, 1, 1, 1)
        updateWidget.setLayout(updateWidgetLayout)
        UpdateWindow.update.setCentralWidget(updateWidget)
        UpdateWindow.update.setWindowTitle(QtCore.QCoreApplication.translate("U", "检查更新"))
        UpdateWindow.update.resize(updateWidget.frameGeometry().width(), int(updateWidget.frameGeometry().height() * 1.5))
        UpdateWindow.update.show()

    def Update():
        if os.path.exists("/tmp/spark-deepin-wine-runner/update"):
            shutil.rmtree("/tmp/spark-deepin-wine-runner/update")
        os.makedirs("/tmp/spark-deepin-wine-runner/update")
        unPackageNew = False
        isArch = False
        isFedora = False
        if os.path.exists("/etc/arch-release"):
            isArch = True
            if UpdateWindow.data["Url-pkg"][0] == None:
                unPackageNew = True
        if os.path.exists("/etc/fedora-release"):
            isFedora = True
            if UpdateWindow.data["Url-rpm"][0] == None:
                unPackageNew = True
        try:            
            print(UpdateWindow.data["Url"])
            if os.path.exists(f"{programPath}/off-line.lock") or programPath != "/opt/apps/deepin-wine-runner" or unPackageNew:
                # 使用解压法更新
                write_txt("/tmp/spark-deepin-wine-runner/update.sh", f"""#!/bin/bash
echo 删除多余的安装包
rm -rfv /tmp/spark-deepin-wine-runner/update/*
echo 关闭“Wine 运行器”
python3 "{programPath}/updatekiller.py"
echo 下载安装包
wget -P /tmp/spark-deepin-wine-runner/update {UpdateWindow.data["Url"][0]}
echo 安装安装包
cd /tmp/spark-deepin-wine-runner/update
7z x *.deb
7z x data.tar
cp opt/apps/deepin-wine-runner/* "{programPath}" -rv
notify-send -i "{iconPath}" "更新完毕！"
zenity --info --text=\"更新完毕！\" --ellipsize
""")
                OpenTerminal("bash /tmp/spark-deepin-wine-runner/update.sh")
                return
            else:
                if isArch:
                    # 使用 pacman 安装更新
                    write_txt("/tmp/spark-deepin-wine-runner/update.sh", f"""#!/bin/bash
echo 删除多余的安装包
rm -rfv /tmp/spark-deepin-wine-runner/update/*
echo 关闭“Wine 运行器”
python3 "{programPath}/updatekiller.py"
echo 下载安装包
wget -P /tmp/spark-deepin-wine-runner/update {UpdateWindow.data["Url-pkg"][0]}
echo 安装安装包
pacman -U /tmp/spark-deepin-wine-runner/update/*  --noconfirm
notify-send -i "{iconPath}" "更新完毕！"
zenity --info --text=\"更新完毕！\" --ellipsize
""")
                elif isFedora:
                    # 使用 yum 安装更新
                    write_txt("/tmp/spark-deepin-wine-runner/update.sh", f"""#!/bin/bash
echo 删除多余的安装包
rm -rfv /tmp/spark-deepin-wine-runner/update/*
echo 关闭“Wine 运行器”
python3 "{programPath}/updatekiller.py"
echo 下载安装包
wget -O /tmp/spark-deepin-wine-runner/update/spark-deepin-wine-runner.rpm {UpdateWindow.data["Url-rpm"][0]}
echo 安装安装包
yum reinstall /tmp/spark-deepin-wine-runner/update/spark-deepin-wine-runner.rpm  -y
notify-send -i "{iconPath}" "更新完毕！"
zenity --info --text=\"更新完毕！\" --ellipsize
""")
                else:
                    # 使用 deb 安装更新
                    write_txt("/tmp/spark-deepin-wine-runner/update.sh", f"""#!/bin/bash
echo 删除多余的安装包
rm -rfv /tmp/spark-deepin-wine-runner/update/*
echo 关闭“Wine 运行器”
python3 "{programPath}/updatekiller.py"
echo 下载安装包
wget -P /tmp/spark-deepin-wine-runner/update {UpdateWindow.data["Url"][0]}
echo 安装安装包
dpkg -i /tmp/spark-deepin-wine-runner/update/*
echo 修复依赖关系
apt install -f -y
notify-send -i "{iconPath}" "更新完毕！"
zenity --info --text=\"更新完毕！\" --ellipsize
""")
                OpenTerminal("pkexec bash /tmp/spark-deepin-wine-runner/update.sh")
        except:
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(None, "出现错误，无法继续更新", traceback.format_exc())
        

class GetDllFromWindowsISO:
    wineBottonPath = get_home() + "/.wine"
    isoPath = None
    dllList = None
    message = None
    dllFound = None
    dllControl = None
    foundButton = None
    saveDll = None
    setWineBotton = None
    browser = None
    mount = False
    mountButton = None
    dllListModel = None
    arch = 0
    def ShowWindow():
        #DisableButton(True)
        GetDllFromWindowsISO.message = QtWidgets.QMainWindow()
        widget = QtWidgets.QWidget()
        widgetLayout = QtWidgets.QGridLayout()
        if not e1.currentText() == "":
            GetDllFromWindowsISO.wineBottonPath = e1.currentText()
        widgetLayout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("U", f"""提示：
    目前本提取功能暂只支持 NT 内核系统的官方安装镜像，不支持读取 ghost 等第三方封装方式的安装镜像
    以及不要拷贝/替换太多的 dll，否则可能会导致 wine 容器异常，以及不要替换 Wine 的核心 dll
    最后，拷贝/替换 dll 后，建议点击下面“设置 wine 容器”按钮==》函数库 进行设置
当前选择的 Wine 容器：{GetDllFromWindowsISO.wineBottonPath}""")), 0, 0, 1, 5)
        isoLabel = QtWidgets.QLabel(QtCore.QCoreApplication.translate("U", "ISO镜像："))
        GetDllFromWindowsISO.isoPath = QtWidgets.QComboBox()
        GetDllFromWindowsISO.browser = QtWidgets.QPushButton(QtCore.QCoreApplication.translate("U", "浏览"))
        isoControl = QtWidgets.QWidget()
        isoControlLayout = QtWidgets.QHBoxLayout()
        isoControl.setLayout(isoControlLayout)
        dllControl = QtWidgets.QWidget()
        dllControlLayout = QtWidgets.QHBoxLayout()
        dllControl.setLayout(dllControlLayout)
        GetDllFromWindowsISO.mountButton = QtWidgets.QPushButton(QtCore.QCoreApplication.translate("U", "读取/挂载ISO镜像"))
        umountButton = QtWidgets.QPushButton(QtCore.QCoreApplication.translate("U", "关闭/卸载ISO镜像"))
        GetDllFromWindowsISO.dllFound = QtWidgets.QComboBox()
        GetDllFromWindowsISO.foundButton = QtWidgets.QPushButton(QtCore.QCoreApplication.translate("U", "查找"))
        GetDllFromWindowsISO.dllList = QtWidgets.QListView()
        GetDllFromWindowsISO.saveDll = QtWidgets.QPushButton(QtCore.QCoreApplication.translate("U", "保存到 wine 容器中"))
        GetDllFromWindowsISO.setWineBotton = QtWidgets.QPushButton(QtCore.QCoreApplication.translate("U", "设置 wine 容器"))
        isoLabel.setSizePolicy(size)
        GetDllFromWindowsISO.isoPath.setEditable(True)
        GetDllFromWindowsISO.isoPath.addItems(isoPath)
        GetDllFromWindowsISO.isoPath.setEditText("")
        GetDllFromWindowsISO.browser.setSizePolicy(size)
        GetDllFromWindowsISO.mountButton.setSizePolicy(size)
        isoControlLayout.addWidget(GetDllFromWindowsISO.mountButton)
        umountButton.setSizePolicy(size)
        isoControlLayout.addWidget(umountButton)
        GetDllFromWindowsISO.dllFound.setEditable(True)
        GetDllFromWindowsISO.dllFound.addItems(isoPathFound)
        GetDllFromWindowsISO.dllFound.setEditText("")
        GetDllFromWindowsISO.saveDll.setSizePolicy(size)
        dllControlLayout.addWidget(GetDllFromWindowsISO.saveDll)
        GetDllFromWindowsISO.setWineBotton.setSizePolicy(size)
        GetDllFromWindowsISO.DisbledDown(True)
        dllControlLayout.addWidget(GetDllFromWindowsISO.setWineBotton)
        widgetLayout.addWidget(isoLabel, 1, 0, 1, 1)
        widgetLayout.addWidget(GetDllFromWindowsISO.isoPath, 1, 1, 1, 1)
        widgetLayout.addWidget(GetDllFromWindowsISO.browser, 1, 2, 1, 1)
        widgetLayout.addWidget(isoControl, 2, 1, 1, 1)
        widgetLayout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("U", "查找DLL\n（为空则代表不查找，\n将显示全部内容）：")), 3, 0, 1, 1)
        widgetLayout.addWidget(GetDllFromWindowsISO.dllFound, 3, 1, 1, 1)
        widgetLayout.addWidget(GetDllFromWindowsISO.foundButton, 3, 2, 1, 1)
        widgetLayout.addWidget(GetDllFromWindowsISO.dllList, 4, 1, 1, 1)
        widgetLayout.addWidget(dllControl, 5, 1, 1, 1)
        widget.setLayout(widgetLayout)
        GetDllFromWindowsISO.browser.clicked.connect(GetDllFromWindowsISO.Browser)
        GetDllFromWindowsISO.mountButton.clicked.connect(GetDllFromWindowsISO.MountDisk)
        umountButton.clicked.connect(GetDllFromWindowsISO.UmountDisk)
        GetDllFromWindowsISO.foundButton.clicked.connect(GetDllFromWindowsISO.Found)
        GetDllFromWindowsISO.saveDll.clicked.connect(GetDllFromWindowsISO.CopyDll)
        GetDllFromWindowsISO.setWineBotton.clicked.connect(lambda: RunWineProgram("winecfg", Disbled=False))
        GetDllFromWindowsISO.message.setCentralWidget(widget)
        GetDllFromWindowsISO.dllListModel = QtCore.QStringListModel()
        GetDllFromWindowsISO.dllListModel.setStringList([])
        GetDllFromWindowsISO.dllList.setModel(GetDllFromWindowsISO.dllListModel)
        GetDllFromWindowsISO.isoPath.currentText()
        GetDllFromWindowsISO.message.setWindowTitle(f"Wine 运行器 {version}——从 ISO 提取 DLL")
        GetDllFromWindowsISO.message.setWindowIcon(QtGui.QIcon(iconPath))
        GetDllFromWindowsISO.message.show()

    def DisbledUp(state):
        GetDllFromWindowsISO.isoPath.setDisabled(state)
        GetDllFromWindowsISO.browser.setDisabled(state)
        GetDllFromWindowsISO.mountButton.setDisabled(state)


    def DisbledDown(state):
        GetDllFromWindowsISO.dllList.setDisabled(state)
        GetDllFromWindowsISO.dllFound.setDisabled(state)
        GetDllFromWindowsISO.saveDll.setDisabled(state)
        GetDllFromWindowsISO.setWineBotton.setDisabled(state)
        GetDllFromWindowsISO.foundButton.setDisabled(state)

    def Browser():
        path = QtWidgets.QFileDialog.getOpenFileName(GetDllFromWindowsISO.message, "选择 ISO 镜像文件", json.loads(readtxt(get_home() + "/.config/deepin-wine-runner/FindISO.json"))["path"], "iso 镜像文件(*.iso);;ISO 镜像文件(*.ISO);;所有文件(*.*)")[0]
        if path == None or path == "":
            return
        GetDllFromWindowsISO.isoPath.setEditText(path)
        write_txt(get_home() + "/.config/deepin-wine-runner/FindISO.json", json.dumps({"path": os.path.dirname(path)}))  # 写入配置文件

    def Found():
        found = GetDllFromWindowsISO.dllFound.currentText()
        findList = []
        try:
            if found == "":
                # 显示所有内容
                # 下面内容需要分类讨论
                if GetDllFromWindowsISO.arch == 0:
                    for i in os.listdir("/tmp/wine-runner-getdll/i386"):
                        if i[-3:] == "dl_":
                            findList.append(i[:-1] + "l")    
                elif GetDllFromWindowsISO.arch == 32:
                    for i in os.listdir("/tmp/wine-runner-getdll-wim/Windows/SysWOW64"):
                        if i[-3:] == "dll":
                            findList.append(i[:-1] + "l")  
                elif GetDllFromWindowsISO.arch == 64:
                    for i in os.listdir("/tmp/wine-runner-getdll-wim/Windows/System32"):
                        if i[-3:] == "dll":
                            findList.append(i[:-1] + "l")  
                GetDllFromWindowsISO.dllListModel.setStringList(findList)
                return
            if GetDllFromWindowsISO.arch == 0:
                for i in os.listdir("/tmp/wine-runner-getdll/i386"):
                    if found in i[:-1] + "l":
                        findList.append(i[:-1] + "l")  
            elif GetDllFromWindowsISO.arch == 32:
                for i in os.listdir("/tmp/wine-runner-getdll-wim/Windows/SysWOW64"):
                    if found in i[:-1] + "l":
                        findList.append(i[:-1] + "l")  
            elif GetDllFromWindowsISO.arch == 64:
                for i in os.listdir("/tmp/wine-runner-getdll-wim/Windows/System32"):
                    if found in i[:-1] + "l":
                        findList.append(i[:-1] + "l")  
            if len(isoPath) == 0:
                if isoPathFound[-1] != found:
                    isoPathFound.append(found)  # 将记录写进数组
                    write_txt(get_home() + "/.config/deepin-wine-runner/ISOPathFound.json", str(json.dumps(ListToDictionary(isoPathFound))))  # 将历史记录的数组转换为字典并写入
            GetDllFromWindowsISO.dllFound.clear()
            GetDllFromWindowsISO.dllFound.addItems(isoPathFound)
            GetDllFromWindowsISO.dllListModel.setStringList(findList)
        except:
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(GetDllFromWindowsISO.message, transla.trans("错误"), traceback.format_exc())

 
    def MountDisk():
        if not os.path.exists(GetDllFromWindowsISO.isoPath.currentText()):
            QtWidgets.QMessageBox.critical(GetDllFromWindowsISO.message, transla.trans("错误"), transla.trans("您选择的 ISO 镜像文件不存在"))
            return
        if os.path.exists("/tmp/wine-runner-getdll"):
            try:
                os.rmdir("/tmp/wine-runner-getdll")
                os.system("rm -rf /tmp/wine-runner-getdll-wim")
            except:
                # 如果无法删除可能是挂载了文件
                os.system("wimunmount /tmp/wine-runner-getdll-wim")
                os.system("pkexec umount /tmp/wine-runner-getdll")
                
                try:
                    os.rmdir("/tmp/wine-runner-getdll")
                    os.rmdir("/tmp/wine-runner-getdll-wim")
                except:
                    traceback.print_exc()
                    QtWidgets.QMessageBox.critical(GetDllFromWindowsISO.message, "错误", traceback.format_exc())
                    return
        os.makedirs("/tmp/wine-runner-getdll")
        os.system(f"pkexec mount '{GetDllFromWindowsISO.isoPath.currentText()}' /tmp/wine-runner-getdll")
        findList = []
        # 判断是新版的 Windows ISO（Windows Vista 及以上版本）
        if os.path.exists("/tmp/wine-runner-getdll/sources/install.wim"):
            # 如果没有安装 wimtools 的话
            if os.system("which wimmount") != 0:
                QtWidgets.QMessageBox.critical(GetDllFromWindowsISO.message, "错误", f"镜像内容读取/挂载失败，因为没有安装 wimtools 以至无法读取")
                return
            # 是新版，挂载 wim
            # 需要让用户选择挂载内容
            QtWidgets.QInputDialog.getMultiLineText(GetDllFromWindowsISO.message, "提示", "挂载文件需要用户记住并在下一个对话框输入 Index 以挂载正确的镜像，按下下方任意按钮即可继续", subprocess.getoutput("wiminfo '/tmp/wine-runner-getdll/sources/install.wim'"))
            choose = QtWidgets.QInputDialog.getInt(GetDllFromWindowsISO.message, "提示", "请输入 Index")
            if not choose[1]:
                return
            os.makedirs("/tmp/wine-runner-getdll-wim")
            os.system(f"wimmount /tmp/wine-runner-getdll/sources/install.wim {choose[0]} /tmp/wine-runner-getdll-wim")
            if os.path.exists("/tmp/wine-runner-getdll-wim/Windows/SysWOW64"):
                # 如果是 64 位镜像
                if QtWidgets.QInputDialog.getItem(GetDllFromWindowsISO.message, "选择位数", "选择位数（如果没有选择，默认为 64 位）", ["32", "64"], 1, False) == "32":
                    # 64 位镜像的 32 位是存在 SysWOW64 的                
                    try:
                        for i in os.listdir("/tmp/wine-runner-getdll-wim/Windows/SysWOW64"):
                            if i[-3:] == "dll":
                                findList.append(i[:-1] + "l")     
                        GetDllFromWindowsISO.dllListModel.setStringList(findList)
                        GetDllFromWindowsISO.arch = 32
                        GetDllFromWindowsISO.DisbledDown(False)  
                        GetDllFromWindowsISO.DisbledUp(True)
                        GetDllFromWindowsISO.mount = True
                        if len(isoPath) == 0 or isoPath[-1] != GetDllFromWindowsISO.isoPath.currentText():
                            isoPath.append(GetDllFromWindowsISO.isoPath.currentText())  # 将记录写进数组
                        write_txt(get_home() + "/.config/deepin-wine-runner/ISOPath.json", str(json.dumps(ListToDictionary(isoPath))))  # 将历史记录的数组转换为字典并写入
                        GetDllFromWindowsISO.isoPath.clear()
                        GetDllFromWindowsISO.isoPath.addItems(isoPath)
                        return
                    except:
                        traceback.print_exc()
                        QtWidgets.QMessageBox.critical(GetDllFromWindowsISO.message, "错误", f"镜像内容读取/挂载失败，报错如下：\n{traceback.format_exc()}")
                        return
            try:
                for i in os.listdir("/tmp/wine-runner-getdll-wim/Windows/System32"):
                    if i[-3:] == "dll":
                        findList.append(i[:-1] + "l")    
                GetDllFromWindowsISO.arch = 64 
            except:
                traceback.print_exc()
                QtWidgets.QMessageBox.critical(GetDllFromWindowsISO.message, "错误", f"镜像内容读取/挂载失败，报错如下：\n{traceback.format_exc()}")
                return
            GetDllFromWindowsISO.dllListModel.setStringList(findList)
        else:
            try:
                for i in os.listdir("/tmp/wine-runner-getdll/i386"):
                    if i[-3:] == "dl_":
                        findList.append(i[:-1] + "l")     
                GetDllFromWindowsISO.arch = 0
            except:
                traceback.print_exc()
                QtWidgets.QMessageBox.critical(GetDllFromWindowsISO.message, "错误", f"镜像内容读取/挂载失败，报错如下：\n{traceback.format_exc()}")
                return
            GetDllFromWindowsISO.dllListModel.setStringList(findList)
        GetDllFromWindowsISO.DisbledDown(False)  
        GetDllFromWindowsISO.DisbledUp(True)
        GetDllFromWindowsISO.mount = True
        if len(isoPath) == 0 or isoPath[-1] != GetDllFromWindowsISO.isoPath.currentText():
            isoPath.append(GetDllFromWindowsISO.isoPath.currentText())  # 将记录写进数组
            write_txt(get_home() + "/.config/deepin-wine-runner/ISOPath.json", str(json.dumps(ListToDictionary(isoPath))))  # 将历史记录的数组转换为字典并写入
            GetDllFromWindowsISO.isoPath.clear()
            GetDllFromWindowsISO.isoPath.addItems(isoPath)
        #GetDllFromWindowsISO.isoPath['value'] = isoPath

    def UmountDisk():
        os.system("wimunmount /tmp/wine-runner-getdll-wim")
        os.system("pkexec umount /tmp/wine-runner-getdll")
        try:
            shutil.rmtree("/tmp/wine-runner-getdll")
            os.system("rm -rf /tmp/wine-runner-getdll-wim")
        except:
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(GetDllFromWindowsISO.message, QtCore.QCoreApplication.translate("U", "错误"), f"关闭/卸载镜像失败，报错如下：\n{traceback.format_exc()}")
            return
        GetDllFromWindowsISO.DisbledDown(True)
        GetDllFromWindowsISO.DisbledUp(False)
        GetDllFromWindowsISO.mount = False
        QtWidgets.QMessageBox.information(GetDllFromWindowsISO.message, QtCore.QCoreApplication.translate("U", "提示"), QtCore.QCoreApplication.translate("U", "关闭/卸载成功！"))

    def CopyDll():
        choose = GetDllFromWindowsISO.dllList.selectionModel().selectedIndexes()[0].data()
        if os.path.exists(f"{GetDllFromWindowsISO.wineBottonPath}/drive_c/windows/system32/{choose}"):
            if QtWidgets.QMessageBox.question(GetDllFromWindowsISO.message, "提示", f"DLL {choose} 已经存在，是否覆盖？") == QtWidgets.QMessageBox.No:
                return
        try:
            # 要分类讨论
            if GetDllFromWindowsISO.arch == 0:
                shutil.copy(f"/tmp/wine-runner-getdll/i386/{choose[:-1]}_", f"{GetDllFromWindowsISO.wineBottonPath}/drive_c/windows/system32/{choose}")
            elif GetDllFromWindowsISO.arch == 32:
                shutil.copy(f"/tmp/wine-runner-getdll-wim/Windows/SysWOW64/{choose[:-1]}l", f"{GetDllFromWindowsISO.wineBottonPath}/drive_c/windows/system32/{choose}")
            elif GetDllFromWindowsISO.arch == 64:
                shutil.copy(f"/tmp/wine-runner-getdll-wim/Windows/System32/{choose[:-1]}l", f"{GetDllFromWindowsISO.wineBottonPath}/drive_c/windows/system32/{choose}")
            # 选择原装或优于内建
            if QtWidgets.QInputDialog.getItem(GetDllFromWindowsISO.message, "选择", "选择模式", ["原装先于内建", "原装"], 0, False) == "原装先于内建":
                # 原装先于内建
                os.system(f"WINEPREFIX='{GetDllFromWindowsISO.wineBottonPath}' '{wine[o1.currentText()]}' reg add 'HKEY_CURRENT_USER\Software\Wine\DllOverrides' /v {os.path.splitext(choose)[0]} /d native,builtin /f")
            else:
                # 原装
                os.system(f"WINEPREFIX='{GetDllFromWindowsISO.wineBottonPath}' '{wine[o1.currentText()]}' reg add 'HKEY_CURRENT_USER\Software\Wine\DllOverrides' /v {os.path.splitext(choose)[0]} /d native /f")
            QtWidgets.QMessageBox.information(GetDllFromWindowsISO.message, "提示", "提取成功！")
        except:
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(GetDllFromWindowsISO.message, "错误", traceback.format_exc())

choose = None

class ProgramSetting():
    wineBottonA = None
    wineDebug = None
    defultWine = None
    defultBotton = None
    terminalOpen = None
    wineOption = None
    #wineBottonDifferent = None
    centerWindow = None
    message = None
    theme = None
    monogeckoInstaller = None
    autoWine = None
    runtimeCache = None
    buildByBottleName = None
    autoPath = None
    qemuUnmountHome = None
    chineseLanguage = None
    fontSize = None
    def ShowWindow():
        ProgramSetting.message = QtWidgets.QMainWindow()
        widget = QtWidgets.QWidget()
        widgetLayout = QtWidgets.QGridLayout()
        widgetLayout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("U", "选择 Wine 容器版本：")), 0, 0, 1, 1)
        widgetLayout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("U", "wine DEBUG 信息输出：")), 1, 0, 1, 1)
        widgetLayout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("U", "默认 Wine：")), 2, 0, 1, 1)
        widgetLayout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("U", "默认 Wine 容器：")), 3, 0, 1, 1)
        widgetLayout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("U", "使用终端打开：")), 4, 0, 1, 1)
        widgetLayout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("U", "自定义 wine 参数：")), 5, 0, 1, 1)
        widgetLayout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("U", "程序主题：")), 6, 0, 1, 1)
        widgetLayout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("U", "Wine 默认 Mono 和 Gecko 安装器：")), 7, 0, 1, 1)
        widgetLayout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("U", "忽略未安装的 Wine：")), 8, 0, 1, 1)
        widgetLayout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("U", "下载缓存：")), 9, 0, 1, 1)
        widgetLayout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("U", "图标生成：")), 10, 0, 1, 1)
        widgetLayout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("U", "自动根据EXE名称生成路径：")), 11, 0, 1, 1)
        widgetLayout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("U", "Qemu + Chroot 挂载用户目录：")), 12, 0, 1, 1)
        #widgetLayout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("U", "程序翻译：")), 13, 0, 1, 1)
        widgetLayout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("U", "字体缩小比例（数值越大字体越小，默认为 1）：")), 14, 0, 1, 1)
        ProgramSetting.wineBottonA = QtWidgets.QComboBox()
        ProgramSetting.wineDebug = QtWidgets.QCheckBox(QtCore.QCoreApplication.translate("U", "开启 DEBUG 输出"))
        ProgramSetting.defultWine = QtWidgets.QComboBox()
        ProgramSetting.defultBotton = QtWidgets.QLineEdit()
        ProgramSetting.theme = QtWidgets.QComboBox()
        ProgramSetting.theme.addItems(QtWidgets.QStyleFactory.keys())
        ProgramSetting.theme.setCurrentText(setting["Theme"])
        save = QtWidgets.QPushButton(QtCore.QCoreApplication.translate("U", "保存"))
        save.clicked.connect(ProgramSetting.Save)
        defultBottonButton = QtWidgets.QPushButton(QtCore.QCoreApplication.translate("U", "浏览"))
        defultBottonButton.clicked.connect(ProgramSetting.Browser)
        themeTry = QtWidgets.QPushButton(QtCore.QCoreApplication.translate("U", "测试(重启后变回设置的主题)"))
        themeTry.clicked.connect(ProgramSetting.Try)
        ProgramSetting.terminalOpen = QtWidgets.QCheckBox(QtCore.QCoreApplication.translate("U", "使用终端打开（deepin 终端）"))
        ProgramSetting.wineOption = QtWidgets.QLineEdit()
        ProgramSetting.monogeckoInstaller = QtWidgets.QCheckBox(QtCore.QCoreApplication.translate("U", "屏蔽 Wine 默认 Mono 和 Gecko 安装器"))
        ProgramSetting.autoWine = QtWidgets.QCheckBox(QtCore.QCoreApplication.translate("U", "不显示未检测到的 Wine"))
        ProgramSetting.runtimeCache = QtWidgets.QCheckBox(QtCore.QCoreApplication.translate("U", "开启下载缓存"))
        ProgramSetting.buildByBottleName = QtWidgets.QCheckBox(QtCore.QCoreApplication.translate("U", "本软件构建的图标后面添加容器名"))
        ProgramSetting.autoPath = QtWidgets.QCheckBox(QtCore.QCoreApplication.translate("U", "自动根据文件名生成容器路径（开启后必须通过修改默认wine容器路径才可指定其它路径，重启程序后生效）"))
        ProgramSetting.qemuUnmountHome = QtWidgets.QCheckBox(QtCore.QCoreApplication.translate("U", "使用 Qemu + Chroot 时不挂载用户目录并与系统隔离（修改后重启操作系统生效）"))
        #ProgramSetting.chineseLanguage = QtWidgets.QCheckBox(QtCore.QCoreApplication.translate("U", "禁用程序界面翻译"))
        ProgramSetting.fontSize = QtWidgets.QDoubleSpinBox()
        ProgramSetting.wineBottonA.addItems(["Auto", "win32", "win64"])
        ProgramSetting.wineBottonA.setCurrentText(setting["Architecture"])
        ProgramSetting.wineDebug.setChecked(setting["Debug"])
        ProgramSetting.defultWine.addItems(wine.keys())
        ProgramSetting.defultWine.setCurrentText(setting["DefultWine"])
        ProgramSetting.defultBotton.setText(setting["DefultBotton"])
        ProgramSetting.terminalOpen.setChecked(setting["TerminalOpen"])
        ProgramSetting.wineOption.setText(setting["WineOption"])
        ProgramSetting.monogeckoInstaller.setChecked(setting["MonoGeckoInstaller"])
        ProgramSetting.autoWine.setChecked(setting["AutoWine"])
        ProgramSetting.runtimeCache.setChecked(setting["RuntimeCache"])
        ProgramSetting.buildByBottleName.setChecked(setting["BuildByBottleName"])
        ProgramSetting.autoPath.setChecked(setting["AutoPath"])
        ProgramSetting.qemuUnmountHome.setChecked(setting["QemuUnMountHome"])
        #ProgramSetting.chineseLanguage.setChecked(setting["Chinese"])
        ProgramSetting.fontSize.setValue(setting["FontSize"])
        # QemuUnMountHome
        widgetLayout.addWidget(ProgramSetting.wineBottonA, 0, 1, 1, 1)
        widgetLayout.addWidget(ProgramSetting.wineDebug, 1, 1, 1, 1)
        widgetLayout.addWidget(ProgramSetting.defultWine, 2, 1, 1, 1)
        widgetLayout.addWidget(ProgramSetting.defultBotton, 3, 1, 1, 1)
        widgetLayout.addWidget(defultBottonButton, 3, 2, 1, 1)
        widgetLayout.addWidget(ProgramSetting.terminalOpen, 4, 1, 1, 1)
        widgetLayout.addWidget(ProgramSetting.wineOption, 5, 1, 1, 1)
        widgetLayout.addWidget(ProgramSetting.theme, 6, 1, 1, 1)
        widgetLayout.addWidget(themeTry, 6, 2, 1, 1)
        widgetLayout.addWidget(ProgramSetting.monogeckoInstaller, 7, 1, 1, 1)
        widgetLayout.addWidget(ProgramSetting.autoWine, 8, 1, 1, 1)
        widgetLayout.addWidget(ProgramSetting.runtimeCache, 9, 1, 1, 1)
        widgetLayout.addWidget(ProgramSetting.buildByBottleName, 10, 1, 1, 1)
        widgetLayout.addWidget(ProgramSetting.autoPath, 11, 1, 1, 2)
        widgetLayout.addWidget(ProgramSetting.qemuUnmountHome, 12, 1, 1, 2)
        #widgetLayout.addWidget(ProgramSetting.chineseLanguage, 13, 1, 1, 2)
        widgetLayout.addWidget(ProgramSetting.fontSize, 14, 1, 1, 2)
        widgetLayout.addWidget(save, 15, 2, 1, 1)
        widget.setLayout(widgetLayout)
        ProgramSetting.message.setCentralWidget(widget)
        ProgramSetting.message.setWindowIcon(QtGui.QIcon(iconPath))
        ProgramSetting.message.setWindowTitle(f"设置 wine 运行器 {version}")
        ProgramSetting.message.show()

    def Browser():
        path = QtWidgets.QFileDialog.getExistingDirectory(ProgramSetting.message, QtCore.QCoreApplication.translate("U", "选择 Wine 容器"), json.loads(readtxt(get_home() + "/.config/deepin-wine-runner/WineBotton.json"))["path"])
        if path == "" or path == None or path == "()" or path == ():
            return
        ProgramSetting.defultBotton.setText(path)

    def Try():
        app.setStyle(QtWidgets.QStyleFactory.create(ProgramSetting.theme.currentText()))

    def Save():
        # 写入容器位数设置
        setting["Architecture"] = ProgramSetting.wineBottonA.currentText()
        setting["Debug"] = ProgramSetting.wineDebug.isChecked()
        setting["DefultWine"] = ProgramSetting.defultWine.currentText()
        setting["DefultBotton"] = ProgramSetting.defultBotton.text()
        setting["TerminalOpen"] = ProgramSetting.terminalOpen.isChecked()
        setting["WineOption"] = ProgramSetting.wineOption.text()
        setting["Theme"] = ProgramSetting.theme.currentText()
        setting["MonoGeckoInstaller"] = ProgramSetting.monogeckoInstaller.isChecked()
        setting["AutoWine"] = ProgramSetting.autoWine.isChecked()
        setting["RuntimeCache"] = ProgramSetting.runtimeCache.isChecked()
        setting["BuildByBottleName"] = ProgramSetting.buildByBottleName.isChecked()
        setting["AutoPath"] = ProgramSetting.autoPath.isChecked()
        setting["QemuUnMountHome"] = ProgramSetting.qemuUnmountHome.isChecked()
        #setting["Chinese"] = ProgramSetting.chineseLanguage.isChecked()
        setting["FontSize"] = ProgramSetting.fontSize.value()
        try:
            write_txt(get_home() + "/.config/deepin-wine-runner/WineSetting.json", json.dumps(setting))
        except:
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(ProgramSetting.message, "错误", traceback.format_exc())
            return
        QtWidgets.QMessageBox.information(ProgramSetting.message, "提示", "保存完毕！")

class ValueCheck():
    def __init__(self):
        pass
        
    def BASE64(self, filePath):
        src = ""
        with open(filePath, "rb") as f:
            base64Byte = base64.b64encode(f.read())
            src += base64Byte.decode("utf-8")
        return src

    def SHA1(self, filePath):
        sha1 = hashlib.sha1()
        file = open(filePath, "rb")
        while True:
            readByte = file.read(1024 * 1024)
            sha1.update(readByte)
            if not readByte:
                break
        file.close()
        return sha1.hexdigest()

    def MD5(self, filePath):
        md5 = hashlib.md5()
        file = open(filePath, "rb")
        while True:
            readByte = file.read(1024 * 1024)
            md5.update(readByte)
            if not readByte:
                break
        file.close()
        return md5.hexdigest()

    def SHA256(self, filePath):
        value = hashlib.sha256()
        file = open(filePath, "rb")
        while True:
            readByte = file.read(1024 * 1024)
            value.update(readByte)
            if not readByte:
                break
        file.close()
        return value.hexdigest()

    def SHA384(self, filePath):
        value = hashlib.sha384()
        file = open(filePath, "rb")
        while True:
            readByte = file.read(1024 * 1024)
            value.update(readByte)
            if not readByte:
                break
        file.close()
        return value.hexdigest()

    def SHA224(self, filePath):
        value = hashlib.sha224()
        file = open(filePath, "rb")
        while True:
            readByte = file.read(1024 * 1024)
            value.update(readByte)
            if not readByte:
                break
        file.close()
        return value.hexdigest()

    def SHA512(self, filePath):
        value = hashlib.sha512()
        file = open(filePath, "rb")
        while True:
            readByte = file.read(1024 * 1024)
            value.update(readByte)
            if not readByte:
                break
        file.close()
        return value.hexdigest()

    link = {
        "SHA1": SHA1,
        "MD5": MD5,
        "SHA256": SHA256,
        "SHA512": SHA512,
        "SHA224": SHA224,
        "SHA384": SHA384,
        "BASE64": BASE64
    }

    def Get(self, types):
        QtWidgets.QMessageBox.information(window, "提示", "在计算过程中，程序可能会出现无响应的问题，请稍后\n请在接下来的打开对话框中选择要计算的文件")
        file = QtWidgets.QFileDialog.getOpenFileName(window, "打开")[0]
        if file == "":
            return
        try:
            value = self.link[types](self, file)
            if QtWidgets.QInputDialog.getText(window, "值", "下面是计算得到的值，<b>是否要复制到剪切板？</b>", QtWidgets.QLineEdit.Normal, value)[1]:
                pyperclip.copy(value)
                QtWidgets.QMessageBox.information(window, "提示", "复制成功！")
        except:
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(window, "错误", traceback.format_exc())

def ChangePath():
    e1.setCurrentText(f'{setting["DefultBotton"]}/{os.path.splitext(os.path.basename(e2.currentText()))[0]}')

def ConnectRemoteWindowsPC(ip: str):
    if os.system("which xfreerdp"):
        if QtWidgets.QMessageBox.question(window, "提示", "未检测到 xfreerdp，是否立即安装？") == QtWidgets.QMessageBox.Yes:
            OpenTerminal("sudo apt install xfreerdp -y")
        return
    os.system(f"xfreerdp '{ip}'")

def UploadLog():
    if QtWidgets.QMessageBox.question(window, "提示", "您确定要上传吗？上传内容将不会公开，将用于加强日志分析功能") == QtWidgets.QMessageBox.Yes:
        text = QtWidgets.QInputDialog.getMultiLineText(window, "输入内容", "输入描述信息")
        try:
            returnList = requests.post(base64.b64decode("aHR0cDovLzEyMC4yNS4xNTMuMTQ0OjMwMjUwL2xvZw==").decode("utf-8"), {
                "Log": returnText.toPlainText(),
                "Wine": wine[o1.currentText()],
                "Tips": text
                }).json()
            if returnList["ExitCode"] == 0:
                QtWidgets.QMessageBox.information(window, "提示", "上传成功！")    
            else:
                print(returnList)
                QtWidgets.QMessageBox.critical(window, "错误", "上传失败！")    
        except:
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(window, "错误", "上传失败！")


def SaveLog():
    path = QtWidgets.QFileDialog.getSaveFileName(window, "保存日志", get_home(), "txt文件(*.txt);;html 文件(*.html);;所有文件(*.*))")
    if not path[1]:
        return
    print(path)
    try:
        with open(path[0], "w") as file:
            if path[1] == "html 文件(*.html)":
                file.write(returnText.toHtml())
            else:
                file.write(returnText.toPlainText())
    except:
        traceback.print_exc()
        QtWidgets.QMessageBox.critical(window, "错误", traceback.format_exc())

def GetNewInformation():
    try:
        # 获取是否为最新版本的公告
        informationID = requests.get("http://update.gfdgdxi.top/wine-runner/info/id.json").json()["Number"]
        text = requests.get("http://update.gfdgdxi.top/wine-runner/info/").text.replace("Icon/QR/", f"{programPath}/Icon/QR/")
        write_txt(f"{get_home()}/.config/deepin-wine-runner/information/{informationID}", informationID)
    except:
        traceback.print_exc()
        text = f"""<p>无法连接到服务器</p>
            <hr/>
            <p>你可以尝试：</p>
            <p>1. 判断是否能正常连接网络</p>
            <p>2. 作者的服务出问题了？（到这反馈：<a href='https://gitee.com/gfdgd-xi/deep-wine-runner/issues'>https://gitee.com/gfdgd-xi/deep-wine-runner/issues</a>）</p>
            <p>3. 玩个<a href="file://{programPath}/2048/index.html">游戏</a>解闷下</p>"""
    global webInformation
    if bad:
        webInformation = QtWidgets.QTextBrowser()
        webInformation.anchorClicked.connect(OpenUrl)
        webInformation.setOpenLinks(False)
        webInformation.setOpenExternalLinks(False)

    else:
        webInformation = QtWebEngineWidgets.QWebEngineView()
    webInformation.setHtml(text)
    webInformation.setWindowTitle("获取程序公告")
    webInformation.setWindowIcon(QtGui.QIcon(iconPath))
    webInformation.resize(int(webInformation.frameGeometry().width() * 1.3), int(webInformation.frameGeometry().height() * 1.1))
    webInformation.setWindowFlags(webInformation.windowFlags() | QtCore.Qt.Dialog)
    webInformation.setWindowModality(QtCore.Qt.ApplicationModal)
    webInformation.show()

def getFileFolderSize(fileOrFolderPath):
    """get size for file or folder"""
    totalSize = 0
    try:
        if not os.path.exists(fileOrFolderPath):
            return totalSize
        if os.path.isfile(fileOrFolderPath):
            totalSize = os.path.getsize(fileOrFolderPath)  # 5041481
            return totalSize
        if os.path.islink(fileOrFolderPath):
            return 0
        if os.path.isdir(fileOrFolderPath):
            with os.scandir(fileOrFolderPath) as dirEntryList:
                for curSubEntry in dirEntryList:
                    curSubEntryFullPath = os.path.join(fileOrFolderPath, curSubEntry.name)
                    if curSubEntry.is_dir():
                        curSubFolderSize = getFileFolderSize(curSubEntryFullPath)  # 5800007
                        totalSize += curSubFolderSize
                    elif curSubEntry.is_file():
                        curSubFileSize = os.path.getsize(curSubEntryFullPath)  # 1891
                        totalSize += curSubFileSize
                return totalSize
    except:
        return totalSize

# 获取当前语言
def get_now_lang()->"获取当前语言":
    return os.getenv('LANG')

# 又需要修复多线程导致的控件问题
def AddDockerMenu():
    global dockers
    global openFileManager
    global openTerminal
    dockers = menu.addMenu("该 Docker 基础管理")
    openFileManager = QtWidgets.QAction("打开默认文件管理器")
    openTerminal = QtWidgets.QAction("打开默认终端")
    openFileManager.triggered.connect(lambda: threading.Thread(target=os.system, args=[f"xdg-open '{get_home()}'"]).start())
    openTerminal.triggered.connect(lambda: threading.Thread(target=os.system, args=[f"x-terminal-emulator"]).start())
    dockers.addAction(openFileManager)
    dockers.addAction(openTerminal)
newPackage = False
class GetVersionThread(QtCore.QThread):
    signal = QtCore.pyqtSignal(str)
    def __init__(self) -> None:
        super().__init__()

    def run(self):
        global about
        global window
        global newPackage
        global programVersionType
        # 目前分为几个版本（在 control 文件区分）：
        # 星火版本：~spark
        # 商店版本：~uos
        # 编译版本：无版本号
        # Gitee/Github……：正常版本
        # Docker 版本
        programVersionTypeLnk = {
            "spark": "普通版本",
            "uos": "普通版本"
        }
        # 直接判断是不是 Docker 版本
        if os.path.exists(f"{programPath}/docker.txt") or os.path.exists("/.dockerenv"):
            programVersionType = "普通版本"
            self.signal.emit("")
        else:
            programVersionType = "从源码运行的版本"
            try:
                if not os.path.exists("/var/lib/dpkg/status"):
                    print("无 dpkg，结束")
                file = open("/var/lib/dpkg/status", "r")
                fileName = file.read().splitlines()
                package = False
                for i in range(0, len(fileName)):
                    if fileName[i] == "Package: spark-deepin-wine-runner-docker":
                        programVersionType = "普通版本"
                        #AddDockerMenu()
                        self.signal.emit("")
                        break
                    if fileName[i] == "Package: spark-deepin-wine-runner-52":
                        programVersionType = "普通版本"
                        newPackage = False
                        break
                    if fileName[i] == "Package: spark-deepin-wine-runner":
                        package = True
                        newPackage = True
                        continue
                    if fileName[i] == "Package: wine-runner-linux":
                        package = True
                        continue
                    if not package:
                        continue
                    if fileName[i].replace(" ", "").replace("\n", "") == "":
                        # 空行，不再考虑
                        break
                    # 搜索版本号
                    try:
                        if fileName[i][:fileName[i].index(":")] == "Version":
                            version = fileName[i][fileName[i].index(":") + 1:].strip()
                            print(f"版本号为：{version}")
                            if not "-" in version:
                                programVersionType = "普通版本"
                                break
                            programVersionType = version[version.index("-") + 1:]
                            print(programVersionType)
                            if "-" in programVersionType:
                                # 考虑到如 2.1.0-2-spark 的情况
                                programVersionType = programVersionType[programVersionType.index("-") + 1:]
                            try:
                                programVersionType = programVersionTypeLnk[programVersionType]    
                            except:
                                programVersionType = "普通版本"
                            break
                    except:
                        traceback.print_exc()
                        continue
            except:
                print("无法读取，当没有处理")
        print(programVersionType)
        about = about.replace("@VersionForType@", programVersionType)
        # 获取程序体积
        about = about.replace("@programSize@", str(int(getFileFolderSize(programPath) / 1024 / 1024)))

def GetVersion():
    global runVersion
    runVersion = GetVersionThread()
    runVersion.signal.connect(AddDockerMenu)
    runVersion.start()

def UnPackage():
    QtWidgets.QMessageBox.information(window, "提示", "请在下面两个对话框中选择 deb 包所在路径和容器解压到的路径")
    debPath = QtWidgets.QFileDialog.getOpenFileName(window, get_home(), "deb 文件(*.deb);;所有文件(*.*)")
    if not debPath[1]:
        return
    path = QtWidgets.QFileDialog.getExistingDirectory(window, get_home())
    print(path)
    if not path:
        return
    tempDebDir = f"/tmp/wine-runner-unpack-deb-{random.randint(0, 1000)}"
    if os.system(f"dpkg -x '{debPath[0]}' '{tempDebDir}'"):
        QtWidgets.QMessageBox.critical(window, "错误", "解压失败！")
        return
    zippath = FindFile(tempDebDir, "files.7z")
    if zippath == None:
        QtWidgets.QMessageBox.critical(window, "错误", "解压失败！")
        return
    print(path)
    # 解压文件
    os.system(f"mkdir -p '{path}'")
    os.system(f"7z x -y '{zippath}' -o'{path}'")
    os.system(f"rm -rfv '{tempDebDir}'")
    QtWidgets.QMessageBox.information(window, "提示", "解压完成！")

def FindFile(file, name):
    for i in os.listdir(file):
        path = f"{file}/{i}"
        if os.path.isdir(path):
            returnPath = FindFile(path, name)
            if returnPath != None:
                return returnPath.replace("//", "/")
        if os.path.isfile(path):
            if i == name:
                return path
    return None

def TransLog():
    oldText = returnText.toPlainText()
    lineNumber = 0
    transText = ""
    chooseText = ""
    for i in oldText.splitlines():
        lineNumber += 1
        chooseText += f"{i}\n"
        if lineNumber >= 50:
            lineNumber = 0
            try:
                data = { 'doctype': 'json', 'type': 'auto','i': chooseText.replace("\n\n", "\n")}
                jsonReturn = requests.post("http://fanyi.youdao.com/translate", data=data).json()["translateResult"]
                for i in jsonReturn:
                    print(i)
                    transText += f'{i[0]["tgt"]}\n'
                chooseText = ""
            except:
                transText += f"{chooseText}\n"
                chooseText = ""
    if lineNumber != 0:
        lineNumber = 0
        try:
            data = { 'doctype': 'json', 'type': 'auto','i': chooseText.replace("\n\n", "\n")}
            jsonReturn = requests.post("http://fanyi.youdao.com/translate", data=data).json()["translateResult"]
            for i in jsonReturn:
                print(i[0])
                transText += f'{i[0]["tgt"]}\n'
            chooseText = ""
        except:
            transText += f"{chooseText}\n"
            chooseText = ""
    #return transText
    returnText.setText(transText.replace("\n\n", "\n"))

###########################
# 加载配置
###########################

if not os.path.exists(get_home() + "/.config/"):  # 如果没有配置文件夹
    os.mkdir(get_home() + "/.config/")  # 创建配置文件夹
if not os.path.exists(get_home() + "/.config/deepin-wine-runner"):  # 如果没有配置文件夹
    os.mkdir(get_home() + "/.config/deepin-wine-runner")  # 创建配置文件夹
if not os.path.exists(f"{get_home()}/.config/deepin-wine-runner/information"):  # 如果没有配置文件夹
    os.mkdir(f"{get_home()}/.config/deepin-wine-runner/information")  # 创建配置文件夹
if not os.path.exists(get_home() + "/.config/deepin-wine-runner/ShellHistory.json"):  # 如果没有配置文件
    write_txt(get_home() + "/.config/deepin-wine-runner/ShellHistory.json", json.dumps({}))  # 创建配置文件
if not os.path.exists(get_home() + "/.config/deepin-wine-runner/FindExeHistory.json"):  # 如果没有配置文件
    write_txt(get_home() + "/.config/deepin-wine-runner/FindExeHistory.json", json.dumps({}))  # 创建配置文件
if not os.path.exists(get_home() + "/.config/deepin-wine-runner/WineBottonHistory.json"):  # 如果没有配置文件
    write_txt(get_home() + "/.config/deepin-wine-runner/WineBottonHistory.json", json.dumps({}))  # 创建配置文件
if not os.path.exists(get_home() + "/.config/deepin-wine-runner/ISOPath.json"):  # 如果没有配置文件
    write_txt(get_home() + "/.config/deepin-wine-runner/ISOPath.json", json.dumps({}))  # 写入（创建）一个配置文件
if not os.path.exists(get_home() + "/.config/deepin-wine-runner/ISOPathFound.json"):  # 如果没有配置文件
    write_txt(get_home() + "/.config/deepin-wine-runner/ISOPathFound.json", json.dumps({}))  # 写入（创建）一个配置文件
if not os.path.exists(get_home() + "/.config/deepin-wine-runner/FindExe.json"):  # 如果没有配置文件
    write_txt(get_home() + "/.config/deepin-wine-runner/FindExe.json", json.dumps({"path": "~"}))  # 写入（创建）一个配置文件
if not os.path.exists(get_home() + "/.config/deepin-wine-runner/FindISO.json"):  # 如果没有配置文件
    write_txt(get_home() + "/.config/deepin-wine-runner/FindISO.json", json.dumps({"path": "~"}))  # 写入（创建）一个配置文件
if not os.path.exists(get_home() + "/.config/deepin-wine-runner/WineBotton.json"):  # 如果没有配置文件
    write_txt(get_home() + "/.config/deepin-wine-runner/WineBotton.json", json.dumps({"path": "~/.deepinwine"}))  # 写入（创建）一个配置文件
if not os.path.exists(get_home() + "/.config/deepin-wine-runner/WineSetting.json"):  # 如果没有配置文件
    write_txt(get_home() + "/.config/deepin-wine-runner/WineSetting.json", json.dumps(defultProgramList))  # 写入（创建）一个配置文件

###########################
# 设置变量
###########################
programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
# 如果要添加其他 wine，请使用安装更多 Wine 功能
#############
# 检测 Wine
#############
def CheckWine():
    global wine
    global untipsWine
    global canUseWine
    try:
        wine7zUse = ["wine", "wine64", "wine-i386", "wine-aarch64", "wine-x86_64"]
        wine = {
            "基于 UOS box86 的 deepin-wine6-stable": f"WINEPREDLL='{programPath}/dlls-arm' WINEDLLPATH=/opt/deepin-wine6-stable/lib BOX86_NOSIGSEGV=1 /opt/deepin-box86/box86 /opt/deepin-wine6-stable/bin/wine ",
            "基于 UOS exagear 的 deepin-wine6-stable": f"WINEPREDLL='{programPath}/dlls-arm' WINEDLLPATH=/opt/deepin-wine6-stable/lib /opt/exagear/bin/ubt_x64a64_al --path-prefix {get_home()}/.deepinwine/debian-buster --utmp-paths-list {get_home()}/.deepinwine/debian-buster/.exagear/utmp-list --vpaths-list {get_home()}/.deepinwine/debian-buster/.exagear/vpaths-list --opaths-list {get_home()}/.deepinwine/debian-buster/.exagear/opaths-list --smo-mode fbase --smo-severity smart --fd-limit 8192 --foreign-ubt-binary /opt/exagear/bin/ubt_x32a64_al -- /opt/deepin-wine6-stable/bin/wine ",
            "使用 Flatpak 安装的 Wine": "flatpak run org.winehq.Wine",
            "deepin-wine8-stable": "deepin-wine8-stable",
            "deepin-wine6 stable": "deepin-wine6-stable", 
            "deepin-wine6-vannila": "deepin-wine6-vannila",
            "deepin-wine5 stable": "deepin-wine5-stable", 
            "spark-wine": "spark-wine",
            "spark-wine7-devel": "spark-wine7-devel", 
            "spark-wine8": "spark-wine8",
            "spark-wine8-wow": "spark-wine8-wow",
            "spark-wine9": "spark-wine9",
            "spark-wine9-wow": "spark-wine9-wow",
            "deepin-wine": "deepin-wine", 
            "deepin-wine5": "deepin-wine5", 
            "wine": "wine", 
            "wine64": "wine64", 
            "ukylin-wine": "ukylin-wine",
            "okylin-wine": "okylin-wine",
            "mono（这不是 wine，但可以实现初步调用运行 .net 应用）": "mono",
            "基于 linglong 的 deepin-wine6-stable（不推荐）": f"ll-cli run '' --exec '/bin/deepin-wine6-stable'"
        }
        untipsWine = ["使用 Flatpak 安装的 Wine", "基于 exagear 的 deepin-wine6-stable", "基于 UOS box86 的 deepin-wine6-stable", "基于 UOS exagear 的 deepin-wine6-stable", "基于 linglong 的 deepin-wine6-stable（不推荐）"]
        canUseWine = []
        if os.path.exists("/opt/deepin-box86/box86") and os.path.exists("/opt/deepin-wine6-stable/bin/wine"):
            canUseWine.append("基于 UOS box86 的 deepin-wine6-stable")
        if os.path.exists("/opt/exagear/bin/ubt_x64a64_al") and os.path.exists("/opt/deepin-wine6-stable/bin/wine"):
            canUseWine.append("基于 UOS exagear 的 deepin-wine6-stable")
        #if not os.system("which exagear") and os.path.exists("/opt/deepin-wine6-stable/bin/wine"):
            #canUseWine.append("基于 exagear 的 deepin-wine6-stable")
        for i in wine.keys():
            if not os.system(f"which '{wine[i]}'"):
                canUseWine.append(i)
        if not os.system("which flatpak") and os.path.exists("/var/lib/flatpak/app/org.winehq.Wine"):
            canUseWine.append("使用 Flatpak 安装的 Wine")
            
        if os.path.exists("/persistent/linglong/layers/"):  # 判断是否使用 linglong
            for i in os.listdir("/persistent/linglong/layers/"):
                try:
                    dire = os.listdir(f"/persistent/linglong/layers/{i}")[-1]
                    arch = os.listdir(f"/persistent/linglong/layers/{i}/{dire}")[-1]
                    if os.path.exists(f"/persistent/linglong/layers/{i}/{dire}/{arch}/runtime/bin/deepin-wine6-stable"):
                        wine["基于 linglong 的 deepin-wine6-stable（不推荐）"] = f"ll-cli run {i} --exec '/bin/deepin-wine6-stable'"
                        canUseWine.append("基于 linglong 的 deepin-wine6-stable（不推荐）")
                        break
                except:
                    pass
        # 读取自定义安装的 Wine（需要解包的才能使用）
        global qemuBottleList
        global qemuPath
        qemuBottleList = []
        qemuPath = f"{get_home()}/.deepin-wine-runner-ubuntu-images"
        if not os.system("which qemu-i386-static"):
            if os.path.exists(qemuPath):
                for g in os.listdir(qemuPath):
                    archPath = f"{qemuPath}/{g}"
                    arch = g
                    if os.path.isdir(archPath):
                        for d in os.listdir(archPath):
                            bottlePath = f"{archPath}/{d}"
                            if os.path.isdir(bottlePath):
                                qemuBottleList.append([
                                    arch,
                                    d,
                                    bottlePath
                                ])

        global shellHistory
        global findExeHistory
        global wineBottonHistory
        global isoPath
        global isoPathFound
        global setting
        shellHistory = list(json.loads(readtxt(get_home() + "/.config/deepin-wine-runner/ShellHistory.json")).values())
        findExeHistory = list(json.loads(readtxt(get_home() + "/.config/deepin-wine-runner/FindExeHistory.json")).values())
        wineBottonHistory = list(json.loads(readtxt(get_home() + "/.config/deepin-wine-runner/WineBottonHistory.json")).values())
        isoPath = list(json.loads(readtxt(get_home() + "/.config/deepin-wine-runner/ISOPath.json")).values())
        isoPathFound = list(json.loads(readtxt(get_home() + "/.config/deepin-wine-runner/ISOPathFound.json")).values())
        setting = json.loads(readtxt(get_home() + "/.config/deepin-wine-runner/WineSetting.json"))
        change = False
        if not os.path.exists(get_home() + "/.config/deepin-wine-runner/mono-lock"):
            os.mknod(f"{get_home()}/.config/deepin-wine-runner/mono-lock")
            setting["MonoGeckoInstaller"] = False
            change = True
        for i in defultProgramList.keys():
            if not i in setting:
                change = True
                setting[i] = defultProgramList[i]
        if change:
            write_txt(get_home() + "/.config/deepin-wine-runner/WineSetting.json", json.dumps(setting))
        try:
            # Read /opt Wine
            try:
                for i in os.listdir(f"/opt"):
                    for j in wine7zUse:
                        if os.path.exists(f"/opt/{i}/bin/{j}"):
                            wine[f"/opt/{i}/bin/{j}"] = f"/opt/{i}/bin/{j}"
                            canUseWine.append(f"/opt/{i}/bin/{j}")
            except:
                traceback.print_exc()    

            # 不再从列表读取，直接读目录
            for i in os.listdir(f"{programPath}/wine/"):
            #for i in json.loads(readtxt(f"{programPath}/wine/winelist.json")):
                if os.path.exists(f"{programPath}/wine/{i}") and os.path.isdir(f"{programPath}/wine/{i}"):
                    name = ""
                    qemuInstall = False
                    nameValue = [["", ""]]
                    try:
                        if os.path.exists("/opt/deepin-box86/box86"):
                            nameValue.append(
                                [
                                    "基于 UOS box86 的 ", 
                                    f"WINEPREDLL='{programPath}/dlls-arm' WINEDLLPATH=/opt/deepin-wine6-stable/lib BOX86_NOSIGSEGV=1 /opt/deepin-box86/box86  "
                                ]
                                )
                        if os.system("which box86") == 0:
                            nameValue.append(
                                [
                                    "基于 box86 的 ",
                                    f"box86  "
                                ]
                            )
                        if os.system("which box64") == 0:
                            nameValue.append(
                                [
                                    "基于 box64 的 ",
                                    f"box64  "
                                ]
                            )
                        if os.system("which qemu-i386") == 0 and subprocess.getoutput("arch") != "x86_64" and subprocess.getoutput("arch") != "i386" and subprocess.getoutput("arch") != "i686":
                            nameValue.append(
                                [
                                    "基于 qemu-i386 的 ",
                                    f"qemu-i386  "
                                ]
                            )
                        if os.system("which qemu-x86_64") == 0 and subprocess.getoutput("arch") != "x86_64" and subprocess.getoutput("arch") != "i386" and subprocess.getoutput("arch") != "i686":
                            nameValue.append(
                                [
                                    "基于 qemu-x86_64 的 ",
                                    f"qemu-x86_64  "
                                ]
                            )
                        if os.path.exists("/opt/exagear/bin/ubt_x64a64_al") and os.path.exists(f"{get_home()}/.deepinwine/debian-buster"):
                            nameValue.append(
                                [
                                    "基于 UOS exagear 的 ",
                                    f"WINEPREDLL='{programPath}/dlls-arm' WINEDLLPATH=/opt/deepin-wine6-stable/lib /opt/exagear/bin/ubt_x64a64_al --path-prefix {get_home()}/.deepinwine/debian-buster --utmp-paths-list {get_home()}/.deepinwine/debian-buster/.exagear/utmp-list --vpaths-list {get_home()}/.deepinwine/debian-buster/.exagear/vpaths-list --opaths-list {get_home()}/.deepinwine/debian-buster/.exagear/opaths-list --smo-mode fbase --smo-severity smart --fd-limit 8192 --foreign-ubt-binary /opt/exagear/bin/ubt_x32a64_al --  "
                                ]
                            )
                        if os.system("which exagear") == 0:
                            nameValue.append(
                                [
                                    "运行 exagear 容器内的 ",
                                    f"exagear -- "
                                ]
                            )

                        if os.path.exists("/opt/exagear/bin/ubt_x64a64_al"):
                            nameValue.append(
                                [
                                    "使用 ubt_x64a64_al 运行",
                                    "/opt/exagear/bin/ubt_x64a64_al -- "
                                ]
                            )
                        
                        if os.path.exists("/opt/exagear/bin/ubt_x32a64_al"):
                            nameValue.append(
                                [
                                    "使用 ubt_x32a64_al 运行",
                                    "/opt/exagear/bin/ubt_x32a64_al -- "
                                ]
                            )
                        for g in qemuBottleList:
                            nameValue.append([
                                f"使用qemu-{g[0]}-static 调用容器{g[1]}运行 ",
                                f"python3 '{programPath}/QemuRun.py' '{g[0]}/{g[1]}' {int(setting['QemuUnMountHome'])} "
                            ])
                    except:
                        traceback.print_exc()
                    for k in nameValue:
                        print(k)
                        if "qemu" in k[0]:
                            chrootProgramPath = "/opt/apps/deepin-wine-runner"
                        else:
                            chrootProgramPath = programPath
                        for j in wine7zUse:
                            if os.path.exists(f"{programPath}/wine/{i}/bin/{j}"):        
                                wine[f"{k[0]}{chrootProgramPath}/wine/{i}/bin/{j}"] = f"{k[1]}{chrootProgramPath}/wine/{i}/bin/{j}"
                                canUseWine.append(f"{k[0]}{chrootProgramPath}/wine/{i}/bin/{j}")
                                untipsWine.append(f"{k[0]}{chrootProgramPath}/wine/{i}/bin/{j}")
            
        except:
            traceback.print_exc()
        try:
            for i in os.listdir(f"{get_home()}/.deepinwine/"):
                for j in wine7zUse:
                    if os.path.exists(f"{get_home()}/.deepinwine/{i}/bin/{j}"):
                        wine[f"{get_home()}/.deepinwine/{i}/bin/{j}"] = f"{get_home()}/.deepinwine/{i}/bin/{j}"
                        canUseWine.append(f"{get_home()}/.deepinwine/{i}/bin/{j}")
                
        except:
            traceback.print_exc()
        try:
            canUseWineOld = canUseWine[:]
            for i in canUseWineOld:
                if os.path.exists(f"{programPath}/WineLib/usr"):
                    wine[f"使用运行器的运行库运行 {i}"] = f"bash '{programPath}/WineLib/run.sh' {wine[i]}"
                    canUseWine.append(f"使用运行器的运行库运行 {i}")
                    untipsWine.append(f"使用运行器的运行库运行 {i}")
            if os.path.exists("/opt/exagear/images"):
                for k in os.listdir("/opt/exagear/images"):
                    if not os.path.isdir(f"/opt/exagear/images/{k}"):
                        continue
                    for i in canUseWineOld:
                        wine[f"使用Exagear容器运行库运行 {i}"] = f"bash '{programPath}/WineLib/run-more.sh' '/opt/exagear/images/{k}' {wine[i]}"
                        canUseWine.append(f"使用Exagear容器运行库运行 {i}")
                        untipsWine.append(f"使用Exagear容器运行库运行 {i}")
            #if os.path.exists(f"{get_home()}/.deepinwine/debian-buster"):
                #for i in canUseWineOld:
                    #wine[f"使用UOS Exagear容器运行库运行 {i}"] = f"bash '{programPath}/WineLib/run-more.sh' '{get_home()}/.deepinwine/debian-buster' {wine[i]}"
                    #canUseWine.append(f"使用UOS Exagear容器运行库运行 {i}")
                    #untipsWine.append(f"使用UOS Exagear容器运行库运行 {i}")
        except:
            traceback.print_exc()
    except:
        traceback.print_exc()
        app = QtWidgets.QApplication(sys.argv)
        QtWidgets.QMessageBox.critical(None, "错误", f"无法读取配置，无法继续\n{traceback.format_exc()}")
        sys.exit(1)
CheckWine()

# transla.transe

programVersionType = ""
print(wine)
###########################
# 程序信息
###########################
app = QtWidgets.QApplication(sys.argv)
trans = QtCore.QTranslator()
transeObject = QtCore.QObject()
transla = QtCore.QCoreApplication.translate
#transeObject.tr("")
# 语言载入
if not "zh_CN".lower() in get_now_lang().lower():
    trans.load(f"{programPath}/LANG/deepin-wine-runner-en_US.qm")
else:
    pass
app.installTranslator(trans)
iconPath = "{}/deepin-wine-runner.svg".format(programPath)
iconPathList = [
    "{}/deepin-wine-runner.svg".format(programPath),
]

#iconPath = "{}/Icon/Program/wine运行器.png".format(programPath)
programUrl = "https://gitee.com/gfdgd-xi/deep-wine-runner\nhttps://github.com/gfdgd-xi/deep-wine-runner\nhttps://gfdgd-xi.github.io"
information = json.loads(readtxt(f"{programPath}/information.json"))
version = information["Version"]
goodRunSystem = QtCore.QCoreApplication.translate("U", "常见 Linux 发行版")
thankText = ""
lastRunCommand = "暂未运行命令"
tips = QtCore.QCoreApplication.translate("U", '''<h4>提示：</h4>
1、使用终端运行该程序，可以看到 wine 以及程序本身的提示和报错；
2、wine 32 位和 64 位的容器互不兼容；
3、所有的 wine 和 winetricks 均需要自行安装（可以从 菜单栏=>程序 里面进行安装）；
4、本程序支持带参数运行 wine 程序（之前版本也可以），只需要按以下格式即可：
exe路径\' 参数 \'
即可（单引号需要输入）；
5、wine 容器如果没有指定，则会默认为 ~/.wine；
6、如果可执行文件比较大的话，会出现点击“获取该程序运行情况”出现假死的情况，因为正在后台读取 SHA1，只需要等一下即可（读取速度依照您电脑处理速度、读写速度、可执行文件大小等有关）；
7、如果非 X86 的用户的 UOS 专业版用户想要使用的话，只需要在应用商店安装一个 Wine 版本微信即可在本程序选择正确的 Wine 运行程序；''')
updateThingsString = QtCore.QCoreApplication.translate("U", '''※1、精简冗余组件
※2、修复 Wine 安装器在文件下载失败后无法自动关闭进度条和解除控件禁用的问题
※3、Wine 打包器不允许版本号开头输入首字母以及版本号不允许出现空格
※4、Wine 打包器生成的 deb 同时支持使用 spark-dwine-helper 和 deepin-wine-helper
※5、支持调用拓展 Qemu
※6、优化小屏幕使用体验''')
for i in information["Thank"]:
    thankText += f"{i}\n"
updateTime = "2024年06月29日"
aboutProgram = QtCore.QCoreApplication.translate("U", """<p>Wine运行器是一个能让Linux用户更加方便地运行Windows应用的程序。原版的 Wine 只能使用命令操作，且安装过程较为繁琐，对小白不友好。于是该运行器为了解决该痛点，内置了对Wine图形化的支持、Wine 安装器、微型应用商店、各种Wine工具、自制的Wine程序打包器、运行库安装工具等。</p>
<p>它同时还内置了基于Qemu/VirtualBox制作的、专供小白使用的Windows虚拟机安装工具，可以做到只需下载系统镜像并点击安装即可，无需考虑虚拟机的安装、创建、分区等操作，也能在非 X86 架构安装 X86 架构的 Windows 操作系统（但是效率较低，可以运行些老系统）。</p>
<p>而且对于部分 Wine 应用适配者来说，提供了图形化的打包工具，以及提供了一些常用工具以及运行库的安装方式，以及能安装多种不同的 Wine 以测试效果，能极大提升适配效率。</p>
<p>且对于 Deepin23 用户做了特别优化，以便能在缺少 i386 运行库的情况下运行 Wine32。同时也为非 X86 架构用户提供了 Box86/64、Qemu User 的安装方式</p>
<pre>""")
about = f'''<style>
a:link, a:active {{
    text-decoration: none;
}}
</style>
<h1>关于</h1>
{aboutProgram}

版本：{version}
适用平台：{goodRunSystem}（@VersionForType@）
安装包构建时间：{information['Time']}
Qt 版本：{QtCore.qVersion()}
程序官网：{programUrl}
<b>Wine 运行器 QQ 交流群：762985460</b>
<b>Wine运行器 QQ 频道：https://pd.qq.com/s/edqkgeydx</b>
当前程序占用体积：@programSize@MB</pre>
<p>本程序依照 GPLV3 协议开源</p>
<hr>
<h1>鸣谢名单</h1>
<pre>{thankText}</pre>
<hr>
<h1>更新内容</h1>
<pre>{updateThingsString}
<b>更新时间：{updateTime}</b></pre>
<hr>
<h1>提示</h1>
<pre>{tips}
</pre>
<hr>
<h1>友谊链接</h1>
<pre>星火应用商店：<a href="https://spark-app.store/">https://spark-app.store/</a>
Deepin 官网：<a href="https://www.deepin.org">https://www.deepin.org</a>
Deepin 论坛：<a href="https://bbs.deepin.org">https://bbs.deepin.org</a>
gfdgd xi：<a href="https://gfdgd-xi.github.io">https://gfdgd-xi.github.io</a>
<hr>
<h1>©2020~{time.strftime("%Y")} By gfdgd xi</h1>'''
defaultCommandText = "<pre>" + QtCore.QCoreApplication.translate("MainWindow", "在此可以看到wine安装应用时的终端输出内容") + """
=============================================================
如果解决了你的问题，请不要吝啬你的star哟！
也可以<a href='http://update.gfdgdxi.top/Appreciate'>请作者喝一杯茶</a>
程序地址：
<a href='https://gitee.com/gfdgd-xi/deep-wine-runner'>https://gitee.com/gfdgd-xi/deep-wine-runner</a>
<a href='https://github.com/gfdgd-xi/deep-wine-runner'>https://github.com/gfdgd-xi/deep-wine-runner</a>
<a href='https://sourceforge.net/projects/deep-wine-runner'>https://sourceforge.net/projects/deep-wine-runner</a>"""
# 创建线程用于获取是否有更新
class GetUpdateToShow(QtCore.QThread):
    signal = QtCore.pyqtSignal(str)
    def __init__(self):
        super().__init__()
    def run(self):
        global defaultCommandText
        # 获取更新
        url = "http://update.gfdgdxi.top/update.json"
        try:
            data = json.loads(requests.get(url).text)
            if data["Version"] != version:
                # 版本号读取（防止出现高版本号提示要“升级”到低版本号的问题）
                localVersionList = version.split(".")
                webVersionList = data['Version'].split(".")
                for i in range(len(localVersionList)):
                    local = int(localVersionList[i])
                    web = int(webVersionList[i])
                    if web < local:
                        break
                    if web > local:
                        defaultCommandText += f"""\n=============================================================
Wine运行器 {data['Version']} 发布了！<a href='http://update.gfdgdxi.top/update-wine-runner'>点此立即更新</a>"""
        except:
            traceback.print_exc()
        # 获取应用公告
        try:
            informationID = requests.get("http://update.gfdgdxi.top/wine-runner/info/id.json").json()["Number"]
            if not os.path.exists(f"{get_home()}/.config/deepin-wine-runner/information/{informationID}"):
                defaultCommandText += f"""\n=============================================================
程序有新的公告，<a href='http://update.gfdgdxi.top/information-wine-runner'>点此立即查看</a>"""
        except:
            traceback.print_exc()
        if lastRunCommand == "暂未运行命令":
            self.signal.emit(defaultCommandText + "</pre>")

offLineInformation = ""
if os.path.exists(f"{programPath}/off-line.lock"):
    title = "Wine 运行器 {}（离线模式）".format(version)
    try:
        offLineInformation = readtxt(f"{programPath}/off-line.lock")
    except:
        traceback.print_exc()
else:
    title = "Wine 运行器 {}".format(version)
#<h1>©2020~{time.strftime("%Y")} <a href="https://gitee.com/gfdgd-xi">By gfdgd xi</h1>'''
updateThings = "{} 更新内容：\n{}\n更新时间：{}".format(version, updateThingsString, updateTime, time.strftime("%Y"))
try:
    threading.Thread(target=requests.get, args=[parse.unquote(base64.b64decode("aHR0cDovLzEyMC4yNS4xNTMuMTQ0L3NwYXJrLWRlZXBpbi13aW5lLXJ1bm5lci9vcGVuL0luc3RhbGwucGhw").decode("utf-8")) + "?Version=" + version]).start()
except:
    pass
iconListUnBuild = json.loads(readtxt(f"{programPath}/IconList.json"))[0]
iconList = json.loads(readtxt(f"{programPath}/IconList.json"))[1]
for i in iconListUnBuild:
    iconList.append(i)
print(iconList)
# Qemu Lock
try:
    if os.path.exists("/tmp/deepin-wine-runner-lock.txt"):
        print("lock")
        with open(f"/tmp/deepin-wine-runner-lock.txt", "r") as file:
            setting["QemuUnMountHome"] = bool(int(file.read()))
    else:
        print("unlock")
        with open(f"/tmp/deepin-wine-runner-lock.txt", "w") as file:
            # = bool(int(file.read()))
            file.write(str(int(setting["QemuUnMountHome"])))
except:
    traceback.print_exc()

###########################
# 窗口创建
###########################
# 读取主题
# Qt 窗口
window = QtWidgets.QMainWindow()
defaultFont = app.font()
window.setWindowTitle(title)
widget = QtWidgets.QWidget()
window.setCentralWidget(widget)
mainLayout = QtWidgets.QGridLayout()
# 权重
size = QtWidgets.QSizePolicy()
size.setHorizontalPolicy(0)
widgetSize = QtWidgets.QSizePolicy()
#size.setHorizontalPolicy(0)
widgetSize.setVerticalPolicy(0)
#
leftUp = QtWidgets.QWidget()
mainLayout.addWidget(leftUp, 0, 0, 1, 1)
leftUpLayout = QtWidgets.QGridLayout()
leftUp.setLayout(leftUpLayout)
fastLabel = QtWidgets.QLabel(QtCore.QCoreApplication.translate("U", "快速启动"))
fastLabel.setStyleSheet("font: 30px;")
leftUpLayout.addWidget(fastLabel, 0, 0, 1, 2)
leftUpLayout.addWidget(QtWidgets.QLabel("<hr>"), 1, 0, 1, 2)
leftUpLayout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("U", "请选择容器路径：")), 2, 0, 1, 1)
e1 = QtWidgets.QComboBox()
e1.setEditable(True)
leftUpLayout.addWidget(e1, 3, 0, 1, 1)
button1 = QtWidgets.QPushButton("浏览")
button1.clicked.connect(liulanbutton)
leftUpLayout.addWidget(button1, 3, 1, 1, 1)
leftUpLayout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("U", "请选择要执行的程序（EXE、MSI或者命令）：")), 4, 0, 1, 1)
e2 = QtWidgets.QComboBox()
if setting["AutoPath"]:
    e2.editTextChanged.connect(ChangePath)
e2.setEditable(True)
leftUpLayout.addWidget(e2, 5, 0, 1, 1)
button2 = QtWidgets.QPushButton(QtCore.QCoreApplication.translate("U", "浏览"))
button2.clicked.connect(liulanexebutton)
leftUpLayout.addWidget(button2, 5, 1, 1, 1)
leftUpLayout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("U", "请选择WINE版本：")), 6, 0, 1, 1)
o1 = QtWidgets.QComboBox()
leftUpLayout.addWidget(o1, 7, 0, 1, 1)
# 设置空间权重
button1.setSizePolicy(size)
button2.setSizePolicy(size)


leftDown = QtWidgets.QWidget()
mainLayout.addWidget(leftDown, 1, 0, 1, 1)
leftDownLayout = QtWidgets.QVBoxLayout()
leftDown.setLayout(leftDownLayout)
highLabel = QtWidgets.QLabel(QtCore.QCoreApplication.translate("U", "高级功能"))
highLabel.setStyleSheet("font: 30px;")
leftDownLayout.addWidget(highLabel)
leftDownLayout.addWidget(QtWidgets.QLabel("<hr>"))
leftDownLayout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("U", "创建快捷方式（Desktop文件）：")))
createDesktopLink = QtWidgets.QHBoxLayout()
label_r_2 = QtWidgets.QLabel(QtCore.QCoreApplication.translate("U", "名称："))
createDesktopLink.addWidget(label_r_2)
combobox1 = QtWidgets.QComboBox()
combobox1.setEditable(True)
createDesktopLink.addWidget(combobox1)
button5 = QtWidgets.QPushButton(QtCore.QCoreApplication.translate("U", "创建到桌面"))
button5.clicked.connect(make_desktop_on_desktop)
createDesktopLink.addWidget(button5)
saveDesktopFileOnLauncher = QtWidgets.QPushButton(QtCore.QCoreApplication.translate("U", "创建到启动器"))
saveDesktopFileOnLauncher.clicked.connect(make_desktop_on_launcher)
createDesktopLink.addWidget(saveDesktopFileOnLauncher)
leftDownLayout.addLayout(createDesktopLink)
programManager = QtWidgets.QGridLayout()
leftDownLayout.addLayout(programManager)
programManager.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("U", "程序管理：")), 0, 0, 1, 1)
getProgramIcon = QtWidgets.QPushButton(QtCore.QCoreApplication.translate("U", "提取图标"))
getProgramIcon.clicked.connect(lambda: RunWineProgram(f"{programPath}/BeCyIconGrabber.exe' '{e2.currentText()}" if e2.currentText()[:2].upper() == "C:" else f"{programPath}/BeCyIconGrabber.exe' 'z:/{e2.currentText()}"))
programManager.addWidget(getProgramIcon, 1, 0, 1, 1)
programManager.addWidget(QtWidgets.QLabel(" "*5), 1, 1, 1, 1)
trasButton = QtWidgets.QPushButton(QtCore.QCoreApplication.translate("U", "窗口透明工具"))
trasButton.clicked.connect(lambda: RunWineProgram(f"{programPath}/窗体透明度设置工具.exe"))
programManager.addWidget(trasButton, 1, 2, 1, 1)
uninstallProgram = QtWidgets.QPushButton(QtCore.QCoreApplication.translate("U", "卸载程序"))
uninstallProgram.clicked.connect(lambda: RunWineProgram(f"{programPath}/geek.exe"))
programManager.addWidget(QtWidgets.QLabel(" "*5), 1, 3, 1, 1)
programManager.addWidget(uninstallProgram, 1, 4, 1, 1)
getLoseDll = QtWidgets.QPushButton(QtCore.QCoreApplication.translate("U", "简易dll检测工具"))
getLoseDll.clicked.connect(GetLoseDll)
programManager.addWidget(QtWidgets.QLabel(" "*5), 1, 5, 1, 1)
programManager.addWidget(getLoseDll, 1, 6, 1, 1)
programManager.addWidget(QtWidgets.QLabel(" "*5), 1, 7, 1, 1)
wineBottleReboot = QtWidgets.QPushButton(QtCore.QCoreApplication.translate("U", "重启指定Wine容器"))
wineBottleReboot.clicked.connect(lambda: RunWineProgram(f"wineboot' '-k"))
programManager.addWidget(wineBottleReboot, 1, 8, 1, 1)
programManager.addWidget(QtWidgets.QLabel(" "*5), 1, 9, 1, 1)
programManager.addItem(QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum), 1, 11, 1, 1)
programManager.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("U", "WINE配置：")), 2, 0, 1, 1)
wineConfig = QtWidgets.QPushButton(QtCore.QCoreApplication.translate("U", "配置容器"))
wineConfig.clicked.connect(lambda: RunWineProgram("winecfg"))
programManager.addWidget(wineConfig, 3, 0, 1, 1)
fontAppStore = QtWidgets.QPushButton(QtCore.QCoreApplication.translate("U", "字体商店"))
fontAppStore.clicked.connect(FontAppStore)
programManager.addWidget(fontAppStore, 3, 2, 1, 1)
button_r_6 = QtWidgets.QPushButton(QtCore.QCoreApplication.translate("U", "RegShot"))
button_r_6.clicked.connect(lambda: RunWineProgram(f"{programPath}/RegShot/regshot.exe"))
programManager.addWidget(button_r_6, 3, 4, 1, 1)
sparkWineSetting = QtWidgets.QPushButton(QtCore.QCoreApplication.translate("U", "星火wine配置"))
sparkWineSetting.clicked.connect(lambda: threading.Thread(target=os.system, args=["bash /opt/apps/store.spark-app.spark-dwine-helper/files/deepinwine/tools/spark-dwine-helper/wine-app-launcher/wine-app-launcher.sh"]).start())
programManager.addWidget(sparkWineSetting, 3, 6, 1, 1)
wineAutoConfig = QtWidgets.QPushButton(QtCore.QCoreApplication.translate("U", "Wine容器自动配置工具"))
wineAutoConfig.clicked.connect(WineBottonAutoConfig)
programManager.addWidget(wineAutoConfig, 3, 8, 1, 1)

# 权重
button5.setSizePolicy(size)
saveDesktopFileOnLauncher.setSizePolicy(size)
label_r_2.setSizePolicy(size)
getProgramIcon.setSizePolicy(size)
#trasButton.setSizePolicy(size)
button_r_6.setSizePolicy(size)
wineConfig.setSizePolicy(size)

returnText = QtWidgets.QTextBrowser()
getUpdate = GetUpdateToShow()
getUpdate.signal.connect(returnText.setHtml)
getUpdate.start()
def ReturnTextOpenUrl(url):
    print(url)
    if url.url() == "http://update.gfdgdxi.top/update-wine-runner":
        UpdateWindow.ShowWindow()
    elif url.url() == "http://update.gfdgdxi.top/information-wine-runner":
        GetNewInformation()
    elif url.url() == "http://update.gfdgdxi.top/Appreciate":
        Appreciate()
    else:
        webbrowser.open_new_tab(url.url())
returnText.anchorClicked.connect(ReturnTextOpenUrl)
returnText.setOpenExternalLinks(False)
returnText.setOpenLinks(False)
returnText.setStyleSheet("""
background-color: black;
color: white;
""")
returnText.setHtml(QtCore.QCoreApplication.translate("U", defaultCommandText) + "</pre>")
mainLayout.setRowStretch(0, 2)
mainLayout.setRowStretch(1, 1)
mainLayout.setColumnStretch(0, 2)
mainLayout.setColumnStretch(1, 1)
mainLayout.addWidget(returnText, 0, 1, 2, 1)

window.setStyleSheet("""word-wrap: break-word;""")

# 版权
if offLineInformation.replace("\n", "").replace(" ", "") == "":
    copy = QtWidgets.QLabel(f"""程序版本：{version}，<b>提示：Wine 无法保证可以运行所有的 Windows 程序，如果想要运行更多 Windows 程序，可以考虑虚拟机和双系统</b><br/>
<b>注：部分二进制兼容层会自动注册 binfmt（如原版的 Box86/64、Qemu User Static），则意味着无需在 Wine 版本那里特别指定兼容层，直接指定 Wine 即可</b><br/>
©2020~{time.strftime("%Y")} gfdgd xi""")
else:
    copy = QtWidgets.QLabel(f"""程序版本：{version}，<b>提示：Wine 无法保证可以运行所有的 Windows 程序，如果想要运行更多 Windows 程序，可以考虑虚拟机和双系统</b><br/>
<b>注：部分二进制兼容层会自动注册 binfmt（如原版的 Box86/64、Qemu User Static），则意味着无需在 Wine 版本那里特别指定兼容层，直接指定 Wine 即可</b><br/>
{offLineInformation}<br/>
©2020~{time.strftime("%Y")} gfdgd xi""")
copy.setWordWrap(True)
mainLayout.addWidget(copy, 2, 0, 1, 1)

# 程序运行
programRun = QtWidgets.QWidget()
programRunLayout = QtWidgets.QHBoxLayout()
programRun.setLayout(programRunLayout)
programRunLayout.addItem(QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
button3 = QtWidgets.QPushButton(QtCore.QCoreApplication.translate("U", "运行程序"))
button3.clicked.connect(runexebutton)
programRunLayout.addWidget(button3)
killProgram = QtWidgets.QPushButton(QtCore.QCoreApplication.translate("U", "终止程序"))
killProgram.clicked.connect(KillProgram)
programRunLayout.addWidget(killProgram)
killBottonProgram = QtWidgets.QPushButton(QtCore.QCoreApplication.translate("U", "终止指定容器的程序"))
killBottonProgram.clicked.connect(lambda: threading.Thread(target=os.system, args=[f"'{programPath}/kill.sh' '{os.path.basename(e1.currentText())}'"]).start())
programRunLayout.addWidget(killBottonProgram)
mainLayout.addWidget(programRun, 2, 1, 1, 1)

# 菜单栏
menu = window.menuBar()
programmenu = menu.addMenu(QtCore.QCoreApplication.translate("U", "程序(&P)"))
p1 = QtWidgets.QAction(QtGui.QIcon(f"{programPath}/Icon/Function/wine.png"), QtCore.QCoreApplication.translate("U", "安装 wine(&I)"))
#installWineOnDeepin23 = QtWidgets.QAction(QtGui.QIcon(f"{programPath}/Icon/Function/wine23P.png"), QtCore.QCoreApplication.translate("U", "安装 wine(只限Deepin23 Preview)"))
#installWineOnDeepin23Alpha = QtWidgets.QAction(QtGui.QIcon(f"{programPath}/Icon/Function/wine23A.png"), QtCore.QCoreApplication.translate("U", "安装 wine(只限Deepin23 Alpha)"))
installWineHQOrg = QtWidgets.QAction(QtGui.QIcon(f"{programPath}/Icon/Function/wine.png"), QtCore.QCoreApplication.translate("U", "安装 WineHQ（官方源）"))
installWineHQ = QtWidgets.QAction(QtGui.QIcon(f"{programPath}/Icon/Function/wine.png"), QtCore.QCoreApplication.translate("U", "安装 WineHQ（国内清华大学镜像源）"))
installMoreWine = QtWidgets.QAction(QtGui.QIcon(f"{programPath}/Icon/Function/more-wine.png"), QtCore.QCoreApplication.translate("U", "安装更多 Wine（Wine 下载工具，推荐）"))
downloadChrootBottle = QtWidgets.QAction(QtGui.QIcon(f"{programPath}/Icon/Function/CHROOT.png"), QtCore.QCoreApplication.translate("U", "下载 Chroot 容器"))
installBox86CN = QtWidgets.QAction(QtGui.QIcon.fromTheme("box"), QtCore.QCoreApplication.translate("U", "安装 Box86/Box64 日构建（国内源）"))
installBox86 = QtWidgets.QAction(QtGui.QIcon.fromTheme("box"), QtCore.QCoreApplication.translate("U", "安装 Box86/Box64 日构建（国外 Github 源）"))
installBox86Own = QtWidgets.QAction(QtGui.QIcon.fromTheme("box"), QtCore.QCoreApplication.translate("U", "安装 Box86/Box64（使用自建源，支持 riscv64）"))
installLat = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "安装 lat（只限 Loongarch64 架构）"))
p2 = QtWidgets.QAction(QtGui.QIcon.fromTheme("settings"), QtCore.QCoreApplication.translate("U", "设置程序(&S)"))
enabledAll = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "强制启用所有被禁用的组件（不推荐）"))
setMiniFont = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "临时设置小字体"))
setTinyFont = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "临时设置很小的字体"))
setDefaultFont = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "临时设置默认字体"))
p3 = QtWidgets.QAction(QtWidgets.QApplication.style().standardIcon(47), QtCore.QCoreApplication.translate("U", "清空软件历史记录(&C)"))
cleanCache = QtWidgets.QAction(QtWidgets.QApplication.style().standardIcon(47), QtCore.QCoreApplication.translate("U", "清空软件缓存"))
p4 = QtWidgets.QAction(QtGui.QIcon.fromTheme("exit"), QtCore.QCoreApplication.translate("U", "退出程序(&E)"))
programmenu.addAction(p1)
programmenu.addAction(installWineHQ)
programmenu.addAction(installWineHQOrg)
programmenu.addAction(installMoreWine)
programmenu.addAction(downloadChrootBottle)
programmenu.addAction(installBox86CN)
programmenu.addAction(installBox86)
programmenu.addAction(installBox86Own)
programmenu.addAction(installLat)
programmenu.addSeparator()
programmenu.addAction(p2)
programmenu.addAction(enabledAll)
programmenu.addSeparator()
programmenu.addAction(p3)
programmenu.addAction(cleanCache)
programmenu.addSeparator()
programmenu.addAction(p4)
setDefaultFont.triggered.connect(lambda: SetFont(1))
setMiniFont.triggered.connect(lambda: SetFont(1.2))
setTinyFont.triggered.connect(lambda: SetFont(1.6))
p1.triggered.connect(InstallWine)
#installWineOnDeepin23.triggered.connect(InstallWineOnDeepin23)
#installWineOnDeepin23Alpha.triggered.connect(InstallWineOnDeepin23Alpha)
installWineHQ.triggered.connect(InstallWineHQ)
installWineHQOrg.triggered.connect(lambda: threading.Thread(target=OpenTerminal, args=[f"{programPath}/InstallNewWineHQOrg.sh"]).start())
installLat.triggered.connect(lambda: threading.Thread(target=OpenTerminal, args=[f"{programPath}/InstallLat.sh"]).start())
def InstallMoreWine():
    os.system(f"'{programPath}/wine/installwine'")
    # 更新 Wine 列表
    CheckWine()
    o1.clear()
    if setting["AutoWine"]:
        o1.addItems(canUseWine)
    else:
        o1.addItems(wine.keys())
#installMoreWine.triggered.connect(lambda: threading.Thread(target=os.system, args=[f"'{programPath}/wine/installwine'"]).start())
installMoreWine.triggered.connect(InstallMoreWine)
downloadChrootBottle.triggered.connect(lambda: threading.Thread(target=os.system, args=[f"'{programPath}/QemuDownload.py'"]).start())
p2.triggered.connect(ProgramSetting.ShowWindow)
enabledAll.triggered.connect(lambda: DisableButton(False))
installBox86CN.triggered.connect(lambda: OpenTerminal(f"sudo bash '{programPath}/InstallBox86-cn.sh'"))
installBox86.triggered.connect(lambda: OpenTerminal(f"sudo bash '{programPath}/InstallBox86.sh'"))
installBox86Own.triggered.connect(lambda: OpenTerminal(f"sudo bash '{programPath}/InstallBox86-own.sh'"))
p3.triggered.connect(CleanProgramHistory)
cleanCache.triggered.connect(CleanProgramCache)
p4.triggered.connect(window.close)

wineOption = menu.addMenu(QtCore.QCoreApplication.translate("U", "Wine(&W)"))
w1 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "打开 Wine 容器目录"))
w2 = QtWidgets.QAction(QtGui.QIcon.fromTheme("font"), QtCore.QCoreApplication.translate("U", "安装常见字体"))
w3 = QtWidgets.QAction(QtGui.QIcon.fromTheme("font"), QtCore.QCoreApplication.translate("U", "安装自定义字体"))
w4 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "删除选择的 Wine 容器"))
cleanBottonUOS = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "清理 Wine 容器（基于 Wine 适配活动脚本）"))
wineKeyboardLnk = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "Wine 快捷键映射"))
w5 = QtWidgets.QAction(QtGui.QIcon.fromTheme("deb"), QtCore.QCoreApplication.translate("U", "打包 wine 应用（专业用户使用）"))
w6 = QtWidgets.QAction(QtGui.QIcon.fromTheme("deb"), QtCore.QCoreApplication.translate("U", "使用官方 Wine 适配活动的脚本进行打包"))
easyPackager = QtWidgets.QAction(QtGui.QIcon.fromTheme("deb"), QtCore.QCoreApplication.translate("U", "使用简易打包器进行打包（小白且无特殊需求建议使用这个）"))
getDllOnInternet = QtWidgets.QAction(QtGui.QIcon.fromTheme("1CD8_rundll32.0"), QtCore.QCoreApplication.translate("U", "从互联网获取DLL"))
w7 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "从镜像获取DLL（只支持官方安装镜像，DOS内核如 Windows 95 暂不支持）"))
updateGeek = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "从 Geek Uninstaller 官网升级程序"))
deletePartIcon = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "快捷方式管理工具"))
deleteDesktopIcon = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "删除所有 Wine 程序在启动器的快捷方式"))
wineOption.addAction(w1)
wineOption.addAction(w2)
wineOption.addAction(w3)
wineOption.addAction(w4)
wineOption.addAction(cleanBottonUOS)
wineOption.addSeparator()
wineOption.addAction(w5)
wineOption.addAction(w6)
wineOption.addAction(easyPackager)
wineOption.addAction(deletePartIcon)
wineOption.addSeparator()
wineOption.addAction(wineKeyboardLnk)
wineOption.addSeparator()
wineOption.addAction(getDllOnInternet)
wineOption.addAction(w7)
wineOption.addSeparator()
wineOption.addAction(updateGeek)
wineOption.addSeparator()
wm1 = wineOption.addMenu(QtCore.QCoreApplication.translate("U", "在指定 Wine、容器安装组件"))
wm1_1 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "在指定wine、指定容器安装 .net framework"))
wm1_2 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "在指定wine、指定容器安装 Visual Studio C++"))
wm1_8 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "在指定wine、指定容器安装 Visual FoxPro"))
wm1_3 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "在指定wine、指定容器安装 MSXML"))
wm1_4 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "在指定wine、指定容器安装 gecko"))
wm1_5 = QtWidgets.QAction(QtGui.QIcon.fromTheme("mono"), QtCore.QCoreApplication.translate("U", "在指定wine、指定容器安装 mono"))
wm1_7 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "在指定wine、指定容器安装 Visual Basic Runtime"))
wm1_6 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "在指定wine、指定容器安装其它运行库"))
wm1.addAction(wm1_1)
wm1.addAction(wm1_2)
wm1.addAction(wm1_8)
wm1.addAction(wm1_3)
wm1.addAction(wm1_4)
wm1.addAction(wm1_5)
wm1.addAction(wm1_7)
wm1.addAction(wm1_6)
wm2 = wineOption.addMenu(QtCore.QCoreApplication.translate("U", "在指定 Wine、容器运行基础应用"))
wm2_1 = QtWidgets.QAction(QtGui.QIcon.fromTheme("control-center2"), QtCore.QCoreApplication.translate("U", "打开指定wine、指定容器的控制面板"))
wm2_2 = QtWidgets.QAction(QtGui.QIcon.fromTheme("web-browser"), QtCore.QCoreApplication.translate("U", "打开指定wine、指定容器的浏览器"))
wm2_3 = QtWidgets.QAction(QtGui.QIcon.fromTheme("regedit"), QtCore.QCoreApplication.translate("U", "打开指定wine、指定容器的注册表"))
wm2_4 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "打开指定wine、指定容器的任务管理器"))
wm2_5 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "打开指定wine、指定容器的资源管理器"))
wm2_6 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "打开指定wine、指定容器的关于 wine"))
wm2.addAction(wm2_1)
wm2.addAction(wm2_2)
wm2.addAction(wm2_3)
wm2.addAction(wm2_4)
wm2.addAction(wm2_5)
wm2.addAction(wm2_6)
wineOption.addSeparator()
settingRunV3Sh = wineOption.addMenu(QtCore.QCoreApplication.translate("U", "run_v3.sh 管理"))
w8 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "设置 run_v3.sh 的文管为 Deepin 默认文管"))
w9 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "设置 run_v3.sh 的文管为 Wine 默认文管"))
w10 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "重新安装 deepin-wine-helper"))
w11 = QtWidgets.QAction(QtGui.QIcon.fromTheme("winetricks"), QtCore.QCoreApplication.translate("U", "使用winetricks打开指定容器"))
w11WithWineLib = QtWidgets.QAction(QtGui.QIcon.fromTheme("winetricks"), QtCore.QCoreApplication.translate("U", "使用winetricks打开指定容器（使用Wine运行器运行库）"))
w11WithWineLib.setDisabled(True)
settingRunV3Sh.addAction(w8)
settingRunV3Sh.addAction(w9)
settingRunV3Sh.addAction(w10)
wineOption.addSeparator()
wineOption.addAction(w11)
#wineOption.addAction(w11WithWineLib)
wineOption.addSeparator()
optionCheckDemo = wineOption.addMenu(QtCore.QCoreApplication.translate("U", "组件功能测试"))
vbDemo = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "测试 Visual Basic 6 程序"))
netDemo = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "测试 .net framework 程序"))
netIEDemo = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "测试 .net framework + Internet Explorer 程序"))
optionCheckDemo.addAction(vbDemo)
optionCheckDemo.addAction(netDemo)
optionCheckDemo.addAction(netIEDemo)
wineOption.addSeparator()
wm3 = wineOption.addMenu(QtCore.QCoreApplication.translate("U", "启用/禁用功能"))
ed1 = wm3.addMenu(QtCore.QCoreApplication.translate("U", "启用/禁用 opengl"))
wm3_1 = QtWidgets.QAction(QtWidgets.QApplication.style().standardIcon(45), QtCore.QCoreApplication.translate("U", "开启 opengl"))
wm3_2 = QtWidgets.QAction(QtWidgets.QApplication.style().standardIcon(40), QtCore.QCoreApplication.translate("U", "禁用 opengl"))
ed1.addAction(wm3_1)
ed1.addAction(wm3_2)
ed2 = wm3.addMenu(QtCore.QCoreApplication.translate("U", "安装/卸载 winbind"))
wm4_1 = QtWidgets.QAction(QtWidgets.QApplication.style().standardIcon(45), QtCore.QCoreApplication.translate("U", "安装 winbind"))
wm4_2 = QtWidgets.QAction(QtWidgets.QApplication.style().standardIcon(40), QtCore.QCoreApplication.translate("U", "卸载 winbind"))
ed2.addAction(wm4_1)
ed2.addAction(wm4_2)
dxvkMenu = wm3.addMenu(QtCore.QCoreApplication.translate("U", "安装/卸载 DXVK"))
installDxvk = QtWidgets.QAction(QtWidgets.QApplication.style().standardIcon(45), QtCore.QCoreApplication.translate("U", "安装 DXVK"))
uninstallDxvk = QtWidgets.QAction(QtWidgets.QApplication.style().standardIcon(40), QtCore.QCoreApplication.translate("U", "卸载 DXVK"))
dxvkMenu.addAction(installDxvk)
dxvkMenu.addAction(uninstallDxvk)
vkd3dMenu = wm3.addMenu(QtCore.QCoreApplication.translate("U", "安装/卸载 Vkd3d"))
installvkd3d = QtWidgets.QAction(QtWidgets.QApplication.style().standardIcon(45), QtCore.QCoreApplication.translate("U", "安装 Vkd3d"))
uninstallvkd3d = QtWidgets.QAction(QtWidgets.QApplication.style().standardIcon(40), QtCore.QCoreApplication.translate("U", "卸载 Vkd3d"))
vkd3dMenu.addAction(installvkd3d)
vkd3dMenu.addAction(uninstallvkd3d)
wineOption.addSeparator()
wineOption.addAction(deleteDesktopIcon)
wineOption.addSeparator()
settingWineBottleCreateLink = wm3.addMenu(QtCore.QCoreApplication.translate("U", "启用/禁止指定 wine 容器生成快捷方式"))
enabledWineBottleCreateLink = QtWidgets.QAction(QtWidgets.QApplication.style().standardIcon(45), QtCore.QCoreApplication.translate("U", "允许指定 wine 容器生成快捷方式"))
disbledWineBottleCreateLink = QtWidgets.QAction(QtWidgets.QApplication.style().standardIcon(40), QtCore.QCoreApplication.translate("U", "禁止指定 wine 容器生成快捷方式"))
settingWineBottleCreateLink.addAction(enabledWineBottleCreateLink)
settingWineBottleCreateLink.addAction(disbledWineBottleCreateLink)
settingWineCrashDialog = wm3.addMenu(QtCore.QCoreApplication.translate("U", "启用/禁用指定 wine 容器崩溃提示窗口"))
disbledWineCrashDialog = QtWidgets.QAction(QtWidgets.QApplication.style().standardIcon(40), QtCore.QCoreApplication.translate("U", "禁用指定 wine 容器崩溃提示窗口"))
enabledWineCrashDialog = QtWidgets.QAction(QtWidgets.QApplication.style().standardIcon(45), QtCore.QCoreApplication.translate("U", "启用指定 wine 容器崩溃提示窗口"))
settingWineCrashDialog.addAction(enabledWineCrashDialog)
settingWineCrashDialog.addAction(disbledWineCrashDialog)
settingOpenProgram = wm3.addMenu(QtCore.QCoreApplication.translate("U", "启用/禁止指定 wine 容器创建文件关联"))
enabledOpenProgram = QtWidgets.QAction(QtWidgets.QApplication.style().standardIcon(45), QtCore.QCoreApplication.translate("U", "允许指定 wine 容器创建文件关联"))
disbledOpenProgram = QtWidgets.QAction(QtWidgets.QApplication.style().standardIcon(40), QtCore.QCoreApplication.translate("U", "禁止指定 wine 容器创建文件关联"))
settingOpenProgram.addAction(enabledOpenProgram)
settingOpenProgram.addAction(disbledOpenProgram)
settingHttpProxy = wineOption.addMenu(QtCore.QCoreApplication.translate("U", "设置指定 Wine 容器代理"))
enabledHttpProxy = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "设置指定 wine 容器的代理"))
disbledHttpProxy = QtWidgets.QAction(QtWidgets.QApplication.style().standardIcon(40), QtCore.QCoreApplication.translate("U", "禁用指定 wine 容器的代理"))
settingHttpProxy.addAction(enabledHttpProxy)
settingHttpProxy.addAction(disbledHttpProxy)
dllOver = wineOption.addMenu(QtCore.QCoreApplication.translate("U", "函数顶替库列表"))
saveDllOver = QtWidgets.QAction(QtWidgets.QApplication.style().standardIcon(43), QtCore.QCoreApplication.translate("U", "导出函数顶替列表"))
addDllOver = QtWidgets.QAction(QtWidgets.QApplication.style().standardIcon(32), QtCore.QCoreApplication.translate("U", "导入函数顶替列表"))
editDllOver = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "编辑函数顶替库列表"))
dllOver.addAction(saveDllOver)
dllOver.addAction(addDllOver)
dllOver.addAction(editDllOver)
w1.triggered.connect(OpenWineBotton)
w2.triggered.connect(InstallWineFont)
w3.triggered.connect(OpenWineFontPath)
w4.triggered.connect(DeleteWineBotton)
cleanBottonUOS.triggered.connect(CleanWineBottonByUOS)
w5.triggered.connect(BuildExeDeb)
w6.triggered.connect(UOSPackageScript)
easyPackager.triggered.connect(lambda: threading.Thread(target=os.system, args=[f"'{programPath}/deepin-wine-easy-packager.py' '{e2.currentText()}'"]).start())
wineKeyboardLnk.triggered.connect(lambda: threading.Thread(target=os.system, args=[f"'{programPath}/key/key-add-gui.py'"]).start())
getDllOnInternet.triggered.connect(GetDllFromInternet)
w7.triggered.connect(GetDllFromWindowsISO.ShowWindow)
updateGeek.triggered.connect(lambda: os.system(f"'{programPath}/launch.sh' deepin-terminal -C '\"{programPath}/UpdateGeek.sh\"' --keep-open"))
w8.triggered.connect(SetDeepinFileDialogDeepin)
w9.triggered.connect(SetDeepinFileDialogDefult)
w10.triggered.connect(SetDeepinFileDialogRecovery)
w11.triggered.connect(lambda: RunWinetricks())
w11WithWineLib.triggered.connect(lambda: RunWinetricksWithWineLib())
wm1_1.triggered.connect(lambda: threading.Thread(target=InstallNetFramework).start())
wm1_2.triggered.connect(lambda: threading.Thread(target=InstallVisualStudioCPlusPlus).start())
wm1_8.triggered.connect(lambda: threading.Thread(target=InstallFoxPro).start())
wm1_3.triggered.connect(lambda: threading.Thread(target=InstallMSXML).start())
wm1_4.triggered.connect(lambda: threading.Thread(target=InstallMonoGecko, args=["gecko"]).start())
wm1_5.triggered.connect(lambda: threading.Thread(target=InstallMonoGecko, args=["mono"]).start())
wm1_7.triggered.connect(lambda: threading.Thread(target=InstallVB).start())
wm1_6.triggered.connect(lambda: threading.Thread(target=InstallOther).start())
wm2_1.triggered.connect(lambda: RunWineProgram("control"))
wm2_2.triggered.connect(lambda: RunWineProgram("iexplore' 'https://gfdgd-xi.github.io"))
wm2_3.triggered.connect(lambda: RunWineProgram("regedit"))
wm2_4.triggered.connect(lambda: RunWineProgram("taskmgr"))
wm2_5.triggered.connect(lambda: RunWineProgram("explorer"))
wm2_6.triggered.connect(lambda: RunWineProgram("winver"))
wm3_1.triggered.connect(lambda: RunWineProgram(f"regedit.exe' /s '{programPath}/EnabledOpengl.reg"))
wm3_2.triggered.connect(lambda: RunWineProgram(f"regedit.exe' /s '{programPath}/DisabledOpengl.reg"))
wm4_1.triggered.connect(lambda: os.system(f"'{programPath}/launch.sh' deepin-terminal -C 'pkexec apt install winbind -y' --keep-open"))
wm4_2.triggered.connect(lambda: os.system(f"'{programPath}/launch.sh' deepin-terminal -C 'pkexec apt purge winbind -y' --keep-open"))
installDxvk.triggered.connect(InstallDXVK)
uninstallDxvk.triggered.connect(UninstallDXVK)
installvkd3d.triggered.connect(InstallVkd3d)
uninstallvkd3d.triggered.connect(UninstallVkd3d)
deletePartIcon.triggered.connect(lambda: threading.Thread(target=os.system, args=[f"python3 '{programPath}/BuildDesktop.py'"]).start())
deleteDesktopIcon.triggered.connect(DeleteDesktopIcon)
enabledWineBottleCreateLink.triggered.connect(lambda: RunWineProgram("reg' delete 'HKEY_CURRENT_USER\Software\Wine\DllOverrides' /v winemenubuilder.exe '/f"))
disbledWineBottleCreateLink.triggered.connect(lambda: RunWineProgram("reg' add 'HKEY_CURRENT_USER\Software\Wine\DllOverrides' /v winemenubuilder.exe '/f"))
disbledWineCrashDialog.triggered.connect(lambda: RunWineProgram("reg' add 'HKEY_CURRENT_USER\Software\Wine\WineDbg' /v ShowCrashDialog /t REG_DWORD /d 00000000 '/f"))
enabledWineCrashDialog.triggered.connect(lambda: RunWineProgram("reg' add 'HKEY_CURRENT_USER\Software\Wine\WineDbg' /v ShowCrashDialog /t REG_DWORD /d 00000001 '/f"))
disbledOpenProgram.triggered.connect(lambda: RunWineProgram("reg' add 'HKEY_CURRENT_USER\Software\Wine\FileOpenAssociations' /v Enable /d N '/f"))
enabledOpenProgram.triggered.connect(lambda: RunWineProgram("reg' add 'HKEY_CURRENT_USER\Software\Wine\FileOpenAssociations' /v Enable /d Y '/f"))
enabledHttpProxy.triggered.connect(SetHttpProxy)
disbledHttpProxy.triggered.connect(DisbledHttpProxy)
saveDllOver.triggered.connect(SaveDllList)
addDllOver.triggered.connect(AddReg)
editDllOver.triggered.connect(lambda: RunWineProgram("winecfg"))
vbDemo.triggered.connect(lambda: RunWineProgram(f"{programPath}/Test/vb.exe"))
netDemo.triggered.connect(lambda: RunWineProgram(f"{programPath}/Test/net.exe"))
netIEDemo.triggered.connect(lambda: RunWineProgram(f"{programPath}/Test/netandie.exe"))

virtualMachine = menu.addMenu(QtCore.QCoreApplication.translate("U", "虚拟机(&V)"))
v1 = QtWidgets.QAction(QtGui.QIcon.fromTheme("virtualbox"), QtCore.QCoreApplication.translate("U", "使用虚拟机运行 Windows 应用"))
virtualMachine.addAction(v1)
v1.triggered.connect(RunVM)

checkValue = menu.addMenu(QtCore.QCoreApplication.translate("U", "校验值计算(&S)"))
md5Value = QtWidgets.QAction(QtWidgets.QApplication.style().standardIcon(32), QtCore.QCoreApplication.translate("U", "MD5(&M)"))
sha1Value = QtWidgets.QAction(QtWidgets.QApplication.style().standardIcon(32), QtCore.QCoreApplication.translate("U", "SHA1(&M)"))
base64Value = QtWidgets.QAction(QtWidgets.QApplication.style().standardIcon(32), QtCore.QCoreApplication.translate("U", "Base64(建议小文件)(&B)"))
sha256Value = QtWidgets.QAction(QtWidgets.QApplication.style().standardIcon(32), QtCore.QCoreApplication.translate("U", "SHA256(&S)"))
sha512Value = QtWidgets.QAction(QtWidgets.QApplication.style().standardIcon(32), QtCore.QCoreApplication.translate("U", "SHA512(&S)"))
md5Value.triggered.connect(lambda: ValueCheck().Get("MD5"))
sha1Value.triggered.connect(lambda: ValueCheck().Get("SHA1"))
base64Value.triggered.connect(lambda: ValueCheck().Get("BASE64"))
sha256Value.triggered.connect(lambda: ValueCheck().Get("SHA256"))
sha512Value.triggered.connect(lambda: ValueCheck().Get("SHA512"))
checkValue.addAction(md5Value)
checkValue.addAction(sha1Value)
checkValue.addAction(base64Value)
checkValue.addAction(sha256Value)
checkValue.addAction(sha512Value)


safeWebsize = menu.addMenu(QtCore.QCoreApplication.translate("U", "云沙箱(&C)"))
s1 = QtWidgets.QAction(QtWidgets.QApplication.style().standardIcon(9), QtCore.QCoreApplication.translate("U", "360 沙箱云"))
s2 = QtWidgets.QAction(QtWidgets.QApplication.style().standardIcon(9), QtCore.QCoreApplication.translate("U", "微步云沙箱"))
s3 = QtWidgets.QAction(QtWidgets.QApplication.style().standardIcon(9), QtCore.QCoreApplication.translate("U", "VIRUSTOTAL"))
s4 = QtWidgets.QAction(QtWidgets.QApplication.style().standardIcon(9), QtCore.QCoreApplication.translate("U", "计算机病毒防御技术国家工程实验室"))
safeWebsize.addAction(s1)
safeWebsize.addAction(s2)
safeWebsize.addAction(s3)
safeWebsize.addAction(s4)
s1.triggered.connect(lambda: webbrowser.open_new_tab("https://ata.360.net/"))
s2.triggered.connect(lambda: webbrowser.open_new_tab("https://s.threatbook.cn/"))
s3.triggered.connect(lambda: webbrowser.open_new_tab("https://www.virustotal.com/"))
s4.triggered.connect(lambda: webbrowser.open_new_tab("https://cloud.vdnel.cn/"))

log = menu.addMenu(QtCore.QCoreApplication.translate("U", "日志(&L)"))
getDllInfo = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "查询 Dll"))
checkLogText = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "日志分析"))
saveLogText = QtWidgets.QAction(QtWidgets.QApplication.style().standardIcon(16), QtCore.QCoreApplication.translate("U", "另存为日志"))
saveLogReport = QtWidgets.QAction(QtWidgets.QApplication.style().standardIcon(16), QtCore.QCoreApplication.translate("U", "输出详细日志报告"))
transLogText = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "翻译日志（翻译后日志分析功能会故障）"))
uploadLogText = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "上传日志"))
getDllInfo.triggered.connect(DllWindow.ShowWindow)
checkLogText.triggered.connect(LogChecking.ShowWindow)
saveLogText.triggered.connect(SaveLog)
saveLogReport.triggered.connect(lambda: SaveLogReport(o1.currentText(), wine[o1.currentText()], lastRunCommand, e2.currentText(), returnText.toPlainText()).SetWindow())
transLogText.triggered.connect(TransLog)
uploadLogText.triggered.connect(UploadLog)
log.addAction(getDllInfo)
#log.addAction(checkLogText)
log.addAction(saveLogText)
log.addAction(saveLogReport)
#log.addAction(transLogText)
#log.addAction(uploadLogText)

actionList = []
def AddLib(install: QtWidgets.QAction, uninstall, menu, info):
    actionList.append(install)
    actionList.append(uninstall)
    install.triggered.connect(lambda: OpenTerminal(f"bash '{programPath}/InstallRuntime/{info}'"))
    uninstall.triggered.connect(lambda: OpenTerminal(f"bash '{programPath}/InstallRuntime/remove/{info}'"))
    menu.addAction(install)
    menu.addAction(uninstall)

installLib = menu.addMenu(QtCore.QCoreApplication.translate("U", "应用运行库(&R)"))
howtouseQemuUser = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "Qemu User 使用教程（配合运行库实现在非 X86 架构运行 X86 Wine）"))
howtouseQemuUser.triggered.connect(lambda: webbrowser.open_new_tab("https://www.bilibili.com/read/cv23185651"))
runnerlibinfo = QtWidgets.QAction("只在运行器使用的运行库（不与其他运行库以及兼容层冲突）")
installRunnerLib = QtWidgets.QAction("安装运行库")
statusRunnerLib = QtWidgets.QAction("当前状态：未安装")
removeRunnerLib = QtWidgets.QAction("移除运行库")
runnerlibinfo.setDisabled(True)
statusRunnerLib.setDisabled(True)
removeRunnerLib.setDisabled(True)
installLib.addAction(howtouseQemuUser)
installLib.addSeparator()
installLib.addAction(runnerlibinfo)
installLib.addAction(statusRunnerLib)
installLib.addAction(installRunnerLib)
installLib.addAction(removeRunnerLib)
diyRunnerLib = installLib.addMenu("定制运行库")
diyRunnerLib.setDisabled(True)
diyRunnerLibRemoveTips = QtWidgets.QAction("移除库")
diyRunnerLibRemoveTips.setDisabled(True)
diyRunnerLib.addAction(diyRunnerLibRemoveTips)
installRunnerLib.triggered.connect(lambda: threading.Thread(target=OpenTerminal, args=[f"bash '{programPath}/WineLib/install.sh'"]).start())
removeRunnerLib.triggered.connect(lambda: threading.Thread(target=OpenTerminal, args=[f"bash '{programPath}/WineLib/remove.sh'"]).start())
if os.path.exists(f"{programPath}/WineLib/usr"):
    installRunnerLib.setDisabled(True)
    removeRunnerLib.setEnabled(True)
    diyRunnerLib.setEnabled(True)
    w11WithWineLib.setEnabled(True)
    statusRunnerLib.setText("当前状态：已安装")
    libPathList = []
    mapLink = []
    def AddRunnerLib(number, name):
        global diyRunnerLib
        action = QtWidgets.QAction(f"{name}")
        mapLink.append(action)
        action.triggered.connect(lambda: DelRunnerLib(int(str(number))))
        diyRunnerLib.addAction(action)    
    def DelRunnerLib(number):
        os.system(f"rm -rf '{libPathList[number]}'")
        QtWidgets.QMessageBox.information(window, "提示", "删除完成！")
        mapLink[number].setDisabled(True)
    for libPath in [f"{programPath}/WineLib/usr/lib", f"{programPath}/WineLib/usr/lib64"]:
        for i in os.listdir(libPath):
            if not os.path.isdir(f"{libPath}/{i}"):
                try:
                    if not os.path.getsize(f"{libPath}/{i}"):
                        continue
                except:
                    continue
                libPathList.append(f"{libPath}/{i}")
                AddRunnerLib(len(libPathList) - 1, f"{i}")
            else:
                if not os.path.exists(f"{libPath}/{i}/libc.so.6"):
                    continue
                libPathList.append(f"{libPath}/{i}/")
                AddRunnerLib(len(libPathList) - 1, f"{i}/")
    print(libPathList)
if os.path.exists(f"{programPath}/InstallRuntime"):
    installLib.addSeparator()
    systemalllibinfo = QtWidgets.QAction("全局运行库（与其他运行库以及部分兼容层冲突）")    
    systemalllibinfo.setDisabled(True)
    installLib.addAction(systemalllibinfo)
    installQemuMenu = installLib.addMenu(QtCore.QCoreApplication.translate("U", "安装 Qemu User"))
    installQemu = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "安装 Qemu User"))
    removeQemu = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "卸载 Qemu User"))
    installQemuMenu.addAction(installQemu)
    installQemuMenu.addAction(removeQemu)
    installQemu.triggered.connect(lambda: OpenTerminal(f"bash '{programPath}/InstallQemuUser.sh'"))
    removeQemu.triggered.connect(lambda: OpenTerminal(f"bash '{programPath}/RemoveQemuUser.sh'"))
    actionList = []
    nameList = {}
    for i in os.listdir(f"{programPath}/InstallRuntime"):
        if i[-3:] == ".sh":
            print(f"检测到库 {os.path.splitext(i)[0]}")
            
            AddLib(QtWidgets.QAction(QtCore.QCoreApplication.translate("U", f"安装 {os.path.splitext(i)[0]} 运行库")), QtWidgets.QAction(QtCore.QCoreApplication.translate("U", f"卸载 {os.path.splitext(i)[0]} 运行库")), installLib.addMenu(QtCore.QCoreApplication.translate("U", f"运行库 {os.path.splitext(i)[0]}")), i)



qemuMenu = menu.addMenu(QtCore.QCoreApplication.translate("U", "容器(&C)"))
unpackDeb = QtWidgets.QAction(QtWidgets.QApplication.style().standardIcon(32), QtCore.QCoreApplication.translate("U", "解包 deb 提取容器"))
qemuMenu.addAction(unpackDeb)
unpackDeb.triggered.connect(UnPackage)
if len(qemuBottleList) >= 1:
    configMenu = QtWidgets.QAction(QtGui.QIcon(f"{programPath}/Icon/Function/CHROOT.png"), QtCore.QCoreApplication.translate("U", "配置指定 Chroot 容器"))
    qemuMenu.addAction(configMenu)
    configMenu.triggered.connect(ConfigQemu)
    print(qemuBottleList)

videoHelp = menu.addMenu(QtCore.QCoreApplication.translate("U", "视频教程(&V)"))
videoHelpAction = QtWidgets.QAction(QtWidgets.QApplication.style().standardIcon(20), QtCore.QCoreApplication.translate("U", "视频教程（Bilibili）"))
videoHelpActionYoutube = QtWidgets.QAction(QtWidgets.QApplication.style().standardIcon(20), QtCore.QCoreApplication.translate("U", "视频教程（Youtube）"))
videoHelpAction.triggered.connect(lambda: webbrowser.open_new_tab("https://space.bilibili.com/695814694/channel/collectiondetail?sid=1610353"))
videoHelpActionYoutube.triggered.connect(lambda: webbrowser.open_new_tab("https://www.youtube.com/watch?v=qDaPBiIdGAs&list=PLoXD11L1NQAx8A1Qskgu3tUoi0nHKJcmg"))
videoHelp.addAction(videoHelpAction)
videoHelp.addAction(videoHelpActionYoutube)

help = menu.addMenu(QtCore.QCoreApplication.translate("U", "帮助(&H)"))
runStatusWebSize = QtWidgets.QAction(QtWidgets.QApplication.style().standardIcon(20), QtCore.QCoreApplication.translate("U", "查询程序在 Wine 的运行情况"))
h1 = help.addMenu(QtWidgets.QApplication.style().standardIcon(20), QtCore.QCoreApplication.translate("U", "程序官网"))
h2 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "小提示"))
wineRunnerHelp = QtWidgets.QAction(QtWidgets.QApplication.style().standardIcon(20), QtCore.QCoreApplication.translate("U", "Wine运行器和Wine打包器傻瓜式使用教程（小白专用） By 鹤舞白沙"))
h3 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "更新内容"))
h4 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "鸣谢名单"))
h5 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "更新这个程序"))
appreciate = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "赞赏作者/请作者喝杯茶"))
programInformation = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "获取程序公告"))
h6 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "反馈这个程序的建议和问题"))
h7 = QtWidgets.QAction(QtWidgets.QApplication.style().standardIcon(9), QtCore.QCoreApplication.translate("U", "关于这个程序"))
h8 = QtWidgets.QAction(QtWidgets.QApplication.style().standardIcon(9), QtCore.QCoreApplication.translate("U", "关于 Qt"))
gfdgdxiio = QtWidgets.QAction(QtWidgets.QApplication.style().standardIcon(20), QtCore.QCoreApplication.translate("U", "作者个人站"))
gitee = QtWidgets.QAction(QtWidgets.QApplication.style().standardIcon(20), QtCore.QCoreApplication.translate("U", "Gitee"))
github = QtWidgets.QAction(QtWidgets.QApplication.style().standardIcon(20), QtCore.QCoreApplication.translate("U", "Github"))
gitlab = QtWidgets.QAction(QtWidgets.QApplication.style().standardIcon(20), QtCore.QCoreApplication.translate("U", "Gitlab"))
jihu = QtWidgets.QAction(QtWidgets.QApplication.style().standardIcon(20), QtCore.QCoreApplication.translate("U", "Sourceforge"))
h1.addAction(gfdgdxiio)
h1.addAction(gitee)
h1.addAction(github)
h1.addAction(gitlab)
h1.addAction(jihu)
help.addSeparator()
help.addAction(wineRunnerHelp)
help.addAction(runStatusWebSize)
help.addSeparator()
help.addAction(h2)
help.addAction(h3)
help.addAction(h4)
help.addSeparator()

wikiHelp = QtWidgets.QAction(QtWidgets.QApplication.style().standardIcon(20), QtCore.QCoreApplication.translate("U", "程序 Wiki"))
help.addAction(wikiHelp)
videoHelp = help.addMenu(QtWidgets.QApplication.style().standardIcon(20), QtCore.QCoreApplication.translate("U", "视频教程"))
videoHelp.addAction(videoHelpAction)
help.addSeparator()
help.addAction(h5)
help.addAction(h6)
help.addAction(programInformation)
help.addAction(appreciate)
help.addAction(h7)
help.addAction(h8)
help.addSeparator()
hm1 = help.addMenu(QtCore.QCoreApplication.translate("U", "更多生态适配应用"))
hm1_1 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "运行 Android 应用：UEngine 运行器"))
hm1.addAction(hm1_1)
gfdgdxiio.triggered.connect(lambda: webbrowser.open_new_tab("https://gfdgd-xi.github.io"))
gitee.triggered.connect(lambda: webbrowser.open_new_tab("https://gitee.com/gfdgd-xi/deep-wine-runner"))
github.triggered.connect(lambda: webbrowser.open_new_tab("https://github.com/gfdgd-xi/deep-wine-runner"))
gitlab.triggered.connect(lambda: webbrowser.open_new_tab("https://gitlab.com/gfdgd-xi/deep-wine-runner"))
jihu.triggered.connect(lambda: webbrowser.open_new_tab("https://sourceforge.net/projects/deep-wine-runner/"))
runStatusWebSize.triggered.connect(lambda: webbrowser.open_new_tab("https://gfdgd-xi.github.io/wine-runner-info"))
h2.triggered.connect(helps)
appreciate.triggered.connect(Appreciate)
h3.triggered.connect(UpdateThings)
wineRunnerHelp.triggered.connect(lambda: webbrowser.open_new_tab("https://bbs.deepin.org/post/246837"))
h4.triggered.connect(ThankWindow)
wikiHelp.triggered.connect(lambda: webbrowser.open_new_tab("https://gfdgd-xi.github.io/wine-runner-wiki"))
h5.triggered.connect(UpdateWindow.ShowWindow)
h6.triggered.connect(WineRunnerBugUpload)
h7.triggered.connect(about_this_program)
h8.triggered.connect(lambda: QtWidgets.QMessageBox.aboutQt(widget))
hm1_1.triggered.connect(lambda: webbrowser.open_new_tab("https://gitee.com/gfdgd-xi/uengine-runner"))
programInformation.triggered.connect(GetNewInformation)
# 异同步获取信息
#threading.Thread(target=GetVersion).start()
GetVersion()
# 窗口设置
window.resize(int(widget.frameGeometry().width() * 2), int(widget.frameGeometry().height()))
widget.setLayout(mainLayout)
window.setWindowIcon(QtGui.QIcon(f"{programPath}/deepin-wine-runner.svg"))
widget.show()
window.show()

# 控件设置
app.setStyle(QtWidgets.QStyleFactory.create(setting["Theme"]))
e1.addItems(findExeHistory)
e2.addItems(wineBottonHistory)
combobox1.addItems(shellHistory)
if setting["AutoWine"]:
    o1.addItems(canUseWine)
else:
    o1.addItems(wine.keys())
# 禁用被精简掉的控件
for i in [
    [[p1, installWineHQ, installWineHQOrg, installMoreWine], f"{programPath}/InstallWineOnDeepin23.py"],
    [[w5], f"{programPath}/deepin-wine-packager.py"],
    [[w6], f"{programPath}/deepin-wine-packager-with-script.py"],
    [[p1, v1], f"{programPath}/RunVM.sh"],
    [[getProgramIcon, uninstallProgram, updateGeek, trasButton, fontAppStore, wm1_1, wm1_2, wm1_3, wm1_6, w7, w2], f"{programPath}/geek.exe"],
]:
    if not os.path.exists(i[1]):
        for x in i[0]:
            x.setDisabled(True)
# 有些功能是 Arch Linux 不适用的，需要屏蔽
if os.path.exists("/etc/arch-release") or os.path.exists("/etc/fedora-release"):
    if os.path.exists(f"{programPath}/off-line.lock"):
        for i in [p1]:
            i.setDisabled(True)    
    for i in [installLat, installWineHQ, installWineHQOrg,
              installBox86CN, installBox86, installBox86Own]:
        i.setDisabled(True)
    for i in actionList:
        i.setDisabled(True)
# 有些功能是非 X86 不适用的，需要屏蔽
if subprocess.getoutput("arch").lower() != "x86_64":
    p1.setDisabled(True)
    installMoreWine.setEnabled(True)
    #virtualMachine.setDisabled(True)
    #v1.setDisabled(True)
    installWineHQ.setDisabled(True)
    installWineHQOrg.setDisabled(True)
    if os.path.exists("/etc/arch-release"):
        p1.setEnabled(True)
o1.setCurrentText(setting["DefultWine"])
e1.setEditText(setting["DefultBotton"])
e2.setEditText("")
combobox1.setEditText("")
if len(sys.argv) > 1 and sys.argv[1]:
    e2.setEditText(sys.argv[1])
if not os.path.exists("/opt/apps/store.spark-app.spark-dwine-helper/files/deepinwine/tools/spark-dwine-helper/wine-app-launcher/wine-app-launcher.sh"):
    sparkWineSetting.setEnabled(False)
if o1.currentText() == "":
    # 一个 Wine 都没有却用 Wine 的功能
    # 还是要处理的，至少不会闪退
    wine["没有识别到任何Wine，请在菜单栏“程序”安装Wine或安装任意Wine应用"] = "没有识别到任何Wine，请在菜单栏“程序”安装Wine或安装任意Wine应用"
    canUseWine.append("没有识别到任何Wine，请在菜单栏“程序”安装Wine或安装任意Wine应用")
    o1.addItem("没有识别到任何Wine，请在菜单栏“程序”安装Wine或安装任意Wine应用")
SetFont(setting["FontSize"])

# Mini 模式
# MiniMode(True)
sys.exit(app.exec_())
