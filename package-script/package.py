#!/usr/bin/env python3
# 使用系统默认的 python3 运行
###########################################################################################
# 作者：gfdgd xi
# 版本：2.2.0
# 更新时间：2022年09月11日
# 感谢：感谢 wine 以及 deepin-wine 团队，提供了 wine 和 deepin-wine 给大家使用，让我能做这个程序
# 基于 Python3 的 tkinter 构建
###########################################################################################
#################
# 引入所需的库
#################
import os
import sys
import json
import threading
import webbrowser
import subprocess
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets
from trans import *

###################
# 程序所需事件
###################
# 读取文本文档
def readtxt(path):
    f = open(path, "r") # 设置文件对象
    str = f.read()  # 获取内容
    f.close()  # 关闭文本对象
    return str  # 返回结果

# 获取用户主目录
def get_home():
    return os.path.expanduser('~')

# 写入文本文档
def WriteTXT(path, things):
    file = open(path, 'w', encoding='UTF-8')  # 设置文件对象
    file.write(things)  # 写入文本
    file.close()  # 关闭文本对象

def DisbledOrEnabled(choose: bool):
    chineseName.setDisabled(choose)
    englishName.setDisabled(choose), 
    debDescription.setDisabled(choose)
    typeName.setDisabled(choose)
    exePath.setDisabled(choose) 
    packageName.setDisabled(choose)
    versionName.setDisabled(choose)
    buildDeb.setDisabled(choose)
    bottonName.setDisabled(choose)


class PackageDebThread(QtCore.QThread):
    signal = QtCore.pyqtSignal(str)
    info = QtCore.pyqtSignal(str)
    def __init__(self) -> None:
        super().__init__()

    def run(self):
        startupWMClassName = os.path.basename(exePath.text().replace("\\", "/"))
        print(startupWMClassName)
        WriteTXT(f"{programPath}/package-hshw.sh", f"""#!/bin/bash

#最终生成的包的描述
export app_description="{debDescription.text()}"
#应用程序英文名
export app_name="{englishName.text()}"
#应用程序中文名
export app_name_zh_cn="{chineseName.text()}"
#desktop文件中的分类
export desktop_file_categories="{typeName.currentText()};"
#desktop文件中StartupWMClass字段。用于让桌面组件将窗口类名与desktop文件相对应。这个值为实际运行的主程序EXE的文件名，wine/crossover在程序运行后会将文件名设置为窗口类名
export desktop_file_main_exe="{startupWMClassName}"
export exec_path="{exePath.text()}"
#最终生成的包的包名,包名的命名规则以deepin开头，加官网域名（需要前后对调位置），如还不能区分再加上应用名
export deb_package_name="{packageName.text()}"
#最终生成的包的版本号，版本号命名规则：应用版本号+deepin+数字
export deb_version_string="{versionName.text()}"
#读取和最终解压的包名
export bottle_name="{bottonName.text()}"

export package_depends="deepin-wine6-stable | deepin-wine6-stable-bcm | deepin-wine6-stable-dcm, spark-dwine-helper | store.spark-app.spark-dwine-helper"
export apprun_cmd="deepin-wine6-stable"
#export package_depends="deepin-wine5-stable | deepin-wine5-stable-bcm | deepin-wine5-stable-dcm, spark-dwine-helper | store.spark-app.spark-dwine-helper"
#export apprun_cmd="deepin-wine5-stable"

# rm -fr final.dir/
# rm -fr icons/
# rm -fr staging.dir/

./script-packager.sh $@
""")
        os.chdir(programPath)
        res = subprocess.Popen(["./package-hshw.sh"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # 实时读取程序返回
        while res.poll() is None:
            try:
                text = res.stdout.readline().decode("utf8")
            except:
                text = ""
            self.signal.emit(text)
            print(text, end="")
        self.info.emit("打包完成！")
        DisbledOrEnabled(False)

class QT:
    run = None

def MessageBoxInformation(text):
    QtWidgets.QMessageBox.information(window, "提示", text)

def PackageDeb():
    DisbledOrEnabled(True)
    for i in [chineseName.text(), englishName.text(), debDescription.text(), typeName.currentText(), exePath.text(), packageName.text(), versionName.text()]:
        if i == "":
            QtWidgets.QMessageBox.information(widget, "提示", "您未填完所有信息，无法继续")
            DisbledOrEnabled(False)
            return
    commandReturn.setText("")
    global lockB
    lockB = False
    QT.run = PackageDebThread()
    QT.run.signal.connect(RunCommand)
    QT.run.info.connect(MessageBoxInformation)
    QT.run.start()

def RunCommand(command):
    if command.replace("\n", "").replace(" ", "") != "":
        commandReturn.append(command.replace("\n", ""))

def ShowHelp():
    QtWidgets.QMessageBox.information(widget, "帮助", f"下面是有关打包器的各个输入框的意义以及有关的 UOS 填写标准\n{tips}")

def OpenPackageFolder():
    os.system(f"xdg-open '{programPath}/package_save/uos'")

# 自动设置包名/容器名
lockB = False
def NameChange(packageOrBotton: int):
    global lockB
    # 0 代表包名
    # 1 代表容器名
    if packageOrBotton == 0 and not lockB:
        bottonName.setText(packageName.text())
    elif packageOrBotton == 1 and bottonName.text() != packageName.text():
        lockB = True

# 获取当前语言
def get_now_lang()->"获取当前语言":
    return os.getenv('LANG')

###########################
# 程序信息
###########################
programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
information = json.loads(readtxt(f"{programPath}/information.json"))
version = information["Version"]
iconPath = "{}/deepin-wine-runner.svg".format(programPath)
# 语言载入
if not get_now_lang() == "zh_CN.UTF-8":
    transla = Trans("en_US", f"{programPath}/trans/packager.json")
else:
    transla = Trans("zh_CN")
tips = transla.transe("U", """第一个文本框是应用程序中文名
第二个文本框是应用程序英文名
第三个文本框是最终生成的包的描述
第四个选择框是desktop文件中的分类
第五个输入框是程序在 Wine 容器的位置，以 c:\\XXX 的形式，盘符必须小写，用反斜杠，如果路径带用户名的话会自动替换为$USER
而 StartupWMClass 字段将会由程序自动生成，作用如下：
desktop文件中StartupWMClass字段。用于让桌面组件将窗口类名与desktop文件相对应。这个值为实际运行的主程序EXE的文件名，wine/crossover在程序运行后会将文件名设置为窗口类名
第六个输入框是最终生成的包的包名,包名的命名规则以deepin开头，加官网域名（需要前后对调位置），如还不能区分再加上应用名
最后一个是最终生成的包的版本号，版本号命名规则：应用版本号+deepin+数字
提示：包名和容器名相同，无法设置为不相同，如果需要设置为不相同，需要用另一个非基于生态适配脚本的打包器
""")

###########################
# 窗口创建
###########################
app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QMainWindow()
widget = QtWidgets.QWidget()
widgetLayout = QtWidgets.QGridLayout()

size = QtWidgets.QSizePolicy()
size.setHorizontalPolicy(0)

chineseName = QtWidgets.QLineEdit()
englishName = QtWidgets.QLineEdit()
debDescription = QtWidgets.QLineEdit()
typeName = QtWidgets.QComboBox()
exePath = QtWidgets.QLineEdit()
packageName = QtWidgets.QLineEdit()
bottonName = QtWidgets.QLineEdit()
versionName = QtWidgets.QLineEdit()
controlFrame = QtWidgets.QHBoxLayout()
buildDeb = QtWidgets.QPushButton(transla.transe("U", "打包"))
debPath = QtWidgets.QPushButton(transla.transe("U", "deb 包生成目录"))
buildDeb.setSizePolicy(size)
debPath.setSizePolicy(size)
commandReturn = QtWidgets.QTextBrowser()
typeName.addItems(["Network", "Chat", "Audio", "Video", "Graphics", "Office", "Translation", "Development", "Utility", "Game", "AudioVideo", "System"])
controlFrame.addWidget(buildDeb)
controlFrame.addWidget(debPath)
widgetLayout.addWidget(QtWidgets.QLabel(transla.transe("U", "程序中文名：")), 0, 0, 1, 1)
widgetLayout.addWidget(QtWidgets.QLabel(transla.transe("U", "程序英文名：")), 1, 0, 1, 1)
widgetLayout.addWidget(QtWidgets.QLabel(transla.transe("U", "包描述：")), 2, 0, 1, 1)
widgetLayout.addWidget(QtWidgets.QLabel(transla.transe("U", "程序分类：")), 3, 0, 1, 1)
widgetLayout.addWidget(QtWidgets.QLabel(transla.transe("U", "程序在 Wine 容器的位置：")), 4, 0, 1, 1)
widgetLayout.addWidget(QtWidgets.QLabel(transla.transe("U", "包名：")), 5, 0, 1, 1)
widgetLayout.addWidget(QtWidgets.QLabel(transla.transe("U", "容器名：")), 6, 0, 1, 1)
widgetLayout.addWidget(QtWidgets.QLabel(transla.transe("U", "版本号：")), 7, 0, 1, 1)
widgetLayout.addWidget(chineseName, 0, 1, 1, 1)
widgetLayout.addWidget(englishName, 1, 1, 1, 1)
widgetLayout.addWidget(debDescription, 2, 1, 1, 1)
widgetLayout.addWidget(typeName, 3, 1, 1, 1)
widgetLayout.addWidget(exePath, 4, 1, 1, 1)
widgetLayout.addWidget(packageName, 5, 1, 1, 1)
widgetLayout.addWidget(bottonName, 6, 1, 1, 1)
widgetLayout.addWidget(versionName, 7, 1, 1, 1)
widgetLayout.addLayout(controlFrame, 8, 0, 1, 2)
widgetLayout.addWidget(commandReturn, 9, 0, 1, 2)
packageName.textChanged.connect(lambda: NameChange(0))
bottonName.textChanged.connect(lambda: NameChange(1))
buildDeb.clicked.connect(PackageDeb)
debPath.clicked.connect(OpenPackageFolder)
widget.setLayout(widgetLayout)
window.setCentralWidget(widget)
window.resize(int(window.frameGeometry().width() * 1.5), int(window.frameGeometry().height()))
window.setWindowIcon(QtGui.QIcon(iconPath))
menu = window.menuBar()
programMenu = menu.addMenu(transla.transe("U", "程序"))
exit = QtWidgets.QAction(transla.transe("U", "退出"))
exit.triggered.connect(window.close)
uploadSparkStore = menu.addMenu(transla.transe("U", "投稿到星火应用商店"))
uploadSparkStoreWebsize = QtWidgets.QAction(transla.transe("U", "从网页端投稿"))
if os.path.exists("/opt/spark-store-submitter/bin/spark-store-submitter"):
    uploadSparkStoreProgram = QtWidgets.QAction(transla.transe("U", "使用投稿器投稿（推荐）"))
else:
    uploadSparkStoreProgram = QtWidgets.QAction(transla.transe("U", "使用投稿器投稿（推荐，请先安装投稿器）"))
    uploadSparkStoreProgram.setDisabled(True)
uploadSparkStore.addAction(uploadSparkStoreProgram)
uploadSparkStore.addAction(uploadSparkStoreWebsize)
uploadSparkStoreWebsize.triggered.connect(lambda: webbrowser.open_new_tab("https://upload.deepinos.org"))
uploadSparkStoreProgram.triggered.connect(lambda: threading.Thread(target=os.system, args=["/opt/spark-store-submitter/bin/spark-store-submitter"]).start())
helpMenu = menu.addMenu(transla.transe("U", "帮助"))
help = QtWidgets.QAction(transla.transe("U", "帮助"))
help.triggered.connect(ShowHelp)
helpMenu.addAction(help)
programMenu.addAction(exit)
print(iconPath)
window.show()
chineseName.setWhatsThis(transla.transe("U", "应用程序中文名"))
englishName.setWhatsThis(transla.transe("U", "应用程序英文名"))
debDescription.setWhatsThis(transla.transe("U", "最终生成的包的描述"))
typeName.setWhatsThis(transla.transe("U", """点击右侧的下拉箭头，选择该软件所属的软件分类即可，常见软件分类名称释义：
Network=网络应用；
Chat=即时通讯或社交沟通；
Video=视频播放；
Graphics=图形图像；
Office=办公学习；
Translation=阅读翻译；
Development=软件开发；
Utility=工具软件或其他应用。
不明白英文的可以百度查询一下软件分类名称的意思。
注意：此时选择的软件分类名称决定了该软件打包后再安装时会安装在启动器中的哪个软件分类目录中。"""))
exePath.setWhatsThis("""程序在 Wine 容器的位置，以 c:\\XXX 的形式，盘符必须小写，用反斜杠，如果路径带用户名的话会自动替换为$USER
而 StartupWMClass 字段将会由程序自动生成，作用如下：
desktop文件中StartupWMClass字段。用于让桌面组件将窗口类名与desktop文件相对应。这个值为实际运行的主程序EXE的文件名，wine/crossover在程序运行后会将文件名设置为窗口类名""")
packageName.setWhatsThis(transla.transe("U", "最终生成的包的包名,包名的命名规则以deepin开头，加官网域名（需要前后对调位置），如还不能区分再加上应用名"))
bottonName.setWhatsThis(transla.transe("U", "容器名"))
versionName.setWhatsThis(transla.transe("U", "最终生成的包的版本号，版本号命名规则：应用版本号+deepin+数字"))
window.setWindowTitle(f"Wine 打包器 {version}——基于统信 Wine 生态活动打包脚本制作")
windowFrameInputValueList = [
    chineseName,
    englishName,
    debDescription,
    typeName,
    exePath,
    packageName,
    versionName
]
sys.exit(app.exec_())