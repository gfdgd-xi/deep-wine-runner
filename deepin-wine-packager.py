#!/usr/bin/env python3
#########################################################################
# 作者：gfdgd xi、为什么您不喜欢熊出没和阿布
# 版本：1.7.0
# 感谢：感谢 deepin-wine 团队，提供了 deepin-wine 给大家使用，让我能做这个程序
# 基于 Python3 的 tkinter 构建
#########################################################################
#################
# 引入所需的库
#################
import os
import sys
import json
import shutil
import random
import pathlib
import traceback
import subprocess
from PIL import Image
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets

#################
# 程序所需事件
#################

def button1_cl():
    path = QtWidgets.QFileDialog.getExistingDirectory(widget, "选择 wine 容器", f"{get_home()}/.deepinwine")
    if path != "":
        e6_text.setText(path)

def button2_cl():
    path = QtWidgets.QFileDialog.getOpenFileName(widget, "选择图标文件", get_home(), "PNG图标(*.png);;SVG图标(*.svg);;全部文件(*.*)")[0]
    if path != "":
        e9_text.setText(path)

def button4_cl():
    path = QtWidgets.QFileDialog.getSaveFileName(widget, "保存 deb 包", get_home(), "deb 文件(*.deb);;所有文件(*.*)", "{}_{}_i386.deb".format(e1_text.text(), e2_text.text()))[0]
    if path != "":
        e12_text.setText(path)

def disabled_or_NORMAL_all(choose):
    choose = not choose
    e1_text.setDisabled(choose)
    e2_text.setDisabled(choose)
    e3_text.setDisabled(choose)
    e4_text.setDisabled(choose)
    e5_text.setDisabled(choose)
    e6_text.setDisabled(choose)
    e7_text.setDisabled(choose)
    e8_text.setDisabled(choose)
    e9_text.setDisabled(choose)
    e10_text.setDisabled(choose)
    e12_text.setDisabled(choose)
    e15_text.setDisabled(choose)
    button1.setDisabled(choose)
    button2.setDisabled(choose)
    button4.setDisabled(choose)
    button5.setDisabled(choose)
    option1_text.setDisabled(choose)
    chooseWineHelperValue.setDisabled(choose)
    wineVersion.setDisabled(choose)
    
class QT:
    thread = None

def make_deb():
    clean_textbox1_things()
    disabled_or_NORMAL_all(False)
    if e1_text.text() == "" or e2_text.text() == "" or e3_text.text() == "" or e4_text.text() == "" or e5_text.text() == "" or e6_text.text() == "" or e7_text.text() == "" or e8_text.text() == "" or e12_text.text() == "":
        QtWidgets.QMessageBox.critical(widget, "错误", "必填信息没有填写完整，无法继续构建 deb 包")
        disabled_or_NORMAL_all(True)
        label13_text_change("必填信息没有填写完整，无法继续构建 deb 包")
        return
    if QtWidgets.QMessageBox.question(widget, "提示", "打包将会改动现在选择的容器，是否继续？") == QtWidgets.QMessageBox.No:
        disabled_or_NORMAL_all(True)
        return
    #thread = threading.Thread(target=make_deb_threading)
    QT.thread = make_deb_threading()
    QT.thread.signal.connect(chang_textbox1_things)
    QT.thread.label.connect(label13_text_change)
    QT.thread.start()
    #thread.start()


def label13_text_change(thing):
    label13_text.setText(f"<p align='center'>当前 deb 打包情况：{thing}</p>")

class make_deb_threading(QtCore.QThread):
    signal = QtCore.pyqtSignal(str)
    label = QtCore.pyqtSignal(str)
    def __init__(self) -> None:
        super().__init__()

    def run_command(self, command):
        res = subprocess.Popen([command], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # 实时读取程序返回
        while res.poll() is None:
            try:
                text = res.stdout.readline().decode("utf8")
            except:
                text = ""
            print(text, end="")
            self.signal.emit(text)

    def run(self):
        #####################################
        # 程序创建的 deb 构建临时文件夹目录树：
        # /XXX
        # ├── DEBIAN
        # │   ├── control
        # │   └── postrm
        # └── opt
        # └── apps
        #     └── XXX
        #         ├── entries
        #         │   ├── applications
        #         │   │   └── XXX.desktop
        #         │   └── icons
        #         │       └── hicolor
        #         │           └── scalable
        #         │               └── apps
        #         │                   └── XXX.png（XXX.svg）
        #         ├── files
        #         │   ├── files.7z
        #         │   └── run.sh
        #         └── info
        #
        # 11 directories, 7 files
        #####################################
        try:
            #####################
            # 判断文件是否存在
            #####################
            self.label.emit("正在检查文件是否存在并为后面步骤准备……")
            a = ""
            if e6_text.text() == "/":
                b = e6_text.text()[:-1]
            else:
                b = e6_text.text()
            if e9_text.text() != "":
                # 获取图片格式（不太准）
                try:
                    im = Image.open(e9_text.text())
                    imms = im.format.lower()
                except: # 未知（就直接设置为 svg 后缀）
                    imms = ".svg"
                a = "/opt/apps/{}/entries/icons/hicolor/scalable/apps/{}.{}".format(e1_text.text(), e1_text.text(), imms)
                if not os.path.exists(e9_text.text()):
                    QtWidgets.QMessageBox.critical(widget, "错误", "图标的路径填写错误，无法进行构建 deb 包")
                    disabled_or_NORMAL_all(True)
                    label13_text_change("图标的路径填写错误，无法进行构建 deb 包")
                    return
            if not os.path.exists(e6_text.text()):
                QtWidgets.QMessageBox.critical(widget, "错误", "路径填写错误，无法继续构建 deb 包")
                disabled_or_NORMAL_all(True)
                label13_text_change("图标的路径填写错误，无法进行构建 deb 包")
                return
            #############
            # 删除文件
            #############
            self.label.emit("正在删除对构建 deb 包有影响的文件……")
            debPackagePath = f"/tmp/{random.randint(0, 9999)}"
            self.run_command(f"rm -rfv /tmp/{debPackagePath}")
            ###############
            # 创建目录
            ###############
            self.label.emit("正在创建目录……")
            os.makedirs("{}/DEBIAN".format(debPackagePath))
            os.makedirs("{}/opt/apps/{}/entries/applications".format(debPackagePath, e1_text.text()))
            os.makedirs("{}/opt/apps/{}/entries/icons/hicolor/scalable/apps".format(debPackagePath, e1_text.text()))
            os.makedirs("{}/opt/apps/{}/files".format(debPackagePath, e1_text.text()))
            ###############
            # 创建文件
            ###############
            self.label.emit("正在创建文件……")
            os.mknod("{}/DEBIAN/control".format(debPackagePath))
            os.mknod("{}/opt/apps/{}/entries/applications/{}.desktop".format(debPackagePath, e1_text.text(), e1_text.text()))
            os.mknod("{}/opt/apps/{}/files/run.sh".format(debPackagePath, e1_text.text()))
            os.mknod("{}/opt/apps/{}/info".format(debPackagePath, e1_text.text()))
            ###############
            # 设置容器
            ###############
            self.label.emit("正在设置 wine 容器")
            os.chdir(b)
            self.run_command("sed -i \"s#$USER#@current_user@#\" ./*.reg")
            os.chdir(f"{b}/drive_c/users")
            self.run_command(f"mv -v '{os.getlogin()}' @current_user@")
            os.chdir(programPath)
            ###############
            # 压缩容器
            ###############
            self.label.emit("正在打包 wine 容器")
            self.run_command("7z a {}/opt/apps/{}/files/files.7z {}/*".format(debPackagePath, e1_text.text(), b))
            ###############
            # 复制图片
            ###############
            self.label.emit("正在复制文件……")
            self.run_command(f"cp -rv '{programPath}/dlls' {debPackagePath}/opt/apps/{e1_text.text()}/files/")
            if e9_text.text() != "":
                shutil.copy(e9_text.text(), "{}/opt/apps/{}/entries/icons/hicolor/scalable/apps/{}.{}".format(debPackagePath, e1_text.text(), e1_text.text(), imms))
            ################
            # 获取文件大小
            ################
            self.label.emit("正在计算文件大小……")
            size = getFileFolderSize(debPackagePath) / 1024
            ################
            # 写入文本文档
            ################
            self.label.emit("正在写入文件……")
            if not chooseWineHelperValue.isChecked():
                write_txt("{}/DEBIAN/control".format(debPackagePath), '''Package: {}
Version: {}
Architecture: i386
Maintainer: {}
Depends: {}, deepin-wine-helper (>= 5.1.30-1), fonts-wqy-microhei, fonts-wqy-zenhei
Section: non-free/otherosfs
Priority: optional
Multi-Arch: foreign
Description: {}
'''.format(e1_text.text(), e2_text.text(), e4_text.text(), wineVersion.currentText(), e3_text.text()))
            else:
                write_txt("{}/DEBIAN/postrm".format(debPackagePath), '''Package: {}
Version: {}
Architecture: i386
Maintainer: {}
Depends: {}, spark-dwine-helper (>= 1.6.2), fonts-wqy-microhei, fonts-wqy-zenhei
Section: non-free/otherosfs
Priority: optional
Multi-Arch: foreign
Description: {}
'''.format(e1_text.text(), e2_text.text(), e4_text.text(), wineVersion.currentText(), e3_text.text()))
            write_txt("{}/opt/apps/{}/files/run.sh".format(debPackagePath, e1_text.text()), f'''#!/bin/bash

if [ "$1" = "remove" ] || [ "$1" = "purge" ];then

echo"清理卸载残留"
for username in ls /home
do
echo /home/$username
if [ -d "/home/$username/.deepinwine/{e5_text.text()}" ]
then
rm -rf "/home/$username/.deepinwine/{e5_text.text()}"
fi
done
else
echo"非卸载，跳过清理"
fi
''')
            write_txt("{}/opt/apps/{}/entries/applications/{}.desktop".format(debPackagePath, e1_text.text(), e1_text.text()), '#!/usr/bin/env xdg-open\n[Desktop Entry]\nEncoding=UTF-8\nType=Application\nX-Created-By={}\nCategories={};\nIcon={}\nExec="/opt/apps/{}/files/run.sh" {}\nName={}\nComment={}\nMimeType={}\nGenericName={}\nTerminal=false\nStartupNotify=false\n'.format(e4_text.text(), option1_text.currentText(), a, e1_text.text(), e15_text.text(), e8_text.text(), e3_text.text(), e10_text.text(), e1_text.text()))
            if not bool(chooseWineHelperValue.text()):
                write_txt("{}/opt/apps/{}/files/run.sh".format(debPackagePath, e1_text.text()), '''#!/bin/sh

#   Copyright (C) 2016 Deepin, Inc.
#
#   Author:     Li LongYu <lilongyu@linuxdeepin.com>
#               Peng Hao <penghao@linuxdeepin.com>

version_gt() {{ test "$(echo "$@" | tr " " "\\n" | sort -V | head -n 1)" != "$1"; }}

BOTTLENAME="{}"
APPVER="{}"
EXEC_PATH="{}"
START_SHELL_PATH="/opt/deepinwine/tools/run_v4.sh"
export MIME_TYPE=""
export DEB_PACKAGE_NAME="{}"
export APPRUN_CMD="{}"
DISABLE_ATTACH_FILE_DIALOG=""
EXPORT_ENVS=""

export SPECIFY_SHELL_DIR=`dirname $START_SHELL_PATH`

ARCHIVE_FILE_DIR="/opt/apps/$DEB_PACKAGE_NAME/files"

export WINEDLLPATH=/opt/$APPRUN_CMD/lib:/opt/$APPRUN_CMD/lib64

export WINEPREDLL="$ARCHIVE_FILE_DIR/dlls"

if [ -z "$DISABLE_ATTACH_FILE_DIALOG" ];then
    export ATTACH_FILE_DIALOG=1
fi

if [ -n "$EXPORT_ENVS" ];then
    export $EXPORT_ENVS
fi

if [ -n "$EXEC_PATH" ];then
    if [ -z "${{EXEC_PATH##*.lnk*}}" ];then
        $START_SHELL_PATH $BOTTLENAME $APPVER "C:/windows/command/start.exe" "/Unix" "$EXEC_PATH" "$@"
    else
        $START_SHELL_PATH $BOTTLENAME $APPVER "$EXEC_PATH" "$@"
    fi
else
    $START_SHELL_PATH $BOTTLENAME $APPVER "uninstaller.exe" "$@"
fi
'''.format(e5_text.text(), e2_text.text(), e7_text.text(), e1_text.text(), wineVersion.currentText()))
            else:
                write_txt("{}/opt/apps/{}/files/run.sh".format(debPackagePath, e1_text.text()), '''#!/bin/sh

#   Copyright (C) 2016 Deepin, Inc.
#
#   Author:     Li LongYu <lilongyu@linuxdeepin.com>
#               Peng Hao <penghao@linuxdeepin.com>

#######################函数段。下文调用的额外功能会在此处声明

Get_Dist_Name()
{{
    if grep -Eqii "Deepin" /etc/issue || grep -Eq "Deepin" /etc/*-release; then
        DISTRO='Deepin'
    elif grep -Eqi "UnionTech" /etc/issue || grep -Eq "UnionTech" /etc/*-release; then
        DISTRO='UniontechOS'
    else
	 DISTRO='OtherOS'
	fi
}}

####获得发行版名称

version_gt() {{ test "$(echo "$@" | tr " " "\n" | sort -V | head -n 1)" != "$1"; }}

BOTTLENAME="{}"
APPVER="{}"
EXEC_PATH="{}"
START_SHELL_PATH="/opt/deepinwine/tools/spark_run_v4.sh"
export MIME_TYPE=""
export DEB_PACKAGE_NAME="{}"
export APPRUN_CMD="{}"
EXPORT_ENVS=""

export SPECIFY_SHELL_DIR=`dirname $START_SHELL_PATH`

ARCHIVE_FILE_DIR="/opt/apps/$DEB_PACKAGE_NAME/files"

export WINEDLLPATH=/opt/$APPRUN_CMD/lib:/opt/$APPRUN_CMD/lib64

export WINEPREDLL="$ARCHIVE_FILE_DIR/dlls"

DISABLE_ATTACH_FILE_DIALOG=""

Get_Dist_Name

if [ "$DISTRO" != "Deepin" ] && [ "$DISTRO" != "UniontechOS" ];then
DISABLE_ATTACH_FILE_DIALOG="1"
echo "非deepin/UOS，默认关闭系统自带的文件选择工具，使用Wine的"
echo "如果你想改变这个行为，请到/opt/apps/$DEB_PACKAGE_NAME/files/$0处修改"
echo "To打包者：如果你要打开自带请注意在适配的发行版上进行测试"
echo "To用户：打包者没有打开这个功能，这证明启用这个功能可能造成运行问题。如果你要修改这个行为，请确保你有一定的动手能力"
fi

if [ -z "$DISABLE_ATTACH_FILE_DIALOG" ];then
    export ATTACH_FILE_DIALOG=1
fi

if [ -n "$EXPORT_ENVS" ];then
    export $EXPORT_ENVS
fi

if [ -n "$EXEC_PATH" ];then
    if [ -z "${{EXEC_PATH##*.lnk*}}" ];then
        $START_SHELL_PATH $BOTTLENAME $APPVER "C:/windows/command/start.exe" "/Unix" "$EXEC_PATH" "$@"
    else
        $START_SHELL_PATH $BOTTLENAME $APPVER "$EXEC_PATH" "$@"
    fi
else
    $START_SHELL_PATH $BOTTLENAME $APPVER "uninstaller.exe" "$@"
fi
'''.format(e5_text.text(), e2_text.text(), e7_text.text(), e1_text.text(), wineVersion.currentText()))
            write_txt("{}/opt/apps/{}/info".format(debPackagePath, e1_text.text()), '{\n    "appid": "' + e1_text.text() + '",\n    "name": "' + e8_text.text() + '",\n    "version": "' + e2_text.text() + '",\n    "arch": ["i386"],\n    "permissions": {\n        "autostart": false,\n        "notification": false,\n        "trayicon": true,\n        "clipboard": true,\n        "account": false,\n        "bluetooth": false,\n        "camera": false,\n        "audio_record": false,\n        "installed_apps": false\n    }\n}')
            ################
            # 修改文件权限
            ################
            self.label.emit("正在修改文件权限……")
            self.run_command("chmod -Rv 644 {}/opt/apps/{}/files/run.sh".format(debPackagePath, e1_text.text()))
            self.run_command("chmod -Rv 644 {}/opt/apps/{}/info".format(debPackagePath, e1_text.text()))
            self.run_command("chmod -Rv 755 {}/opt/apps/{}/files/run.sh".format(debPackagePath, e1_text.text()))
            self.run_command("chmod -Rv 755 {}/opt/apps/{}/entries/applications/{}.desktop".format(debPackagePath, e1_text.text(), e1_text.text()))
            ################
            # 构建 deb 包
            ################
            self.label.emit("正在构建 deb 包……")
            self.run_command("dpkg -b {} {}".format(debPackagePath, e12_text.text()))
            ################
            # 完成构建
            ################
            self.label.emit("完成构建！")
            disabled_or_NORMAL_all(True)
            QtWidgets.QMessageBox.information(widget, "提示", "打包完毕！")
        except:
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(widget, "错误", "程序出现错误，错误信息：\n{}".format(traceback.format_exc()))
            self.label.emit("deb 包构建出现错误")
            self.signal.emit(traceback.format_exc())
            disabled_or_NORMAL_all(True)

# 写入文本文档
def write_txt(path, things):
    file = open(path, 'a+', encoding='UTF-8')  # 设置文件对象
    file.write(things)  # 写入文本
    file.close()  # 关闭文本对象

def chang_textbox1_things(things):
    if things.replace("\n", "").replace(" ", "") == "":
        return
    textbox1.append(things)

def clean_textbox1_things():
    textbox1.setText("")


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

# 显示“提示”窗口
def helps():
    QtWidgets.QMessageBox.information(widget, "提示", tips)

# 读取文本文档
def readtxt(path):
    f = open(path, "r") # 设置文件对象
    str = f.read()  # 获取内容
    f.close()  # 关闭文本对象
    return str  # 返回结果

# 获取用户主目录
def get_home():
    return os.path.expanduser('~')

###############
# 程序信息
###############
# 如果要添加其他 wine，请在字典添加其名称和执行路径
wine = {"deepin-wine": "deepin-wine", "deepin-wine5": "deepin-wine5", "wine": "wine", "wine64": "wine64", "deepin-wine5 stable": "deepin-wine5-stable", "deepin-wine6 stable": "deepin-wine6-stable", "spark-wine7-devel": "spark-wine7-devel", "ukylin-wine": "ukylin-wine"}
os.chdir("/")
programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
iconPath = "{}/icon.png".format(programPath)
information = json.loads(readtxt(f"{programPath}/information.json"))
version = information["Version"]
tips = """提示：
1、deb 打包软件包名要求：
软件包名只能含有小写字母(a-z)、数字(0-9)、加号(+)和减号(-)、以及点号(.)，软件包名最短长度两个字符；它必须以字母开头
2、如果要填写路径，有“浏览……”按钮的是要填本计算机对应文件的路径，否则就是填写安装到其他计算机使用的路径
3、输入 wine 的容器路径时最后面请不要输入“/”
4、输入可执行文件的运行路径时是以“C:/XXX/XXX.exe”的格式进行输入，默认是以 C： 为开头，不用“\”做命令的分隔，而是用“/”
5、.desktop 的图标只支持 PNG 格式和 SVG 格式，其他格式无法显示图标
6、路径建议不要带空格，容易出问题"""

###############
# 窗口创建
###############
app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QMainWindow()
widget = QtWidgets.QWidget()
widgetLayout = QtWidgets.QGridLayout()
# 设置变量以修改和获取值项
wineVersion = QtWidgets.QComboBox()
wineVersion.addItems(wine.keys())
wineVersion.setCurrentText("deepin-wine6 stable")
e1_text = QtWidgets.QLineEdit()
e2_text = QtWidgets.QLineEdit()
e3_text = QtWidgets.QLineEdit()
e4_text = QtWidgets.QLineEdit()
e5_text = QtWidgets.QLineEdit()
e6_text = QtWidgets.QLineEdit()
e7_text = QtWidgets.QLineEdit()
e8_text = QtWidgets.QLineEdit()
e9_text = QtWidgets.QLineEdit()
e10_text = QtWidgets.QLineEdit()
e12_text = QtWidgets.QLineEdit()
e15_text = QtWidgets.QLineEdit()
label13_text = QtWidgets.QLabel("<p align='center'>当前 deb 打包情况：暂未打包</p>")
option1_text = QtWidgets.QComboBox()
button1 = QtWidgets.QPushButton("浏览……")
button2 = QtWidgets.QPushButton("浏览……")
button4 = QtWidgets.QPushButton("浏览……")
button5 = QtWidgets.QPushButton("打包……")
textbox1 = QtWidgets.QTextBrowser()
option1_text.addItems(["Network", "Chat", "Audio", "Video", "Graphics", "Office", "Translation", "Development", "Utility", "System"])
option1_text.setCurrentText("Network")
wineFrame = QtWidgets.QHBoxLayout()
chooseWineHelperValue = QtWidgets.QCheckBox("使用星火wine helper（如不勾选默认为deepin-wine-helper）")
button1.clicked.connect(button1_cl)
button2.clicked.connect(button2_cl)
button4.clicked.connect(button4_cl)
button5.clicked.connect(make_deb)
wineFrame.addWidget(wineVersion)
wineFrame.addWidget(chooseWineHelperValue)
# 创建控件
widgetLayout.addWidget(QtWidgets.QLabel("要打包的 deb 包的包名（※必填）："), 0, 0, 1, 1)
widgetLayout.addWidget(QtWidgets.QLabel("要打包的 deb 包的版本号（※必填）："), 1, 0, 1, 1)
widgetLayout.addWidget(QtWidgets.QLabel("要打包的 deb 包的说明（※必填）："), 2, 0, 1, 1)
widgetLayout.addWidget(QtWidgets.QLabel("要打包的 deb 包的维护者（※必填）："), 3, 0, 1, 1)
widgetLayout.addWidget(QtWidgets.QLabel("要解压的 wine 容器的容器名（※必填）："), 4, 0, 1, 1)
widgetLayout.addWidget(QtWidgets.QLabel("要解压的 wine 容器（※必填）："), 5, 0, 1, 1)
widgetLayout.addWidget(QtWidgets.QLabel("要解压的 wine 容器里需要运行的可执行文件路径（※必填）："), 6, 0, 1, 1)
widgetLayout.addWidget(QtWidgets.QLabel("要显示的 .desktop 文件的分类（※必填）："), 7, 0, 1, 1)
widgetLayout.addWidget(QtWidgets.QLabel("要解压的 wine 容器里需要运行的可执行文件的参数（选填）："), 8, 0, 1, 1)
widgetLayout.addWidget(QtWidgets.QLabel("要显示的 .desktop 文件的名称（※必填）："), 9, 0, 1, 1)
widgetLayout.addWidget(QtWidgets.QLabel("要显示的 .desktop 文件的图标（选填）："), 10, 0, 1, 1)
widgetLayout.addWidget(QtWidgets.QLabel("要显示的 .desktop 文件的 MimeType 内容（选填）："), 11, 0, 1, 1)
widgetLayout.addWidget(QtWidgets.QLabel("选择打包的 wine 版本（※必选）："), 12, 0, 1, 1)
widgetLayout.addWidget(QtWidgets.QLabel("打包 deb 的保存路径（※必填）："), 13, 0, 1, 1)
widgetLayout.addWidget(e1_text, 0, 1, 1, 1)
widgetLayout.addWidget(e2_text, 1, 1, 1, 1)
widgetLayout.addWidget(e3_text, 2, 1, 1, 1)
widgetLayout.addWidget(e4_text, 3, 1, 1, 1)
widgetLayout.addWidget(e5_text, 4, 1, 1, 1)
widgetLayout.addWidget(e6_text, 5, 1, 1, 1)
widgetLayout.addWidget(button1, 5, 2, 1, 1)
widgetLayout.addWidget(e7_text, 6, 1, 1, 1)
widgetLayout.addWidget(option1_text, 7, 1, 1, 1)
widgetLayout.addWidget(e15_text, 8, 1, 1, 1)
widgetLayout.addWidget(e8_text, 9, 1, 1, 1)
widgetLayout.addWidget(e9_text, 10, 1, 1, 1)
widgetLayout.addWidget(button2, 10, 2, 1, 1)
widgetLayout.addWidget(e10_text, 11, 1, 1, 1)
widgetLayout.addLayout(wineFrame, 12, 1, 1, 1)
widgetLayout.addWidget(e12_text, 13, 1, 1, 1)
widgetLayout.addWidget(button4, 13, 2, 1, 1)
widgetLayout.addWidget(button5, 14, 1, 1, 1)
widgetLayout.addWidget(label13_text, 15, 0, 1, 3)
widgetLayout.addWidget(textbox1, 16, 0, 1, 3)
menu = window.menuBar()
programmenu = menu.addMenu("程序")
help = menu.addMenu("帮助")
exit = QtWidgets.QAction("退出程序")
tip = QtWidgets.QAction("小提示")
exit.triggered.connect(window.close)
tip.triggered.connect(helps)
programmenu.addAction(exit)
help.addAction(tip)
# 控件配置
try:
    e6_text.setText(sys.argv[1])
    e5_text.setText(pathlib.PurePath(sys.argv[1]).name)
    wineVersion.setCurrentText(sys.argv[2])
except:
    pass
widget.setLayout(widgetLayout)
window.setCentralWidget(widget)
window.setWindowTitle(f"wine 应用打包器 {version}")
window.setWindowIcon(QtGui.QIcon(iconPath))
window.show()
sys.exit(app.exec_())