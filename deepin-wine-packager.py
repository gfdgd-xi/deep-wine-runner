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
import updatekiller
import threading
import traceback
import subprocess
import webbrowser
from PIL import Image
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets
from trans import *
from DefaultSetting import *
from Model import *
import globalenv

TMPDIR = os.getenv("TMPDIR")
if (TMPDIR == None):
    TMPDIR = ""

#################
# 程序所需事件
#################

def button1_cl():
    path = QtWidgets.QFileDialog.getExistingDirectory(widget, transla.transe("U", "选择 wine 容器"), f"{get_home()}/.deepinwine")
    if path != "":
        e6_text.setText(path)

def button2_cl(number):
    path = QtWidgets.QFileDialog.getOpenFileName(widget, transla.transe("U", "选择图标文件"), get_home(), "PNG图标(*.png);;SVG图标(*.svg);;全部文件(*.*)")[0]
    if path != "":
        mapLink[number].setText(path)

def button4_cl():
    path = QtWidgets.QFileDialog.getSaveFileName(widget, transla.transe("U", "保存 deb 包"), get_home(), "deb 文件(*.deb);;所有文件(*.*)", "{}_{}_all.deb".format(e1_text.text(), e2_text.text()))[0]
    if path != "":
        e12_text.setText(path)

def disabled_or_NORMAL_all(choose):
    choose = not choose
    enableCopyIconToDesktop.setDisabled(choose)
    disabledMono.setDisabled(choose)
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
    desktopIconTab.setDisabled(choose)
    build7z.setDisabled(choose)
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
    debFirstArch.setDisabled(choose)
    helperConfigPathButton.setDisabled(choose)
    helperConfigPathText.setDisabled(choose)
    debContainHelper.setDisabled(choose)
    #if not choose:
    #    ChangeArchCombobox()
    #    ChangeWine()
    
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

class build7z_threading(QtCore.QThread):
    signal = QtCore.pyqtSignal(str)
    label = QtCore.pyqtSignal(str)
    getSavePath = QtCore.pyqtSignal(str)
    errorMsg = QtCore.pyqtSignal(str)
    infoMsg = QtCore.pyqtSignal(str)
    disabled_or_NORMAL_all = QtCore.pyqtSignal(bool)
    build = ""
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
        path = self.build
        try:
            self.disabled_or_NORMAL_all.emit(False)
            if e6_text.text() == "/":
                b = e6_text.text()[:-1]
            else:
                b = e6_text.text()
            debInformation = [
                {
                    # I386 wine 打包配置文件
                    "Wine": wine[wineVersion.currentText()]
                },
                {
                    # ARM64 通用 wine 打包配置文件
                    "Wine": f"WINEPREDLL='{programPath}/dlls-arm' WINEDLLPATH=/opt/deepin-wine6-stable/lib BOX86_NOSIGSEGV=1 /opt/deepin-box86/box86 /opt/deepin-wine6-stable/bin/wine ",
                }
            ]
            if not path[1] or path[0] == "":
                return
            debPackagePath = path[0]
            Build7z(b, self, debInformation, debPackagePath)
            self.infoMsg.emit("打包完成！")
            self.disabled_or_NORMAL_all.emit(True)
        except:
            traceback.print_exc()
            self.errorMsg.emit(traceback.format_exc())

        
def Build7z(b, self, debInformation, debPackagePath):
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
    elif debArch.currentIndex() == 2 and e6_text.text()[-3: ] != ".7z":
        os.chdir(b)
        # 对用户目录进行处理
        self.run_command("sed -i \"s#$USER#crossover#\" ./*.reg")
        os.chdir(f"{b}/drive_c/users")
        if os.path.exists(f"{b}/drive_c/users/crossover"):
            self.run_command(f"rm -rfv '{b}/drive_c/users/crossover'")
        self.run_command(f"mv -fv '{os.getlogin()}' crossover")
        # 删除因为脚本失误导致用户目录嵌套（如果存在）
        if os.path.exists(f"{b}{b}/drive_c/users/crossover/crossover"):
            shutil.rmtree(f"{b}{b}/drive_c/users/crossover/crossover")
        # 删除无用的软链
        self.run_command(f"rm -fv '{b}/drive_c/users/crossover/我的'*")
        self.run_command(f"rm -fv '{b}/drive_c/users/crossover/My '*")
        self.run_command(f"rm -fv '{b}/drive_c/users/crossover/Desktop'")
        self.run_command(f"rm -fv '{b}/drive_c/users/crossover/Downloads'")
        self.run_command(f"rm -fv '{b}/drive_c/users/crossover/Templates'")
    os.chdir(programPath)
    ###############
    # 压缩容器
    ###############
    self.label.emit("正在打包 wine 容器")
    # 都有 7z 了为什么要打包呢？
    if e6_text.text()[-3: ] == ".7z":
        shutil.copy(e6_text.text(), f"{debPackagePath}/opt/apps/{e1_text.text()}/files/files.7z")
    else:
        if debArch.currentIndex() == 2:
            # Crossover 包直接拷贝容器即可，无需打包 7z
            os.system(f"cp -rv '{b}' '{debPackagePath}/opt/cxoffice/support/{e5_text.text()}'")
            return
        if debPackagePath[-3: ] == ".7z":
            self.run_command("7z a -snh -snl '{}' '{}/'*".format(debPackagePath, b))
        else:
            self.run_command("7z a -snh -snl {}/opt/apps/{}/files/files.7z '{}/'*".format(debPackagePath, e1_text.text(), b))


def Build7zButton_Clicked():
    path = QtWidgets.QFileDialog.getSaveFileName(window, "选择保存位置", get_home(), "7z文件(*.7z);;所有文件(*.*)")
    print(path)
    QT.thread = build7z_threading(path)
    QT.thread.signal.connect(chang_textbox1_things)
    QT.thread.label.connect(label13_text_change)
    QT.thread.getSavePath.connect(SavePathGet)
    QT.thread.errorMsg.connect(ErrorMsg)
    QT.thread.infoMsg.connect(InfoMsg)
    QT.thread.disabled_or_NORMAL_all.connect(disabled_or_NORMAL_all)
    QT.thread.start()

def make_deb(build=False):
    global bottleNameLock
    clean_textbox1_things()
    disabled_or_NORMAL_all(False)
    badComplete = False
    # 规范检测
    if e1_text.text().lower() != e1_text.text():
        if QtWidgets.QMessageBox.warning(window, "提示", f"包名 {e1_text.text()} 似乎不符合规范，可能会导致打包后的包无法投稿到应用商店，是否继续？\n可参考 deb 安装包打包标准", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No) == QtWidgets.QMessageBox.No:
            disabled_or_NORMAL_all(True)
            label13_text_change("用户已取消")
            return    
    for i in range(len(iconUiList)):
        if os.path.splitext(iconUiList[i][4].text())[1] == ".ico":
            if QtWidgets.QMessageBox.warning(window, "提示", f"图标 {iconUiList[i][4].text()} 似乎为 ico 格式，可能会导致打包后的程序在启动器的图标无法正常显示，是否继续？", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No) == QtWidgets.QMessageBox.No:
                disabled_or_NORMAL_all(True)
                label13_text_change("用户已取消")
                return    
        if os.path.exists(iconUiList[i][0].text()) and not "c:" in iconUiList[i][0].text().lower():
            if not e6_text.text() in iconUiList[i][0].text():
                if QtWidgets.QMessageBox.warning(window, "提示", f"路径 {iconUiList[i][0].text()} 似乎不符合规范且不位于容器内，可能会导致打包后的程序无法运行，是否继续？\n可参考 Windows 下的文件路径", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No) == QtWidgets.QMessageBox.No:
                    disabled_or_NORMAL_all(True)
                    label13_text_change("用户已取消")
                    return    
            if QtWidgets.QMessageBox.warning(window, "提示", f"路径 {iconUiList[i][0].text()} 似乎不符合规范，可能会导致打包后的程序无法运行，是否继续？\n可参考 Windows 下的文件路径", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No) == QtWidgets.QMessageBox.No:
                disabled_or_NORMAL_all(True)
                label13_text_change("用户已取消")
                return
        for k in [0, 3]:
            if iconUiList[i][k].text().replace(" ", "") == "":
                badComplete = True
    if badComplete or e1_text.text() == "" or e2_text.text() == "" or e3_text.text() == "" or e4_text.text() == "" or e5_text.text() == "" or e6_text.text() == "" or e7_text.text() == "" or e8_text.text() == "" or e12_text.text() == "":
        QtWidgets.QMessageBox.critical(widget, "错误", "必填信息没有填写完整，无法继续构建 deb 包")
        disabled_or_NORMAL_all(True)
        label13_text_change("必填信息没有填写完整，无法继续构建 deb 包")
        return
    if QtWidgets.QMessageBox.question(widget, transla.transe("U", "提示"), transla.transe("U", "打包将会改动现在选择的容器，是否继续？")) == QtWidgets.QMessageBox.No:
        disabled_or_NORMAL_all(True)
        return
    # 警告信息
    for i in iconUiList:
        if os.path.exists(i[0].text()):
            if QtWidgets.QMessageBox.warning(window, "警告", "输入的路径似乎是一个绝对路径\n不建议打包绝对路径，建议是 Wine 容器内路径\n是否继续打包？", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No) == QtWidgets.QMessageBox.No:
                disabled_or_NORMAL_all(True)
                return
        if "c:/user" in i[0].text().replace(" ", "").replace("\\", "/").lower():
            if QtWidgets.QMessageBox.warning(window, "警告", "输入的路径似乎是在容器的用户目录内，打包后可能会出现找不到 exe 的情况，是否继续？", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No) == QtWidgets.QMessageBox.No:
                disabled_or_NORMAL_all(True)
                return
        if i[0].text()[:2].lower() == "c:" and not os.path.exists("{}/drive_c/{}".format(
            e6_text.text(), 
            i[0].text()[3:].replace("\\", '/'))):
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
    bottleNameLock = False
    QT.thread.start()
    #thread.start()


def label13_text_change(thing):
    label13_text.setText(f"<p align='center'>当前 deb 打包情况：{thing}</p>")

def ReplaceText(string: str, lists: list):
    for i in lists:
        string = string.replace(i[0], i[1])
    return string

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
            if desktopIconTab.count() <= 1:
                if e9_text.text() != "":
                    # 获取图片格式（不太准）
                    try:
                        im = Image.open(e9_text.text())
                        imms = im.format.lower()
                    except: # 未知（就直接设置为 svg 后缀）
                        imms = "svg"
                    a = "/opt/apps/{}/entries/icons/hicolor/scalable/apps/{}.{}".format(e1_text.text(), e1_text.text(), imms)
                    if not os.path.exists(e9_text.text()):
                        self.errorMsg.emit("图标的路径填写错误，无法进行构建 deb 包")
                        self.disabled_or_NORMAL_all.emit(True)
                        self.label.emit("图标的路径填写错误，无法进行构建 deb 包")
                        return
            else:
                a = []
                for i in iconUiList:
                    if i[4].text != "":
                        # 获取图片格式（不太准）
                        try:
                            im = Image.open(e9_text.text())
                            imms = im.format.lower()
                        except:
                            imms = ".svg"
                        a.append("/opt/apps/{}/entries/icons/hicolor/scalable/apps/{}-{}.{}".format(e1_text.text(), e1_text.text(), os.path.splitext(os.path.basename(i[0].text().replace("\\", "/")))[0], imms))
                        if not os.path.exists(i[4].text()):
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
                    "Architecture": debFirstArch.currentText(),
                    "Depends": [
                        f"{wine[wineVersion.currentText()]}, deepin-wine-helper | com.wine-helper.deepin, fonts-wqy-microhei, fonts-wqy-zenhei",
                        f"{wine[wineVersion.currentText()]}, spark-dwine-helper | store.spark-app.spark-dwine-helper | deepin-wine-helper | com.wine-helper.deepin, fonts-wqy-microhei, fonts-wqy-zenhei"
                        ][int(chooseWineHelperValue.isChecked())],
                    "postinst": ['', readtxt(f"{programPath}/packager-config/postinst")][enableCopyIconToDesktop.isChecked()],
                    "postrm": ["", readtxt(f"{programPath}/packager-config/postrm")][int(rmBash.isChecked())],
                    "run.sh": [
                        readtxt(f"{programPath}/packager-config/run-old.sh"), 
                        readtxt(f"{programPath}/packager-config/run.sh")
                        ][chooseWineHelperValue.isChecked()],
                        "info": readtxt(f"{programPath}/packager-config/uos-info.json")
                },
                {
                    # ARM64 通用 wine 打包配置文件
                    "Wine": f"WINEPREDLL='{programPath}/dlls-arm' WINEDLLPATH=/opt/deepin-wine6-stable/lib BOX86_NOSIGSEGV=1 /opt/deepin-box86/box86 /opt/deepin-wine6-stable/bin/wine ",
                    "Architecture": "arm64",
                    "Depends": "com.deepin-wine6-stable.deepin (>= 6.0deepin31), com.wine-helper.deepin (>= 0.0.8), com.deepin-box86.deepin (>= 0.2.6deepin3), deepin-elf-verify (>= 1.1.1-1)",
                    "postinst": f"""#!/bin/bash
{['', f'''PACKAGE_NAME="{e1_text.text()}"
for username in $(ls /home)  
do
    echo /home/$username
    if [ -d /home/$username/桌面 ]; then
        cp /opt/apps/$PACKAGE_NAME/entries/applications/* /home/$username/桌面
    fi
    if [ -d /home/$username/Desktop ]; then
        cp /opt/apps/$PACKAGE_NAME/entries/applications/* /home/$username/Desktop
    fi
done'''][enableCopyIconToDesktop.isChecked()]}
ACTIVEX_NAME=""

if [ -f "/opt/apps/{e1_text.text()}/files/install.sh" ];then
    /opt/apps/{e1_text.text()}/files/install.sh -i
fi

if [ -n "$ACTIVEX_NAME" ]; then
    if [ ! -d "/usr/lib/mozilla/plugins" ];then
        mkdir -p /usr/lib/mozilla/plugins
    fi
    cp /usr/lib/pipelight/libpipelight.so /usr/lib/mozilla/plugins/libpipelight-${{ACTIVEX_NAME}}.so
    glib-compile-schemas /usr/share/glib-2.0/schemas/
fi

# Make sure the script returns 0
true
""",
                    # 因为 arm 不依赖 helper，所以要自带 kill.sh
                    "kill.sh": readtxt(f"{programPath}/packager-config/arm-kill.sh"),
                    "postrm": [f"""#!/bin/sh

ACTIVEX_NAME=""

if [ -f "/opt/apps/{e1_text.text()}/files/install.sh" ];then
    /opt/apps/{e1_text.text()}/files/install.sh -r
fi

if [ -n "$ACTIVEX_NAME" ]; then
    rm /usr/lib/mozilla/plugins/libpipelight-${{ACTIVEX_NAME}}.so
    glib-compile-schemas /usr/share/glib-2.0/schemas/
fi

# Make sure the script returns 0
true
""", readtxt(f"{programPath}/packager-config/postrm")][int(rmBash.isChecked())],
                "run.sh": readtxt(f"{programPath}/packager-config/run.sh"),
                "info": readtxt(f"{programPath}/packager-config/uos-info.sh")
                }
            ]
            print("c")
            if os.path.exists(wine[wineVersion.currentText()]):
                debInformation[0]["Depends"] = ["deepin-wine-helper | com.wine-helper.deepin",
                        "spark-dwine-helper | store.spark-app.spark-dwine-helper | deepin-wine-helper | com.wine-helper.deepin"
                        ][int(chooseWineHelperValue.isChecked())] #+ ["", "libasound2 (>= 1.0.16), libc6 (>= 2.28), libglib2.0-0 (>= 2.12.0), libgphoto2-6 (>= 2.5.10), libgphoto2-port12 (>= 2.5.10), libgstreamer-plugins-base1.0-0 (>= 1.0.0), libgstreamer1.0-0 (>= 1.4.0), liblcms2-2 (>= 2.2+git20110628), libldap-2.4-2 (>= 2.4.7), libmpg123-0 (>= 1.13.7), libopenal1 (>= 1.14), libpcap0.8 (>= 0.9.8), libpulse0 (>= 0.99.1), libudev1 (>= 183), libvkd3d1 (>= 1.0), libx11-6, libxext6, libxml2 (>= 2.9.0), ocl-icd-libopencl1 | libopencl1, udis86, zlib1g (>= 1:1.1.4), libasound2-plugins, libncurses6 | libncurses5 | libncurses, deepin-wine-plugin-virtual\nRecommends: libcapi20-3, libcups2, libdbus-1-3, libfontconfig1, libfreetype6, libglu1-mesa | libglu1, libgnutls30 | libgnutls28 | libgnutls26, libgsm1, libgssapi-krb5-2, libjpeg62-turbo | libjpeg8, libkrb5-3, libodbc1, libosmesa6, libpng16-16 | libpng12-0, libsane | libsane1, libsdl2-2.0-0, libtiff5, libv4l-0, libxcomposite1, libxcursor1, libxfixes3, libxi6, libxinerama1, libxrandr2, libxrender1, libxslt1.1, libxxf86vm1"][]
                print("d")
                debInformation[0]["run.sh"] = readtxt(f"{programPath}/packager-config/run.sh")

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
                debPackagePath = f"{TMPDIR}/tmp/{random.randint(0, 9999)}"
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
            os.makedirs("{}/usr/share/applications".format(debPackagePath))
            os.makedirs("{}/opt/apps/{}/entries/icons/hicolor/scalable/apps".format(debPackagePath, e1_text.text()))
            os.makedirs("{}/opt/apps/{}/files".format(debPackagePath, e1_text.text()))
            ###############
            # 创建文件
            ###############
            self.label.emit("正在创建文件……")
            os.mknod("{}/DEBIAN/control".format(debPackagePath))
            os.mknod("{}/opt/apps/{}/info".format(debPackagePath, e1_text.text()))
            #########!!!!!!!
            Build7z(b, self, debInformation, debPackagePath)
            ###############
            # 压缩 Wine
            ###############
            # Deepin Wine 包
            print("e")
            self.label.emit("正在处理 Wine")
            if os.path.exists(wine[wineVersion.currentText()]):
                shutil.copy(f"{programPath}/gtkGetFileNameDlg", f"{debPackagePath}/opt/apps/{e1_text.text()}/files/gtkGetFileNameDlg")
                #self.run_command(f"7z a -snh -snl '{debPackagePath}/opt/apps/{e1_text.text()}/files/wine_archive.7z' '{wine[wineVersion.currentText()]}/*'")
                # 不打包为 7z 资源包以让 UOS 可以签名到这些文件
                self.run_command(f"mkdir -pv '{debPackagePath}/opt/apps/{e1_text.text()}/files/wine'")
                self.run_command(f"cp -r '{wine[wineVersion.currentText()]}/'* '{debPackagePath}/opt/apps/{e1_text.text()}/files/wine'")
            ###############
            # 复制文件
            ###############
            self.label.emit("正在复制文件……")
            if os.path.exists(wine[wineVersion.currentText()]):
                shutil.copy(f"{programPath}/gtkGetFileNameDlg", f"{debPackagePath}/opt/apps/{e1_text.text()}/files")
            if debArch.currentIndex() == 1:
                # 解包文件
                if not os.path.exists(f"{programPath}/dlls-arm"):
                    self.run_command(f"7z x \"{programPath}/dlls-arm.7z\" -o\"{programPath}\"")
                    os.remove(f"{programPath}/dlls-arm.7z")
                if not os.path.exists(f"{programPath}/arm-package"):
                    self.run_command(f"7z x \"{programPath}/arm-package.7z\" -o\"{programPath}\"")
                    os.remove(f"{programPath}/arm-package.7z")
                self.run_command(f"cp -rv '{programPath}/dlls-arm' {debPackagePath}/opt/apps/{e1_text.text()}/files/dlls")
                self.run_command(f"cp -rv '{programPath}/exa' {debPackagePath}/opt/apps/{e1_text.text()}/files/exa")
                self.run_command(f"cp -rv '{programPath}/arm-package/'* {debPackagePath}/opt/apps/{e1_text.text()}/files/") 
            if desktopIconTab.count() <= 1:
                if e9_text.text() != "":
                    shutil.copy(e9_text.text(), "{}/opt/apps/{}/entries/icons/hicolor/scalable/apps/{}.{}".format(debPackagePath, e1_text.text(), e1_text.text(), imms))
            else:
                for i in range(len(a)):
                    shutil.copy(iconUiList[i][4].text(), "{}/{}".format(debPackagePath, a[i]))
            ################
            # 获取文件大小
            ################
            self.label.emit("正在计算文件大小……")
            size = int(getFileFolderSize(debPackagePath) / 1000)
            ################
            # 写入文本文档
            ################
            self.label.emit("正在写入文件……")
            if debRecommend.text() == "":
                write_txt(f"{debPackagePath}/DEBIAN/control", f'''Package: {e1_text.text()}
Version: {e2_text.text()}
Architecture: {debInformation[debArch.currentIndex()]["Architecture"]}
Maintainer: {e4_text.text()}
Depends: {debDepends.text()}
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
Depends: {debDepends.text()}
Recommends: {debRecommend.text()}
Section: non-free/otherosfs
Priority: optional
Multi-Arch: foreign
Installed-Size: {size}
Description: {e3_text.text()}
''')
            try:
                # 因为不一定含有此项，所以需要 try except
                if debInformation[debArch.currentIndex()]["preinst"] != "":
                    write_txt(f"{debPackagePath}/DEBIAN/preinst", debInformation[debArch.currentIndex()]["preinst"])
                if debInformation[debArch.currentIndex()]["prerm"] != "":
                    write_txt(f"{debPackagePath}/DEBIAN/prerm", debInformation[debArch.currentIndex()]["prerm"])
            except:
                pass
            line = "\\"
            if iconUiList[0][2].text().replace(" ", "") == "":
                command = f"--uri {iconUiList[0][2].text()}"
            else:
                command = iconUiList[0][2].text()
            replaceMap = [
                ["@@@BOTTLENAME@@@", e5_text.text()],
                ["@@@APPVER@@@", e2_text.text()],
                ["@@@EXEC_PATH@@@", e7_text.text()],
                ["@@@DEB_PACKAGE_NAME@@@", e1_text.text()],
                ["@@@APPRUN_CMD@@@", [
                    wine[wineVersion.currentText()], 
                    f"/opt/apps/{e1_text.text()}/files/wine/bin/wine"
                ][os.path.exists(f'{debPackagePath}/opt/apps/{e1_text.text()}/files/')]],
                ["@@@EXEC_NAME@@@", os.path.basename(e7_text.text().replace("\\", "/"))],
                ["@@@ARCH@@@", debFirstArch.currentText()],
                ["@@@APP_NAME@@@", e8_text.text()],
                ["@@@MAINTAINER@@@", e4_text.text()],
                ["@@@DESCRIPTION@@@", e3_text.text()],
                ["@@@DESKTOP_EXEC@@@", 
                 f'''"/opt/apps/{e1_text.text()}/files/run.sh" {command}'''],
                ["@@@DESKTOP_NAME@@@", iconUiList[0][3].text()],
                ["@@@DESKTOP_MIMETYPE@@@", iconUiList[0][5].text()],
                ["@@@DESKTOP_CATEGORIES@@@", iconUiList[0][1].currentText()]
            ]
            # a 是图标（为什么当初要取这个变量名）
            # 如果只有一个图标则为 str,两个及以上则为 list
            if (type(a) == list):
                replaceMap.append(["@@@ICON@@@", a[0]])
            else:
                replaceMap.append(["@@@ICON@@@", a])
            # 配置 postinst 和 postrm
            if debInformation[debArch.currentIndex()]["postinst"] != "":
                write_txt(f"{debPackagePath}/DEBIAN/postinst", ReplaceText(debInformation[debArch.currentIndex()]["postinst"], replaceMap))
            if debInformation[debArch.currentIndex()]["postrm"] != "":
                write_txt(f"{debPackagePath}/DEBIAN/postrm", ReplaceText(debInformation[debArch.currentIndex()]["postrm"], replaceMap))
            # 配置 UOS deb 包的 info 权限文件                  
            write_txt("{}/opt/apps/{}/info".format(debPackagePath, e1_text.text()), ReplaceText(debInformation[debArch.currentIndex()]["info"], replaceMap))
            line = "\\"
            # 要开始分类讨论了
            if debArch.currentIndex() == 0 or debArch.currentIndex() == 1:
                if desktopIconTab.count() <= 1:
                    desktopFile = ReplaceText(readtxt(f"{programPath}/packager-config/app.desktop"), replaceMap)
                    write_txt(f"{debPackagePath}/opt/apps/{e1_text.text()}/files/run.sh", ReplaceText(debInformation[debArch.currentIndex()]["run.sh"], replaceMap))
                    write_txt("{}/usr/share/applications/{}.desktop".format(debPackagePath, e1_text.text()), desktopFile)
                    write_txt("{}/opt/apps/{}/entries/applications/{}.desktop".format(debPackagePath, e1_text.text(), e1_text.text()), desktopFile)
                else:
                    for i in iconUiList:
                        if i[2].text().replace(" ", "") == "":
                            command = f"--uri {i[2].text()}"
                        else:
                            command = i[2].text()
                        replaceMap = [
                            ["@@@BOTTLENAME@@@", e5_text.text()],
                            ["@@@APPVER@@@", e2_text.text()],
                            ["@@@EXEC_PATH@@@", i[0].text()],
                            ["@@@DEB_PACKAGE_NAME@@@", e1_text.text()],
                            ["@@@APPRUN_CMD@@@", [
                                wine[wineVersion.currentText()], 
                                f"/opt/apps/{e1_text.text()}/files/wine/bin/wine"
                            ][os.path.exists(f'{debPackagePath}/opt/apps/{e1_text.text()}/files/')]],
                            ["@@@EXEC_NAME@@@", os.path.basename(i[0].text().replace("\\", "/"))],
                            ["@@@ARCH@@@", debFirstArch.currentText()],
                            ["@@@APP_NAME@@@", i[3].text()],
                            ["@@@MAINTAINER@@@", e4_text.text()],
                            ["@@@DESCRIPTION@@@", e3_text.text()],
                            ["@@@DESKTOP_EXEC@@@", 
                                f'''"/opt/apps/{e1_text.text()}/files/{os.path.splitext(os.path.basename(i[0].text().replace(line, "/")))[0]}.sh" {command}'''],
                            ["@@@DESKTOP_NAME@@@", i[3].text()],
                            ["@@@DESKTOP_MIMETYPE@@@", i[5].text()],
                            ["@@@DESKTOP_CATEGORIES@@@", i[1].currentText()]
                        ]
                        # a 是图标（为什么当初要取这个变量名）
                        # 如果只有一个图标则为 str,两个及以上则为 list
                        if (type(a) == list):
                            replaceMap.append(["@@@ICON@@@", a[0]])
                        else:
                            replaceMap.append(["@@@ICON@@@", a])
                        line = "\\"
                        desktopFile = ReplaceText(readtxt(f"{programPath}/packager-config/app.desktop"), replaceMap)
                        write_txt(f"{debPackagePath}/opt/apps/{e1_text.text()}/files/{os.path.splitext(os.path.basename(i[0].text().replace(line, '/')))[0]}.sh", ReplaceText(debInformation[debArch.currentIndex()]["run.sh"], replaceMap))
                        if i[2].text().replace(" ", "") == "":
                            command = f"--uri {i[2].text()}"
                        else:
                            command = i[2].text()
                        write_txt("{}/opt/apps/{}/entries/applications/{}-{}.desktop".format(debPackagePath, e1_text.text(), e1_text.text(), os.path.splitext(os.path.basename(i[0].text().replace("\\", "/")))[0]), desktopFile)
                        write_txt("{}/usr/share/applications/{}-{}.desktop".format(debPackagePath, e1_text.text(), os.path.splitext(os.path.basename(i[0].text().replace("\\", "/")))[0]), desktopFile)
            if helperConfigPath != None and helperConfigPath != "":
                os.makedirs(f"{debPackagePath}/opt/deepinwine/tools/spark_run_v4_app_configs")
                if e6_text.text()[-3: ] == ".7z":
                    shutil.copy(helperConfigPath, f"{debPackagePath}/opt/deepinwine/tools/spark_run_v4_app_configs/{os.path.splitext(os.path.basename(e6_text.text()))[0]}.sh")
                else:
                    shutil.copy(helperConfigPath, f"{debPackagePath}/opt/deepinwine/tools/spark_run_v4_app_configs/{os.path.basename(e6_text.text())}.sh")
            # 如果选择内置 helper,则拷贝 helper 至 /opt/apps/@@@packager@@@/files 下
            if (debContainHelper.isChecked()):
                os.system(f"cp -rv '{programPath}/packager-config/deepinwine/' '{debPackagePath}/opt/apps/{e1_text.text()}/files'")
            ################
            # 修改文件权限
            ################
            self.label.emit("正在修改文件权限……")
            self.run_command("chmod -Rv 0755 {}/DEBIAN".format(debPackagePath))
            self.run_command("chmod -Rv 644 {}/opt/apps/{}/files/run.sh".format(debPackagePath, e1_text.text()))
            self.run_command("chmod -Rv 644 {}/opt/apps/{}/info".format(debPackagePath, e1_text.text()))
            self.run_command("chmod -Rv 755 {}/opt/apps/{}/files/*.sh".format(debPackagePath, e1_text.text()))
            self.run_command("chmod -Rv 755 {}/opt/apps/{}/entries/applications/*.desktop".format(debPackagePath, e1_text.text(), e1_text.text()))
            self.run_command("chmod -Rv 755 {}/usr/share/applications/*.desktop".format(debPackagePath, e1_text.text()))
            ################
            # 构建 deb 包
            ################
            if not self.build:
                self.label.emit("正在构建 deb 包……")
                if (os.path.exists(wine[wineVersion.currentText()])):
                    self.run_command("bash -c 'dpkg-deb -Z xz -z 9 -b \"{}\" \"{}\"'".format(debPackagePath, e12_text.text()))
                else:
                    self.run_command("bash -c 'dpkg-deb -Z xz -z 0 -b \"{}\" \"{}\"'".format(debPackagePath, e12_text.text()))
            ################
            # 删除临时文件
            ################
            if not self.build:
                self.label.emit("正在删除临时文件……")
                self.run_command(f"rm -rfv '{debPackagePath}'")
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
    if not option:
        chooseWineHelperValue.setChecked(False)
    wineVersion.setEnabled(option)
    useInstallWineArch.setEnabled(option)
    #rmBash.setEnabled(option)
    if debArch.currentIndex() == 0:
        ChangeWine()
        debFirstArch.setEnabled(True)
        debFirstArch.setCurrentIndex(0)
    else:
        debFirstArch.setCurrentIndex(2)
        debFirstArch.setDisabled(True)
        debDepends.setText("com.deepin-wine6-stable.deepin (>= 6.0deepin31), com.wine-helper.deepin (>= 0.0.8), com.deepin-box86.deepin (>= 0.2.6deepin3), deepin-elf-verify (>= 1.1.1-1)")

def InstallDeb():
    os.system(f"xdg-open '{e12_text.text()}'")

def OpenConfigFile():
    path = QtWidgets.QFileDialog.getOpenFileName(window, "打开列表", get_home(), "JSON 文件(*.json);;所有文件(*.*)")
    try:
        if path[0] == "" and path[0] == None:
            return
        try:
            with open(path[0], "r") as file:
                openInfo = json.loads(file.read())
        except:
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(window, "错误", traceback.format_exc())
            return
        for i in openInfo:
            option = openInfo[i][0]
            if option == "L":
                allInfoList[i][1].setText(openInfo[i][1])
            elif option == "Co":
                allInfoList[i][1].setCurrentIndex(openInfo[i][1])
            elif option == "Ch":
                allInfoList[i][1].setChecked(openInfo[i][1])
            elif option == "Str-SparkHelperConfigPath":
                allInfoList[i][1] = openInfo[i][1]
                if openInfo[i][1] != None:
                    helperConfigPathText.setText(os.path.basename(openInfo[i][1]))
            elif option == "List-Desktop":
                if len(openInfo[i][1]) > 1:
                    for k in openInfo[i][1][1:]:
                        AddTab(k)
            
                for k in range(len(openInfo[i][1][0])):
                    try:
                        iconUiList[0][k].setText(openInfo[i][1][0][k])
                    except:
                        try:
                            iconUiList[0][k].setCurrentIndex(openInfo[i][1][0][k])
                        except:
                            print(k)
                            traceback.print_exc()
    except:
        traceback.print_exc()
        QtWidgets.QMessageBox.critical(window, "错误", traceback.format_exc())

def SaveConfigList():
    saveInfo = {}
    try:
        for i in allInfoList:
            option = allInfoList[i][0]
            print(i)
            if option == "L":
                saveInfo[i] = ["L", allInfoList[i][1].text()]
            elif option == "Co":
                saveInfo[i] = ["Co", allInfoList[i][1].currentIndex()]
            elif option == "Ch":
                saveInfo[i] = ["Ch", allInfoList[i][1].isChecked()]
            elif option == "Str-SparkHelperConfigPath":
                saveInfo[i] = ["Str-SparkHelperConfigPath", allInfoList[i][1]]
            elif option == "List-Desktop":
                print("aaa")
                desktopTabList = []
            
                for d in allInfoList[i][1]:
                    desktopInfoList = []
                    for k in d:
                        try:
                            desktopInfoList.append(k.text())
                        except:
                            try:
                                desktopInfoList.append(k.currentIndex())
                            except:
                                traceback.print_exc()
                    desktopTabList.append(desktopInfoList)
                saveInfo[i] = ["List-Desktop", desktopTabList]
        path = QtWidgets.QFileDialog.getSaveFileName(window, "保存列表", get_home(), "JSON 文件(*.json);;所有文件(*.*)")
        print(path)
        if path[0] != "" and path[0] != None:
            try:
                with open(path[0], "w") as file:
                    file.write(json.dumps(saveInfo, ensure_ascii=False, indent=4))
            except:
                traceback.print_exc()
                QtWidgets.QMessageBox.critical(window, "错误", traceback.format_exc())
    except:
        traceback.print_exc()
        QtWidgets.QMessageBox.critical(window, "错误", traceback.format_exc())

def ClearHelperConfigPathText():
    global helperConfigPath
    helperConfigPath = None
    helperConfigPathText.setText("点击浏览按钮指定软件包适配脚本")

def BrowserHelperConfigPathText():
    global helperConfigPath
    path = QtWidgets.QFileDialog.getOpenFileName(window, "选择 sh 文件", get_home(), "shell 脚本(*.sh);;所有文件(*.*)")[0]
    if path == "" or path == None:
        return
    helperConfigPath = path
    helperConfigPathText.setText(os.path.basename(path))

def ChangeWine():
    useInstallWineArch.setEnabled(os.path.exists(wine[wineVersion.currentText()]))
    debDepends.setText([f"{wine[wineVersion.currentText()]} | {wine[wineVersion.currentText()]}-bcm | {wine[wineVersion.currentText()]}-dcm | com.{wine[wineVersion.currentText()]}.deepin, deepin-wine-helper | com.wine-helper.deepin, fonts-wqy-microhei, fonts-wqy-zenhei",
                        f"{wine[wineVersion.currentText()]} | {wine[wineVersion.currentText()]}-bcm | {wine[wineVersion.currentText()]}-dcm | com.{wine[wineVersion.currentText()]}.deepin, spark-dwine-helper | store.spark-app.spark-dwine-helper | deepin-wine-helper | com.wine-helper.deepin, fonts-wqy-microhei, fonts-wqy-zenhei"
                        ][int(chooseWineHelperValue.isChecked())])
    debRecommend.setText("")
    helperConfigPathText.setEnabled(chooseWineHelperValue.isChecked())
    helperConfigPathButton.setEnabled(chooseWineHelperValue.isChecked())
    if (debContainHelper.isChecked() and not os.path.exists(wine[wineVersion.currentText()])):
        debDepends.setText(f"{wine[wineVersion.currentText()]} | {wine[wineVersion.currentText()]}-bcm | {wine[wineVersion.currentText()]}-dcm | com.{wine[wineVersion.currentText()]}.deepin, fonts-wqy-microhei, fonts-wqy-zenhei")
    if os.path.exists(wine[wineVersion.currentText()]) and not debContainHelper.isChecked():
        debDepends.setText(["deepin-wine-helper | com.wine-helper.deepin",
                        "spark-dwine-helper | store.spark-app.spark-dwine-helper | deepin-wine-helper | com.wine-helper.deepin"
                        ][int(chooseWineHelperValue.isChecked())])
    if (debContainHelper.isChecked() and os.path.exists(wine[wineVersion.currentText()])):
        debDepends.setText("fonts-wqy-microhei, fonts-wqy-zenhei")

# 获取用户桌面目录
def get_desktop_path():
    if (not os.path.exists(get_home() + "/.config/user-dirs.dirs")):
        return f"{get_home()}/Desktop"
    for line in open(get_home() + "/.config/user-dirs.dirs"):  # 以行来读取配置文件
        desktop_index = line.find("XDG_DESKTOP_DIR=\"")  # 寻找是否有对应项，有返回 0，没有返回 -1
        if desktop_index != -1:  # 如果有对应项
            break  # 结束循环
    if desktop_index == -1:  # 如果是提前结束，值一定≠-1，如果是没有提前结束，值一定＝-1
        return f"{get_home()}/Desktop"
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
    architecture = [debFirstArch.currentText(), "arm64", "arm64"]
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
    path = f"{TMPDIR}/tmp/deb-unzip-{random.randint(0, 1000)}"
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
                # 在选择 arm 架构的情况下不勾选
                if name == "START_SHELL_PATH" and value == "/opt/deepinwine/tools/spark_run_v4.sh" and debArch.currentIndex() == 0:
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
                # 在选择 arm 架构的情况下不勾选
                if name == "START_SHELL_PATH" and value == "/opt/deepinwine/tools/spark_run_v4.sh" and debArch.currentIndex() == 0:
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
                # 在选择 arm 架构的情况下不勾选
                if name == "START_SHELL_PATH" and value == "/opt/deepinwine/tools/spark_run_v4.sh" and debArch.currentIndex() == 0:
                    # helper
                    chooseWineHelperValue.setChecked(True)
                if name == "APPRUN_CMD" and value in wineValue:
                    wineVersion.setCurrentText(wineValue[dependsItem])
            except:
                print(f"忽略行：{i}")

def ChangeTapTitle():
    if desktopIconTab.count() <= 1:
        desktopIconTab.setTabText(0, "run.sh")
        return
    title = os.path.basename(iconUiList[desktopIconTab.currentIndex()][0].text().replace("\\", "/"))
    desktopIconTab.setTabText(desktopIconTab.currentIndex(), title)

mapLink = []

def AddTab(defaultValue=[]):
    global mapLink
    button2 = QtWidgets.QPushButton(transla.transe("U", "浏览……"))
    e7_text = QtWidgets.QLineEdit()
    e8_text = QtWidgets.QLineEdit()
    e9_text = QtWidgets.QLineEdit()
    e10_text = QtWidgets.QLineEdit()
    e15_text = QtWidgets.QLineEdit()
    iconTab1 = QtWidgets.QWidget()
    option1_text = QtWidgets.QComboBox()
    option1_text.addItems(["Network", "Chat", "Audio", "Video", "Graphics", "Office", "Translation", "Development", "Utility"])
    option1_text.setCurrentText("Network")
    number = int(str(len(mapLink)))
    button2.clicked.connect(lambda: button2_cl(number))
    mapLink.append(e9_text)
    #desktopIconTabLayout = QtWidgets.QGridLayout()
    desktopIconTabLayout = QtWidgets.QGridLayout()
    desktopIconTabLayout.addWidget(QtWidgets.QLabel(transla.transe("U", "wine 容器里需要运行的可执行文件路径（※必填）：")), 6, 0, 1, 1)
    desktopIconTabLayout.addWidget(QtWidgets.QLabel(transla.transe("U", "要显示的 .desktop 文件的分类（※必填）：")), 7, 0, 1, 1)
    desktopIconTabLayout.addWidget(QtWidgets.QLabel(transla.transe("U", "wine 容器里需要运行的可执行文件的参数：")), 8, 0, 1, 1)
    desktopIconTabLayout.addWidget(QtWidgets.QLabel(transla.transe("U", "要显示的 .desktop 文件的名称（※必填）：")), 9, 0, 1, 1)
    desktopIconTabLayout.addWidget(QtWidgets.QLabel(transla.transe("U", "要显示的 .desktop 文件的图标：")), 10, 0, 1, 1)
    desktopIconTabLayout.addWidget(QtWidgets.QLabel(transla.transe("U", ".desktop 的 MimeType：")), 11, 0, 1, 1)
    iconTab1.setLayout(desktopIconTabLayout)
    desktopIconTab.addTab(iconTab1, f"图标{desktopIconTab.count() + 1}")
    desktopIconTabLayout.addWidget(e7_text, 6, 1, 1, 1)
    desktopIconTabLayout.addWidget(option1_text, 7, 1, 1, 1)
    desktopIconTabLayout.addWidget(e15_text, 8, 1, 1, 1)
    desktopIconTabLayout.addWidget(e8_text, 9, 1, 1, 1)
    desktopIconTabLayout.addWidget(e9_text, 10, 1, 1, 1)
    desktopIconTabLayout.addWidget(button2, 10, 2, 1, 1)
    desktopIconTabLayout.addWidget(e10_text, 11, 1, 1, 1)
    e8_text.setWhatsThis(transla.transe("U", """填写该软件的中文或英文名称。"""))
    e9_text.setWhatsThis(transla.transe("U", """图标只支持PNG格式和SVG格式，其他格式无法显示。"""))
    e15_text.setWhatsThis(transla.transe("U", "程序参数，如%u，一般不需要"))
    e7_text.setWhatsThis(transla.transe("U", """可执行文件的运行路径格式是“C:/XXX/XXX.exe”（不包含引号）"""))
    option1_text.setWhatsThis(transla.transe("U", """点击右侧的下拉箭头，选择该软件所属的软件分类即可，常见软件分类名称释义：
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
    e7_text.textChanged.connect(ChangeTapTitle)
    e7_text.setPlaceholderText("例如 c:/Program Files/Tencent/QQ/Bin/QQ.exe")
    e9_text.setPlaceholderText(transla.transe("U", "支持 png 和 svg 格式，不支持 ico 格式"))
    e10_text.setWhatsThis(transla.transe("U", "快捷方式的 MimeType 项，一般为空即可"))
    iconUiList.append([e7_text, option1_text, e15_text, e8_text, e9_text, e10_text])
    if defaultValue != []:
        for i in range(len(iconUiList[-1])):
            try:
                iconUiList[-1][i].setText(defaultValue[i])
            except:
                try:
                    iconUiList[-1][i].setCurrentIndex(defaultValue[i])
                except:
                    traceback.print_exc()
    print(iconUiList)

def DelTab():
    print(desktopIconTab.count())
    if desktopIconTab.count() <= 1:
        return
    del iconUiList[desktopIconTab.currentIndex()]
    desktopIconTab.removeTab(desktopIconTab.currentIndex())

def ChangeBottleName():
    global bottleNameLock
    global bottleNameChangeLock
    replaceForum = [e1_text, e2_text]
    for i in replaceForum:
        if " " in i.text():
            i.setText(i.text().replace(" ", ""))
    # 进行版本号限制
    if len(e2_text.text()) > 0:
        if ord(e2_text.text()[0]) < 48 or ord(e2_text.text()[0]) > 57:
            e2_text.setText(e2_text.text()[1:])
    # 调整逻辑，容器名默认与包名相同
    bottleNameChangeLock = True
    e5_text.setText(e1_text.text())


# 获取当前语言
def get_now_lang()->"获取当前语言":
    return os.getenv('LANG')

def ToRpm():
    if os.system("which alien"):
        QtWidgets.QMessageBox.critical(window, "错误", "无法找到 alien 命令，请先安装 alien")
        return
    if os.system("which fakeroot"):
        QtWidgets.QMessageBox.critical(window, "错误", "无法找到 fakeroot 命令，请先安装 fakeroot")
        return
    os.system(f"cd '{os.path.dirname(e12_text.text())}' ; fakeroot alien -r '{e12_text.text()}' -c")
    QtWidgets.QMessageBox.information(window, "提示", "打包完成！")

def ToTarZst():
    if os.system("which debtap"):
        QtWidgets.QMessageBox.critical(window, "错误", "无法找到 debtap 命令，请先安装 debtap")
        return
    OpenTerminal(f"sudo debtap -Q '{e12_text.text()}'")
    QtWidgets.QMessageBox.information(window, "提示", "打包完成！")

bottleNameLock = False
###############
# 程序信息
###############
programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
# 如果要添加其他 wine，请在字典添加其名称和执行路径
wine = {"deepin-wine": "deepin-wine", "deepin-wine5": "deepin-wine5", "wine": "wine", "wine64": "wine64", "deepin-wine5 stable": "deepin-wine5-stable", "deepin-wine6 stable": "deepin-wine6-stable", "spark-wine7-devel": "spark-wine7-devel", "ukylin-wine": "ukylin-wine", "okylin-wine": "okylin-wine", "spark-wine8": "spark-wine8", "spark-wine8-wow": "spark-wine8-wow", "deepin-wine6-vannila": "deepin-wine6-vannila", "deepin-wine8-stable": "deepin-wine8-stable", "spark-wine9": "spark-wine9", "spark-wine9-wow": "spark-wine9-wow", "spark-wine": "spark-wine"}
wineValue = {"deepin-wine": "deepin-wine", "deepin-wine5": "deepin-wine5", "wine": "wine", "wine64": "wine64", "deepin-wine5-stable": "deepin-wine5 stable", "deepin-wine6-stable": "deepin-wine6 stable", "spark-wine7-devel": "spark-wine7-devel", "ukylin-wine": "ukylin-wine", "okylin-wine": "okylin-wine", "spark-wine8": "spark-wine8", "spark-wine8-wow": "spark-wine8-wow", "deepin-wine6-vannila": "deepin-wine6-vannila", "deepin-wine8-stable": "deepin-wine8-stable", "spark-wine": "spark-wine"}
# 读取 wine 本地列表
try:
    for i in os.listdir("/opt"):
        if os.path.exists(f"/opt/{i}/bin/wine"):
            wine[f"/opt/{i}/bin/wine"] = f"/opt/{i}/bin/wine"
except:
    pass
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
iconUiList = []
helperConfigPath = None
iconPath = "{}/deepin-wine-runner.svg".format(programPath)
information = json.loads(readtxt(f"{programPath}/information.json"))
version = information["Version"]
# 语言载入
if not get_now_lang() == "zh_CN.UTF-8":
    #trans = QtCore.QTranslator()
    #trans.load(f"{programPath}/LANG/deepin-wine-runner-en_US.qm")
    #app.installTranslator(trans)
    transla = Trans("en_US", f"{programPath}/trans/deepin-wine-packager.json")
else:
    transla = Trans("zh_CN")
tips = transla.transe("U", """提示：
1、deb 打包软件包名要求：
软件包名只能含有小写字母(a-z)、数字(0-9)、加号(+)和减号(-)、以及点号(.)，软件包名最短长度两个字符；它必须以字母开头
2、如果要填写路径，有“浏览……”按钮的是要填本计算机对应文件的路径，否则就是填写安装到其他计算机使用的路径
3、输入 wine 的容器路径时最后面请不要输入“/”
4、输入可执行文件的运行路径时是以“C:/XXX/XXX.exe”的格式进行输入，默认是以 C： 为开头，不用“\”做命令的分隔，而是用“/”
5、.desktop 的图标只支持 PNG 格式和 SVG 格式，其他格式无法显示图标
6、路径建议不要带空格，容易出问题""")

###############
# 窗口创建
###############

if (__name__ == "__main__"):
    app = QtWidgets.QApplication(sys.argv)
else:
    app = globalenv.get_value("app")
window = QtWidgets.QMainWindow()
widget = QtWidgets.QWidget()

defaultFont = window.font()
#hScroll = QtWidgets.QScrollArea()
#hScroll.setWidget(widget)
#hScroll.verticalScrollBar().setValue(hScroll.verticalScrollBar().maximum())
#hScroll.horizontalScrollBar().setValue(hScroll.horizontalScrollBar().maximum())
widgetLayout = QtWidgets.QGridLayout()
# 设置变量以修改和获取值项
wineVersion = QtWidgets.QComboBox()
wineVersion.addItems(wine.keys())
wineVersion.setCurrentText("deepin-wine8-stable")
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
button1 = QtWidgets.QPushButton(transla.transe("U", "浏览……"))
button2 = QtWidgets.QPushButton(transla.transe("U", "浏览……"))
button4 = QtWidgets.QPushButton(transla.transe("U", "浏览……"))
debControlFrame = QtWidgets.QHBoxLayout()
button5 = QtWidgets.QPushButton(transla.transe("U", "打包……"))
installDeb = QtWidgets.QPushButton(transla.transe("U", "安装打包完成的 deb……"))
buildDebDir = QtWidgets.QPushButton(transla.transe("U", "根据填写内容打包模板"))
build7z = QtWidgets.QPushButton(transla.transe("U", "打包容器 7z 包"))
debControlFrame.addWidget(button5)
debControlFrame.addWidget(installDeb)
rmBash = QtWidgets.QCheckBox(transla.transe("U", "设置卸载该 deb 后自动删除该容器"))
cleanBottonByUOS = QtWidgets.QCheckBox(transla.transe("U", "使用统信 Wine 生态适配活动容器清理脚本"))
disabledMono = QtWidgets.QCheckBox(transla.transe("U", "禁用 Mono 和 Gecko 安装器"))
enableCopyIconToDesktop = QtWidgets.QCheckBox(transla.transe("U", "安装时自动拷贝快捷方式至桌面"))
debContainHelper = QtWidgets.QCheckBox(transla.transe("U", "deb 包内置 helper"))
debArch = QtWidgets.QComboBox()
debArch.addItems(["默认选项", "arm64(box86+exagear)"])
#debArch.addItems(["i386", "arm64(box86+exagear)", "all(crossover)"])
textbox1 = QtWidgets.QTextBrowser()
option1_text.addItems(["Network", "Chat", "Audio", "Video", "Graphics", "Office", "Translation", "Development", "Utility", "Game", "AudioVideo", "System"])
option1_text.setCurrentText("Network")
wineFrame = QtWidgets.QHBoxLayout()
chooseWineHelperValue = QtWidgets.QCheckBox(transla.transe("U", "使用星火wine helper\n（如不勾选默认为deepin-wine-helper）"))
chooseWineHelperValue.setVisible(False)
helperConfigPathLayout = QtWidgets.QHBoxLayout()
helperConfigPathButton = QtWidgets.QPushButton("浏览")
helperConfigPathText = QtWidgets.QLabel("点击浏览按钮指定软件包适配脚本")
helperConfigPathLayout.addWidget(helperConfigPathButton)
helperConfigPathLayout.addWidget(helperConfigPathText)
helperConfigPathButton.clicked.connect(BrowserHelperConfigPathText)
helperConfigPathButton.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
helperConfigPathMenu = QtWidgets.QMenu(window)
delHelperConfigPath = QtWidgets.QAction("取消选择")
delHelperConfigPath.triggered.connect(ClearHelperConfigPathText)
helperConfigPathMenu.addAction(delHelperConfigPath)
helperConfigPathButton.customContextMenuRequested.connect(lambda: helperConfigPathMenu.exec_(QtGui.QCursor.pos()))
button1.clicked.connect(button1_cl)
button2.clicked.connect(lambda: button2_cl(0))
mapLink.append(e9_text)
button4.clicked.connect(button4_cl)
button5.clicked.connect(make_deb)
buildDebDir.clicked.connect(lambda: make_deb(True))
build7z.clicked.connect(Build7zButton_Clicked)
installDeb.clicked.connect(InstallDeb)
wineFrame.addWidget(wineVersion)
e1_text.textChanged.connect(ChangeBottleName)
e2_text.textChanged.connect(ChangeBottleName)
e6_text.textChanged.connect(ChangeBottleName)
e7_text.textChanged.connect(ChangeTapTitle)
widgetLayout.addWidget(QtWidgets.QLabel(transla.transe("U", "要打包的 deb 包的包名（※必填）：")), 0, 0, 1, 1)
widgetLayout.addWidget(QtWidgets.QLabel(transla.transe("U", "deb 包版本号（※必填）：")), 1, 0, 1, 1)
widgetLayout.addWidget(QtWidgets.QLabel(transla.transe("U", "deb 包说明（※必填）：")), 2, 0, 1, 1)
widgetLayout.addWidget(QtWidgets.QLabel(transla.transe("U", "deb 包维护者（※必填）：")), 3, 0, 1, 1)
widgetLayout.addWidget(QtWidgets.QLabel(transla.transe("U", "Wine 容器名称（※必填，推荐默认）：")), 4, 0, 1, 1)
widgetLayout.addWidget(QtWidgets.QLabel(transla.transe("U", "要打包 wine 容器的路径（※必填）：")), 5, 0, 1, 1)
desktopIconTab = QtWidgets.QTabWidget()
controlWidget = QtWidgets.QWidget()
controlWidgetLayout = QtWidgets.QHBoxLayout()
desktopIconTabAdd = QtWidgets.QPushButton("+")
desktopIconTabDel = QtWidgets.QPushButton("-")
desktopIconTabAdd.setWhatsThis("添加新图标")
desktopIconTabDel.setWhatsThis("移除选中图标")
controlWidgetLayout.addWidget(desktopIconTabAdd)
controlWidgetLayout.addWidget(desktopIconTabDel)
controlWidget.setLayout(controlWidgetLayout)
desktopIconTabAdd.clicked.connect(AddTab)
desktopIconTabDel.clicked.connect(DelTab)
iconTab1 = QtWidgets.QWidget()
desktopIconTabLayout = QtWidgets.QGridLayout()
desktopIconTabLayout.addWidget(QtWidgets.QLabel(transla.transe("U", "wine 容器里需要运行的可执行文件路径（※必填）：")), 6, 0, 1, 1)
desktopIconTabLayout.addWidget(QtWidgets.QLabel(transla.transe("U", "要显示的 .desktop 文件的分类（※必填）：")), 7, 0, 1, 1)
desktopIconTabLayout.addWidget(QtWidgets.QLabel(transla.transe("U", "wine 容器里需要运行的可执行文件的参数：")), 8, 0, 1, 1)
desktopIconTabLayout.addWidget(QtWidgets.QLabel(transla.transe("U", "要显示的 .desktop 文件的名称（※必填）：")), 9, 0, 1, 1)
desktopIconTabLayout.addWidget(QtWidgets.QLabel(transla.transe("U", "要显示的 .desktop 文件的图标：")), 10, 0, 1, 1)
desktopIconTabLayout.addWidget(QtWidgets.QLabel(transla.transe("U", ".desktop 的 MimeType：")), 11, 0, 1, 1)
iconTab1.setLayout(desktopIconTabLayout)
#desktopIconTab.setTabPosition(QtWidgets.QTabWidget.East)
desktopIconTab.addTab(iconTab1, "默认图标")
desktopIconTab.setCornerWidget(controlWidget)
widgetLayout.addWidget(desktopIconTab, 8, 0, 6, 3)
widgetLayout.addWidget(QtWidgets.QLabel(transla.transe("U", "选择打包的 wine 版本（※必选）：")), 6, 0, 1, 1)
widgetLayout.addWidget(QtWidgets.QLabel(transla.transe("U", "打包 deb 的保存路径（※必填）：")), 7, 0, 1, 1)
widgetLayout.addWidget(e1_text, 0, 1, 1, 1)
widgetLayout.addWidget(e2_text, 1, 1, 1, 1)
widgetLayout.addWidget(e3_text, 2, 1, 1, 1)
widgetLayout.addWidget(e4_text, 3, 1, 1, 1)
widgetLayout.addWidget(e5_text, 4, 1, 1, 1)
widgetLayout.addWidget(e6_text, 5, 1, 1, 1)
widgetLayout.addWidget(button1, 5, 2, 1, 1)
desktopIconTabLayout.addWidget(e7_text, 6, 1, 1, 1)
desktopIconTabLayout.addWidget(option1_text, 7, 1, 1, 1)
desktopIconTabLayout.addWidget(e15_text, 8, 1, 1, 1)
desktopIconTabLayout.addWidget(e8_text, 9, 1, 1, 1)
desktopIconTabLayout.addWidget(e9_text, 10, 1, 1, 1)
desktopIconTabLayout.addWidget(button2, 10, 2, 1, 1)
desktopIconTabLayout.addWidget(e10_text, 11, 1, 1, 1)
iconUiList.append([e7_text, option1_text, e15_text, e8_text, e9_text, e10_text])
e3_text.textChanged.connect(lambda: e3_text.setText(e3_text.text().replace("\n", "")))
print(iconUiList)
widgetLayout.addLayout(wineFrame, 6, 1, 1, 1)
widgetLayout.addWidget(e12_text, 7, 1, 1, 1)
widgetLayout.addWidget(button4, 7, 2, 1, 1)
widgetLayout.addLayout(debControlFrame, 16, 1, 1, 1)
widgetLayout.addWidget(label13_text, 17, 0, 1, 3)
widgetLayout.addWidget(textbox1, 18, 0, 1, 3)
# 高级功能
moreSetting = QtWidgets.QGroupBox(transla.transe("U", "高级设置"))
debDepends = QtWidgets.QLineEdit()
debRecommend = QtWidgets.QLineEdit()
debFirstArch = QtWidgets.QComboBox()
debFirstArch.addItems(["all", "i386", "amd64", "armhf", "arm64", "loongarch64", "loong64", "riscv64"])
debFirstArch.setCurrentIndex(0)
debFirstArch.currentIndexChanged.connect(AutoPathSet)
debDepends.setPlaceholderText(transla.transe("U", "deb 包的依赖(如无特殊需求默认即可)"))
debDepends.setText("deepin-wine6-stable, deepin-wine-helper (>= 5.1.30-1), fonts-wqy-microhei, fonts-wqy-zenhei")
debRecommend.setPlaceholderText(transla.transe("U", "deb 包的推荐依赖(非强制，一般默认即可)"))
moreSettingLayout = QtWidgets.QVBoxLayout()
localWineVersion = QtWidgets.QComboBox()
useInstallWineArch = QtWidgets.QComboBox()
useInstallWineArch.addItems(["wine", "wine64"])
moreSettingLayout.addWidget(QtWidgets.QLabel(transla.transe("U", "Wine 位数(只限本地需要打包集成的Wine)：\n提示：32位的Wine不能使用64位容器")))
#moreSettingLayout.addWidget(localWineVersion)
moreSettingLayout.addWidget(useInstallWineArch)
moreSettingLayout.addWidget(QtWidgets.QLabel(transla.transe("U", "deb 包选项：")))
moreSettingLayout.addWidget(rmBash)
moreSettingLayout.addWidget(cleanBottonByUOS)
moreSettingLayout.addWidget(chooseWineHelperValue)
moreSettingLayout.addLayout(helperConfigPathLayout)
moreSettingLayout.addWidget(disabledMono)
moreSettingLayout.addWidget(enableCopyIconToDesktop)
moreSettingLayout.addWidget(debContainHelper)
moreSettingLayout.addWidget(QtWidgets.QLabel(transla.transe("U", "deb 的依赖(强制，如无特殊需求默认即可)：")))
moreSettingLayout.addWidget(debDepends)
moreSettingLayout.addWidget(QtWidgets.QLabel(transla.transe("U", "deb 的推荐依赖(非强制，一般默认即可)：")))
moreSettingLayout.addWidget(debRecommend)
moreSettingLayout.addWidget(QtWidgets.QLabel(transla.transe("U", "打包 deb 架构：")))
moreSettingLayout.addWidget(debFirstArch)
moreSettingLayout.addWidget(QtWidgets.QLabel(transla.transe("U", "打包选项：")))
moreSettingLayout.addWidget(debArch)
moreSetting.setLayout(moreSettingLayout)
widgetLayout.addWidget(moreSetting, 0, 3, 16, 2)
widgetLayout.addWidget(build7z, 16, 3)
widgetLayout.addWidget(buildDebDir, 16, 4)
useInstallWineArch.setDisabled(True)
debContainHelper.clicked.connect(ChangeWine)
wineVersion.currentTextChanged.connect(ChangeWine)
chooseWineHelperValue.stateChanged.connect(ChangeWine)
e1_text.textChanged.connect(AutoPathSet)
e2_text.textChanged.connect(AutoPathSet)
debArch.currentIndexChanged.connect(AutoPathSet)
debArch.currentIndexChanged.connect(ChangeArchCombobox)
e12_text.textChanged.connect(UserPathSet)
e1_text.setPlaceholderText("例如 spark-deepin-wine-runner，不建议有大写字符")
e2_text.setPlaceholderText(f"例如 {version}")
e7_text.setPlaceholderText("例如 c:/Program Files/Tencent/QQ/Bin/QQ.exe")
e9_text.setPlaceholderText(transla.transe("U", "支持 png 和 svg 格式，不支持 ico 格式"))
# 菜单栏
menu = window.menuBar()
programmenu = menu.addMenu(transla.transe("U", "程序（&P）"))
debMenu = menu.addMenu(transla.transe("U", "deb 包"))
uploadSparkStore = menu.addMenu(transla.transe("U", "投稿到星火应用商店"))
help = menu.addMenu(transla.transe("U", "帮助"))
openFile = QtWidgets.QAction(transla.transe("U", "打开配置文件"))
saveFile = QtWidgets.QAction(transla.transe("U", "保存配置文件"))
setMiniFont = QtWidgets.QAction(transla.transe("U", "使用小字体"))
setDefaultFont = QtWidgets.QAction(transla.transe("U", "使用默认大小字体"))
hideShowText = QtWidgets.QAction(transla.transe("U", "隐藏输出框"))
hideShowText.setCheckable(True)
exit = QtWidgets.QAction(transla.transe("U", "退出程序"))
debE = QtWidgets.QAction(transla.transe("U", "只读取 Control 信息"))
debX = QtWidgets.QAction(transla.transe("U", "读取所有（需解包，时间较久）"))
uploadSparkStoreWebsize = QtWidgets.QAction(transla.transe("U", "从网页端投稿"))
if os.path.exists("/opt/spark-store-submitter/bin/spark-store-submitter"):
    uploadSparkStoreProgram = QtWidgets.QAction(transla.transe("U", "使用投稿器投稿（推荐）"))
else:
    uploadSparkStoreProgram = QtWidgets.QAction(transla.transe("U", "使用投稿器投稿（推荐，请先安装投稿器）"))
    uploadSparkStoreProgram.setDisabled(True)
tip = QtWidgets.QAction(transla.transe("U", "小提示"))
getPdfHelp = QtWidgets.QAction(transla.transe("U", "Wine运行器和Wine打包器傻瓜式使用教程（小白专用）\nBy @雁舞白沙"))
videoHelp = menu.addMenu(transla.transe("U", "视频教程(&V)"))
videoHelpAction = QtWidgets.QAction(QtWidgets.QApplication.style().standardIcon(20), transla.transe("U", "视频教程"))
videoHelpAction.triggered.connect(lambda: webbrowser.open_new_tab("https://space.bilibili.com/695814694/channel/collectiondetail?sid=1610353"))
videoHelp.addAction(videoHelpAction)
openFile.triggered.connect(OpenConfigFile)
saveFile.triggered.connect(SaveConfigList)
hideShowText.triggered.connect(lambda: textbox1.setHidden(hideShowText.isChecked()))
exit.triggered.connect(window.close)
tip.triggered.connect(helps)
wineDepend = menu.addMenu("Wine 应用依赖（非 Deepin/UOS 发行版）")
uosPackingTools = QtWidgets.QAction("安装维护打包工具箱（需要先安装星火应用商店）")
sparkStoreWebsite = QtWidgets.QAction("打开星火应用商店官网")
if os.system("which spark-store"):
    uosPackingTools.setDisabled(True)
uosPackingTools.triggered.connect(lambda: threading.Thread(target=os.system, args=["spark-store spk://store/tools/uos-packaging-tools"]).start())
sparkStoreWebsite.triggered.connect(lambda: webbrowser.open_new_tab("https://spark-app.store/"))
wineDepend.addAction(sparkStoreWebsite)
wineDepend.addAction(uosPackingTools)
turnDebToOther = menu.addMenu("转换安装包格式")
toRpm = QtWidgets.QAction("转 rpm")
toTarZst = QtWidgets.QAction("转 tar.zst")
toRpm.triggered.connect(ToRpm)
toTarZst.triggered.connect(ToTarZst)
turnDebToOther.addAction(toRpm)
turnDebToOther.addAction(toTarZst)
programmenu.addAction(openFile)
programmenu.addAction(saveFile)
#programmenu.addSeparator()
#programmenu.addAction(setMiniFont)
#programmenu.addAction(setDefaultFont)
programmenu.addAction(hideShowText)
programmenu.addSeparator()
programmenu.addAction(exit)
debMenu.addAction(debE)
debMenu.addAction(debX)
uploadSparkStore.addAction(uploadSparkStoreProgram)
uploadSparkStore.addAction(uploadSparkStoreWebsize)
debE.triggered.connect(lambda: ReadDeb(False))
debX.triggered.connect(lambda: ReadDeb(True))
uploadSparkStoreWebsize.triggered.connect(lambda: webbrowser.open_new_tab("https://upload.deepinos.org.cn"))
uploadSparkStoreProgram.triggered.connect(lambda: threading.Thread(target=os.system, args=[f"/opt/spark-store-submitter/bin/spark-store-submitter '{e12_text.text()}'"]).start())
getPdfHelp.triggered.connect(lambda: webbrowser.open_new_tab("https://bbs.deepin.org/post/246837"))
help.addAction(tip)
help.addAction(getPdfHelp)
# 控件配置
try:
    e6_text.setText(sys.argv[1].replace("~", get_home()))
    e5_text.setText(pathlib.PurePath(sys.argv[1]).name)
    wineVersion.setCurrentText(sys.argv[2])
except:
    pass
rmBash.setChecked(True)
disabledMono.setChecked(True)
cleanBottonByUOS.setChecked(True)
chooseWineHelperValue.setChecked(True)
e12_text.setText(f"{get_desktop_path()}/demo_1.0.0_all.deb")
widget.setLayout(widgetLayout)
window.setWindowTitle(f"wine 应用打包器 {version}")
window.setWindowIcon(QtGui.QIcon(iconPath))
window.resize(int(window.frameSize().width() * 2.1), int(window.frameSize().height()))
e1_text.setWhatsThis("""安装包的包名，推荐类似 com.xxx.spark 这种倒置域名的格式，当然类似 spark-xxx 这种也可以，但是包名只能含有<b>小写字母（a-z）、数字（0-9）、加号（+）和减号（-）、以及点号(.)</b>，软件包名最短长度为两个字符，且包名必须以字母开头。""")
# 创建控件
e2_text.setWhatsThis(transla.transe("U", """安装包的版本号，一般推荐格式为 <b><u>程序版本号</u>spark<u>修订号</u></b>，例如 23.01spark0，23.01 就是程序版本号，0 为修订号，代表第一版版本"""))
e3_text.setWhatsThis(transla.transe("U", """安装包的说明，随意但最好能程序的介绍之类方便用户快速了解安装包内容的文字，推荐只用英文"""))
e4_text.setWhatsThis(transla.transe("U", """安装包的维护者，推荐格式为：<b><u>打包者</u>&lt;<u>邮箱</u>&gt;</b> ，例如 gfdgd xi&lt;3025613752@qq.com&gt;，多个打包者用半角符号“,”分隔"""))
e5_text.setWhatsThis(f"<p>解压容器到其它机器的容器名称，一般自动带出</p><p><img src='{programPath}/Icon/Screen/202211121646232464_image.png'></p>")
e6_text.setWhatsThis(transla.transe("U", f"要打包的容器所在路径，也可以选择已经好打包的 7z 文件，一般自动带出"))
e7_text.setWhatsThis("""程序在 wine 容器的路径，格式一般为 c:/xxx/xxx.exe""")
debArch.setWhatsThis(transla.transe("U", "选择生成 deb 包所对应的架构"))
wineVersion.setWhatsThis("deb 包使用的 Wine")
option1_text.setWhatsThis("程序在启动器的快捷方式分类")
rmBash.setWhatsThis(transla.transe("U", "清理容器无用内容，一般建议勾选，最新版本默认勾选，如果有特殊需求（如容器内有 mono、gecko 等）建议取消勾选"))
debDepends.setWhatsThis(transla.transe("U", "生成 deb 包所需的依赖，一般情况下默认即可"))
debRecommend.setWhatsThis(transla.transe("U", "生成 deb 包的推荐依赖，一般情况下为空即可"))
cleanBottonByUOS.setWhatsThis(transla.transe("U", "清理容器无用内容，一般建议勾选，最新版本默认勾选，如果有特殊需求（如容器内有 mono、gecko 等）建议取消勾选"))
chooseWineHelperValue.setWhatsThis(transla.transe("U", "使用星火 dwine helper 替换 Deepin Wine Helper，投稿星火应用商店的话建议勾选，最新版本默认勾选（如果打包 arm 包将不会提供选择）"))
option1_text.setWhatsThis("""点击右侧的下拉箭头，选择该软件所属的软件分类即可，常见软件分类名称释义：
Network=网络应用；
Chat=即时通讯或社交沟通；
Video=视频播放；
Audio=音乐欣赏；
AudioVideo=视频播放；
Graphics=图形图像；
Game=游戏娱乐；
Office=办公学习；
Translation=阅读翻译；
Development=软件开发；
Reading=阅读翻译；
System=系统管理；
Utility=工具软件或其他应用。
不明白英文的可以百度查询一下软件分类名称的意思。
注意：此时选择的软件分类名称决定了该软件打包后再安装时会安装在启动器中的哪个软件分类目录中。""")
e8_text.setWhatsThis(transla.transe("U", """在启动器快捷方式的名称"""))
e9_text.setWhatsThis(transla.transe("U", """在启动器快捷方式的图标（不支持 ico 格式，推荐使用 svg、png 格式）"""))
e10_text.setWhatsThis(transla.transe("U", "快捷方式的 MimeType 项，一般为空即可"))
option1_text.setWhatsThis(transla.transe("U", "打包的 Wine 版本，根据实际情况选择（如果打包 arm 包将不会提供选择）"))
e12_text.setWhatsThis(transla.transe("U", "打包出的 deb 生成的位置，一般自动生成"))
e15_text.setWhatsThis(transla.transe("U", "程序参数，如%u，一般不需要"))
build7z.setWhatsThis(transla.transe("U", "只打包容器生成 7z 包，不做其它操作"))
buildDebDir.setWhatsThis(transla.transe("U", "构建 deb 包目录，但不打包成 deb"))
textbox1.setWhatsThis(transla.transe("U", "查看打包过程中命令返回内容"))
button5.setWhatsThis(transla.transe("U", "点击该按钮打包生成 deb"))
installDeb.setWhatsThis(transla.transe("U", "调用默认的 deb 安装工具安装生成的 deb"))

allInfoList = {
    "Package": ["L", e1_text],
    "Version": ["L", e2_text],
    "Description": ["L", e3_text],
    "Maintainer": ["L", e4_text],
    "BottleName": ["L", e5_text],
    "BottlePath": ["L", e6_text],
    "WineVersion": ["Co", wineVersion],
    "DebSavePath": ["L", e12_text],
    "Desktop": ["List-Desktop", iconUiList],
    "UseInstallWineArch": ["Co", useInstallWineArch],
    "RemoveBash": ["Ch", rmBash],
    "CleanBottleByUOS": ["Ch", cleanBottonByUOS],
    "ChooseWineHelperValue": ["Ch", chooseWineHelperValue],
    "DisabledMono": ["Ch", disabledMono],
    "EnableCopyIconToDesktop": ["Ch", enableCopyIconToDesktop],
    "ContainHelper": ["Ch", debContainHelper],
    "DebDepends": ["L", debDepends],
    "DebRecommend": ["L", debRecommend],
    "DebFirstArch": ["Co", debFirstArch],
    "DebArch": ["Co", debArch],
    "SparkHelperConfigPath": ["Str-SparkHelperConfigPath", helperConfigPath]
}
# 设置字体
SetFont(app)
#window.setWindowFlag(QtGui.Qt)

window.setCentralWidget(widget)
# 判断是否为小屏幕，是则设置滚动条并全屏
if (window.frameGeometry().width() > app.primaryScreen().availableGeometry().size().width() * 0.8 or 
   window.frameGeometry().height() > app.primaryScreen().availableGeometry().size().height() * 0.9):
    # 设置滚动条
    areaScroll = QtWidgets.QScrollArea(window)
    areaScroll.setWidgetResizable(True)
    areaScroll.setWidget(widget)
    areaScroll.setFrameShape(QtWidgets.QFrame.NoFrame)
    window.setCentralWidget(areaScroll)
    window.showMaximized()  # 设置全屏

if (__name__ == "__main__"):
    window.show()
    sys.exit(app.exec_())
    # TODO：解包只读control和解包全部读取
