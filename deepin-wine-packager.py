#!/usr/bin/env python3
#########################################################################
# 作者：gfdgd xi、为什么您不喜欢熊出没和阿布
# 版本：2.0.1
# 感谢：感谢 deepin-wine 团队，提供了 deepin-wine 给大家使用，让我能做这个程序
# 基于 Python3 的 PyQt5 构建
#########################################################################
#################
# 引入所需的库
#################
import os
import sys
import time
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
    path = QtWidgets.QFileDialog.getExistingDirectory(widget, QtCore.QCoreApplication.translate("U", "选择 wine 容器"), f"{get_home()}/.deepinwine")
    if path != "":
        e6_text.setText(path)

def button2_cl():
    path = QtWidgets.QFileDialog.getOpenFileName(widget, QtCore.QCoreApplication.translate("U", "选择图标文件"), get_home(), "PNG图标(*.png);;SVG图标(*.svg);;全部文件(*.*)")[0]
    if path != "":
        e9_text.setText(path)

def button4_cl():
    path = QtWidgets.QFileDialog.getSaveFileName(widget, QtCore.QCoreApplication.translate("U", "保存 deb 包"), get_home(), "deb 文件(*.deb);;所有文件(*.*)", "{}_{}_i386.deb".format(e1_text.text(), e2_text.text()))[0]
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
    debArch.setDisabled(choose)
    rmBash.setDisabled(choose)
    cleanBottonByUOS.setDisabled(choose)
    installDeb.setDisabled(choose)
    useInstallWineArch.setDisabled(choose)
    buildDebDir.setDisabled(choose)
    debDepends.setDisabled(choose)
    debRecommend.setDisabled(choose)
    if not choose:
        ChangeArchCombobox()
        ChangeWine()
    
class QT:
    thread = None

savePath = ""
savePathBlock = False
def SavePathGet(temp):
    global savePath
    global savePathBlock
    savePath = QtWidgets.QFileDialog.getExistingDirectory(widget, "选择模板生成位置", get_home())
    savePathBlock = True

def ErrorMsg(info):
    QtWidgets.QMessageBox.critical(widget, "错误", info)

def InfoMsg(info):
    QtWidgets.QMessageBox.information(widget, "提示", info)

def make_deb(build=False):
    clean_textbox1_things()
    disabled_or_NORMAL_all(False)
    if e1_text.text() == "" or e2_text.text() == "" or e3_text.text() == "" or e4_text.text() == "" or e5_text.text() == "" or e6_text.text() == "" or e7_text.text() == "" or e8_text.text() == "" or e12_text.text() == "":
        QtWidgets.QMessageBox.critical(widget, "错误", "必填信息没有填写完整，无法继续构建 deb 包")
        disabled_or_NORMAL_all(True)
        label13_text_change("必填信息没有填写完整，无法继续构建 deb 包")
        return
    if QtWidgets.QMessageBox.question(widget, QtCore.QCoreApplication.translate("U", "提示"), QtCore.QCoreApplication.translate("U", "打包将会改动现在选择的容器，是否继续？")) == QtWidgets.QMessageBox.No:
        disabled_or_NORMAL_all(True)
        return
    # 警告信息
    if os.path.exists(e7_text.text()):
        if QtWidgets.QMessageBox.warning(window, "警告", "输入的路径似乎是一个绝对路径\n不建议打包绝对路径，建议是 Wine 容器内路径\n是否继续打包？", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No) == QtWidgets.QMessageBox.No:
            disabled_or_NORMAL_all(True)
            return
    if e7_text.text()[:2].lower() == "c:" and not os.path.exists("{}/drive_c/{}".format(
        e6_text.text(), 
        e7_text.text()[3:].replace("\\", '/'))):
        if QtWidgets.QMessageBox.warning(window, "警告", "输入的路径似乎在 Wine 容器不存在（如果只是大小写错误导致的误判，请忽略）\n是否继续打包？", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No) == QtWidgets.QMessageBox.No:
            disabled_or_NORMAL_all(True)
            return
    #thread = threading.Thread(target=make_deb_threading)
    QT.thread = make_deb_threading(build)
    QT.thread.signal.connect(chang_textbox1_things)
    QT.thread.label.connect(label13_text_change)
    QT.thread.getSavePath.connect(SavePathGet)
    QT.thread.errorMsg.connect(ErrorMsg)
    QT.thread.infoMsg.connect(InfoMsg)
    QT.thread.disabled_or_NORMAL_all.connect(disabled_or_NORMAL_all)
    QT.thread.start()
    #thread.start()


def label13_text_change(thing):
    label13_text.setText(f"<p align='center'>当前 deb 打包情况：{thing}</p>")

class make_deb_threading(QtCore.QThread):

    signal = QtCore.pyqtSignal(str)
    label = QtCore.pyqtSignal(str)
    getSavePath = QtCore.pyqtSignal(str)
    errorMsg = QtCore.pyqtSignal(str)
    infoMsg = QtCore.pyqtSignal(str)
    disabled_or_NORMAL_all = QtCore.pyqtSignal(bool)
    build = False
    def __init__(self, build) -> None:
        super().__init__()
        self.build = build

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
                    self.errorMsg.emit("图标的路径填写错误，无法进行构建 deb 包")
                    self.disabled_or_NORMAL_all.emit(True)
                    self.label.emit("图标的路径填写错误，无法进行构建 deb 包")
                    return
            if not os.path.exists(e6_text.text()):
                print("aa")
                self.errorMsg.emit("路径填写错误，无法继续构建 deb 包")
                print("aaa1")
                self.disabled_or_NORMAL_all.emit(True)
                self.label.emit("容器路径填写错误，无法进行构建 deb 包")
                print("bbb")
                return
            debInformation = [
                {
                    # I386 wine 打包配置文件
                    "Wine": wine[wineVersion.currentText()],
                    "Architecture": "i386",
                    "Depends": [
                        f"{wine[wineVersion.currentText()]}, deepin-wine-helper (>= 5.1.30-1), fonts-wqy-microhei, fonts-wqy-zenhei",
                        f"{wine[wineVersion.currentText()]}, spark-dwine-helper | store.spark-app.spark-dwine-helper, fonts-wqy-microhei, fonts-wqy-zenhei"
                        ][int(chooseWineHelperValue.isChecked())],
                    "postinst": "",
                    "postrm": ["", f"""#!/bin/bash

if [ "$1" = "remove" ] || [ "$1" = "purge" ];then

echo "清理卸载残留"
for username in `ls /home`
    do
        echo /home/$username
        if [ -d "/home/$username/.deepinwine/{e5_text.text()}" ]
            then
                rm -rf "/home/$username/.deepinwine/{e5_text.text()}"
            fi
    done
else
    echo "非卸载，跳过清理"
fi"""][int(rmBash.isChecked())],
                    "run.sh": [
                        f"""#!/bin/sh

#   Copyright (C) 2016 Deepin, Inc.
#
#   Author:     Li LongYu <lilongyu@linuxdeepin.com>
#               Peng Hao <penghao@linuxdeepin.com>

version_gt() {{ test "$(echo "$@" | tr " " "\\n" | sort -V | head -n 1)" != "$1"; }}

BOTTLENAME="{e5_text.text()}"
APPVER="{e2_text.text()}"
EXEC_PATH="{e7_text.text()}"
START_SHELL_PATH="/opt/deepinwine/tools/run_v4.sh"
export MIME_TYPE=""
export DEB_PACKAGE_NAME="{e1_text.text()}"
export APPRUN_CMD="{wine[wineVersion.currentText()]}"
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
fi""", 
                        f"""#!/bin/sh

#   Copyright (C) 2016 Deepin, Inc.
#
#   Author:     Li LongYu <lilongyu@linuxdeepin.com>
#               Peng Hao <penghao@linuxdeepin.com>
#
#
#   Copyright (C) 2022 The Spark Project
#
#
#   Modifier    shenmo <shenmo@spark-app.store>
#
#
#

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

#########################预设值段

version_gt() {{ test "$(echo "$@" | tr " " "\n" | sort -V | head -n 1)" != "$1"; }}
####用于比较版本？未实装
BOTTLENAME="{e5_text.text()}"
APPVER="{e2_text.text()}"
EXEC_PATH="{e7_text.text()}"
##### 软件在wine中的启动路径
START_SHELL_PATH="/opt/deepinwine/tools/spark_run_v4.sh"
export MIME_TYPE=""
#####没什么用
export DEB_PACKAGE_NAME="{e1_text.text()}"
####这里写包名才能在启动的时候正确找到files.7z,似乎也和杀残留进程有关
export APPRUN_CMD="{wine[wineVersion.currentText()]}"
#####wine启动指令，建议
EXPORT_ENVS=""

export SPECIFY_SHELL_DIR=`dirname $START_SHELL_PATH`

ARCHIVE_FILE_DIR="/opt/apps/$DEB_PACKAGE_NAME/files"

export WINEDLLPATH=/opt/$APPRUN_CMD/lib:/opt/$APPRUN_CMD/lib64

export WINEPREDLL="$ARCHIVE_FILE_DIR/dlls"

DISABLE_ATTACH_FILE_DIALOG=""
##默认为空。若为1，则不使用系统自带的文件选择，而是使用wine的
##对于deepin/UOS，大部分的应用都不需要使用wine的，如果有需求（比如wine应用选择的限定种类文件系统的文管不支持）
##请填1。
##注意：因为非DDE的环境不确定，所以默认会在非Deepin/UOS发行版上禁用这个功能。如果你确认在适配的发行版上可以正常启动，请注释或者删除下面这段

##############<<<<<<<<<禁用文件选择工具开始
Get_Dist_Name
#此功能实现参见结尾函数段
if [ "$DISTRO" != "Deepin" ] && [ "$DISTRO" != "UniontechOS" ];then
DISABLE_ATTACH_FILE_DIALOG="1"
echo "非deepin/UOS，默认关闭系统自带的文件选择工具，使用Wine的"
echo "如果你想改变这个行为，请到/opt/apps/$DEB_PACKAGE_NAME/files/$0处修改"
echo "To打包者：如果你要打开自带请注意在适配的发行版上进行测试"
echo "To用户：打包者没有打开这个功能，这证明启用这个功能可能造成运行问题。如果你要修改这个行为，请确保你有一定的动手能力"
fi
##############>>>>>>>>>禁用文件选择工具结束

##############<<<<<<<<<屏蔽mono和gecko安装器开始
##默认屏蔽mono和gecko安装器
#if [ "$APPRUN_CMD" = "spark-wine7-devel" ];then

#export WINEDLLOVERRIDES="mscoree,mshtml="
#echo "为了降低打包体积，默认关闭gecko和momo，如有需要，注释此行（仅对spark-wine7-devel有效）"

#fi
##############>>>>>>>>>屏蔽mono和gecko安装器结束

#########################执行段




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
fi"""
                        ][chooseWineHelperValue.isChecked()],
                        "info": f'''{{
    "appid": "{e1_text.text()}",
    "name": "{e8_text.text()}",
    "version": "{e2_text.text()}",
    "arch": ["i386"],
    "permissions": {{
        "autostart": false,
        "notification": false,
        "trayicon": true,
        "clipboard": true,
        "account": false,
        "bluetooth": false,
        "camera": true,
        "audio_record": true,
        "installed_apps": false
    }}
}}'''
                },
                {
                    # ARM64 BOX86 wine 打包配置文件
                    "Wine": f"WINEPREDLL='{programPath}/dlls-arm' WINEDLLPATH=/opt/deepin-wine6-stable/lib BOX86_NOSIGSEGV=1 /opt/deepin-box86/box86 /opt/deepin-wine6-stable/bin/wine ",
                    "Architecture": "arm64",
                    "Depends": "deepin-elf-verify (>= 0.0.16.7-1), com.deepin-wine6-stable.deepin(>=6.0deepin14), com.deepin-box86.deepin(>=0.2.3deepin8), p7zip-full, fonts-wqy-microhei, fonts-noto-cjk",
                    "postinst": f"""#!/bin/sh
DEB_PATH=/opt/apps/{e1_text.text()}
NVIDIA_DISP_CARD=`lspci | grep VGA | grep NVIDIA`
if [ -f $DEB_PATH/files/wined3d.dll.so ] && [ ! -z "$NVIDIA_DISP_CARD" ];then
	mv $DEB_PATH/files/wined3d.dll.so $DEB_PATH/files/dlls
fi
true
""",
                    "postrm": f"""#!/bin/sh

BOTTLE="$HOME/.deepinwine/{e5_text.text()}"
WINESERVER=/opt/deepin-wine6-stable/bin/wineserver

if [ -d "$BOTTLE" ];then
	WINEPREFIX=$BOTTLE $WINESERVER -k
	rm $BOTTLE -rf
fi

true""",
                    "run.sh": f"""#!/bin/bash
DEB_PATH="/opt/apps/{e1_text.text()}"
WINE="/opt/deepin-wine6-stable/bin/wine"
WINESERVER="/opt/deepin-wine6-stable/bin/wineserver"
BOX86="/opt/deepin-box86/box86"
EXE="{e7_text.text()}"
NEW_VERSION="{e2_text.text()}"
BOTTLE="$HOME/.deepinwine/{e5_text.text()}"

reconstruct_bottle_symlink() {{

    if [ -L $BOTTLE/drive_c/users/$USER/Desktop ]; then
        rm -f $BOTTLE/drive_c/users/$USER/Desktop
        ln -s $HOME/Desktop $BOTTLE/drive_c/users/$USER/Desktop
    fi
    if [ -L $BOTTLE/drive_c/users/$USER/Documents ]; then
        rm -f $BOTTLE/drive_c/users/$USER/Documents
        ln -s $HOME/Documents $BOTTLE/drive_c/users/$USER/Documents
    fi
    if [ -L $BOTTLE/drive_c/users/$USER/Downloads ]; then
        rm -f $BOTTLE/drive_c/users/$USER/Downloads
        ln -s $HOME/Downloads $BOTTLE/drive_c/users/$USER/Downloads
    fi

    if [ -L "$BOTTLE/drive_c/users/$USER/My Documents" ]; then
        rm -f "$BOTTLE/drive_c/users/$USER/My Documents"
        ln -s $HOME/Documents "$BOTTLE/drive_c/users/$USER/My Documents"
    fi

    if [ -L "$BOTTLE/drive_c/users/$USER/My Music" ]; then
        rm -f "$BOTTLE/drive_c/users/$USER/My Music"
        ln -s $HOME/Music "$BOTTLE/drive_c/users/$USER/My Music"
    fi
    if [ -L "$BOTTLE/drive_c/users/$USER/My Videos" ]; then
        rm -f "$BOTTLE/drive_c/users/$USER/My Videos"
        ln -s $HOME/Videos "$BOTTLE/drive_c/users/$USER/My Videos"
    fi
}}

if [ ! -d "$HOME/.deepinwine" ];then
    mkdir -p "$HOME/.deepinwine"
fi

if [ -f $BOTTLE/VERSION ];then
    old_version=""
    while read line; do
    old_version=$line
    done < $BOTTLE/VERSION
    if [ "$old_version" != "$NEW_VERSION" ];then
	WINEPREFIX=$BOTTLE $BOX86 $WINESERVER -k
        rm -rf $BOTTLE
    fi
fi

if [ -d $BOTTLE ] && [ ! -f $BOTTLE/VERSION ];then
	WINEPREFIX=$BOTTLE $BOX86 $WINESERVER -k
	rm -rf $BOTTLE
fi

if [ ! -d $BOTTLE ];then
    7z x "$DEB_PATH/files/files.7z" -o"$BOTTLE" -aoa
    mv "$BOTTLE/drive_c/users/@current_user@" "$BOTTLE/drive_c/users/$USER"
    sed -i "s#@current_user@#$USER#" $BOTTLE/*.reg
    reconstruct_bottle_symlink
    echo $NEW_VERSION > $BOTTLE/VERSION
fi

export WINEPREDLL=$DEB_PATH/files/dlls
export ATTACH_FILE_DIALOG=1
export WINEDLLPATH=/opt/deepin-wine6-stable/lib
WINEPREFIX=$BOTTLE $BOX86 $WINE "$EXE" &""",
                "info": f'''{{
    "appid": "{e1_text.text()}",
    "name": "{e8_text.text()}",
    "version": "{e2_text.text()}",
    "arch": ["arm64"],
    "permissions": {{
        "autostart": false,
        "notification": false,
        "trayicon": true,
        "clipboard": true,
        "account": false,
        "bluetooth": false,
        "camera": true,
        "audio_record": true,
        "installed_apps": false
    }}
}}'''
                },
                {
                    # ARM64 exagear wine 打包配置文件
                    "Wine": f"/opt/exagear/bin/ubt_x64a64_al --path-prefix {get_home()}/.deepinwine/debian-buster --utmp-paths-list {get_home()}/.deepinwine/debian-buster/.exagear/utmp-list --vpaths-list {get_home()}/.deepinwine/debian-buster/.exagear/vpaths-list --opaths-list {get_home()}/.deepinwine/debian-buster/.exagear/opaths-list --smo-mode fbase --smo-severity smart --fd-limit 8192 --foreign-ubt-binary /opt/exagear/bin/ubt_x32a64_al -- /opt/deepin-wine6-stable/bin/wine ",
                    "Architecture": "arm64",
                    "Depends": "zenity, com.deepin-wine6-stable.deepin(>=6.0deepin14), deepin-wine-exagear-images(>=10deepin4), com.deepin-box86.deepin(>=0.2.3deepin9), p7zip-full, fonts-wqy-microhei, fonts-noto-cjk",
                    "postinst": "",
                    "postrm": "",
                    "run.sh": f"""#!/bin/bash
DEB_PATH="/opt/apps/{e1_text.text()}"
WINE="/opt/deepin-wine6-stable/bin/wine"
WINESERVER="/opt/deepin-wine6-stable/bin/wineserver"
EMU="/opt/exagear/bin/ubt_x64a64_al"
IMAGE_PATH=$HOME/.deepinwine/debian-buster
EMU_ARGS="--path-prefix $IMAGE_PATH --utmp-paths-list $IMAGE_PATH/.exagear/utmp-list --vpaths-list $IMAGE_PATH/.exagear/vpaths-list --opaths-list $IMAGE_PATH/.exagear/opaths-list --smo-mode fbase --smo-severity smart --fd-limit 8192 --foreign-ubt-binary /opt/exagear/bin/ubt_x32a64_al -- "
EXE="{e7_text.text()}"
NEW_VERSION="6.4.1deepin1"
BOTTLE="$HOME/.deepinwine/{e5_text.text()}"
KUNPENG=`lscpu | grep 'Model name' | grep Kunpeng`
IMG_ARCHIVE_DIR=/opt/deepin-wine-exagear-images/debian-buster
IMAGE_VER="{e2_text.text()}"
LOCALTIME=`readlink -f /etc/localtime`

export LC_ALL=$LANG
export XMODIFIERS=$XMODIFIERS
export DESKTOP_SESSION=deepin

if command -v zenity >/dev/null 2>&1; then
	progressbar()
	{{
		WINDOWID="" zenity --progress --title="$1" --text="$2" --pulsate --width=400 --auto-close --no-cancel ||
		WINDOWID="" zenity --progress --title="$1" --text="$2" --pulsate --width=400 --auto-close
	}}

else
	progressbar()
	{{
		cat -
	}}
fi

reconstruct_bottle_symlink() {{

    if [ -L $BOTTLE/drive_c/users/$USER/Desktop ]; then
        rm -f $BOTTLE/drive_c/users/$USER/Desktop
        ln -s $HOME/Desktop $BOTTLE/drive_c/users/$USER/Desktop
    fi
    if [ -L $BOTTLE/drive_c/users/$USER/Documents ]; then
        rm -f $BOTTLE/drive_c/users/$USER/Documents
        ln -s $HOME/Documents $BOTTLE/drive_c/users/$USER/Documents
    fi
    if [ -L $BOTTLE/drive_c/users/$USER/Downloads ]; then
        rm -f $BOTTLE/drive_c/users/$USER/Downloads
        ln -s $HOME/Downloads $BOTTLE/drive_c/users/$USER/Downloads
    fi

    if [ -L "$BOTTLE/drive_c/users/$USER/My Documents" ]; then
        rm -f "$BOTTLE/drive_c/users/$USER/My Documents"
        ln -s $HOME/Documents "$BOTTLE/drive_c/users/$USER/My Documents"
    fi

    if [ -L "$BOTTLE/drive_c/users/$USER/My Music" ]; then
        rm -f "$BOTTLE/drive_c/users/$USER/My Music"
        ln -s $HOME/Music "$BOTTLE/drive_c/users/$USER/My Music"
    fi
    if [ -L "$BOTTLE/drive_c/users/$USER/My Videos" ]; then
        rm -f "$BOTTLE/drive_c/users/$USER/My Videos"
        ln -s $HOME/Videos "$BOTTLE/drive_c/users/$USER/My Videos"
    fi
}}

extract_image() {{
[doge]
    progpid=$(ps -ef | grep "zenity --progress --title=${{BOTTLE}}" | grep -v grep)
    if [ -n "$progpid" ];then
	    echo "one $BOTTLE app is extracting runtime images too."
	    exit 0
    fi

    7z x "$IMG_ARCHIVE_DIR/files.7z" -o"$IMAGE_PATH" -aoa | progressbar "$BOTTLE" "正在释放环境..."
    cp /usr/bin/dde-file-manager $IMAGE_PATH/usr/bin/dde-file-manager
    rm $IMAGE_PATH/etc/localtime
    ln -s $LOCALTIME $IMAGE_PATH/etc/localtime
    if [ -d $IMAGE_PATH/etc/resolvconf ];then
        rm $IMAGE_PATH/etc/resolvconf
    fi
    if [ -d /etc/resolvconf ];then
    	cp /etc/resolvconf $IMAGE_PATH/etc/ -rf
    fi
    cp /etc/resolv.conf $IMAGE_PATH/etc/
    cp /etc/hosts $IMAGE_PATH/etc/
    echo $IMAGE_VER > $IMAGE_PATH/VERSION
}}

get_link_err_nums() {{

	find  $IMAGE_PATH -type l ! -exec test -e {{}} \; -print | wc -l
}}

if [ ! -d "$HOME/.deepinwine" ];then
    mkdir -p "$HOME/.deepinwine"
fi

if [ -f $BOTTLE/VERSION ];then
    old_version=`cat $BOTTLE/VERSION`
    if [ "$old_version" != "$NEW_VERSION" ];then
        WINEPREFIX=$BOTTLE $EMU $EMU_ARGS $WINESERVER -k
        rm -rf $BOTTLE
    fi
fi
Update_D() {{
    if [ -L "$BOTTLE/dosdevices/d:" ]; then
        rm -f "$BOTTLE/dosdevices/d:"
        ln -s $Downloads "$BOTTLE/dosdevices/d:"
    fi
  if [ -L "$BOTTLE/dosdevices/d：" ]; then
        rm -f "$BOTTLE/dosdevices/d："
        ln -s $Downloads "$BOTTLE/dosdevices/d："
    fi
}}
if [ ! -d $BOTTLE ];then

    7z x "$DEB_PATH/files/files.7z" -o"$BOTTLE" -aoa
    mv "$BOTTLE/drive_c/users/@current_user@" "$BOTTLE/drive_c/users/$USER"
    sed -i "s#@current_user@#$USER#" $BOTTLE/*.reg
    reconstruct_bottle_symlink
    echo $NEW_VERSION > $BOTTLE/VERSION
fi

if [ ! -z "$KUNPENG" ];then
    if [ ! -e $IMAGE_PATH/VERSION ];then
        extract_image
    fi

    OLD_IMAGE_VER=`cat $IMAGE_PATH/VERSION`
    if [ "$OLD_IMAGE_VER" != "$IMAGE_VER" ];then
        extract_image
    fi

    echo "======$(get_link_err_nums)===="
    if [ "$(get_link_err_nums)" -gt "120" ];then
        extract_image
    fi
fi

## mount /data/ dir to geust
if [ -d $IMAGE_PATH ] && [ ! -d $IMAGE_PATH/data ];then
	mkdir $IMAGE_PATH/data
	cp $DEB_PATH/files/exa/vpaths-list $IMAGE_PATH/.exagear
fi

export WINEPREDLL=$DEB_PATH/files/dlls
export ATTACH_FILE_DIALOG=1
export WINEDLLPATH=/opt/deepin-wine6-stable/lib
WINEPREFIX=$BOTTLE $EMU $EMU_ARGS $WINE  $WINE wineboot --init
 Update_D
WINEPREFIX=$BOTTLE $EMU $EMU_ARGS $WINE "$EXE" --disable-gpu &""",
                "info": f'''{{
    "appid": "{e1_text.text()}",
    "name": "{e8_text.text()}",
    "version": "{e2_text.text()}",
    "arch": ["arm64"],
    "permissions": {{
        "autostart": false,
        "notification": false,
        "trayicon": true,
        "clipboard": true,
        "account": false,
        "bluetooth": false,
        "camera": true,
        "audio_record": true,
        "installed_apps": false
    }}
}}'''}
            ]
            print("c")
            if os.path.exists(wine[wineVersion.currentText()]):
                debInformation[0]["Depends"] = ["deepin-wine-helper (>= 5.1.30-1)",
                        "spark-dwine-helper | store.spark-app.spark-dwine-helper"
                        ][int(chooseWineHelperValue.isChecked())] #+ ["", "libasound2 (>= 1.0.16), libc6 (>= 2.28), libglib2.0-0 (>= 2.12.0), libgphoto2-6 (>= 2.5.10), libgphoto2-port12 (>= 2.5.10), libgstreamer-plugins-base1.0-0 (>= 1.0.0), libgstreamer1.0-0 (>= 1.4.0), liblcms2-2 (>= 2.2+git20110628), libldap-2.4-2 (>= 2.4.7), libmpg123-0 (>= 1.13.7), libopenal1 (>= 1.14), libpcap0.8 (>= 0.9.8), libpulse0 (>= 0.99.1), libudev1 (>= 183), libvkd3d1 (>= 1.0), libx11-6, libxext6, libxml2 (>= 2.9.0), ocl-icd-libopencl1 | libopencl1, udis86, zlib1g (>= 1:1.1.4), libasound2-plugins, libncurses6 | libncurses5 | libncurses, deepin-wine-plugin-virtual\nRecommends: libcapi20-3, libcups2, libdbus-1-3, libfontconfig1, libfreetype6, libglu1-mesa | libglu1, libgnutls30 | libgnutls28 | libgnutls26, libgsm1, libgssapi-krb5-2, libjpeg62-turbo | libjpeg8, libkrb5-3, libodbc1, libosmesa6, libpng16-16 | libpng12-0, libsane | libsane1, libsdl2-2.0-0, libtiff5, libv4l-0, libxcomposite1, libxcursor1, libxfixes3, libxi6, libxinerama1, libxrandr2, libxrender1, libxslt1.1, libxxf86vm1"][]
                print("d")
                debInformation[0]["run.sh"] = f'''#!/bin/sh

#   Copyright (C) 2016 Deepin, Inc.
#
#   Author:     Li LongYu <lilongyu@linuxdeepin.com>
#               Peng Hao <penghao@linuxdeepin.com>

version_gt() {{ test "$(echo "$@" | tr " " "\n" | sort -V | head -n 1)" != "$1"; }}

extract_archive()
{{
    archive=$1
    version_file=$2
    dest_dir=$3
    if [ -f "$archive" ] && [ -n "$dest_dir" ] && [ "$dest_dir" != "." ];then
        archive_version=`cat $version_file`
        if [ -d "$dest_dir" ];then
            if [ -f "$dest_dir/VERSION" ];then
                dest_version=`cat $dest_dir/VERSION`
                if version_gt "$archive_version" "$dest_version";then
                    7z x "$archive" -o/"$dest_dir" -aoa
                    echo "$archive_version" > "$dest_dir/VERSION"
                fi
            fi
        else
            mkdir -p $dest_dir
            7z x "$archive" -o/"$dest_dir" -aoa
            echo "$archive_version" > "$dest_dir/VERSION"
        fi
    fi
}}

BOTTLENAME="{e5_text.text()}"
APPVER="{e2_text.text()}"
EXEC_PATH="{e7_text.text()}"
START_SHELL_PATH="{["/opt/deepinwine/tools/run_v4.sh", "/opt/deepinwine/tools/spark_run_v4.sh"][int(chooseWineHelperValue.isChecked())]}"
export MIME_TYPE=""
export DEB_PACKAGE_NAME="{e1_text.text()}"
export APPRUN_CMD="$HOME/.deepinwine/{os.path.basename(wine[wineVersion.currentText()]).replace('.7z', '')}/bin/{useInstallWineArch.currentText()}"
export PATCH_LOADER_ENV=""
export FILEDLG_PLUGIN="/opt/apps/$DEB_PACKAGE_NAME/files/gtkGetFileNameDlg"
DISABLE_ATTACH_FILE_DIALOG="1"
export SPECIFY_SHELL_DIR=`dirname $START_SHELL_PATH`

DEEPIN_WINE_BIN_DIR=`dirname $APPRUN_CMD`
DEEPIN_WINE_DIR=`dirname $DEEPIN_WINE_BIN_DIR`
ARCHIVE_FILE_DIR="/opt/apps/$DEB_PACKAGE_NAME/files"

if [ -n "$PATCH_LOADER_ENV" ] && [ -n "$EXEC_PATH" ];then
    export $PATCH_LOADER_ENV
fi

extract_archive "$ARCHIVE_FILE_DIR/wine_archive.7z" "$ARCHIVE_FILE_DIR/wine_archive.md5sum" "$DEEPIN_WINE_DIR"

if [ -d "$DEEPIN_WINE_BIN_DIR" ] && [ "$DEEPIN_WINE_BIN_DIR" != "." ];then
    export DEEPIN_WINE_BIN_DIR
fi

if [ -z "$DISABLE_ATTACH_FILE_DIALOG" ];then
    export ATTACH_FILE_DIALOG=1
fi

if [ -n "$EXEC_PATH" ];then
    $START_SHELL_PATH $BOTTLENAME $APPVER "$EXEC_PATH" "$@"
else
    $START_SHELL_PATH $BOTTLENAME $APPVER "uninstaller.exe" "$@"
fi
'''

            #############
            # 删除文件
            #############
            self.label.emit("正在删除对构建 deb 包有影响的文件……")
            if self.build:
                global savePath
                global savePathBlock
                savePathBlock = False
                self.getSavePath.emit("")
                # 必须保证信号完全执行才可以继续
                # 所以自制信号锁
                while not savePathBlock:
                    time.sleep(0.1)
                #
                if savePath == "":
                    print("ggg")
                    self.disabled_or_NORMAL_all.emit(True)
                    return
                print("aaa")
                debPackagePath = savePath
                print("g")
            else:
                debPackagePath = f"/tmp/{random.randint(0, 9999)}"
            #self.run_command(f"rm -rfv /tmp/{debPackagePath}")
            print("f")
            # 为了避免删库，必须保证是 deb 文件构建目录才进行清空
            if os.path.exists(f"{debPackagePath}/DEBIAN/control"):
                self.run_command(f"rm -rfv '{debPackagePath}/usr'")
                self.run_command(f"rm -rfv '{debPackagePath}/opt'")
                self.run_command(f"rm -rfv '{debPackagePath}/DEBIAN'")
            print("d")
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
            if e6_text.text()[-3: ] != ".7z":
                os.chdir(programPath)
                if cleanBottonByUOS.isChecked():
                    self.run_command(f"WINE='{debInformation[debArch.currentIndex()]['Wine']}' '{programPath}/cleanbottle.sh' '{b}'")
                os.chdir(b)
                # 对用户目录进行处理
                self.run_command("sed -i \"s#$USER#@current_user@#\" ./*.reg")
                os.chdir(f"{b}/drive_c/users")
                if os.path.exists(f"{b}/drive_c/users/@current_user@"):
                    self.run_command(f"rm -rfv '{b}/drive_c/users/@current_user@'")
                self.run_command(f"mv -fv '{os.getlogin()}' @current_user@")
                # 如果缩放文件 scale.txt 存在，需要移除以便用户自行调节缩放设置
                if os.path.exists(f"{b}/scale.txt"):
                    os.remove(f"{b}/scale.txt")
                # 删除因为脚本失误导致用户目录嵌套（如果存在）
                if os.path.exists(f"{b}{b}/drive_c/users/@current_user@/@current_user@"):
                    shutil.rmtree(f"{b}{b}/drive_c/users/@current_user@/@current_user@")
                # 删除无用的软链
                self.run_command(f"rm -fv '{b}/drive_c/users/@current_user@/我的'*")
                self.run_command(f"rm -fv '{b}/drive_c/users/@current_user@/My '*")
                self.run_command(f"rm -fv '{b}/drive_c/users/@current_user@/Desktop'")
                self.run_command(f"rm -fv '{b}/drive_c/users/@current_user@/Downloads'")
                self.run_command(f"rm -fv '{b}/drive_c/users/@current_user@/Templates'")
            os.chdir(programPath)
            ###############
            # 压缩 Wine
            ###############
            print("e")
            self.label.emit("正在处理 Wine")
            if os.path.exists(wine[wineVersion.currentText()]):
                shutil.copy(f"{programPath}/gtkGetFileNameDlg", f"{debPackagePath}/opt/apps/{e1_text.text()}/files/gtkGetFileNameDlg")
                if wine[wineVersion.currentText()][-3:] == ".7z":
                    # 都有了为什么要打包呢？
                    shutil.copy(wine[wineVersion.currentText()], f"{debPackagePath}/opt/apps/{e1_text.text()}/files/wine_archive.7z")
                else:
                    self.run_command(f"7z a '{debPackagePath}/opt/apps/{e1_text.text()}/files/wine_archive.7z' '{wine[wineVersion.currentText()]}/*'")
            ###############
            # 压缩容器
            ###############
            self.label.emit("正在打包 wine 容器")
            # 都有 7z 了为什么要打包呢？
            if e6_text.text()[-3: ] == ".7z":
                shutil.copy(e6_text.text(), f"{debPackagePath}/opt/apps/{e1_text.text()}/files/files.7z")
            else:
                self.run_command("7z a {}/opt/apps/{}/files/files.7z {}/*".format(debPackagePath, e1_text.text(), b))
            ###############
            # 复制文件
            ###############
            self.label.emit("正在复制文件……")
            if os.path.exists(wine[wineVersion.currentText()]):
                shutil.copy(f"{programPath}/gtkGetFileNameDlg", f"{debPackagePath}/opt/apps/{e1_text.text()}/files")
            # arm64 box86 需要复制 dlls-arm 目录
            if debArch.currentIndex() == 1:
                if not os.path.exists(f"{programPath}/dlls-arm"):
                    self.run_command(f"7z x \"{programPath}/dlls-arm.7z\" -o\"{programPath}\"")
                    os.remove(f"{programPath}/dlls-arm.7z")
                if not os.path.exists(f"{programPath}/wined3d.dll.so"):
                    self.run_command(f"7z x \"{programPath}/wined3d.dll.so.7z\" -o\"{programPath}\"")
                    os.remove(f"{programPath}/wined3d.dll.so.7z")
                self.run_command(f"cp -rv '{programPath}/dlls-arm' {debPackagePath}/opt/apps/{e1_text.text()}/files/dlls")
                self.run_command(f"cp -rv '{programPath}/wined3d.dll.so' {debPackagePath}/opt/apps/{e1_text.text()}/files/")
            elif debArch.currentIndex() == 2:
                if not os.path.exists(f"{programPath}/exagear"):
                    self.run_command(f"aria2c -x 16 -s 16 -d \"{programPath}\" -o \"exagear.7z\" https://code.gitlink.org.cn/gfdgd_xi/wine-runner-list/raw/branch/master/other/exagear.7z")
                    self.run_command(f"7z x \"{programPath}/exagear.7z\" -o\"{programPath}\"")
                    os.remove(f"{programPath}/exagear.7z")
                self.run_command(f"cp -rv '{programPath}/exagear/*' {debPackagePath}/opt/apps/{e1_text.text()}/files/")
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
            if debRecommend.text() == "":
                write_txt(f"{debPackagePath}/DEBIAN/control", f'''Package: {e1_text.text()}
Version: {e2_text.text()}
Architecture: {debInformation[debArch.currentIndex()]["Architecture"]}
Maintainer: {e4_text.text()}
Depends: {debInformation[debArch.currentIndex()]["Depends"]}
Section: non-free/otherosfs
Priority: optional
Multi-Arch: foreign
Installed-Size: {size}
Description: {e3_text.text()}
''')
            else:
                write_txt(f"{debPackagePath}/DEBIAN/control", f'''Package: {e1_text.text()}
Version: {e2_text.text()}
Architecture: {debInformation[debArch.currentIndex()]["Architecture"]}
Maintainer: {e4_text.text()}
Depends: {debInformation[debArch.currentIndex()]["Depends"]}
Recommends: {debRecommend.text()}
Section: non-free/otherosfs
Priority: optional
Multi-Arch: foreign
Installed-Size: {size}
Description: {e3_text.text()}
''')
            if debInformation[debArch.currentIndex()]["postinst"] != "":
                write_txt(f"{debPackagePath}/DEBIAN/postinst", debInformation[debArch.currentIndex()]["postinst"])
            if debInformation[debArch.currentIndex()]["postrm"] != "":
                write_txt(f"{debPackagePath}/DEBIAN/postrm", debInformation[debArch.currentIndex()]["postrm"])
            write_txt("{}/opt/apps/{}/entries/applications/{}.desktop".format(debPackagePath, e1_text.text(), e1_text.text()), '#!/usr/bin/env xdg-open\n[Desktop Entry]\nEncoding=UTF-8\nType=Application\nX-Created-By={}\nCategories={};\nIcon={}\nExec="/opt/apps/{}/files/run.sh" {}\nName={}\nComment={}\nMimeType={}\nGenericName={}\nTerminal=false\nStartupNotify=false\n'.format(e4_text.text(), option1_text.currentText(), a, e1_text.text(), e15_text.text(), e8_text.text(), e3_text.text(), e10_text.text(), e1_text.text()))
            write_txt(f"{debPackagePath}/opt/apps/{e1_text.text()}/files/run.sh", debInformation[debArch.currentIndex()]["run.sh"])
            write_txt("{}/opt/apps/{}/info".format(debPackagePath, e1_text.text()), debInformation[debArch.currentIndex()]["info"])
            ################
            # 修改文件权限
            ################
            self.label.emit("正在修改文件权限……")
            self.run_command("chmod -Rv 644 {}/opt/apps/{}/files/run.sh".format(debPackagePath, e1_text.text()))
            self.run_command("chmod -Rv 644 {}/opt/apps/{}/info".format(debPackagePath, e1_text.text()))
            self.run_command("chmod -Rv 0755 {}/DEBIAN".format(debPackagePath))
            self.run_command("chmod -Rv 755 {}/opt/apps/{}/files/run.sh".format(debPackagePath, e1_text.text()))
            self.run_command("chmod -Rv 755 {}/opt/apps/{}/entries/applications/{}.desktop".format(debPackagePath, e1_text.text(), e1_text.text()))
            ################
            # 构建 deb 包
            ################
            if not self.build:
                self.label.emit("正在构建 deb 包……")
                self.run_command("dpkg -b {} {}".format(debPackagePath, e12_text.text()))
            ################
            # 完成构建
            ################
            self.label.emit("完成构建！")
            self.disabled_or_NORMAL_all.emit(True)
            self.infoMsg.emit("打包完毕！")
            global change
            change = False
        except:
            traceback.print_exc()
            self.errorMsg.emit("程序出现错误，错误信息：\n{}".format(traceback.format_exc()))
            self.label.emit("deb 包构建出现错误")
            self.signal.emit(traceback.format_exc())
            self.disabled_or_NORMAL_all.emit(True)

# 写入文本文档
def write_txt(path, things):
    file = open(path, 'a+', encoding='UTF-8')  # 设置文件对象
    file.write(things)  # 写入文本
    file.close()  # 关闭文本对象

def chang_textbox1_things(things):
    if things.replace("\n", "").replace(" ", "") == "":
        return
    textbox1.append(things.replace("\n", ""))

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

def ChangeArchCombobox():
    global chooseWineHelperValue
    option = True
    if debArch.currentIndex() != 0:
        option = False
    chooseWineHelperValue.setEnabled(option)
    wineVersion.setEnabled(option)
    useInstallWineArch.setEnabled(option)
    rmBash.setEnabled(option)
    if debArch.currentIndex() == 0:
        ChangeWine()
    elif debArch.currentIndex() == 1:
        debDepends.setText("deepin-elf-verify (>= 0.0.16.7-1), com.deepin-wine6-stable.deepin(>=6.0deepin14), com.deepin-box86.deepin(>=0.2.3deepin8), p7zip-full, fonts-wqy-microhei, fonts-noto-cjk")
    elif debArch.currentIndex() == 2:
        debDepends.setText("zenity, com.deepin-wine6-stable.deepin(>=6.0deepin14), deepin-wine-exagear-images(>=10deepin4), com.deepin-box86.deepin(>=0.2.3deepin9), p7zip-full, fonts-wqy-microhei, fonts-noto-cjk")

def InstallDeb():
    os.system(f"xdg-open '{e12_text.text()}'")

def ChangeWine():
    useInstallWineArch.setEnabled(os.path.exists(wine[wineVersion.currentText()]))
    debDepends.setText([f"{wine[wineVersion.currentText()]}, deepin-wine-helper (>= 5.1.30-1), fonts-wqy-microhei, fonts-wqy-zenhei",
                        f"{wine[wineVersion.currentText()]}, spark-dwine-helper | store.spark-app.spark-dwine-helper, fonts-wqy-microhei, fonts-wqy-zenhei"
                        ][int(chooseWineHelperValue.isChecked())])
    debRecommend.setText("")
    if os.path.exists(wine[wineVersion.currentText()]):
        debDepends.setText(["deepin-wine-helper (>= 5.1.30-1)",
                        "spark-dwine-helper | store.spark-app.spark-dwine-helper"
                        ][int(chooseWineHelperValue.isChecked())])
        if "deepin-wine5-stable" in wine[wineVersion.currentText()]:
            debDepends.setText("libasound2 (>= 1.0.16), libc6 (>= 2.28), libglib2.0-0 (>= 2.12.0), libgphoto2-6 (>= 2.5.10), libgphoto2-port12 (>= 2.5.10), libgstreamer-plugins-base1.0-0 (>= 1.0.0), libgstreamer1.0-0 (>= 1.4.0), liblcms2-2 (>= 2.2+git20110628), libldap-2.4-2 (>= 2.4.7), libmpg123-0 (>= 1.13.7), libopenal1 (>= 1.14), libpcap0.8 (>= 0.9.8), libpulse0 (>= 0.99.1), libudev1 (>= 183), libvkd3d1 (>= 1.0), libx11-6, libxext6, libxml2 (>= 2.9.0), ocl-icd-libopencl1 | libopencl1, udis86, zlib1g (>= 1:1.1.4), libasound2-plugins, libncurses6 | libncurses5 | libncurses, deepin-wine-plugin-virtual")
            debRecommend.setText("libcapi20-3, libcups2, libdbus-1-3, libfontconfig1, libfreetype6, libglu1-mesa | libglu1, libgnutls30 | libgnutls28 | libgnutls26, libgsm1, libgssapi-krb5-2, libjpeg62-turbo | libjpeg8, libkrb5-3, libodbc1, libosmesa6, libpng16-16 | libpng12-0, libsane | libsane1, libsdl2-2.0-0, libtiff5, libv4l-0, libxcomposite1, libxcursor1, libxfixes3, libxi6, libxinerama1, libxrandr2, libxrender1, libxslt1.1, libxxf86vm1")

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

change = False
autoChange = True  # 有第一次的路径自动设置
def AutoPathSet():
    global autoChange
    autoChange = True
    architecture = ["i386", "arm64", "arm64"]
    if not change:
        e12_text.setText(f"{get_desktop_path()}/{e1_text.text()}_{e2_text.text()}_{architecture[debArch.currentIndex()]}.deb")

def UserPathSet():
    global change
    global autoChange
    if autoChange:
        autoChange = False
        return
    change = True

def ReadDeb(unzip = False):
    # 获取路径
    debPath = QtWidgets.QFileDialog.getOpenFileName(window, "读取 deb 包", get_home(), "deb包(*.deb);;所有文件(*.*)")[0]
    print(debPath)
    if debPath == "":
        return
    # 分类讨论
    path = f"/tmp/deb-unzip-{random.randint(0, 1000)}"
    # 新建文件夹
    os.system(f"mkdir -p '{path}'")
    # 解包 control 文件
    os.system(f"dpkg -e '{debPath}' '{path}/DEBIAN'")
    # 读取 control 文件
    file = open(f"{path}/DEBIAN/control", "r")
    lists = file.read().splitlines()

    # 控件映射表
    lnkMap = {
        "Package": e1_text,
        "Version": e2_text,
        "Description": e3_text,
        "Maintainer": e4_text,
        "Recommends": debRecommend,
        "Depends": debDepends
    }

    for i in lists:
        # 遍历文件
        items = i.strip()
        try:
            lnkMap[items[:items.index(":")]].setText(items[items.index(":") + 1:].strip())
            if unzip:
                # 解压全部文件将不在 control 分析 wine 版本以提升运行效率
                continue
            print(items[:items.index(":")])
            if items[:items.index(":")] == "Depends":
                # 以下可以通过依赖判断使用什么 wine
                depends = items[items.index(":") + 1:].strip().split(",")
                for i in depends:
                    print(i)
                    # 读取
                    if "(" in i:
                        # 如果有括号（即版本号限制的情况）
                        temp = i.strip()
                        dependsItem = temp[:temp.index("(")]
                    else:
                        dependsItem = i.strip()
                    try:
                        # 这个 wine 是理论上用于运行的 wine
                        print(wineValue[dependsItem])
                        wineVersion.setCurrentText(wineValue[dependsItem])
                        break
                    except:
                        print("此 Wine 不存在")
        except:
            # 报错忽略
            print(f"“{items}”项忽略")

    # 判断 postrm 文件是不是自动移除脚本
    # postrm 文件不存在就不需要考虑
    # 三个特征：
    # 1、/home/$username/.deepinwine
    # 2、非卸载，跳过清理
    # 3、清理卸载残留
    # 都符合才算
    rmBash.setChecked(False)
    if os.path.exists(f"{path}/DEBIAN/postrm"):
        # 读取文件进行特征筛查
        file = open(f"{path}/DEBIAN/postrm", "r")
        postrm = file.read()
        if "/home/$username/.deepinwine" in postrm and "非卸载，跳过清理" in postrm and "清理卸载残留" in postrm:
            rmBash.setChecked(True)
        file.close()
    # 解包主文件
    if not unzip:
        # 只解压 control 文件的话，结束
        # 顺便删除临时文件
        os.system(f"rm -rfv '{path}'")
        return
    os.system(f"dpkg -x '{debPath}' '{path}'")
    # 读取文件
    # 目前只能实现读取 Wine 运行器（生态适配脚本的也可以读取）打包的 deb
    # opt/apps/XXX/files/run.sh 的文件读取识别
    if not os.path.exists(f"{path}/opt/apps/"):
        return
    # 取默认第一个
    package = os.listdir(f"{path}/opt/apps/")[0]
    # 读 7z（基本不读取）
    if os.path.exists(f"{path}/opt/apps/{package}/files/files.7z"):
        e6_text.setText(f"{path}/opt/apps/{package}/files/files.7z")
    lnkMap = {
        "Icon": e9_text,
        "Name": e8_text,
        "MimeType": e10_text
    }
    # 读 desktop 文件
    if os.path.exists(f"{path}/opt/apps/{package}/entries/applications"):
        filePath = f"{path}/opt/apps/{package}/entries/applications/{os.listdir(f'{path}/opt/apps/{package}/entries/applications')[0]}"
        file = open(filePath, "r")
        items = file.read().splitlines()
        file.close()
        for i in items:
            # 按行解析
            if i.replace(" ", "").replace("\n", "") == "":
                # 空行，忽略
                continue
            # 忽略注释
            line = i
            if "#" in line:
                line = line[:line.index("#")]
            # 判断是否合法
            try:
                name = line[:line.index("=")].strip()
                value = line[line.index("=") + 1:]#.replace("\"", "").strip()
                if name in lnkMap:
                    lnkMap[name].setText(value)
                    continue
                # 其它的特殊情况判断
                if name == "Exec":
                    value = value[value.index(".sh") + 3:].strip()
                    if value[0] == "\"":
                        value = value[1:].strip()
                    # helper
                    e15_text.setText(value)
                if name == "Categories":
                    option1_text.setCurrentText(value)
            except:
                print(f"忽略行：{i}")
    lnkMap = {
        "BOTTLENAME": e5_text,
        "EXEC_PATH": e7_text
        #"APPRUN_CMD"
    }
    # 读 run.sh
    if os.path.exists(f"{path}/opt/apps/{package}/files/run.sh"):
        file = open(f"{path}/opt/apps/{package}/files/run.sh", "r")
        items = file.read().splitlines()
        file.close()
        for i in items:
            # 按行解析
            if i.replace(" ", "").replace("\n", "") == "":
                # 空行，忽略
                continue
            # 忽略 export
            line = i.replace("export ", "")
            # 忽略注释
            if "#" in line:
                line = line[:line.index("#")]
            # 判断是否合法
            try:
                name = line[:line.index("=")].strip()
                value = line[line.index("=") + 1:].replace("\"", "").strip()
                #lnkMap[name].setText(value)
                if name in lnkMap:
                    lnkMap[name].setText(value)
                    continue
                # 其它的特殊情况判断
                if name == "START_SHELL_PATH" and value == "/opt/deepinwine/tools/spark_run_v4.sh":
                    # helper
                    chooseWineHelperValue.setChecked(True)
                if name == "APPRUN_CMD" and value in wineValue:
                    wineVersion.setCurrentText(wineValue[dependsItem])
            except:
                print(f"忽略行：{i}")
    elif os.path.exists(f"{path}/opt/apps/{package}/files/run_with_box86.sh"):
        file = open(f"{path}/opt/apps/{package}/files/run_with_box86.sh", "r")
        items = file.read().splitlines()
        file.close()
        for i in items:
            # 按行解析
            if i.replace(" ", "").replace("\n", "") == "":
                # 空行，忽略
                continue
            # 忽略 export
            line = i.replace("export ", "")
            # 忽略注释
            if "#" in line:
                line = line[:line.index("#")]
            # 判断是否合法
            try:
                name = line[:line.index("=")].strip()
                value = line[line.index("=") + 1:].replace("\"", "").strip()
                #lnkMap[name].setText(value)
                if name in lnkMap:
                    lnkMap[name].setText(value)
                    continue
                # 其它的特殊情况判断
                if name == "START_SHELL_PATH" and value == "/opt/deepinwine/tools/spark_run_v4.sh":
                    # helper
                    chooseWineHelperValue.setChecked(True)
                if name == "APPRUN_CMD" and value in wineValue:
                    wineVersion.setCurrentText(wineValue[dependsItem])
            except:
                print(f"忽略行：{i}")
    elif os.path.exists(f"{path}/opt/apps/{package}/files/run_with_exagear.sh"):
        file = open(f"{path}/opt/apps/{package}/files/run_with_exagear.sh", "r")
        items = file.read().splitlines()
        file.close()
        for i in items:
            # 按行解析
            if i.replace(" ", "").replace("\n", "") == "":
                # 空行，忽略
                continue
            # 忽略 export
            line = i.replace("export ", "")
            # 忽略注释
            if "#" in line:
                line = line[:line.index("#")]
            # 判断是否合法
            try:
                name = line[:line.index("=")].strip()
                value = line[line.index("=") + 1:].replace("\"", "").strip()
                #lnkMap[name].setText(value)
                if name in lnkMap:
                    lnkMap[name].setText(value)
                    continue
                # 其它的特殊情况判断
                if name == "START_SHELL_PATH" and value == "/opt/deepinwine/tools/spark_run_v4.sh":
                    # helper
                    chooseWineHelperValue.setChecked(True)
                if name == "APPRUN_CMD" and value in wineValue:
                    wineVersion.setCurrentText(wineValue[dependsItem])
            except:
                print(f"忽略行：{i}")



###############
# 程序信息
###############
programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
# 如果要添加其他 wine，请在字典添加其名称和执行路径
wine = {"deepin-wine": "deepin-wine", "deepin-wine5": "deepin-wine5", "wine": "wine", "wine64": "wine64", "deepin-wine5 stable": "deepin-wine5-stable", "deepin-wine6 stable": "deepin-wine6-stable", "spark-wine7-devel": "spark-wine7-devel", "ukylin-wine": "ukylin-wine"}
wineValue = {"deepin-wine": "deepin-wine", "deepin-wine5": "deepin-wine5", "wine": "wine", "wine64": "wine64", "deepin-wine5-stable": "deepin-wine5 stable", "deepin-wine6-stable": "deepin-wine6 stable", "spark-wine7-devel": "spark-wine7-devel", "ukylin-wine": "ukylin-wine"}
# 读取 wine 本地列表
for i in ["/opt/wine-staging", "/opt/wine-dev", "/opt/wine-stable", "/opt/spark-wine7-devel"]:
    if os.path.exists(i):
        wine[i] = i
try:
    for i in os.listdir(f"{get_home()}/.deepinwine"):
        if os.path.exists(f"{get_home()}/.deepinwine/{i}/bin/wine"):
            wine[f"{get_home()}/.deepinwine/{i}"] = f"{get_home()}/.deepinwine/{i}"
except:
    pass
try:
    for i in json.loads(readtxt(f"{programPath}/wine/winelist.json")):
        if os.path.exists(f"{programPath}/wine/{i}.7z"):
            wine[f"{programPath}/wine/{i}.7z"] = f"{programPath}/wine/{i}.7z"
            continue
        if os.path.exists(f"{programPath}/wine/{i}"):
            wine[f"{programPath}/wine/{i}"] = f"{programPath}/wine/{i}"
except:
    pass
os.chdir("/")
iconPath = "{}/deepin-wine-runner.svg".format(programPath)
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
button1 = QtWidgets.QPushButton(QtCore.QCoreApplication.translate("U", "浏览……"))
button2 = QtWidgets.QPushButton(QtCore.QCoreApplication.translate("U", "浏览……"))
button4 = QtWidgets.QPushButton(QtCore.QCoreApplication.translate("U", "浏览……"))
debControlFrame = QtWidgets.QHBoxLayout()
button5 = QtWidgets.QPushButton(QtCore.QCoreApplication.translate("U", "打包……"))
installDeb = QtWidgets.QPushButton(QtCore.QCoreApplication.translate("U", "安装打包完成的 deb……"))
buildDebDir = QtWidgets.QPushButton(QtCore.QCoreApplication.translate("U", "根据填写内容打包模板"))
debControlFrame.addWidget(button5)
debControlFrame.addWidget(installDeb)
rmBash = QtWidgets.QCheckBox(QtCore.QCoreApplication.translate("U", "设置卸载该 deb 后自动删除该容器"))
cleanBottonByUOS = QtWidgets.QCheckBox(QtCore.QCoreApplication.translate("U", "使用统信 Wine 生态适配活动容器清理脚本"))
debArch = QtWidgets.QComboBox()
debArch.addItems(["i386", "arm64(box86)", "arm64(exagear)"])
textbox1 = QtWidgets.QTextBrowser()
option1_text.addItems(["Network", "Chat", "Audio", "Video", "Graphics", "Office", "Translation", "Development", "Utility"])
option1_text.setCurrentText("Network")
wineFrame = QtWidgets.QHBoxLayout()
chooseWineHelperValue = QtWidgets.QCheckBox(QtCore.QCoreApplication.translate("U", "使用星火wine helper\n（如不勾选默认为deepin-wine-helper）"))
button1.clicked.connect(button1_cl)
button2.clicked.connect(button2_cl)
button4.clicked.connect(button4_cl)
button5.clicked.connect(make_deb)
buildDebDir.clicked.connect(lambda: make_deb(True))
installDeb.clicked.connect(InstallDeb)
wineFrame.addWidget(wineVersion)
# 创建控件
widgetLayout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("U", "要打包的 deb 包的包名（※必填）：")), 0, 0, 1, 1)
widgetLayout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("U", "要打包的 deb 包的版本号（※必填）：")), 1, 0, 1, 1)
widgetLayout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("U", "要打包的 deb 包的说明（※必填）：")), 2, 0, 1, 1)
widgetLayout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("U", "要打包的 deb 包的维护者（※必填）：")), 3, 0, 1, 1)
widgetLayout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("U", "要解压的 wine 容器的容器名（※必填）：")), 4, 0, 1, 1)
widgetLayout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("U", "要解压的 wine 容器（※必填）：")), 5, 0, 1, 1)
widgetLayout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("U", "wine 容器里需要运行的可执行文件路径（※必填）：")), 6, 0, 1, 1)
widgetLayout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("U", "要显示的 .desktop 文件的分类（※必填）：")), 7, 0, 1, 1)
widgetLayout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("U", "wine 容器里需要运行的可执行文件的参数（选填）：")), 8, 0, 1, 1)
widgetLayout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("U", "要显示的 .desktop 文件的名称（※必填）：")), 9, 0, 1, 1)
widgetLayout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("U", "要显示的 .desktop 文件的图标（选填）：")), 10, 0, 1, 1)
widgetLayout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("U", "选择打包的 wine 版本（※必选）：")), 12, 0, 1, 1)
widgetLayout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("U", "打包 deb 的保存路径（※必填）：")), 13, 0, 1, 1)
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
widgetLayout.addLayout(wineFrame, 12, 1, 1, 1)
widgetLayout.addWidget(e12_text, 13, 1, 1, 1)
widgetLayout.addWidget(button4, 13, 2, 1, 1)
widgetLayout.addLayout(debControlFrame, 16, 1, 1, 1)
widgetLayout.addWidget(label13_text, 17, 0, 1, 3)
widgetLayout.addWidget(textbox1, 18, 0, 1, 3)
# 高级功能
moreSetting = QtWidgets.QGroupBox(QtCore.QCoreApplication.translate("U", "高级设置"))
debDepends = QtWidgets.QLineEdit()
debRecommend = QtWidgets.QLineEdit()
debDepends.setPlaceholderText(QtCore.QCoreApplication.translate("U", "deb 包的依赖(如无特殊需求默认即可)"))
debDepends.setText("deepin-wine6-stable, deepin-wine-helper (>= 5.1.30-1), fonts-wqy-microhei, fonts-wqy-zenhei")
debRecommend.setPlaceholderText(QtCore.QCoreApplication.translate("U", "deb 包的推荐依赖(非强制，一般默认即可)"))
moreSettingLayout = QtWidgets.QVBoxLayout()
localWineVersion = QtWidgets.QComboBox()
useInstallWineArch = QtWidgets.QComboBox()
useInstallWineArch.addItems(["wine", "wine64"])
moreSettingLayout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("U", "Wine 位数(只限本地需要打包集成的Wine)：\n提示：32位的Wine不能使用64位容器")))
#moreSettingLayout.addWidget(localWineVersion)
moreSettingLayout.addWidget(useInstallWineArch)
moreSettingLayout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("U", "deb 包选项：")))
moreSettingLayout.addWidget(rmBash)
moreSettingLayout.addWidget(cleanBottonByUOS)
moreSettingLayout.addWidget(chooseWineHelperValue)
moreSettingLayout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("U", "deb 的依赖(强制，如无特殊需求默认即可)：")))
moreSettingLayout.addWidget(debDepends)
moreSettingLayout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("U", "deb 的推荐依赖(非强制，一般默认即可)：")))
moreSettingLayout.addWidget(debRecommend)
moreSettingLayout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("U", "要显示的 .desktop 文件的 MimeType：")))
moreSettingLayout.addWidget(e10_text)
moreSettingLayout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("U", "打包 deb 架构：")))
moreSettingLayout.addWidget(debArch)
moreSetting.setLayout(moreSettingLayout)
widgetLayout.addWidget(moreSetting, 0, 3, 16, 1)
widgetLayout.addWidget(buildDebDir, 16, 3)
useInstallWineArch.setDisabled(True)
wineVersion.currentTextChanged.connect(ChangeWine)
chooseWineHelperValue.stateChanged.connect(ChangeWine)
e1_text.textChanged.connect(AutoPathSet)
e2_text.textChanged.connect(AutoPathSet)
debArch.currentIndexChanged.connect(AutoPathSet)
debArch.currentIndexChanged.connect(ChangeArchCombobox)
e12_text.textChanged.connect(UserPathSet)
# 菜单栏
menu = window.menuBar()
programmenu = menu.addMenu(QtCore.QCoreApplication.translate("U", "程序"))
debMenu = menu.addMenu(QtCore.QCoreApplication.translate("U", "deb 包"))
help = menu.addMenu(QtCore.QCoreApplication.translate("U", "帮助"))
exit = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "退出程序"))
debE = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "只读取 Control 信息"))
debX = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "读取所有（需解包，时间较久）"))
tip = QtWidgets.QAction(QtCore.QCoreApplication.translate("U", "小提示"))
exit.triggered.connect(window.close)
tip.triggered.connect(helps)
programmenu.addAction(exit)
debMenu.addAction(debE)
debMenu.addAction(debX)
debE.triggered.connect(lambda: ReadDeb(False))
debX.triggered.connect(lambda: ReadDeb(True))
help.addAction(tip)
# 控件配置
try:
    e6_text.setText(sys.argv[1].replace("~", get_home()))
    e5_text.setText(pathlib.PurePath(sys.argv[1]).name)
    wineVersion.setCurrentText(sys.argv[2])
except:
    pass
e12_text.setText(f"{get_desktop_path()}/demo_1.0.0_i386.deb")
widget.setLayout(widgetLayout)
window.setCentralWidget(widget)
window.setWindowTitle(f"wine 应用打包器 {version}")
window.setWindowIcon(QtGui.QIcon(iconPath))
window.resize(int(window.frameSize().width() * 2.1), window.frameSize().height())
window.show()
sys.exit(app.exec_())
# Flag：解包只读control和解包全部读取