#!/usr/bin/env python3
# 使用系统默认的 python3 运行
#################################################################################################################
# 作者：gfdgd xi、为什么您不喜欢熊出没和阿布呢
# 版本：2.2.0
# 更新时间：2022年09月24日
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
import base64
import shutil
import hashlib
import platform
import threading
import traceback
import webbrowser
import subprocess
import req as requests
import urllib.parse as parse
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets
from Model import *

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
    path = QtWidgets.QFileDialog.getOpenFileName(widget, "选择 exe 可执行文件", json.loads(readtxt(get_home() + "/.config/deepin-wine-runner/FindExe.json"))["path"], "exe 可执行文件(*.exe);;EXE 可执行文件(*.EXE);;所有文件(*.*)")
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

def DisableButton(things):
    button_r_6.setDisabled(things)
    button1.setDisabled(things)
    button2.setDisabled(things)
    button3.setDisabled(things)
    wineConfig.setDisabled(things)
    e1.setDisabled(things)
    e2.setDisabled(things)
    o1.setDisabled(things)
    miniAppStore.setDisabled(things)
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
        if o1.currentText() == "基于 exagear 的 deepin-wine6-stable" or o1.currentText() == "基于 box86 的 deepin-wine6-stable":
            wineUsingOption = ""
        if o1.currentText() == "基于 box86 的 deepin-wine6-stable" or o1.currentText() == "基于 exagear 的 deepin-wine6-stable":
            if not os.path.exists(f"{programPath}/dlls-arm"):
                if os.system(f"7z x -y \"{programPath}/dlls-arm.7z\" -o\"{programPath}\""):
                    QtWidgets.QMessageBox.critical(widget, "错误", "无法解压资源")
                    return
                os.remove(f"{programPath}/dlls-arm.7z")
        if setting["TerminalOpen"]:
            res = ""
            if e2.currentText()[-4:] == ".msi" and os.path.exists(e2.currentText()):
                OpenTerminal("env WINEPREFIX='" + wineBottonPath + "' " + option + wine[o1.currentText()] + " msiexec /i '" + e2.currentText() + "' " + setting["WineOption"])
            else:
                OpenTerminal("env WINEPREFIX='" + wineBottonPath + "' " + option + wine[o1.currentText()] + " '" + e2.currentText() + "' " + setting["WineOption"])
            #res = subprocess.Popen([f"'{programPath}/launch.sh' deepin-terminal -C \"WINEPREFIX='" + wineBottonPath + "' " + option + wine[o1.currentText()] + " '" + e2.currentText() + "' " + setting["WineOption"] + "\" --keep-open" + wineUsingOption], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        else:
            if e2.currentText()[-4:] == ".msi" and os.path.exists(e2.currentText()):
                res = subprocess.Popen(["WINEPREFIX='" + wineBottonPath + "' " + option + wine[o1.currentText()] + " msiexec /i '" + e2.currentText() + "' " + setting["WineOption"]], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            else:
                print(["WINEPREFIX='" + wineBottonPath + "' " + option + wine[o1.currentText()] + " '" + e2.currentText() + "' " + setting["WineOption"]])
                res = subprocess.Popen(["WINEPREFIX='" + wineBottonPath + "' " + option + wine[o1.currentText()] + " '" + e2.currentText() + "' " + setting["WineOption"]], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # 实时读取程序返回
        #
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
  

# 显示“关于这个程序”窗口
def about_this_program()->"显示“关于这个程序”窗口":
    global about
    global title
    global iconPath
    QT.message = QtWidgets.QMainWindow()  
    QT.message.setWindowIcon(QtGui.QIcon(iconPath))
    messageWidget = QtWidgets.QWidget()
    QT.message.setWindowTitle(f"关于 {title}")
    messageLayout = QtWidgets.QGridLayout()
    messageLayout.addWidget(QtWidgets.QLabel(f"<img width=256 src='{iconPath}'>"), 0, 0, 1, 1, QtCore.Qt.AlignTop)
    aboutInfo = QtWidgets.QTextBrowser(messageWidget)
    aboutInfo.setHtml(about)
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
            if o1.currentText() == "基于 box86 的 deepin-wine6-stable" or o1.currentText() == "基于 exagear 的 deepin-wine6-stable":
                if not os.path.exists(f"{programPath}/dlls-arm"):
                    if os.system(f"7z x -y \"{programPath}/dlls-arm.7z\" -o\"{programPath}\""):
                        QtWidgets.QMessageBox.critical(widget, "错误", "无法解压资源")
                        return
                    os.remove(f"{programPath}/dlls-arm.7z")
            if o1.currentText() == "基于 exagear 的 deepin-wine6-stable" or o1.currentText() == "基于 box86 的 deepin-wine6-stable":
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
            if o1.currentText() == "基于 exagear 的 deepin-wine6-stable" or o1.currentText() == "基于 box86 的 deepin-wine6-stable":
                wineUsingOption = ""
            if o1.currentText() == "基于 box86 的 deepin-wine6-stable" or o1.currentText() == "基于 exagear 的 deepin-wine6-stable":
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


# 重启本应用程序
def ReStartProgram():
    python = sys.executable
    os.execl(python, python, * sys.argv)

def KillProgram():
    os.system(f"killall {wine[o1.currentText()]} -9")
    os.system("killall winedbg -9")

def InstallWine():
    threading.Thread(target=OpenTerminal, args=[f"'{programPath}/AllInstall.py'"]).start()

def InstallWineOnDeepin23():
    threading.Thread(target=OpenTerminal, args=[f"'{programPath}/InstallWineOnDeepin23.py'"]).start()

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

class RunWineProgramThread(QtCore.QThread):
    signal = QtCore.pyqtSignal(str)
    showHistory = QtCore.pyqtSignal(str)
    def __init__(self, wineProgram, history = False, Disbled = True):
        super().__init__()
        self.wineProgram = wineProgram
        self.history = history
        self.Disbled = Disbled

    def run(self):
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
        if o1.currentText() == "基于 exagear 的 deepin-wine6-stable":
            os.system(f"'{programPath}/deepin-wine-runner-create-botton.py' '{wineBottonPath}'")
        if o1.currentText() == "基于 exagear 的 deepin-wine6-stable" or o1.currentText() == "基于 box86 的 deepin-wine6-stable":
            wineUsingOption = ""
        if o1.currentText() == "基于 box86 的 deepin-wine6-stable" or o1.currentText() == "基于 exagear 的 deepin-wine6-stable":
            if not os.path.exists(f"{programPath}/dlls-arm"):
                if os.system(f"7z x -y \"{programPath}/dlls-arm.7z\" -o\"{programPath}\""):
                    QtWidgets.QMessageBox.critical(widget, "错误", "无法解压资源")
                    return
                os.remove(f"{programPath}/dlls-arm.7z")
        if setting["TerminalOpen"]:
            res = ""
            OpenTerminal(f"env WINEPREFIX='" + wineBottonPath + "' " + option + wine[o1.currentText()] + " '" + self.wineProgram + "' " + setting["WineOption"] + " " + wineUsingOption)
            #res = subprocess.Popen([f"'{programPath}/launch.sh' deepin-terminal -C \"WINEPREFIX='" + wineBottonPath + "' " + option + wine[o1.currentText()] + " '" + self.wineProgram + "' " + setting["WineOption"] + " " + wineUsingOption + "\" --keep-open"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        else:
            res = subprocess.Popen(["WINEPREFIX='" + wineBottonPath + "' " + option + wine[o1.currentText()] + " '" + self.wineProgram + "' " + setting["WineOption"]], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
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
    if not CheckProgramIsInstall(wine[o1.currentText()]) and o1.currentText() != "基于 linglong 的 deepin-wine6-stable（不推荐）" and o1.currentText() != "基于 exagear 的 deepin-wine6-stable" and o1.currentText() != "基于 box86 的 deepin-wine6-stable":
        if not CheckProgramIsInstall(wine[o1.currentText()]) and not o1.currentText() in untipsWine:
            DisableButton(False)
            return
    returnText.setText("")
    runProgram = RunWineProgramThread(wineProgram, history, Disbled)
    runProgram.signal.connect(QT.ShowWineReturn)
    runProgram.showHistory.connect(QT.ShowHistory)
    runProgram.start()

class RunWinetricksThread(QtCore.QThread):
    signal = QtCore.pyqtSignal(str)
    def __init__(self):
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
        if o1.currentText() == "基于 exagear 的 deepin-wine6-stable" or o1.currentText() == "基于 box86 的 deepin-wine6-stable":
            wineUsingOption = ""
        if o1.currentText() == "基于 box86 的 deepin-wine6-stable" or o1.currentText() == "基于 exagear 的 deepin-wine6-stable":
            if not os.path.exists(f"{programPath}/dlls-arm"):
                if os.system(f"7z x -y \"{programPath}/dlls-arm.7z\" -o\"{programPath}\""):
                    QtWidgets.QMessageBox.critical(widget, "错误", "无法解压资源")
                    return
                os.remove(f"{programPath}/dlls-arm.7z")
        if setting["TerminalOpen"]:
            res = ""
            # 用终端开应该不用返回输出内容了
            OpenTerminal(f"WINEPREFIX='{wineBottonPath}' {option} WINE=" + subprocess.getoutput(f"which {wine[o1.currentText()]}").replace(" ", "").replace("\n", "") + f" winetricks --gui {wineUsingOption}")
            #res = subprocess.Popen([f"'{programPath}/launch.sh' deepin-terminal -C \"WINEPREFIX='{wineBottonPath}' {option} WINE=" + subprocess.getoutput(f"which {wine[o1.currentText()]}").replace(" ", "").replace("\n", "") + f" winetricks --gui {wineUsingOption}\" --keep-open"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        else:    
            res = subprocess.Popen([f"WINEPREFIX='{wineBottonPath}' {option} WINE='" + subprocess.getoutput(f"which {wine[o1.currentText()]}").replace(" ", "").replace("\n", "") + "' winetricks --gui"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
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
def RunWinetricks():
    global runWinetricks
    DisableButton(True)
    if not CheckProgramIsInstall(wine[o1.currentText()]) and o1.currentText() != "基于 linglong 的 deepin-wine6-stable（不推荐）" and o1.currentText() != "基于 exagear 的 deepin-wine6-stable" and o1.currentText() != "基于 box86 的 deepin-wine6-stable":
        if not CheckProgramIsInstall(wine[o1.currentText()]) and not o1.currentText() in untipsWine:
            DisableButton(False)
            return
    if o1.currentText() == "基于 box86 的 deepin-wine6-stable" or o1.currentText() == "基于 exagear 的 deepin-wine6-stable":
        if not os.path.exists(f"{programPath}/dlls-arm"):
            if os.system(f"7z x -y \"{programPath}/dlls-arm.7z\" -o\"{programPath}\""):
                QtWidgets.QMessageBox.critical(widget, "错误", "无法解压资源")
                return
            os.remove(f"{programPath}/dlls-arm.7z")
    returnText.setText("")
    runWinetricks = RunWinetricksThread()
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
    os.system(f"'{programPath}/AutoConfig.py' '{wine[o1.currentText()]}' '{wineBottonPath}'")

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
    OpenTerminal(f"env WINE='{wine[o1.currentText()]}' WINE64='{wine[o1.currentText()]}' WINEPREFIX='{wineBottonPath}' '{programPath}/dxvk/setup_dxvk.sh' install")
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

def MiniAppStore():
    if e1.currentText()== "":
        wineBottonPath = setting["DefultBotton"]
    else:
        wineBottonPath = e1.currentText()
    OpenTerminal(f"'{programPath}/AppStore.py' '{wineBottonPath}' '{wine[o1.currentText()]}'")

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

def CleanProgram():
    OpenTerminal(f"{programPath}/clean-unuse-program.py")

class UpdateWindow():
    data = {}
    update = None
    def ShowWindow():
        UpdateWindow.update = QtWidgets.QMainWindow()
        updateWidget = QtWidgets.QWidget()
        updateWidgetLayout = QtWidgets.QGridLayout()
        versionLabel = QtWidgets.QLabel(f"当前版本：{version}\n最新版本：未知\n更新内容：")
        updateText = QtWidgets.QTextBrowser()
        ok = QtWidgets.QPushButton(QtCore.QCoreApplication.translate("U", "更新（更新过程中会关闭所有Python应用，包括这个应用）"))
        ok.clicked.connect(UpdateWindow.Update)
        cancel = QtWidgets.QPushButton("取消")
        cancel.clicked.connect(UpdateWindow.update.close)
        if "从源码运行的版本" == programVersionType:
            versionLabel = QtWidgets.QLabel(f"当前版本：{version}\n最新版本：未知（从源码运行不提供更新）\n更新内容：")
            updateText.setText("从源码运行不提供更新")
            ok.setDisabled(True)
        else:
            if "deepin/UOS 应用商店版本<带签名>" == programVersionType:
                url = "aHR0cDovLzEyMC4yNS4xNTMuMTQ0L3NwYXJrLWRlZXBpbi13aW5lLXJ1bm5lci91cGRhdGUtdW9zLmpzb24="
            elif "星火应用商店版本" == programVersionType:
                url = "aHR0cDovLzEyMC4yNS4xNTMuMTQ0L3NwYXJrLWRlZXBpbi13aW5lLXJ1bm5lci91cGRhdGUtc3BhcmsuanNvbg=="
            else: 
                url = "aHR0cDovLzEyMC4yNS4xNTMuMTQ0L3NwYXJrLWRlZXBpbi13aW5lLXJ1bm5lci91cGRhdGUuanNvbg=="
            try:
                UpdateWindow.data = json.loads(requests.get(base64.b64decode(url).decode("utf-8")).text)
                versionLabel = QtWidgets.QLabel(f"当前版本：{version}\n最新版本：{UpdateWindow.data['Version']}\n更新内容：")
                if UpdateWindow.data["Version"] == version:
                    updateText.setText(QtCore.QCoreApplication.translate("U", "此为最新版本，无需更新"))
                    ok.setDisabled(True)
                else:
                    updateText.setText(UpdateWindow.data["New"].replace("\\n", "\n"))
            except:
                traceback.print_exc()
                QtWidgets.QMessageBox.critical(updateWidget, QtCore.QCoreApplication.translate("U", "错误"), QtCore.QCoreApplication.translate("U", "无法连接服务器！"))
                updateText.setText("无法连接服务器，无法更新")
                ok.setDisabled(True)
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
        try:            
            print(UpdateWindow.data["Url"])
            write_txt("/tmp/spark-deepin-wine-runner/update.sh", f"""#!/bin/bash
echo 删除多余的安装包
rm -rfv /tmp/spark-deepin-wine-runner/update/*
echo 关闭“Wine 运行器”以及其它“Python 应用”
killall python3
echo 下载安装包
wget -P /tmp/spark-deepin-wine-runner/update {UpdateWindow.data["Url"][0]}
echo 安装安装包
dpkg -i /tmp/spark-deepin-wine-runner/update/*
echo 修复依赖关系
apt install -f -y
notify-send -i "{iconPath}" "更新完毕！"
zenity --info --text=\"更新完毕！\" --ellipsize
""")
        except:
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(None, "出现错误，无法继续更新", traceback.format_exc())
        OpenTerminal("pkexec bash /tmp/spark-deepin-wine-runner/update.sh")

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
        widgetLayout.addWidget(QtWidgets.QLabel(f"""提示：
    目前本提取功能暂只支持 NT 内核系统的官方安装镜像，不支持读取 ghost 等第三方封装方式的安装镜像
    以及不要拷贝/替换太多的 dll，否则可能会导致 wine 容器异常，以及不要替换 Wine 的核心 dll
    最后，拷贝/替换 dll 后，建议点击下面“设置 wine 容器”按钮==》函数库 进行设置
当前选择的 Wine 容器：{GetDllFromWindowsISO.wineBottonPath}"""), 0, 0, 1, 5)
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
            QtWidgets.QMessageBox.critical(GetDllFromWindowsISO.message, "错误", traceback.format_exc())

 
    def MountDisk():
        if not os.path.exists(GetDllFromWindowsISO.isoPath.currentText()):
            QtWidgets.QMessageBox.critical(GetDllFromWindowsISO.message, "错误", "您选择的 ISO 镜像文件不存在")
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
class ProgramRunStatusShow():
    msgWindow = None
    def ShowWindow():
        global choose
        choose = None
        dateVersion = ""
        if not os.path.exists(e2.currentText()):
            QtWidgets.QMessageBox.information(widget, "提示", "您输入的 exe 不存在")
            return
        try:
            sha = ProgramRunStatusUpload.GetSHA1(e2.currentText())
            lists = json.loads(requests.get(base64.b64decode("aHR0cDovLzEyMC4yNS4xNTMuMTQ0L3NwYXJrLWRlZXBpbi13aW5lLXJ1bm5lci9hcHAv").decode("utf-8") + sha + base64.b64decode("L2FsbC5qc29u").decode("utf-8")).text)
            r = requests.get(base64.b64decode("aHR0cDovLzEyMC4yNS4xNTMuMTQ0L3NwYXJrLWRlZXBpbi13aW5lLXJ1bm5lci9hcHAv").decode("utf-8") + sha + base64.b64decode("L3RpdGxlLnR4dA==").decode("utf-8"))
            r.encoding = "utf-8"
            title = r.text
        except:
            choosemsg = QtWidgets.QMessageBox()
            choosemsg.setText("""暂时还没有该软件的运行情况信息，请问需要？""")
            choosemsg.setWindowTitle("提示")
            def Choose(choices):
                global choose
                choose = choices
            choosemsg.addButton("取消", QtWidgets.QMessageBox.ActionRole).clicked.connect(lambda: Choose(0))
            choosemsg.addButton("提交评分", QtWidgets.QMessageBox.ActionRole).clicked.connect(lambda: Choose(1))
            choosemsg.addButton("预测评分（不准确）", QtWidgets.QMessageBox.ActionRole).clicked.connect(lambda: Choose(2))
            choosemsg.exec_()
            if choose == None or choose == 0:
                return
            if choose == 1:
                ProgramRunStatusUpload.ShowWindow(sha)
                return
            if choose == 2:
                try:
                    lists = [0, 0, 0, 0, 0, 0, 0, 0]
                    info = json.loads(requests.get(base64.b64decode("aHR0cDovLzEyMC4yNS4xNTMuMTQ0OjMwMjUwL0FJP1NIQTE9").decode("utf-8") + sha).text)
                    lists[int(info["Fen"])] = 1
                    dateVersion = info["Version"]
                    title = "null"
                except:
                    traceback.print_exc()
                    QtWidgets.QMessageBox.critical(window, "错误", "无法获取预测数值")
                    return        
            
            
        informationList = [
            "0分：无法运行并且也没有报错，自己无法解决",
            "1分：无法运行但有报错，自己无法解决",
            "2分：可以运行但是效果很差，几乎无法使用",
            "3分：可以运行且勉强可以使用",
            "4分：可以运行，体验大差不差，还是有点小问题",
            "5分：可以运行且完全没有bug和问题，和在 Windows 上一样",
            "含有不良内容，不宜安装",
            "含有病毒、木马等对计算机有害的软件"
        ]
        try:
            if title.lower() == "null":
                title = "未知应用"
        except:
            title = "未知应用"
        maxHead = lists.index(max(lists))
        ProgramRunStatusShow.msgWindow = QtWidgets.QMainWindow()
        msgWidget = QtWidgets.QWidget()
        msgWidgetLayout = QtWidgets.QGridLayout()
        starLayout = QtWidgets.QHBoxLayout()
        uploadButton = QtWidgets.QPushButton(QtCore.QCoreApplication.translate("U", "点此上传运行情况"))
        uploadButton.clicked.connect(lambda: ProgramRunStatusUpload.ShowWindow(sha, title))
        msgWidgetLayout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("U", "综合评价：")), 0, 0)
        msgWidgetLayout.addLayout(starLayout, 0, 1)
        msgWidgetLayout.addWidget(QtWidgets.QLabel(informationList[maxHead]), 1, 0, 1, 2)
        msgWidgetLayout.addWidget(QtWidgets.QLabel("" if dateVersion == "" else f"数据版本：{dateVersion}"), 2, 0, 1, 2)
        msgWidgetLayout.addWidget(uploadButton, 3, 0, 1, 2)
        end = 5
        if maxHead > 5:
            for i in range(end):
                starLayout.addWidget(QtWidgets.QLabel(f"<img src='{programPath}/Icon/BadStar.svg' width=50>"))
        else:
            for i in range(maxHead):
                starLayout.addWidget(QtWidgets.QLabel(f"<img src='{programPath}/Icon/Star.svg' width=50>"))
            head = maxHead
            for i in range(head, end):
                starLayout.addWidget(QtWidgets.QLabel(f"<img src='{programPath}/Icon/UnStar.svg' width=50>"))
        msgWidget.setLayout(msgWidgetLayout)
        ProgramRunStatusShow.msgWindow.setCentralWidget(msgWidget)
        ProgramRunStatusShow.msgWindow.setWindowIcon(QtGui.QIcon(iconPath))
        ProgramRunStatusShow.msgWindow.setWindowTitle(f"应用“{title}”的运行情况")
        ProgramRunStatusShow.msgWindow.show()

class ProgramRunStatusUpload():
    msgWindow = None
    starLayout = None
    fen = None
    starList = []
    sha1Value = ""
    programName = None
    def ChangeStar():
        if ProgramRunStatusUpload.fen.currentIndex() > 5:
            for i in ProgramRunStatusUpload.starList:
                i.setText(f"<img src='{programPath}/Icon/BadStar.svg' width=25>")
            return
        for i in range(ProgramRunStatusUpload.fen.currentIndex()):
            ProgramRunStatusUpload.starList[i].setText(f"<img src='{programPath}/Icon/Star.svg' width=25>")
        head = ProgramRunStatusUpload.fen.currentIndex() 
        end = len(ProgramRunStatusUpload.starList)
        for i in range(head, end):
            ProgramRunStatusUpload.starList[i].setText(f"<img src='{programPath}/Icon/UnStar.svg' width=25>")
        
    def ShowWindow(sha="", title=""):
        ProgramRunStatusUpload.starList = []
        ProgramRunStatusUpload.sha1Value = sha
        ProgramRunStatusUpload.msgWindow = QtWidgets.QMainWindow()
        msgWidget = QtWidgets.QWidget()
        msgWidgetLayout = QtWidgets.QGridLayout()
        ProgramRunStatusUpload.programName = QtWidgets.QLineEdit()
        ProgramRunStatusUpload.fen = QtWidgets.QComboBox()
        ProgramRunStatusUpload.starLayout = QtWidgets.QHBoxLayout()
        upload = QtWidgets.QPushButton(QtCore.QCoreApplication.translate("U", "上传"))
        upload.clicked.connect(ProgramRunStatusUpload.Upload)
        if title != "":
            ProgramRunStatusUpload.programName.setText(title)
            ProgramRunStatusUpload.programName.setDisabled(True)
        # 生成星星列表
        for i in [1, 1, 1, 1, 0]:
            ProgramRunStatusUpload.starList.append(QtWidgets.QLabel(f"<img src='{programPath}/Icon/{['Un', ''][i]}Star.svg' width=25>"))
            ProgramRunStatusUpload.starLayout.addWidget(ProgramRunStatusUpload.starList[-1])
        ProgramRunStatusUpload.starLayout.addItem(QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        ProgramRunStatusUpload.programName.setPlaceholderText(QtCore.QCoreApplication.translate("U", "如果这个程序和程序名确实是合法还是检测到敏感词，改为“NULL”即可"))
        ProgramRunStatusUpload.fen.addItems(["0分：无法运行并且也没有报错，自己无法解决",
    "1分：无法运行但有报错，自己无法解决",
    "2分：可以运行但是效果很差，几乎无法使用",
    "3分：可以运行且勉强可以使用",
    "4分：可以运行，体验大差不差，还是有点小问题",
    "5分：可以运行且完全没有bug和问题，和在 Windows 上一样",
    "含有不良内容，不宜安装",
    "含有病毒、木马等对计算机有害的软件"])
        ProgramRunStatusUpload.fen.setCurrentIndex(4)
        ProgramRunStatusUpload.fen.currentIndexChanged.connect(ProgramRunStatusUpload.ChangeStar)
        msgWidgetLayout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("U", "程序名：")), 0, 0)
        msgWidgetLayout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("U", "评分：")), 1, 0)
        msgWidgetLayout.addWidget(ProgramRunStatusUpload.programName, 0, 1)
        msgWidgetLayout.addWidget(ProgramRunStatusUpload.fen, 1, 1)
        msgWidgetLayout.addLayout(ProgramRunStatusUpload.starLayout, 2, 1)
        msgWidgetLayout.addWidget(upload, 3, 1)
        msgWidget.setLayout(msgWidgetLayout)
        ProgramRunStatusUpload.msgWindow.setCentralWidget(msgWidget)
        ProgramRunStatusUpload.msgWindow.setWindowTitle(QtCore.QCoreApplication.translate("U", "上传程序运行情况"))
        ProgramRunStatusUpload.msgWindow.setWindowIcon(QtGui.QIcon(iconPath))
        ProgramRunStatusUpload.msgWindow.show()

    def Upload():
        if not os.path.exists(e2.currentText()):
            QtWidgets.QMessageBox.critical(None, "错误", "exe 文件不存在！")
            return
        if ProgramRunStatusUpload.programName.text() == "":
            QtWidgets.QMessageBox.critical(None, "错误", "程序名称不能为空！")
            return
        try:
            if ProgramRunStatusUpload.sha1Value == "":
                ProgramRunStatusUpload.sha1Value = ProgramRunStatusUpload.GetSHA1(e2.currentText())
            QtWidgets.QMessageBox.information(None, QtCore.QCoreApplication.translate("U", "提示"), json.loads(requests.post(base64.b64decode("aHR0cDovLzEyMC4yNS4xNTMuMTQ0OjMwMjUw").decode("utf-8"), {
            "SHA1": ProgramRunStatusUpload.sha1Value,
            "Name": ProgramRunStatusUpload.programName.text(),
            "Fen": ProgramRunStatusUpload.fen.currentIndex(),
            "Wine": o1.currentText()
            }).text)["Error"])
        except:
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(None, QtCore.QCoreApplication.translate("U", "错误"), QtCore.QCoreApplication.translate("U", "数据上传失败！"))

    def GetSHA1(filePath):
        sha1 = hashlib.sha1()
        file = open(filePath, "rb")
        while True:
            readByte = file.read(1024 * 1024)
            sha1.update(readByte)
            if not readByte:
                break
        file.close()
        return sha1.hexdigest()

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
        ProgramSetting.autoPath = QtWidgets.QCheckBox(QtCore.QCoreApplication.translate("U", "自动根据文件名生成容器路径（开启后必须通过修改默认wine容器路径才可指定其它路径，重启后生效）"))
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
        widgetLayout.addWidget(save, 12, 2, 1, 1)
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
            QtWidgets.QInputDialog.getMultiLineText(window, "值", "计算得到的值", self.link[types](self, file))
        except:
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(window, "错误", traceback.format_exc())

def ChangePath():
    e1.setCurrentText(f'{setting["DefultBotton"]}/{os.path.splitext(os.path.basename(e2.currentText()))[0]}')

###########################
# 加载配置
###########################
defultProgramList = {
    "Architecture": "Auto",
    "Debug": True,
    "DefultWine": "deepin-wine6 stable",
    "DefultBotton" : get_home() + "/.wine",
    "TerminalOpen": False,
    "WineOption": "",
    "WineBottonDifferent": False,
    "CenterWindow": False,
    "Theme": "",
    "MonoGeckoInstaller": True,
    "AutoWine": True,
    "RuntimeCache": True,
    "MustRead": False,
    "BuildByBottleName": False,
    "AutoPath": False
}
if not os.path.exists(get_home() + "/.config/deepin-wine-runner"):  # 如果没有配置文件夹
    os.mkdir(get_home() + "/.config/deepin-wine-runner")  # 创建配置文件夹
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
# 如果要添加其他 wine，请在字典添加其名称和执行路径
try:
    wine = {
        "基于 box86 的 deepin-wine6-stable": f"WINEPREDLL='{programPath}/dlls-arm' WINEDLLPATH=/opt/deepin-wine6-stable/lib BOX86_NOSIGSEGV=1 /opt/deepin-box86/box86 /opt/deepin-wine6-stable/bin/wine ",
        "基于 exagear 的 deepin-wine6-stable": f"WINEPREDLL='{programPath}/dlls-arm' WINEDLLPATH=/opt/deepin-wine6-stable/lib /opt/exagear/bin/ubt_x64a64_al --path-prefix {get_home()}/.deepinwine/debian-buster --utmp-paths-list {get_home()}/.deepinwine/debian-buster/.exagear/utmp-list --vpaths-list {get_home()}/.deepinwine/debian-buster/.exagear/vpaths-list --opaths-list {get_home()}/.deepinwine/debian-buster/.exagear/opaths-list --smo-mode fbase --smo-severity smart --fd-limit 8192 --foreign-ubt-binary /opt/exagear/bin/ubt_x32a64_al -- /opt/deepin-wine6-stable/bin/wine ",
        "deepin-wine6 stable": "deepin-wine6-stable", 
        "deepin-wine5 stable": "deepin-wine5-stable", 
        "spark-wine7-devel": "spark-wine7-devel", 
        "deepin-wine": "deepin-wine", 
        "deepin-wine5": "deepin-wine5", 
        "wine": "wine", 
        "wine64": "wine64", 
        "ukylin-wine": "ukylin-wine",
        "基于 linglong 的 deepin-wine6-stable（不推荐）": f"ll-cli run '' --exec '/bin/deepin-wine6-stable'"
    }
    untipsWine = ["基于 box86 的 deepin-wine6-stable", "基于 exagear 的 deepin-wine6-stable", "基于 linglong 的 deepin-wine6-stable（不推荐）"]
    canUseWine = []
    if os.path.exists("/opt/deepin-box86/box86"):
        canUseWine.append("基于 box86 的 deepin-wine6-stable")
    if os.path.exists("/opt/exagear/bin/ubt_x64a64_al"):
        canUseWine.append("基于 exagear 的 deepin-wine6-stable")
    for i in wine.keys():
        if not os.system(f"which '{wine[i]}'"):
            canUseWine.append(i)
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
    try:
        for i in json.loads(readtxt(f"{programPath}/wine/winelist.json")):
            if os.path.exists(f"{programPath}/wine/{i}"):
                name = ""
                value = ""
                try:
                    if os.path.exists("/opt/deepin-box86/box86"):
                        name = "基于 box86 的 "
                        value = f"WINEPREDLL='{programPath}/dlls-arm' WINEDLLPATH=/opt/deepin-wine6-stable/lib BOX86_NOSIGSEGV=1 /opt/deepin-box86/box86  "
                    if os.path.exists("/opt/exagear/bin/ubt_x64a64_al"):
                        name = "基于 exagear 的 "
                        value = f"WINEPREDLL='{programPath}/dlls-arm' WINEDLLPATH=/opt/deepin-wine6-stable/lib /opt/exagear/bin/ubt_x64a64_al --path-prefix {get_home()}/.deepinwine/debian-buster --utmp-paths-list {get_home()}/.deepinwine/debian-buster/.exagear/utmp-list --vpaths-list {get_home()}/.deepinwine/debian-buster/.exagear/vpaths-list --opaths-list {get_home()}/.deepinwine/debian-buster/.exagear/opaths-list --smo-mode fbase --smo-severity smart --fd-limit 8192 --foreign-ubt-binary /opt/exagear/bin/ubt_x32a64_al --  "
                except:
                    pass
                if os.path.exists(f"{programPath}/wine/{i}/bin/wine"):
                    wine[f"{name}{programPath}/wine/{i}/bin/wine"] = f"{value}{programPath}/wine/{i}/bin/wine"
                    canUseWine.append(f"{name}{programPath}/wine/{i}/bin/wine")
                    untipsWine.append(f"{name}{programPath}/wine/{i}/bin/wine")
                if os.path.exists(f"{programPath}/wine/{i}/bin/wine64"):
                    wine[f"{name}{programPath}/wine/{i}/bin/wine64"] = f"{value}{programPath}/wine/{i}/bin/wine64"
                    canUseWine.append(f"{name}{programPath}/wine/{i}/bin/wine64")
                    untipsWine.append(f"{name}{programPath}/wine/{i}/bin/wine64")
    except:
        pass
    try:
        for i in os.listdir(f"{get_home()}/.deepinwine/"):
            if os.path.exists(f"{get_home()}/.deepinwine/{i}/bin/wine"):
                wine[f"{get_home()}/.deepinwine/{i}/bin/wine"] = f"{get_home()}/.deepinwine/{i}/bin/wine"
                canUseWine.append(f"{get_home()}/.deepinwine/{i}/bin/wine")
            if os.path.exists(f"{get_home()}/.deepinwine/{i}/bin/wine64"):
                wine[f"{get_home()}/.deepinwine/{i}/bin/wine64"] = f"{get_home()}/.deepinwine/{i}/bin/wine64"
                canUseWine.append(f"{get_home()}/.deepinwine/{i}/bin/wine64")
    except:
        pass
    shellHistory = list(json.loads(readtxt(get_home() + "/.config/deepin-wine-runner/ShellHistory.json")).values())
    findExeHistory = list(json.loads(readtxt(get_home() + "/.config/deepin-wine-runner/FindExeHistory.json")).values())
    wineBottonHistory = list(json.loads(readtxt(get_home() + "/.config/deepin-wine-runner/WineBottonHistory.json")).values())
    isoPath = list(json.loads(readtxt(get_home() + "/.config/deepin-wine-runner/ISOPath.json")).values())
    isoPathFound = list(json.loads(readtxt(get_home() + "/.config/deepin-wine-runner/ISOPathFound.json")).values())
    setting = json.loads(readtxt(get_home() + "/.config/deepin-wine-runner/WineSetting.json"))
    change = False
    for i in defultProgramList.keys():
        if not i in setting:
            change = True
            setting[i] = defultProgramList[i]
    if change:
        write_txt(get_home() + "/.config/deepin-wine-runner/WineSetting.json", json.dumps(setting))
except:
    traceback.print_exc()
    app = QtWidgets.QApplication(sys.argv)
    QtWidgets.QMessageBox.critical(None, "错误", f"无法读取配置，无法继续\n{traceback.format_exc()}")
    sys.exit(1)

def getFileFolderSize(fileOrFolderPath):
    """get size for file or folder"""
    totalSize = 0
    if not os.path.exists(fileOrFolderPath):
        return totalSize
    if os.path.isfile(fileOrFolderPath):
        totalSize = os.path.getsize(fileOrFolderPath)  # 5041481
        return totalSize
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

# 获取当前语言
def get_now_lang()->"获取当前语言":
    return os.getenv('LANG')

def GetVersion():
    global about
    global programVersionType
    # 目前分为几个版本（在 control 文件区分）：
    # 星火版本：~spark
    # 商店版本：~uos
    # 编译版本：无版本号
    # Gitee/Github……：正常版本
    programVersionTypeLnk = {
        "spark": "星火应用商店版本",
        "uos": "deepin/UOS 应用商店版本<带签名>"
    }
    programVersionType = "从源码运行的版本"
    try:
        if not os.path.exists("/var/lib/dpkg/status"):
            print("无 dpkg，结束")
        file = open("/var/lib/dpkg/status", "r")
        fileName = file.read().splitlines()
        package = False
        for i in range(0, len(fileName)):
            if fileName[i] == "Package: spark-deepin-wine-runner-52":
                programVersionType = "吾爱专版"
                window.setWindowTitle(f"{title} 吾爱专版")
                break
            if fileName[i] == "Package: spark-deepin-wine-runner":
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
                        programVersionType = "从Gitee/Github/Gitlink等平台获取的版本"
                        break
                    programVersionType = version[version.index("-") + 1:]
                    print(programVersionType)
                    if "-" in programVersionType:
                        # 考虑到如 2.1.0-2-spark 的情况
                        programVersionType = programVersionType[programVersionType.index("-") + 1:]
                    try:
                        programVersionType = programVersionTypeLnk[programVersionType]    
                    except:
                        programVersionType = "从Gitee/Github/Gitlink等平台获取的版本"
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

programVersionType = ""
print(wine)
###########################
# 程序信息
###########################
iconPath = "{}/deepin-wine-runner.svg".format(programPath)
programUrl = "https://gitee.com/gfdgd-xi/deep-wine-runner\nhttps://github.com/gfdgd-xi/deep-wine-runner\nhttps://www.gitlink.org.cn/gfdgd_xi/deep-wine-runner\nhttps://gfdgd-xi.github.io"
information = json.loads(readtxt(f"{programPath}/information.json"))
version = information["Version"]
goodRunSystem = "常见 Linux 发行版"
thankText = ""
tips = '''<h4>提示：</h4>
1、使用终端运行该程序，可以看到 wine 以及程序本身的提示和报错;
2、wine 32 位和 64 位的容器互不兼容;
3、所有的 wine 和 winetricks 均需要自行安装（可以从 菜单栏=>程序 里面进行安装）
4、本程序支持带参数运行 wine 程序（之前版本也可以），只需要按以下格式即可：
exe路径\' 参数 \'
即可（单引号需要输入）
5、wine 容器如果没有指定，则会默认为 ~/.wine
6、如果可执行文件比较大的话，会出现点击“获取该程序运行情况”出现假死的情况，因为正在后台读取 SHA1，只需要等一下即可（读取速度依照您电脑处理速度、读写速度、可执行文件大小等有关）
7、对于非 X86 的用户来说，请不要使用本程序自带的 Wine 安装程序和 Windows 虚拟机安装功能（检测到为非 X86 架构会自动禁用）
8、如果非 X86 的用户的 UOS 专业版用户想要使用的话，只需要在应用商店安装一个 Wine 版本微信即可在本程序选择正确的 Wine 运行程序
9、在使用 linglong 包的 Wine 应用时，必须安装至少一个 linglong 的使用 Wine 软件包才会出现该选项，
而程序识别到的 Wine 是按 linglong 的使用 Wine 软件包名的字母排序第一个的 Wine，且生成的容器不在用户目录下，而是在容器的用户目录下（~/.deepinwine、/tmp、桌面、下载、文档等被映射的目录除外），
同理需要运行的 EXE 也必须在被映射的目录内
10、如果是使用 Deepin 23 的 Wine 安装脚本，请切记——安装过程会临时添加 Deepin 20 的 apt 源，不要中断安装以及
<b>千万不要中断后不删除源的情况下 apt upgrade ！！！</b>中断后只需重新打开脚本输入 repair 或者随意安装一个 Wine（会自动执行恢复操作）即可
以及此脚本安装的 Wine 无法保证 100% 能使用，以及副作用是会提示
<code>N: 鉴于仓库 'https://community-packages.deepin.com/beige beige InRelease' 不支持 'i386' 体系结构，跳过配置文件 'main/binary-i386/Packages' 的获取。</code>'''
updateThingsString = '''<h2>2.2.0-1 更新内容</h2>
※1、修复基于生态适配活动打包器对话框过多并修改了小提示内容
<h2>2.2.0 更新内容</h2>
※1、Dll 提取工具支持 NT 6.X 及以上版本的 Dll 提取并优化了提示文本
※2、支持卸载后自动删除缓存/配置文件（删除配置文件只限 purge 参数删除）
※3、DEBUG 模式输出更多信息以方便调试（原本只输出 pid、Err）
※4、支持安装 msi 文件
※5、修复无法正常评分的问题
※6、修复 QQ、TIM 安装后无法正常生成快捷方式的问题
※7、基于生态适配活动的打包器更换为 spark-wine-helper 以及添加自动删除残留脚本
※8、打包器支持从 deb 文件读取信息
※9、修复在 UOS 专业版（鲲鹏）无法正常运行的问题以及组件安装功能无法正常执行安装命令的问题
※10、修复出现星火应用商店和官方应用商店反复提示更新死循环的问题
※11、新增评分分数预测功能（不准）
※12、更换程序接口
※13、将 WineHQ 的源换为国内源
14、更新组件安装的离线列表
15、不再强制依赖深度终端，只做推荐安装
16、基于生态活动适配脚本的打包器在打包完成后会弹出对话框提示打包完成
17、优化打包器的 spark wine helper 依赖设置方式
18、新增 RegShot（注册表比对工具）
19、添加 Wine 运行器评分数据的搜索功能
<b>以下更新内容旧版本也适用（只限 2.1.0 及以上版本）</b>
※1、在“安装更多Wine”的Wine安装工具中上新 Wine
※2、云 Dll 工具上新 Dll
※3、VCPP、net 运行库安装工具新增运行库
'''
for i in information["Thank"]:
    thankText += f"{i}\n"
updateTime = "2022年09月24日"
about = f'''<h1>关于</h1>
<p>一个能让Linux用户更加方便运行Windows应用的程序，内置了对wine图形化的支持和各种Wine工具和自制Wine程序打包器、运行库安装工具等等</p>
<p>同时也内置了基于VirtualBox制作的小白Windows虚拟机安装工具，可以做到只需要用户下载系统镜像并点击安装即可，无需顾及虚拟机安装、创建、虚拟机的分区等等</p>
<p>本程序依照 GPLV3 协议开源</p>
<pre>

一个图形化了如下命令的程序（最简单格式）
<code>env WINEPREFIX=容器路径 wine（wine的路径） 可执行文件路径</code>
让你可以简易方便的使用 wine

版本：{version}
适用平台：{goodRunSystem}（@VersionForType@）
Qt 版本：{QtCore.qVersion()}
程序官网：{programUrl}
程序占用体积：@programSize@MB</pre>
<hr>
<h1>谢明名单</h1>
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
<h1>©2020~{time.strftime("%Y")} gfdgd xi、为什么您不喜欢熊出没和阿布呢</h1>'''
title = "Wine 运行器 {}".format(version)
updateThings = "{} 更新内容：\n{}\n更新时间：{}".format(version, updateThingsString, updateTime, time.strftime("%Y"))
try:
    threading.Thread(target=requests.get, args=[parse.unquote(base64.b64decode("aHR0cDovLzEyMC4yNS4xNTMuMTQ0L3NwYXJrLWRlZXBpbi13aW5lLXJ1bm5lci9vcGVuL0luc3RhbGwucGhw").decode("utf-8")) + "?Version=" + version]).start()
except:
    pass
iconListUnBuild = [
    ["QQ", "wineBottonPath/drive_c/Program Files/Tencent/QQ/Bin/QQ.exe"],
    ["QQ", "wineBottonPath/drive_c/Program Files (x86)/Tencent/QQ/Bin/QQ.exe"],
    ["TIM", "wineBottonPath/drive_c/Program Files/Tencent/TIM/Bin/TIM.exe"],
    ["TIM", "wineBottonPath/drive_c/Program Files (x86)/Tencent/TIM/Bin/TIM.exe"]
]
iconList = [
    ["微信", "wineBottonPath/drive_c/Program Files/Tencent/WeChat/WeChat.exe"],
    ["微信", "wineBottonPath/drive_c/Program Files (x86)/Tencent/WeChat/WeChat.exe"],
    ["UltraISO", "wineBottonPath/drive_c/Program Files/UltraISO/UltraISO.exe"],
    ["UltraISO", "wineBottonPath/drive_c/Program Files (x86)/UltraISO/UltraISO.exe"],
    ["迅雷", "wineBottonPath/drive_c/Program Files/Thunder Network/MiniThunder/Bin/ThunderMini.exe"],
    ["迅雷", "wineBottonPath/drive_c/Program Files (x86)/Thunder Network/MiniThunder/Bin/ThunderMini.exe"],
    ["Microsoft Office Word", "wineBottonPath/drive_c/Program Files/Microsoft Office/Office12/WINWORD.EXE"],
    ["Microsoft Office Word", "wineBottonPath/drive_c/Program Files (x86)/Microsoft Office/Office12/WINWORD.EXE"]
]
for i in iconListUnBuild:
    iconList.append(i)
print(iconList)

###########################
# 窗口创建
###########################
# 读取主题
# Qt 窗口
app = QtWidgets.QApplication(sys.argv)
# 语言载入
if not get_now_lang() == "zh_CN.UTF-8":
    trans = QtCore.QTranslator()
    trans.load(f"{programPath}/LANG/deepin-wine-runner-en_US.qm")
    app.installTranslator(trans)
window = QtWidgets.QMainWindow()
window.setWindowTitle(title)
# 异同步获取信息
threading.Thread(target=GetVersion).start()
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
leftUpLayout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("U", "请选择要执行的程序：")), 4, 0, 1, 1)
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
saveDesktopFileOnLauncher = QtWidgets.QPushButton(QtCore.QCoreApplication.translate("U", "创建到开始菜单"))
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
miniAppStore = QtWidgets.QPushButton(QtCore.QCoreApplication.translate("U", "微型应用商店"))
miniAppStore.clicked.connect(lambda: threading.Thread(target=MiniAppStore).start())
programManager.addWidget(QtWidgets.QLabel(" "*5), 1, 5, 1, 1)
programManager.addWidget(miniAppStore, 1, 6, 1, 1)
programManager.addWidget(QtWidgets.QLabel(" "*5), 1, 7, 1, 1)
getProgramStatus = QtWidgets.QPushButton(QtCore.QCoreApplication.translate("U", "获取该程序运行情况"))
getProgramStatus.clicked.connect(ProgramRunStatusShow.ShowWindow)
programManager.addWidget(getProgramStatus, 1, 8, 1, 1)
programManager.addItem(QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum), 1, 9, 1, 1)
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
sparkWineSetting.clicked.connect(lambda: threading.Thread(target=os.system, args=["/opt/durapps/spark-dwine-helper/spark-dwine-helper-settings/settings.sh"]).start())
programManager.addWidget(sparkWineSetting, 3, 6, 1, 1)
wineAutoConfig = QtWidgets.QPushButton(QtCore.QCoreApplication.translate("U", "自动/手动配置 Wine 容器"))
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
returnText.setStyleSheet("""
background-color: black;
color: white;
""")
returnText.setText(QtCore.QCoreApplication.translate("U", "在此可以看到wine安装应用时的终端输出内容"))
mainLayout.setRowStretch(0, 2)
mainLayout.setRowStretch(1, 1)
mainLayout.setColumnStretch(0, 2)
mainLayout.setColumnStretch(1, 1)
mainLayout.addWidget(returnText, 0, 1, 2, 1)

# 版权
copy = QtWidgets.QLabel(f"""\n程序版本：{version}，<b>提示：Wine 无法运行所有的 Windows 程序，如果想要运行更多可执行程序，可以考虑虚拟机和双系统</b><br>
©2020~{time.strftime("%Y")} gfdgd xi、为什么您不喜欢熊出没和阿布呢""")
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
mainLayout.addWidget(programRun, 2, 1, 1, 1)

# 菜单栏
menu = window.menuBar()
programmenu = menu.addMenu(QtCore.QCoreApplication.translate("U", "程序(&P)"))
p1 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "安装 wine(&I)"))
installWineOnDeepin23 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "安装 wine(只限Deepin23)"))
installWineHQ = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "安装 WineHQ"))
installMoreWine = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "安装更多 Wine"))
p2 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "设置程序(&S)"))
p3 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "清空软件历史记录(&C)"))
cleanCache = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "清空软件缓存"))
cleanProgramUnuse = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "删除程序组件"))
p4 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "退出程序(&E)"))
programmenu.addAction(p1)
programmenu.addAction(installWineOnDeepin23)
programmenu.addAction(installWineHQ)
programmenu.addAction(installMoreWine)
programmenu.addSeparator()
programmenu.addAction(p2)
programmenu.addSeparator()
programmenu.addAction(p3)
programmenu.addAction(cleanCache)
programmenu.addAction(cleanProgramUnuse)
programmenu.addSeparator()
programmenu.addAction(p4)
p1.triggered.connect(InstallWine)
installWineOnDeepin23.triggered.connect(InstallWineOnDeepin23)
installWineHQ.triggered.connect(InstallWineHQ)
installMoreWine.triggered.connect(lambda: threading.Thread(target=os.system, args=[f"'{programPath}/wine/installwine'"]).start())
p2.triggered.connect(ProgramSetting.ShowWindow)
p3.triggered.connect(CleanProgramHistory)
cleanCache.triggered.connect(CleanProgramCache)
cleanProgramUnuse.triggered.connect(CleanProgram)
p4.triggered.connect(window.close)

wineOption = menu.addMenu(QtCore.QCoreApplication.translate("U", "Wine(&W)"))
w1 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "打开 Wine 容器目录"))
w2 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "安装常见字体"))
w3 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "安装自定义字体"))
w4 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "删除选择的 Wine 容器"))
cleanBottonUOS = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "清理 Wine 容器（基于 Wine 适配活动脚本）"))
w5 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "打包 wine 应用"))
w6 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "使用官方 Wine 适配活动的脚本进行打包"))
getDllOnInternet = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "从互联网获取DLL"))
w7 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "从镜像获取DLL（只支持官方安装镜像，DOS内核如 Windows 95 暂不支持）"))
updateGeek = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "从 Geek Uninstaller 官网升级程序"))
deleteDesktopIcon = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "删除所有 Wine 程序在启动器的快捷方式"))
wineOption.addAction(w1)
wineOption.addAction(w2)
wineOption.addAction(w3)
wineOption.addAction(w4)
wineOption.addAction(cleanBottonUOS)
wineOption.addSeparator()
wineOption.addAction(w5)
wineOption.addAction(w6)
wineOption.addSeparator()
wineOption.addAction(getDllOnInternet)
wineOption.addAction(w7)
wineOption.addSeparator()
wineOption.addAction(updateGeek)
wineOption.addSeparator()
wm1 = wineOption.addMenu(QtCore.QCoreApplication.translate("U", "在指定 Wine、容器安装组件"))
wm1_1 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "在指定wine、指定容器安装 .net framework"))
wm1_2 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "在指定wine、指定容器安装 Visual Studio C++"))
wm1_3 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "在指定wine、指定容器安装 MSXML"))
wm1_4 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "在指定wine、指定容器安装 gecko"))
wm1_5 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "在指定wine、指定容器安装 mono"))
wm1_6 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "在指定wine、指定容器安装其它运行库"))
wm1.addAction(wm1_1)
wm1.addAction(wm1_2)
wm1.addAction(wm1_3)
wm1.addAction(wm1_4)
wm1.addAction(wm1_5)
wm1.addAction(wm1_6)
wm2 = wineOption.addMenu(QtCore.QCoreApplication.translate("U", "在指定 Wine、容器运行基础应用"))
wm2_1 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "打开指定wine、指定容器的控制面板"))
wm2_2 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "打开指定wine、指定容器的浏览器"))
wm2_3 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "打开指定wine、指定容器的注册表"))
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
w8 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "设置 run_v3.sh 的文管为 Deepin 默认文管"))
w9 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "设置 run_v3.sh 的文管为 Wine 默认文管"))
w10 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "重新安装 deepin-wine-helper"))
w11 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "使用winetricks打开指定容器"))
wineOption.addAction(w8)
wineOption.addAction(w9)
wineOption.addAction(w10)
wineOption.addSeparator()
wineOption.addAction(w11)
wineOption.addSeparator()
wm3 = wineOption.addMenu(QtCore.QCoreApplication.translate("U", "启用/禁用 opengl"))
wm3_1 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "开启 opengl"))
wm3_2 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "禁用 opengl"))
wm3.addAction(wm3_1)
wm3.addAction(wm3_2)
wm4 = wineOption.addMenu(QtCore.QCoreApplication.translate("U", "安装/卸载 winbind"))
wm4_1 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "安装 winbind"))
wm4_2 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "卸载 winbind"))
wm4.addAction(wm4_1)
wm4.addAction(wm4_2)
dxvkMenu = wineOption.addMenu(QtCore.QCoreApplication.translate("U", "安装/卸载 DXVK"))
installDxvk = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "安装 DXVK"))
uninstallDxvk = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "卸载 DXVK"))
dxvkMenu.addAction(installDxvk)
dxvkMenu.addAction(uninstallDxvk)
wineOption.addAction(deleteDesktopIcon)
settingWineBottleCreateLink = wineOption.addMenu(QtCore.QCoreApplication.translate("U", "允许/禁止指定 wine 容器生成快捷方式"))
enabledWineBottleCreateLink = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "允许指定 wine 容器生成快捷方式"))
disbledWineBottleCreateLink = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "禁止指定 wine 容器生成快捷方式"))
settingWineBottleCreateLink.addAction(enabledWineBottleCreateLink)
settingWineBottleCreateLink.addAction(disbledWineBottleCreateLink)
w1.triggered.connect(OpenWineBotton)
w2.triggered.connect(InstallWineFont)
w3.triggered.connect(OpenWineFontPath)
w4.triggered.connect(DeleteWineBotton)
cleanBottonUOS.triggered.connect(CleanWineBottonByUOS)
w5.triggered.connect(BuildExeDeb)
w6.triggered.connect(UOSPackageScript)
getDllOnInternet.triggered.connect(GetDllFromInternet)
w7.triggered.connect(GetDllFromWindowsISO.ShowWindow)
updateGeek.triggered.connect(lambda: os.system(f"'{programPath}/launch.sh' deepin-terminal -C '\"{programPath}/UpdateGeek.sh\"' --keep-open"))
w8.triggered.connect(SetDeepinFileDialogDeepin)
w9.triggered.connect(SetDeepinFileDialogDefult)
w10.triggered.connect(SetDeepinFileDialogRecovery)
w11.triggered.connect(lambda: RunWinetricks())
wm1_1.triggered.connect(lambda: threading.Thread(target=InstallNetFramework).start())
wm1_2.triggered.connect(lambda: threading.Thread(target=InstallVisualStudioCPlusPlus).start())
wm1_3.triggered.connect(lambda: threading.Thread(target=InstallMSXML).start())
wm1_4.triggered.connect(lambda: threading.Thread(target=InstallMonoGecko, args=["gecko"]).start())
wm1_5.triggered.connect(lambda: threading.Thread(target=InstallMonoGecko, args=["mono"]).start())
wm1_6.triggered.connect(lambda: threading.Thread(target=InstallOther).start())
wm2_1.triggered.connect(lambda: RunWineProgram("control"))
wm2_2.triggered.connect(lambda: RunWineProgram("iexplore' 'https://www.deepin.org"))
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
deleteDesktopIcon.triggered.connect(DeleteDesktopIcon)
enabledWineBottleCreateLink.triggered.connect(lambda: RunWineProgram("reg' delete 'HKEY_CURRENT_USER\Software\Wine\DllOverrides' /v winemenubuilder.exe '/f"))
disbledWineBottleCreateLink.triggered.connect(lambda: RunWineProgram("reg' add 'HKEY_CURRENT_USER\Software\Wine\DllOverrides' /v winemenubuilder.exe '/f"))

virtualMachine = menu.addMenu(QtCore.QCoreApplication.translate("U", "虚拟机(&V)"))
v1 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "使用 Virtualbox 虚拟机运行 Windows 应用"))
virtualMachine.addAction(v1)
v1.triggered.connect(RunVM)

checkValue = menu.addMenu(QtCore.QCoreApplication.translate("U", "校验值计算(&S)"))
md5Value = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "MD5(&M)"))
sha1Value = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "SHA1(&M)"))
base64Value = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "Base64(建议小文件)(&B)"))
sha256Value = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "SHA256(&S)"))
sha512Value = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "SHA512(&S)"))
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
s1 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "360 沙箱云"))
s2 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "微步云沙箱"))
s3 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "VIRUSTOTAL"))
safeWebsize.addAction(s1)
safeWebsize.addAction(s2)
safeWebsize.addAction(s3)
s1.triggered.connect(lambda: webbrowser.open_new_tab("https://ata.360.net/"))
s2.triggered.connect(lambda: webbrowser.open_new_tab("https://s.threatbook.cn/"))
s3.triggered.connect(lambda: webbrowser.open_new_tab("https://www.virustotal.com/"))

help = menu.addMenu(QtCore.QCoreApplication.translate("U", "帮助(&H)"))
runStatusWebSize = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "查询程序在 Wine 的运行情况"))
h1 = help.addMenu(QtCore.QCoreApplication.translate("U", "程序官网"))
h2 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "小提示"))
h3 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "更新内容"))
h4 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "谢明名单"))
h5 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "更新这个程序"))
h6 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "反馈这个程序的建议和问题"))
h7 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "关于这个程序"))
h8 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "关于 Qt"))
gfdgdxiio = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "作者个人站"))
gitee = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "Gitee"))
github = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "Github"))
gitlink = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "Gitlink"))
gitlab = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "Gitlab"))
jihu = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "极狐"))
h1.addAction(gfdgdxiio)
h1.addAction(gitee)
h1.addAction(github)
h1.addAction(gitlink)
h1.addAction(gitlab)
h1.addAction(jihu)
help.addSeparator()
help.addAction(runStatusWebSize)
help.addSeparator()
help.addAction(h2)
help.addAction(h3)
help.addAction(h4)
help.addSeparator()
videoHelp = help.addMenu(QtCore.QCoreApplication.translate("U", "视频教程"))
easyHelp = QtWidgets.QAction("简易使用教程")
buildHelp = QtWidgets.QAction("打包教程")
videoHelp.addAction(easyHelp)
videoHelp.addAction(buildHelp)
help.addSeparator()
help.addAction(h5)
help.addAction(h6)
help.addAction(h7)
help.addAction(h8)
help.addSeparator()
hm1 = help.addMenu(QtCore.QCoreApplication.translate("U", "更多生态适配应用"))
hm1_1 = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "运行 Android 应用：UEngine 运行器"))
hm1.addAction(hm1_1)
gfdgdxiio.triggered.connect(lambda: webbrowser.open_new_tab("https://gfdgd-xi.github.io"))
gitee.triggered.connect(lambda: webbrowser.open_new_tab("https://gitee.com/gfdgd-xi/deep-wine-runner"))
github.triggered.connect(lambda: webbrowser.open_new_tab("https://github.com/gfdgd-xi/deep-wine-runner"))
gitlink.triggered.connect(lambda: webbrowser.open_new_tab("https://gitlink.org.cn/gfdgd_xi/deep-wine-runner"))
gitlab.triggered.connect(lambda: webbrowser.open_new_tab("https://gitlab.com/gfdgd-xi/deep-wine-runner"))
jihu.triggered.connect(lambda: webbrowser.open_new_tab("https://jihulab.com//gfdgd-xi/deep-wine-runner"))
runStatusWebSize.triggered.connect(lambda: webbrowser.open_new_tab("https://gfdgd-xi.github.io/wine-runner-info"))
h2.triggered.connect(helps)
h3.triggered.connect(UpdateThings)
h4.triggered.connect(ThankWindow)
easyHelp.triggered.connect(lambda: webbrowser.open_new_tab("https://www.bilibili.com/video/BV1ma411972Y"))
buildHelp.triggered.connect(lambda: webbrowser.open_new_tab("https://www.bilibili.com/video/BV1EU4y1k7zr"))
h5.triggered.connect(UpdateWindow.ShowWindow)
h6.triggered.connect(WineRunnerBugUpload)
h7.triggered.connect(about_this_program)
h8.triggered.connect(lambda: QtWidgets.QMessageBox.aboutQt(widget))
hm1_1.triggered.connect(lambda: webbrowser.open_new_tab("https://gitee.com/gfdgd-xi/uengine-runner"))

# 窗口设置
window.resize(widget.frameGeometry().width() * 2, widget.frameGeometry().height())
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
    [[p1, installWineOnDeepin23, installWineHQ, installMoreWine], f"{programPath}/InstallWineOnDeepin23.py"],
    [[w5], f"{programPath}/deepin-wine-packager.py"],
    [[w6], f"{programPath}/deepin-wine-packager-with-script.py"],
    [[p1, v1], f"{programPath}/RunVM.sh"],
    [[getProgramIcon, uninstallProgram, updateGeek, trasButton, miniAppStore, fontAppStore, wm1_1, wm1_2, wm1_3, wm1_6, w7, w2], f"{programPath}/geek.exe"],
]:
    if not os.path.exists(i[1]):
        for x in i[0]:
            x.setDisabled(True)
# 有些功能是非 X86 不适用的，需要屏蔽
if subprocess.getoutput("arch").lower() != "x86_64":
    p1.setDisabled(True)
    installWineOnDeepin23.setDisabled(True)
    installMoreWine.setEnabled(True)
    virtualMachine.setDisabled(True)
    v1.setDisabled(True)
    installWineHQ.setDisabled(True)
    pass
o1.setCurrentText(setting["DefultWine"])
e1.setEditText(setting["DefultBotton"])
e2.setEditText("")
combobox1.setEditText("")
if len(sys.argv) > 1 and sys.argv[1]:
    e2.setEditText(sys.argv[1])
if not os.path.exists("/opt/durapps/spark-dwine-helper/spark-dwine-helper-settings/settings.sh"):
    sparkWineSetting.setEnabled(False)
if o1.currentText() == "":
    # 一个 Wine 都没有却用 Wine 的功能
    # 还是要处理的，至少不会闪退
    wine["没有识别到任何Wine，请在菜单栏“程序”安装Wine或安装任意Wine应用"] = "没有识别到任何Wine，请在菜单栏“程序”安装Wine或安装任意Wine应用"
    canUseWine.append("没有识别到任何Wine，请在菜单栏“程序”安装Wine或安装任意Wine应用")
    o1.addItem("没有识别到任何Wine，请在菜单栏“程序”安装Wine或安装任意Wine应用")


sys.exit(app.exec_())
