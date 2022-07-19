#!/usr/bin/env python3
# 使用系统默认的 python3 运行
###########################################################################################
# 作者：gfdgd xi、为什么您不喜欢熊出没和阿布呢
# 版本：1.7.0
# 更新时间：2022年07月16日
# 感谢：感谢 wine 以及 deepin-wine 团队，提供了 wine 和 deepin-wine 给大家使用，让我能做这个程序
# 基于 Python3 的 tkinter 构建
###########################################################################################
#################
# 引入所需的库
#################
import os
import sys
import time
import json
import shutil
import requests
import threading
import traceback
import webbrowser
import subprocess
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets
import PIL.Image as Image
import PIL.ImageTk as ImageTk

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
    if not CheckProgramIsInstall(wine[o1.currentText()]):
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
        if e1.currentText() == "":
            wineBottonPath = setting["DefultBotton"]
        else:
            wineBottonPath = e1.currentText()
        option = ""
        if setting["Architecture"] != "Auto":
            option += f"WINEARCH={setting['Architecture']} "
        if not setting["Debug"]:
            option += "WINEDEBUG=-all "
        if setting["TerminalOpen"]:
            res = subprocess.Popen([f"'{programPath}/launch.sh' deepin-terminal -C \"WINEPREFIX='" + wineBottonPath + "' " + option + wine[o1.currentText()] + " '" + e2.currentText() + "' " + setting["WineOption"] + "\" --keep-open"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        else:
            res = subprocess.Popen(["WINEPREFIX='" + wineBottonPath + "' " + option + wine[o1.currentText()] + " '" + e2.currentText() + "' " + setting["WineOption"]], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # 实时读取程序返回
        #
        while res.poll() is None:
            try:
                text = res.stdout.readline().decode("utf8")
            except:
                text = ""
            self.signal.emit(text)
            print(text)
        findExeHistory.append(wineBottonPath)  # 将记录写进数组
        wineBottonHistory.append(e2.currentText())  # 将记录写进数组
        write_txt(get_home() + "/.config/deepin-wine-runner/FindExeHistory.json", str(json.dumps(ListToDictionary(findExeHistory))))  # 将历史记录的数组转换为字典并写入
        write_txt(get_home() + "/.config/deepin-wine-runner/WineBottonHistory.json", str(json.dumps(ListToDictionary(wineBottonHistory))))  # 将历史记录的数组转换为字典并写入
        self.showHistory.emit("")
        DisableButton(False)
  

# 显示“关于这个程序”窗口
def about_this_program()->"显示“关于这个程序”窗口":
    global about
    global title
    global iconPath
    QT.message = QtWidgets.QMainWindow()  
    messageWidget = QtWidgets.QWidget()
    QT.message.setWindowTitle(f"关于 {title}")
    messageLayout = QtWidgets.QGridLayout()
    messageLayout.addWidget(QtWidgets.QLabel(f"<img src='{iconPath}'>"), 0, 0, 1, 1, QtCore.Qt.AlignTop)
    aboutInfo = QtWidgets.QTextBrowser(messageWidget)
    aboutInfo.setHtml(about)
    messageLayout.addWidget(aboutInfo, 0, 1, 1, 1)
    ok = QtWidgets.QPushButton("确定")
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
    if combobox1.currentText() == "" or e2.currentText() == "":  # 判断文本框是否有内容
        QtWidgets.QMessageBox.information(widget, "提示", "没有填写需要使用 exe 应用或保存的文件名")
        return
    if not CheckProgramIsInstall(wine[o1.currentText()]):
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
        write_txt(get_home() + "/.local/share/applications/" + combobox1.currentText() + ".desktop", f'''[Desktop Entry]
Name={combobox1.currentText()}
Exec=env WINEPREFIX='{wineBottonPath}' {option} {wine[o1.currentText()]} '{e2.currentText()}' {setting["WineOption"]}
Icon={iconPath}
Type=Application
StartupNotify=true''') # 写入文本文档
        shellHistory.append(combobox1.currentText())  # 将记录写进数组
        write_txt(get_home() + "/.config/deepin-wine-runner/ShellHistory.json", str(json.dumps(ListToDictionary(shellHistory))))  # 将历史记录的数组转换为字典并写入
        combobox1.clear()
        combobox1.addItems(shellHistory)
        QtWidgets.QMessageBox.information(widget, "提示", "生成完成！")  # 显示完成对话框

# 生成 desktop 文件在桌面
# （第四个按钮的事件）
def make_desktop_on_desktop():
    if combobox1.currentText() == "" or e2.currentText() == "":  # 判断文本框是否有内容
        QtWidgets.QMessageBox.information(widget, "提示", "没有填写需要使用 exe 应用或保存的文件名")
        return
    if not CheckProgramIsInstall(wine[o1.currentText()]):
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
        os.mknod(get_desktop_path() + "/" + combobox1.currentText() + ".desktop")
        option = ""
        if setting["Architecture"] != "Auto":
            option += f"WINEARCH={setting['Architecture']} "
        if not setting["Debug"]:
            option += "WINEDEBUG=-all "
        write_txt(get_desktop_path() + "/" + combobox1.currentText() + ".desktop", f'''[Desktop Entry]
Name={combobox1.currentText()}
Exec=env WINEPREFIX='{wineBottonPath}' {option} {wine[o1.currentText()]} '{e2.currentText()}' {setting["WineOption"]}
Icon={iconPath}
Type=Application
StartupNotify=true''') # 写入文本文档
        shellHistory.append(combobox1.currentText())  # 将记录写进数组
        write_txt(get_home() + "/.config/deepin-wine-runner/ShellHistory.json", str(json.dumps(ListToDictionary(shellHistory))))  # 将历史记录的数组转换为字典并写入
        combobox1.clear()
        combobox1.addItems(shellHistory)
        QtWidgets.QMessageBox.information(widget, "提示", "生成完成！")  # 显示完成对话框

# 数组转字典
def ListToDictionary(list):
    dictionary = {}
    for i in range(len(list)):
        dictionary[i] = list[i]
    return dictionary

def CleanProgramHistory():
    if QtWidgets.QMessageBox.question(title="警告", message="删除后将无法恢复，你确定吗？\n删除后软件将会自动重启。") == QtWidgets.QMessageBox.Yes:
        shutil.rmtree(get_home() + "/.config/deepin-wine-runner")
        ReStartProgram()

# 重启本应用程序
def ReStartProgram():
    python = sys.executable
    os.execl(python, python, * sys.argv)

def KillProgram():
    os.system(f"killall {wine[o1.currentText()]} -9")
    os.system("killall winedbg -9")

def InstallWine():
    threading.Thread(target=os.system, args=[f"'{programPath}/launch.sh' deepin-terminal -e \"{programPath}/AllInstall.py\""]).start()

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
    QtWidgets.QMessageBox.information(widget, "提示", "如果安装字体？只需要把字体文件复制到此字体目录\n按下“OK”按钮可以打开字体目录")
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
        if setting["Architecture"] != "Auto":
            option += f"WINEARCH={setting['Architecture']} "
        if not setting["Debug"]:
            option += "WINEDEBUG=-all "
        if setting["TerminalOpen"]:
            res = subprocess.Popen([f"'{programPath}/launch.sh' deepin-terminal -C \"WINEPREFIX='" + wineBottonPath + "' " + option + wine[o1.currentText()] + " '" + self.wineProgram + "' " + setting["WineOption"] + "\" --keep-open"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        else:
            res = subprocess.Popen(["WINEPREFIX='" + wineBottonPath + "' " + option + wine[o1.currentText()] + " '" + self.wineProgram + "' " + setting["WineOption"]], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # 实时读取程序返回
        while res.poll() is None:
            try:
                text = res.stdout.readline().decode("utf8")
            except:
                text = ""
            self.signal.emit(text)
            print(text)
        if self.history:
            findExeHistory.append(wineBottonPath)  # 将记录写进数组
            wineBottonHistory.append(e2.currentText())  # 将记录写进数组
            write_txt(get_home() + "/.config/deepin-wine-runner/FindExeHistory.json", str(json.dumps(ListToDictionary(findExeHistory))))  # 将历史记录的数组转换为字典并写入
            write_txt(get_home() + "/.config/deepin-wine-runner/WineBottonHistory.json", str(json.dumps(ListToDictionary(wineBottonHistory))))  # 将历史记录的数组转换为字典并写入
            self.showHistory.emit("")
            #e1['value'] = findExeHistory
            #e2['value'] = wineBottonHistory
        if self.Disbled:
            DisableButton(False)

    
runProgram = None
def RunWineProgram(wineProgram, history = False, Disbled = True):
    global runProgram
    DisableButton(True)
    if not CheckProgramIsInstall(wine[o1.currentText()]):
        if QtWidgets.QMessageBox.question(title="提示", message="检查到您未安装这个 wine，是否继续使用这个 wine 运行？") == QtWidgets.QMessageBox.No:
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
        if setting["TerminalOpen"]:
            res = subprocess.Popen([f"'{programPath}/launch.sh' deepin-terminal -C \"WINEPREFIX='{wineBottonPath}' {option} WINE=" + subprocess.getoutput(f"which {wine[o1.currentText()]}").replace(" ", "").replace("\n", "") + " winetricks --gui\" --keep-open"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
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
    if not CheckProgramIsInstall(wine[o1.currentText()]):
        if QtWidgets.QMessageBox.question(widget, "提示", "检查到您未安装这个 wine，是否继续使用这个 wine 运行？") == QtWidgets.QMessageBox.No:
            DisableButton(False)
            return
    returnText.setText("")
    runWinetricks = RunWinetricksThread()
    runWinetricks.signal.connect(QT.ShowWineReturn)
    runWinetricks.start()
    
    

def InstallMonoGecko(program):
    DisableButton(True)
    if e1.currentText() == "":
        wineBottonPath = setting["DefultBotton"]
    else:
        wineBottonPath = e1.currentText()
    os.system(f"'{programPath}/launch.sh' deepin-terminal -C \"'{programPath}/InstallMono.py' '{wineBottonPath}' {wine[o1.currentText()]} {program}\" --keep-open")
    DisableButton(False)

def InstallNetFramework():
    DisableButton(True)
    if e1.currentText() == "":
        wineBottonPath = setting["DefultBotton"]
    else:
        wineBottonPath = e1.currentText()
    os.system(f"'{programPath}/launch.sh' deepin-terminal -C \"'{programPath}/InstallNetFramework.py' '{wineBottonPath}' {wine[o1.currentText()]}\" --keep-open")
    DisableButton(False)

def InstallVisualStudioCPlusPlus():
    DisableButton(True)
    if e1.currentText() == "":
        wineBottonPath = setting["DefultBotton"]
    else:
        wineBottonPath = e1.currentText()
    os.system(f"'{programPath}/launch.sh' deepin-terminal -C \"'{programPath}/InstallVisualCPlusPlus.py' '{wineBottonPath}' {wine[o1.currentText()]}\" --keep-open")
    DisableButton(False)

def InstallMSXML():
    DisableButton(True)
    if e1.currentText() == "":
        wineBottonPath = setting["DefultBotton"]
    else:
        wineBottonPath = e1.currentText()
    os.system(f"'{programPath}/launch.sh' deepin-terminal -C \"'{programPath}/InstallMsxml.py' '{wineBottonPath}' {wine[o1.currentText()]}\" --keep-open")
    DisableButton(False)

def InstallOther():
    DisableButton(True)
    if e1.currentText()== "":
        wineBottonPath = setting["DefultBotton"]
    else:
        wineBottonPath = e1.currentText()
    os.system(f"'{programPath}/launch.sh' deepin-terminal -C \"'{programPath}/InstallOther.py' '{wineBottonPath}' {wine[o1.currentText()]}\" --keep-open")
    DisableButton(False)

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
    threading.Thread(target=os.system, args=[f"'{programPath}/launch.sh' deepin-terminal -C 'pkexec \"{programPath}/deepin-wine-venturi-setter.py\" recovery' --keep-open"]).start()

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
    threading.Thread(target=os.system, args=[f"'{programPath}/launch.sh' deepin-terminal -C 'echo 这些字体来自星火应用商店 && sudo ss-apt-fast install ms-core-fonts winfonts -y' --keep-open"]).start()

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

class UpdateWindow():
    data = {}
    update = None
    def ShowWindow():
        UpdateWindow.update = QtWidgets.QMainWindow()
        updateWidget = QtWidgets.QWidget()
        updateWidgetLayout = QtWidgets.QGridLayout()
        versionLabel = QtWidgets.QLabel(f"当前版本：{version}\n最新版本：未知\n更新内容：")
        updateText = QtWidgets.QTextBrowser()
        ok = QtWidgets.QPushButton("更新（更新过程中会关闭所有Python应用，包括这个应用）")
        ok.clicked.connect(UpdateWindow.Update)
        cancel = QtWidgets.QPushButton("取消")
        cancel.clicked.connect(UpdateWindow.update.close)
        try:
            UpdateWindow.data = json.loads(requests.get("http://120.25.153.144/spark-deepin-wine-runner/update.json").text)
            versionLabel = QtWidgets.QLabel(f"当前版本：{version}\n最新版本：{UpdateWindow.data['Version']}\n更新内容：")
            if UpdateWindow.data["Version"] == version:
                updateText.setText("此为最新版本，无需更新")
                ok.setDisabled(True)
            else:
                updateText.setText(UpdateWindow.data["New"].replace("\\n", "\n"))
        except:
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(updateWidget, "错误", "无法连接服务器！")
        updateWidgetLayout.addWidget(versionLabel, 0, 0, 1, 1)
        updateWidgetLayout.addWidget(updateText, 1, 0, 1, 3)
        updateWidgetLayout.addWidget(ok, 2, 2, 1, 1)
        updateWidgetLayout.addWidget(cancel, 2, 1, 1, 1)
        updateWidget.setLayout(updateWidgetLayout)
        UpdateWindow.update.setCentralWidget(updateWidget)
        UpdateWindow.update.setWindowTitle("检查更新")
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
        os.system(f"'{programPath}/launch.sh' deepin-terminal -e pkexec bash /tmp/spark-deepin-wine-runner/update.sh")

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
    def ShowWindow():
        #DisableButton(True)
        GetDllFromWindowsISO.message = QtWidgets.QMainWindow()
        widget = QtWidgets.QWidget()
        widgetLayout = QtWidgets.QGridLayout()
        if not e1.currentText() == "":
            GetDllFromWindowsISO.wineBottonPath = e1.currentText()
        widgetLayout.addWidget(QtWidgets.QLabel(f"""提示：
    目前本提取功能只支持 Windows XP 以及 Windows Server 2003 等老系统的官方安装镜像，只支持读取 i386 安装方法的安装镜像，不支持读取 wim、ghost 安装方式
    以及不要拷贝/替换太多的 dll，否则可能会导致 wine 容器异常
    最后，拷贝/替换 dll 后，建议点击下面“设置 wine 容器”按钮==》函数库 进行设置
当前选择的 Wine 容器：{GetDllFromWindowsISO.wineBottonPath}"""), 0, 0, 1, 5)
        isoLabel = QtWidgets.QLabel("ISO镜像：")
        GetDllFromWindowsISO.isoPath = QtWidgets.QComboBox()
        GetDllFromWindowsISO.browser = QtWidgets.QPushButton("浏览")
        isoControl = QtWidgets.QWidget()
        isoControlLayout = QtWidgets.QHBoxLayout()
        isoControl.setLayout(isoControlLayout)
        dllControl = QtWidgets.QWidget()
        dllControlLayout = QtWidgets.QHBoxLayout()
        dllControl.setLayout(dllControlLayout)
        GetDllFromWindowsISO.mountButton = QtWidgets.QPushButton("读取/挂载ISO镜像")
        umountButton = QtWidgets.QPushButton("关闭/卸载ISO镜像")
        GetDllFromWindowsISO.dllFound = QtWidgets.QComboBox()
        GetDllFromWindowsISO.foundButton = QtWidgets.QPushButton("查找")
        GetDllFromWindowsISO.dllList = QtWidgets.QListView()
        GetDllFromWindowsISO.saveDll = QtWidgets.QPushButton("保存到 wine 容器中")
        GetDllFromWindowsISO.setWineBotton = QtWidgets.QPushButton("设置 wine 容器")
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
        widgetLayout.addWidget(QtWidgets.QLabel("查找DLL\n（为空则代表不查找，\n将显示全部内容）："), 3, 0, 1, 1)
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
                for i in os.listdir("/tmp/wine-runner-getdll/i386"):
                    if i[-3:] == "dl_":
                        findList.append(i[:-1] + "l")    
                return
            for i in os.listdir("/tmp/wine-runner-getdll/i386"):
                if found in i[:-1] + "l":
                    findList.append(i[:-1] + "l")  
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
            except:
                # 如果无法删除可能是挂载了文件
                os.system("pkexec umount /tmp/wine-runner-getdll")
                try:
                    os.rmdir("/tmp/wine-runner-getdll")
                except:
                    traceback.print_exc()
                    QtWidgets.QMessageBox.critical(GetDllFromWindowsISO.message, "错误", traceback.format_exc())
                    return
        os.makedirs("/tmp/wine-runner-getdll")
        os.system(f"pkexec mount '{GetDllFromWindowsISO.isoPath.currentText()}' /tmp/wine-runner-getdll")
        findList = []
        try:
            for i in os.listdir("/tmp/wine-runner-getdll/i386"):
                if i[-3:] == "dl_":
                    findList.append(i[:-1] + "l")     
        except:
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(GetDllFromWindowsISO.message, "错误", f"镜像内容读取/挂载失败，报错如下：\n{traceback.format_exc()}")
            return
        GetDllFromWindowsISO.dllListModel.setStringList(findList)
        GetDllFromWindowsISO.DisbledDown(False)  
        GetDllFromWindowsISO.DisbledUp(True)
        GetDllFromWindowsISO.mount = True
        isoPath.append(GetDllFromWindowsISO.isoPath.currentText())  # 将记录写进数组
        write_txt(get_home() + "/.config/deepin-wine-runner/ISOPath.json", str(json.dumps(ListToDictionary(isoPath))))  # 将历史记录的数组转换为字典并写入
        GetDllFromWindowsISO.isoPath.clear()
        GetDllFromWindowsISO.isoPath.addItems(isoPath)
        #GetDllFromWindowsISO.isoPath['value'] = isoPath

    def UmountDisk():
        os.system("pkexec umount /tmp/wine-runner-getdll")
        try:
            shutil.rmtree("/tmp/wine-runner-getdll")
        except:
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(GetDllFromWindowsISO.message, "错误", f"关闭/卸载镜像失败，报错如下：\n{traceback.format_exc()}")
            return
        GetDllFromWindowsISO.DisbledDown(True)
        GetDllFromWindowsISO.DisbledUp(False)
        GetDllFromWindowsISO.mount = False
        QtWidgets.QMessageBox.information(GetDllFromWindowsISO.message, "提示", "关闭/卸载成功！")

    def CopyDll():
        choose = GetDllFromWindowsISO.dllList.selectionModel().selectedIndexes()[0].data()
        if os.path.exists(f"{GetDllFromWindowsISO.wineBottonPath}/drive_c/windows/system32/{choose}"):
            if QtWidgets.QMessageBox.question(title="提示", message=f"DLL {choose} 已经存在，是否覆盖？") == QtWidgets.QMessageBox.No:
                return
        try:
            shutil.copy(f"/tmp/wine-runner-getdll/i386/{choose[:-1]}_", f"{GetDllFromWindowsISO.wineBottonPath}/drive_c/windows/system32/{choose}")
            QtWidgets.QMessageBox.information(GetDllFromWindowsISO.message, "提示", "提取成功！")
        except:
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(GetDllFromWindowsISO.message, "错误", traceback.format_exc())
            
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
    def ShowWindow():
        ProgramSetting.message = QtWidgets.QMainWindow()
        widget = QtWidgets.QWidget()
        widgetLayout = QtWidgets.QGridLayout()
        widgetLayout.addWidget(QtWidgets.QLabel("选择 Wine 容器版本："), 0, 0, 1, 1)
        widgetLayout.addWidget(QtWidgets.QLabel("wine DEBUG 信息输出："), 1, 0, 1, 1)
        widgetLayout.addWidget(QtWidgets.QLabel("默认 Wine："), 2, 0, 1, 1)
        widgetLayout.addWidget(QtWidgets.QLabel("默认 Wine 容器："), 3, 0, 1, 1)
        widgetLayout.addWidget(QtWidgets.QLabel("使用终端打开："), 4, 0, 1, 1)
        widgetLayout.addWidget(QtWidgets.QLabel("自定义 wine 参数："), 5, 0, 1, 1)
        ProgramSetting.wineBottonA = QtWidgets.QComboBox()
        ProgramSetting.wineDebug = QtWidgets.QCheckBox("开启 DEBUG 输出")
        ProgramSetting.defultWine = QtWidgets.QComboBox()
        ProgramSetting.defultBotton = QtWidgets.QLineEdit()
        save = QtWidgets.QPushButton("保存")
        save.clicked.connect(ProgramSetting.Save)
        defultBottonButton = QtWidgets.QPushButton("浏览")
        defultBottonButton.clicked.connect(ProgramSetting.Browser)
        ProgramSetting.terminalOpen = QtWidgets.QCheckBox("使用终端打开（deepin 终端）")
        ProgramSetting.wineOption = QtWidgets.QLineEdit()
        ProgramSetting.wineBottonA.addItems(["Auto", "win32", "win64"])
        ProgramSetting.wineBottonA.setCurrentText(setting["Architecture"])
        ProgramSetting.wineDebug.setChecked(setting["Debug"])
        ProgramSetting.defultWine.addItems(wine.keys())
        ProgramSetting.defultWine.setCurrentText(setting["DefultWine"])
        ProgramSetting.defultBotton.setText(setting["DefultBotton"])
        ProgramSetting.terminalOpen.setChecked(setting["TerminalOpen"])
        ProgramSetting.wineOption.setText(setting["WineOption"])
        widgetLayout.addWidget(ProgramSetting.wineBottonA, 0, 1, 1, 1)
        widgetLayout.addWidget(ProgramSetting.wineDebug, 1, 1, 1, 1)
        widgetLayout.addWidget(ProgramSetting.defultWine, 2, 1, 1, 1)
        widgetLayout.addWidget(ProgramSetting.defultBotton, 3, 1, 1, 1)
        widgetLayout.addWidget(defultBottonButton, 3, 2, 1, 1)
        widgetLayout.addWidget(ProgramSetting.terminalOpen, 4, 1, 1, 1)
        widgetLayout.addWidget(ProgramSetting.wineOption, 5, 1, 1, 1)
        widgetLayout.addWidget(save, 6, 2, 1, 1)
        widget.setLayout(widgetLayout)
        ProgramSetting.message.setCentralWidget(widget)
        ProgramSetting.message.setWindowTitle(f"设置 wine 运行器 {version}")
        ProgramSetting.message.show()
        return

    def Browser():
        path = QtWidgets.QFileDialog.getExistingDirectory(ProgramSetting.message, "选择 Wine 容器", json.loads(readtxt(get_home() + "/.config/deepin-wine-runner/WineBotton.json"))["path"])
        if path == "" or path == None or path == "()" or path == ():
            return
        ProgramSetting.defultBotton.setText(path)

    def Save():
        # 写入容器位数设置
        setting["Architecture"] = ProgramSetting.wineBottonA.currentText()
        setting["Debug"] = ProgramSetting.wineDebug.isChecked()
        setting["DefultWine"] = ProgramSetting.defultWine.currentText()
        setting["DefultBotton"] = ProgramSetting.defultBotton.text()
        setting["TerminalOpen"] = ProgramSetting.terminalOpen.isChecked()
        setting["WineOption"] = ProgramSetting.wineOption.text()
        try:
            write_txt(get_home() + "/.config/deepin-wine-runner/WineSetting.json", json.dumps(setting))
        except:
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(ProgramSetting.message, "错误", traceback.format_exc())
            return
        QtWidgets.QMessageBox.information(ProgramSetting.message, "提示", "保存完毕！")

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
    "CenterWindow": False
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
# 如果要添加其他 wine，请在字典添加其名称和执行路径
try:
    wine = {"deepin-wine": "deepin-wine", "deepin-wine5": "deepin-wine5", "wine": "wine", "wine64": "wine64", "deepin-wine5 stable": "deepin-wine5-stable", "deepin-wine6 stable": "deepin-wine6-stable", "spark-wine7-devel": "spark-wine7-devel", "ukylin-wine": "ukylin-wine"}
    shellHistory = list(json.loads(readtxt(get_home() + "/.config/deepin-wine-runner/ShellHistory.json")).values())
    findExeHistory = list(json.loads(readtxt(get_home() + "/.config/deepin-wine-runner/FindExeHistory.json")).values())
    wineBottonHistory = list(json.loads(readtxt(get_home() + "/.config/deepin-wine-runner/WineBottonHistory.json")).values())
    isoPath = list(json.loads(readtxt(get_home() + "/.config/deepin-wine-runner/ISOPath.json")).values())
    isoPathFound = list(json.loads(readtxt(get_home() + "/.config/deepin-wine-runner/ISOPathFound.json")).values())
    setting = json.loads(readtxt(get_home() + "/.config/deepin-wine-runner/WineSetting.json"))
    change = False
    for i in ["Architecture", "Debug", "DefultWine", "DefultBotton", "TerminalOpen", "WineOption", "WineBottonDifferent", "CenterWindow"]:
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

###########################
# 程序信息
###########################
programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
iconPath = "{}/icon.png".format(programPath)
programUrl = "https://gitee.com/gfdgd-xi/deep-wine-runner\nhttps://github.com/gfdgd-xi/deep-wine-runner\nhttps://www.gitlink.org.cn/gfdgd_xi/deep-wine-runner"
information = json.loads(readtxt(f"{programPath}/information.json"))
version = information["Version"]
goodRunSystem = "Linux"
thankText = ""
tips = '''提示：
1、使用终端运行该程序，可以看到 wine 以及程序本身的提示和报错;
2、wine 32 位和 64 位的容器互不兼容;
3、所有的 wine 和 winetricks 均需要自行安装（可以从 菜单栏=>程序 里面进行安装）
4、本程序支持带参数运行 wine 程序（之前版本也可以），只需要按以下格式即可：
exe路径\' 参数 \'
即可（单引号需要输入）
5、wine 容器如果没有指定，则会默认为 ~/.wine'''
updateThingsString = '''※1、界面大改造，从使用 Tkinter 改为 Qt，参考了 @134******28 和 @sgb76 提供的设计方案和代码
※2、添加了基于 UOS 生态适配活动打包脚本的打包器，以及基于 Virtualbox 的简易 Windows 镜像安装工具
※3、将 pip 由阿里源改为华为源，提升下载安装速度，并删除使用 pip 下载库的功能（已不需要，废弃）
4、添加 @delsin 和 @神末shenmo 建议的 postrm 脚本
5、优化多屏窗口居中问题
6、修复 1.6.0 程序无法保存设置的问题
7、修复 1.6.0 的更新程序无法正常更新的问题
8、升级 Geek Uninstaller 版本
'''
for i in information["Thank"]:
    thankText += f"{i}\n"
updateTime = "2022年07月18日"
about = f'''<h1>关于</h1>
<pre>一个基于 Python3 的 tkinter 制作的 wine 运行器

版本：{version}
适用平台：{goodRunSystem}
Qt 版本：{QtCore.qVersion()}
程序官网：{programUrl}</pre>
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
title = "wine 运行器 {}".format(version)
updateThings = "{} 更新内容：\n{}\n更新时间：{}".format(version, updateThingsString, updateTime, time.strftime("%Y"))


###########################
# 窗口创建
###########################
# 因为没有完全改完，所以需要这些东西来兼容 tkinter 的主题
# 读取主题
# Qt 窗口
app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QMainWindow()
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
fastLabel = QtWidgets.QLabel("快速启动")
fastLabel.setStyleSheet("font: 30px;")
leftUpLayout.addWidget(fastLabel, 0, 0, 1, 2)
leftUpLayout.addWidget(QtWidgets.QLabel("<hr>"), 1, 0, 1, 2)
leftUpLayout.addWidget(QtWidgets.QLabel("请选择容器路径："), 2, 0, 1, 1)
e1 = QtWidgets.QComboBox()
e1.setEditable(True)
leftUpLayout.addWidget(e1, 3, 0, 1, 1)
button1 = QtWidgets.QPushButton("浏览")
button1.clicked.connect(liulanbutton)
leftUpLayout.addWidget(button1, 3, 1, 1, 1)
leftUpLayout.addWidget(QtWidgets.QLabel("请选择要执行的程序："), 4, 0, 1, 1)
e2 = QtWidgets.QComboBox()
e2.setEditable(True)
leftUpLayout.addWidget(e2, 5, 0, 1, 1)
button2 = QtWidgets.QPushButton("浏览")
button2.clicked.connect(liulanexebutton)
leftUpLayout.addWidget(button2, 5, 1, 1, 1)
leftUpLayout.addWidget(QtWidgets.QLabel("请选择WINE版本："), 6, 0, 1, 1)
o1 = QtWidgets.QComboBox()
leftUpLayout.addWidget(o1, 7, 0, 1, 1)
# 设置空间权重
button1.setSizePolicy(size)
button2.setSizePolicy(size)


leftDown = QtWidgets.QWidget()
mainLayout.addWidget(leftDown, 1, 0, 1, 1)
leftDownLayout = QtWidgets.QVBoxLayout()
leftDown.setLayout(leftDownLayout)
highLabel = QtWidgets.QLabel("高级功能")
highLabel.setStyleSheet("font: 30px;")
leftDownLayout.addWidget(highLabel)
leftDownLayout.addWidget(QtWidgets.QLabel("<hr>"))
leftDownLayout.addWidget(QtWidgets.QLabel("创建快捷方式（Desktop文件）："))
createDesktopLink = QtWidgets.QHBoxLayout()
label_r_2 = QtWidgets.QLabel("名称：")
createDesktopLink.addWidget(label_r_2)
combobox1 = QtWidgets.QComboBox()
combobox1.setEditable(True)
createDesktopLink.addWidget(combobox1)
button5 = QtWidgets.QPushButton("创建到桌面")
button5.clicked.connect(make_desktop_on_desktop)
createDesktopLink.addWidget(button5)
saveDesktopFileOnLauncher = QtWidgets.QPushButton("创建到开始菜单")
saveDesktopFileOnLauncher.clicked.connect(make_desktop_on_launcher)
createDesktopLink.addWidget(saveDesktopFileOnLauncher)
leftDownLayout.addLayout(createDesktopLink)
programManager = QtWidgets.QGridLayout()
leftDownLayout.addLayout(programManager)
programManager.addWidget(QtWidgets.QLabel("程序管理："), 0, 0, 1, 1)
getProgramIcon = QtWidgets.QPushButton("提取图标")
getProgramIcon.clicked.connect(lambda: RunWineProgram(f"{programPath}/BeCyIconGrabber.exe"))
programManager.addWidget(getProgramIcon, 1, 0, 1, 1)
programManager.addWidget(QtWidgets.QLabel(" "*5), 1, 1, 1, 1)
trasButton = QtWidgets.QPushButton("窗口透明工具")
trasButton.clicked.connect(lambda: RunWineProgram(f"{programPath}/窗体透明度设置工具.exe"))
programManager.addWidget(trasButton, 1, 2, 1, 1)
uninstallProgram = QtWidgets.QPushButton("卸载程序")
uninstallProgram.clicked.connect(lambda: RunWineProgram(f"{programPath}/geek.exe"))
programManager.addWidget(QtWidgets.QLabel(" "*5), 1, 3, 1, 1)
programManager.addWidget(uninstallProgram, 1, 4, 1, 1)
programManager.addItem(QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum), 1, 5, 1, 1)
programManager.addWidget(QtWidgets.QLabel("WINE配置："), 2, 0, 1, 1)
wineConfig = QtWidgets.QPushButton("配置容器")
wineConfig.clicked.connect(lambda: RunWineProgram("winecfg"))
programManager.addWidget(wineConfig, 3, 0, 1, 1)
button_r_6 = QtWidgets.QPushButton("安装字体")
button_r_6.clicked.connect(OpenWineFontPath)
programManager.addWidget(button_r_6, 3, 2, 1, 1)
sparkWineSetting = QtWidgets.QPushButton("星火wine配置")
sparkWineSetting.clicked.connect(lambda: threading.Thread(target=os.system, args=["/opt/durapps/spark-dwine-helper/spark-dwine-helper-settings/settings.sh"]).start())
programManager.addWidget(sparkWineSetting, 3, 4, 1, 1)
# 权重
button5.setSizePolicy(size)
saveDesktopFileOnLauncher.setSizePolicy(size)
label_r_2.setSizePolicy(size)
getProgramIcon.setSizePolicy(size)
trasButton.setSizePolicy(size)
#uninstallProgram.setSizePolicy(size)
wineConfig.setSizePolicy(size)

returnText = QtWidgets.QTextBrowser()
returnText.setStyleSheet("""
background-color: black;
color: white;
""")
returnText.setText("在此可以看到wine安装应用时的终端输出内容")
mainLayout.setRowStretch(0, 2)
mainLayout.setRowStretch(1, 1)
mainLayout.setColumnStretch(0, 2)
mainLayout.setColumnStretch(1, 1)
mainLayout.addWidget(returnText, 0, 1, 2, 1)

# 版权
copy = QtWidgets.QLabel(f"""\n程序版本：{version}
©2020~{time.strftime("%Y")} gfdgd xi、为什么您不喜欢熊出没和阿布呢""")
mainLayout.addWidget(copy, 2, 0, 1, 1)

# 程序运行
programRun = QtWidgets.QWidget()
programRunLayout = QtWidgets.QHBoxLayout()
programRun.setLayout(programRunLayout)
programRunLayout.addItem(QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
button3 = QtWidgets.QPushButton("运行程序")
button3.clicked.connect(runexebutton)
programRunLayout.addWidget(button3)
killProgram = QtWidgets.QPushButton("终止程序")
killProgram.clicked.connect(KillProgram)
programRunLayout.addWidget(killProgram)
mainLayout.addWidget(programRun, 2, 1, 1, 1)

# 菜单栏
menu = window.menuBar()
programmenu = menu.addMenu("程序(&P)")
p1 = QtWidgets.QAction("安装 wine(&I)")
p2 = QtWidgets.QAction("设置程序(&S)")
p3 = QtWidgets.QAction("清空软件历史记录(&C)")
p4 = QtWidgets.QAction("退出程序(&E)")
programmenu.addAction(p1)
programmenu.addSeparator()
programmenu.addAction(p2)
programmenu.addAction(p3)
programmenu.addSeparator()
programmenu.addAction(p4)
p1.triggered.connect(InstallWine)
p2.triggered.connect(ProgramSetting.ShowWindow)
p3.triggered.connect(CleanProgramHistory)
p4.triggered.connect(window.close)

wineOption = menu.addMenu("Wine(&W)")
w1 = QtWidgets.QAction("打开 Wine 容器目录")
w2 = QtWidgets.QAction("安装常见字体")
w3 = QtWidgets.QAction("安装自定义字体")
w4 = QtWidgets.QAction("删除选择的 Wine 容器")
w5 = QtWidgets.QAction("打包 wine 应用")
w6 = QtWidgets.QAction("使用官方 Wine 适配活动的脚本进行打包（测试只支持UOS）")
w7 = QtWidgets.QAction("从镜像获取DLL（只支持Windows XP、Windows Server 2003官方安装镜像）")
wineOption.addAction(w1)
wineOption.addAction(w2)
wineOption.addAction(w3)
wineOption.addAction(w4)
wineOption.addSeparator()
wineOption.addAction(w5)
wineOption.addAction(w6)
wineOption.addSeparator()
wineOption.addAction(w7)
wm1 = wineOption.addMenu("在指定 Wine、容器安装组件")
wm1_1 = QtWidgets.QAction("在指定wine、指定容器安装 .net framework")
wm1_2 = QtWidgets.QAction("在指定wine、指定容器安装 Visual Studio C++")
wm1_3 = QtWidgets.QAction("在指定wine、指定容器安装 MSXML")
wm1_4 = QtWidgets.QAction("在指定wine、指定容器安装 gecko")
wm1_5 = QtWidgets.QAction("在指定wine、指定容器安装 mono")
wm1_6 = QtWidgets.QAction("在指定wine、指定容器安装其它运行库")
wm1.addAction(wm1_1)
wm1.addAction(wm1_2)
wm1.addAction(wm1_3)
wm1.addAction(wm1_4)
wm1.addAction(wm1_5)
wm1.addAction(wm1_6)
wm2 = wineOption.addMenu("在指定 Wine、容器运行基础应用")
wm2_1 = QtWidgets.QAction("打开指定wine、指定容器的控制面板")
wm2_2 = QtWidgets.QAction("打开指定wine、指定容器的浏览器")
wm2_3 = QtWidgets.QAction("打开指定wine、指定容器的注册表")
wm2_4 = QtWidgets.QAction("打开指定wine、指定容器的任务管理器")
wm2_5 = QtWidgets.QAction("打开指定wine、指定容器的资源管理器")
wm2_6 = QtWidgets.QAction("打开指定wine、指定容器的关于 wine")
wm2.addAction(wm2_1)
wm2.addAction(wm2_2)
wm2.addAction(wm2_3)
wm2.addAction(wm2_4)
wm2.addAction(wm2_5)
wm2.addAction(wm2_6)
wineOption.addSeparator()
w8 = QtWidgets.QAction("设置 run_v3.sh 的文管为 Deepin 默认文管")
w9 = QtWidgets.QAction("设置 run_v3.sh 的文管为 Wine 默认文管")
w10 = QtWidgets.QAction("重新安装 deepin-wine-helper")
w11 = QtWidgets.QAction("使用winetricks打开指定容器")
wineOption.addAction(w8)
wineOption.addAction(w9)
wineOption.addAction(w10)
wineOption.addSeparator()
wineOption.addAction(w11)
wineOption.addSeparator()
wm3 = wineOption.addMenu("启用/禁用 opengl")
wm3_1 = QtWidgets.QAction("开启 opengl")
wm3_2 = QtWidgets.QAction("禁用 opengl")
wm3.addAction(wm3_1)
wm3.addAction(wm3_2)
wm4 = wineOption.addMenu("安装/卸载 winbind")
wm4_1 = QtWidgets.QAction("安装 winbind")
wm4_2 = QtWidgets.QAction("卸载 winbind")
wm4.addAction(wm4_1)
wm4.addAction(wm4_2)
w1.triggered.connect(OpenWineBotton)
w2.triggered.connect(InstallWineFont)
w3.triggered.connect(OpenWineFontPath)
w4.triggered.connect(DeleteWineBotton)
w5.triggered.connect(BuildExeDeb)
w6.triggered.connect(UOSPackageScript)
w7.triggered.connect(GetDllFromWindowsISO.ShowWindow)
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

virtualMachine = menu.addMenu("虚拟机(&V)")
v1 = QtWidgets.QAction("使用 Virtualbox 虚拟机运行 Windows 应用")
virtualMachine.addAction(v1)
v1.triggered.connect(RunVM)

safeWebsize = menu.addMenu("云沙箱(&C)")
s1 = QtWidgets.QAction("360 沙箱云")
s2 = QtWidgets.QAction("微步云沙箱")
s3 = QtWidgets.QAction("VIRUSTOTAL")
safeWebsize.addAction(s1)
safeWebsize.addAction(s2)
safeWebsize.addAction(s3)
s1.triggered.connect(lambda: webbrowser.open_new_tab("https://ata.360.net/"))
s2.triggered.connect(lambda: webbrowser.open_new_tab("https://s.threatbook.cn/"))
s3.triggered.connect(lambda: webbrowser.open_new_tab("https://www.virustotal.com/"))

help = menu.addMenu("帮助(&H)")
h1 = QtWidgets.QAction("程序官网")
h2 = QtWidgets.QAction("小提示")
h3 = QtWidgets.QAction("更新内容")
h4 = QtWidgets.QAction("谢明名单")
h5 = QtWidgets.QAction("更新这个程序")
h6 = QtWidgets.QAction("反馈这个程序的建议和问题")
h7 = QtWidgets.QAction("关于这个程序")
h8 = QtWidgets.QAction("关于 Qt")
help.addAction(h1)
help.addSeparator()
help.addAction(h2)
help.addAction(h3)
help.addAction(h4)
help.addSeparator()
help.addAction(h5)
help.addAction(h6)
help.addAction(h7)
help.addAction(h8)
help.addSeparator()
hm1 = help.addMenu("更多生态适配应用")
hm1_1 = QtWidgets.QAction("运行 Android 应用：UEngine 运行器")
hm1.addAction(hm1_1)
h1.triggered.connect(OpenProgramURL)
h2.triggered.connect(helps)
h3.triggered.connect(UpdateThings)
h4.triggered.connect(ThankWindow)
h5.triggered.connect(UpdateWindow.ShowWindow)
h6.triggered.connect(WineRunnerBugUpload)
h7.triggered.connect(about_this_program)
h8.triggered.connect(lambda: QtWidgets.QMessageBox.aboutQt(widget))
hm1_1.triggered.connect(lambda: webbrowser.open_new_tab("https://gitee.com/gfdgd-xi/uengine-runner"))

# 窗口设置
window.resize(widget.frameGeometry().width() * 2, widget.frameGeometry().height())
widget.setLayout(mainLayout)
window.setWindowTitle(title)
window.setWindowIcon(QtGui.QIcon(f"{programPath}/icon.png"))
widget.show()
window.show()

# 控件设置
e1.addItems(findExeHistory)
e2.addItems(wineBottonHistory)
combobox1.addItems(shellHistory)
o1.addItems(wine.keys())
o1.setCurrentText(setting["DefultWine"])
e1.setEditText(setting["DefultBotton"])
e2.setEditText("")
combobox1.setEditText("")
if len(sys.argv) > 1 and sys.argv[1]:
    e2.setEditText(sys.argv[1])
if not os.path.exists("/opt/durapps/spark-dwine-helper/spark-dwine-helper-settings/settings.sh"):
    sparkWineSetting.setEnabled(False)
sys.exit(app.exec_())
