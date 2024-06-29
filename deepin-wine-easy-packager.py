#!/usr/bin/env python3
import os
import sys
import json
import time
import threading
import updatekiller
import random
try:
    import xpinyin
except:
    os.system("python3 -m pip install --upgrade xpinyin --trusted-host https://repo.huaweicloud.com -i https://repo.huaweicloud.com/repository/pypi/simple")
    os.system("python3 -m pip install --upgrade xpinyin --trusted-host https://repo.huaweicloud.com -i https://repo.huaweicloud.com/repository/pypi/simple --break-system-packages")
    import xpinyin
import traceback
import subprocess
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets
from DefaultSetting import *

def ShowText(text: str):
    if text.replace(" ", "").replace("\n", "") == "":
        return
    logText.append(text.replace("\n", ""))
    
def ErrorMessage(text: str):
    QtWidgets.QMessageBox.critical(window, "错误", text)

def InformationMessage(text: str):
    QtWidgets.QMessageBox.information(window, "提示", text)

questionChoose = False
questionStatus = False
def QuestionMessage(text: str):
    global questionChoose
    global questionStatus
    # 清零
    questionChoose = False
    questionStatus = False
    if QtWidgets.QMessageBox.question(window, "提示", text) == QtWidgets.QMessageBox.Yes:
        questionChoose = True
        print(questionChoose)
        questionStatus = True
        return
    questionChoose = False
    questionStatus = True
    

def DisbledAndEnabledAll(choose: bool):
    exePath.setDisabled(choose)
    browserExeButton.setDisabled(choose)
    buildButton.setDisabled(choose)

# 获取用户主目录
def get_home():
    return os.path.expanduser('~')

def get_desktop_path():
    try:
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
    except:
        traceback.print_exc()
        return get_home()

def CleanPressCompleteDownloadState(option):
    global pressCompleteDownload
    pressCompleteDownload = False
    installCmpleteButton.setEnabled(True)

# 读取 lnk 文件
def GetLnkDesktop(path):
    lnkList = []
    for i in os.listdir(path):
        filePath = f"{path}/{i}"
        if os.path.islink(filePath):
            # 忽略 link 链接
            continue
        if os.path.isdir(filePath):
            lists = GetLnkDesktop(filePath)
            for k in lists:
                lnkList.append(k)
            continue
        if os.path.isfile(filePath) and os.path.splitext(filePath)[1] == ".lnk":
            with open(filePath, "rb") as file:
                while True:
                    things = file.readline().lower()
                    if things == b"":
                        break
                    print(things[1: -2].split("\x00".encode("gbk")))
                    for k in things[1: -2].split("\x00".encode("gbk")):
                        if "c:".encode("gbk") in k:
                            print(k.decode("gbk"))
                            lnkList.append([filePath, k.decode("gbk")])
    return lnkList

def ReplaceText(string: str, lists: list):
    for i in lists:
        string = string.replace(i[0], i[1])
    return string

control = '''Package: @@@Package@@@
Version: @@@Version@@@
Architecture: all
Maintainer: @@@Maintainer@@@
Depends: @@@Depends@@@
Section: non-free/otherosfs
Priority: optional
Multi-Arch: foreign
Installed-Size: @@@Installed-Size@@@
Description: @@@Description@@@
'''

info = f'''{{
    "appid": "@@@Package@@@",
    "name": "@@@Name@@@",
    "version": "@@@Version@@@",
    "arch": ["all"],
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
postinst = f"""#!/bin/bash
PACKAGE_NAME="@@@Package@@@"
for username in $(ls /home)  
do
    echo /home/$username
    if [ -d /home/$username/桌面 ]; then
        cp /opt/apps/$PACKAGE_NAME/entries/applications/* /home/$username/桌面
    fi
    if [ -d /home/$username/Desktop ]; then
        cp /opt/apps/$PACKAGE_NAME/entries/applications/* /home/$username/Desktop
    fi
done
"""
postrm = f"""#!/bin/bash
if [ "$1" = "remove" ] || [ "$1" = "purge" ];then

echo "清理卸载残留"
CONTAINER_NAME="@@@Package@@@"

if [ -z $CONTAINER_NAME ];then
echo "W: 没有指定容器，跳过清理容器。请手动前往 ~/.deepinwine/ 下删除"
exit
fi

/opt/deepinwine/tools/kill.sh $CONTAINER_NAME
###这里注意，如果没写CONTAINER_NAME,会把QQ杀了

for username in $(ls /home)  
    do
      echo /home/$username
        if [ -d /home/$username/.deepinwine/$CONTAINER_NAME ]  
        then
        rm -rf /home/$username/.deepinwine/$CONTAINER_NAME
        fi
    done
else
echo "非卸载，跳过清理"
fi"""

runsh = f'''#!/bin/sh

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
    elif grep -Eqi "UOS" /etc/issue || grep -Eq "UOS" /etc/*-release; then
        DISTRO='UniontechOS'
    else
	 DISTRO='OtherOS'
	fi
}}


####获得发行版名称

#########################预设值段

version_gt() {{ test "$(echo "$@" | tr " " "\n" | sort -V | head -n 1)" != "$1"; }}
####用于比较版本？未实装
BOTTLENAME="@@@Package@@@"
APPVER="@@@Version@@@"
EXEC_PATH="@@@EXEC_PATH@@@"
##### 软件在wine中的启动路径
if [ -e "/opt/deepinwine/tools/spark_run_v4.sh" ] ;then
    START_SHELL_PATH="/opt/deepinwine/tools/spark_run_v4.sh"
else
    START_SHELL_PATH="/opt/deepinwine/tools/run_v4.sh"
fi
ENABLE_DOT_NET=""
####若使用spark-wine时需要用到.net，则请把ENABLE_DOT_NET设为true，同时在依赖中写spark-wine7-mono
#export BOX86_EMU_CMD="/opt/spark-box86/box86"
####仅在Arm且不可使用exagear时可用，作用是强制使用box86而不是deepin-box86.如果你想要这样做，请取消注释
export MIME_TYPE=""

export DEB_PACKAGE_NAME="@@@Package@@@"
####这里写包名才能在启动的时候正确找到files.7z,似乎也和杀残留进程有关
export APPRUN_CMD="@@Wine@@"
#####wine启动指令，建议
#EXPORT_ENVS="wine的动态链接库路径"
##例如我的wine应用是使用的dwine6的32位容器，那么我要填LD_LIBRARY_PATH=$LD_LIBRARY;/opt/deepin-wine6-stable/lib
## 如果用不到就不填，不要删除前面的注释用的#

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
#此功能实现参见开头函数段
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
if [ "$APPRUN_CMD" = "spark-wine7-devel" ] || [ "$APPRUN_CMD" = "spark-wine" ]|| [ "$APPRUN_CMD" = "spark-wine8" ] && [ -z "$ENABLE_DOT_NET" ];then

#export WINEDLLOVERRIDES="mscoree=d,mshtml=d,control.exe=d"
export WINEDLLOVERRIDES="control.exe=d"
#### "为了降低打包体积，默认关闭gecko和momo，如有需要，注释此行（仅对spark-wine7-devel有效）"

fi
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
        $START_SHELL_PATH $BOTTLENAME $APPVER "C:/windows/command/start.exe" "/Unix" "$EXEC_PATH" "$@"
    fi
else
    $START_SHELL_PATH $BOTTLENAME $APPVER "uninstaller.exe" "$@"
fi



'''

desktopFile = f'''#!/usr/bin/env xdg-open
[Desktop Entry]
Encoding=UTF-8
Type=Application
X-Created-By=@@@Maintainer@@@
Icon=@@@Icon@@@
Exec="/opt/apps/@@@Package@@@/files/run.sh"
Name=@@@Name@@@
Comment=@@@Description@@@
MimeType=
GenericName=@@@Package@@@
Terminal=false
StartupNotify=false'''

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


def WriteTxt(path, things):
    with open(path, "w") as file:
        file.write(things)

def ReadTxt(path):
    things = ""
    with open(path, "r") as file:
        things = file.read()
    return things

def GetEXEVersion(exePath, bottlePath=get_home() + "/.wine"):
    versionPath = f"/tmp/wine-runner-exe-version-{random.randint(0, 1000)}.txt"
    if os.system(f"WINEPREFIX='{bottlePath}' {chooseWine} '{programPath}/GetEXEVersion.exe' '{exePath}' '{versionPath}'"):
        return "1.0.0"
    try:
        exeVersion = ReadTxt(versionPath).replace("\n", "")
        if exeVersion.replace(" ", "") == "":
            return "1.0.0"
        return exeVersion
    except:
        traceback.print_exc()
        return "1.0.0"

def StrToByteToStr(text: str):
    lists = text.split("\\x")
    for i in range(len(lists)):
        lists[i]
    return text

def UnUseUpperCharPath(path: str):
    pathList = []
    lowerList = path.split("/")[1:]
    for i in lowerList:
        path = "/" + "/".join(pathList)
        before = len(pathList)
        for k in os.listdir(path):       
            if k.lower() == i.lower():
                pathList.append(k)
                break
        end = len(pathList)
        if before == end:
            raise OSError("文件路径不存在")
    return "/" + "/".join(pathList)

def ReadMe():
    QtWidgets.QMessageBox.information(window, "提示", """1、目前只支持打包 X86 架构的 deb 包，暂未支持 arm；
2、需要区分要打包的程序是绿色软件还是单文件安装包，两个对应的打包方式不相同；
3、打包绿色软件时为尽可能减小程序体积，请将绿化后的程序（或程序文件夹）单独拷贝到干净的目录后再浏览选择主程序打包；
4、打包详情：
    ①调用 Wine：Deepin Wine6 Stable
    ②调用 Helper：Spark Wine Helper
    ③有卸载自动移除容器脚本""")


class RunThread(QtCore.QThread):
    showLogText = QtCore.pyqtSignal(str)
    error = QtCore.pyqtSignal(str)
    info = QtCore.pyqtSignal(str)
    question = QtCore.pyqtSignal(str)
    disbledAll = QtCore.pyqtSignal(bool)
    cleanPressState = QtCore.pyqtSignal(bool)
    def RunCommand(self, command):
        res = subprocess.Popen([command], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while res.poll() is None:
            try:
                text = res.stdout.readline().decode("utf8")
            except:
                text = ""
            self.showLogText.emit(text)
            print(text, end="")

    def __init__(self) -> None:
        super().__init__()
    
    def GetEXEVersion(self, exePath, bottlePath=get_home() + "/.wine"):
        versionPath = f"/tmp/wine-runner-exe-version-{random.randint(0, 1000)}.txt"
        self.RunCommand(f"WINEPREFIX='{bottlePath}' {chooseWine} '{programPath}/GetEXEVersion.exe' '{exePath}' '{versionPath}'")
        try:
            exeVersion = ReadTxt(versionPath).replace("\n", "")
            if exeVersion.replace(" ", "") == "":
                return "1.0.0"
            return exeVersion
        except:
            traceback.print_exc()
            return "1.0.0"

    def QuestionMsg(self, text):
        global questionStatus
        questionStatus = False
        self.question.emit(text)
        while not questionStatus:
            time.sleep(0.1)
        print(questionChoose)
        return questionChoose

    def run(self):
        try:   
            self.disbledAll.emit(True)
            if not self.QuestionMsg("在此过程中，需要回答一系列的问题以进行打包，点击确定继续"):
                self.disbledAll.emit(False)
                return
            bottlePath = f"/tmp/deepin-wine-runner-bottle-{random.randint(0, 10000)}"
            # 清空容器以保证能正常使用
            if os.path.exists(bottlePath):
                self.RunCommand(f"rm -rfv '{bottlePath}'")
            ############# 后面将全部调用 deepin wine6 stable 进行操作
            exeName = os.path.basename(exePath.text())
            # 暂定
            packageName = xpinyin.Pinyin().get_pinyin(os.path.splitext(exeName)[0].replace(" ", ""), "").lower().replace(" ", "").replace("_", ".").replace("-", ".").replace("..", ".")
            
            if " " in packageName:
                packageName = ""
                for i in os.path.splitext(exeName)[0].split(" "):
                    packageName += xpinyin.Pinyin().get_pinyin(i).lower().replace(" ", "").replace("_", ".").replace("-", ".").replace("..", ".") + "."
                    print(packageName)
                packageName = packageName[:-1]
            debPackageName = "com." + packageName + ".spark"
            debPackageVersion = "1.0.0"
            programIconPath = f"/opt/apps/{debPackageName}/entries/icons/hicolor/scalable/apps/{debPackageName}.png"
            debMaintainer = os.getlogin()
            debBuildPath = f"/tmp/deepin-wine-packager-builder-{debPackageName}-{random.randint(0, 1000)}"
            bottlePackagePath = f"{debBuildPath}/opt/apps/{debPackageName}/files/files.7z"
            desktopPath = get_desktop_path()
            ############## 运行 EXE
            if self.QuestionMsg("请问此可执行文件是安装包还是绿色软件？是安装包请按 Yes，绿色软件按 No"):
                # 清空无益处的 lnk 文件
                lnkPath = f"{bottlePath}/drive_c/ProgramData/Microsoft/Windows/Start Menu/Programs"
                self.RunCommand(f"rm -rfv '{lnkPath}'")
                self.RunCommand(f"mkdir -pv '{bottlePath}'")
                self.RunCommand(f"chmod 777 -Rv '{bottlePath}'")
                # 禁止生成 .desktop 文件
                self.RunCommand(f"WINEPREFIX='{bottlePath}' {chooseWine} 'reg' 'add' 'HKEY_CURRENT_USER\Software\Wine\DllOverrides' /v winemenubuilder.exe '/f'")
                # 写入字体
                self.RunCommand(f"WINEPREFIX='{bottlePath}' '{programPath}/AutoShell/command/installfont' 1")
                # 安装包
                self.info.emit("请在运行完安装程序后按下打包器主界面的“安装程序执行完成按钮”以进行下一步操作")
                global pressCompleteDownload
                pressCompleteDownload = False
                installCmpleteButton.setEnabled(True)
                self.RunCommand(f"WINEPREFIX='{bottlePath}' {chooseWine} '{exePath.text()}' &")  # 非堵塞线程
                
                # 安装锁，锁解除后才可继续
                while not pressCompleteDownload:
                    time.sleep(0.1)
                # 杀死容器内应用
                self.RunCommand(f"'{programPath}/kill.sh' '{os.path.basename(bottlePath)}'")
                # 识别 lnk
                lnkList = GetLnkDesktop(lnkPath)
                if len(lnkList) <= 0:
                    self.error.emit("无法识别到任何 lnk 快捷方式")
                    self.RunCommand(f"rm -rfv '{debBuildPath}' > /dev/null")
                    self.RunCommand(f"rm -rfv '{bottlePath}' > /dev/null")
                    self.disbledAll.emit(False)
                    return
                # 选择最优 lnk
                secondChooseList = []
                for k in lnkList:
                    lnkPath = k[0].lower()
                    lnkExePath = k[1].lower()
                    if "卸载" in lnkPath or "uninstall" in lnkPath or "update" in lnkPath or "网页" in lnkPath or "websize" in lnkPath or not ".exe" in lnkExePath:
                        continue
                    secondChooseList.append(k)
                if len(secondChooseList) <= 0:
                    secondChooseList = lnkList
                rightLnk = secondChooseList[0]
                miniLenge = len(rightLnk[1])
                for k in secondChooseList:
                    # 择优选择路径最短一项
                    if len(k[1]) < miniLenge:
                        rightLnk = k
                        miniLenge = len(rightLnk[1])
                replacePackageMap = {
                    " ": "",
                    "--": "-",
                    "_": "-",
                    "-": ".",
                    "(": "",
                    ")": "",
                    "&": "",
                    "*": "",
                    "..": "."
                }
                pkgNameTemp = xpinyin.Pinyin().get_pinyin(os.path.splitext(os.path.basename(rightLnk[0]))[0].replace(" ", "")).lower()
                for i in replacePackageMap.keys():
                    pkgNameTemp = pkgNameTemp.replace(i, replacePackageMap[i])
                debPackageName = "com." + pkgNameTemp + ".spark"
                programIconPath = f"/opt/apps/{debPackageName}/entries/icons/hicolor/scalable/apps/{debPackageName}.png"
                bottlePackagePath = f"{debBuildPath}/opt/apps/{debPackageName}/files/files.7z"
                self.RunCommand(f"mkdir -pv '{debBuildPath}/opt/apps/{debPackageName}/entries/icons/hicolor/scalable/apps/'")
                folderExePath = os.path.dirname(rightLnk[1].replace("\\", "/").replace("c:/", bottlePath))
                exePathInBottle = rightLnk[1]
                exeName = os.path.splitext(os.path.basename(folderExePath))[0]
                exePathInSystem = rightLnk[1].replace("\\", "/").replace("c:", f"{bottlePath}/drive_c")
                debPackageVersion = self.GetEXEVersion(exePathInSystem, bottlePath)
                cpNow = False
                for i in iconList:
                    path = i[1].replace("wineBottonPath", bottlePath).lower()
                    if path == exePathInSystem.lower():
                        self.RunCommand(f"cp -rv '{programPath}/Icon/{i[0]}.svg' '{debBuildPath}/{programIconPath}'")
                        exeName = i[0]
                        cpNow = True
                        break
                if not cpNow:
                    self.RunCommand(f"'{programPath}/wrestool' '{UnUseUpperCharPath(exePathInSystem)}' -x -t 14 > '{debBuildPath}/{programIconPath}'")
            else:
                #/home/gfdgd_xi/Desktop/新建文件夹1/BeCyIconGrabber.exe
                # 绿色软件
                self.RunCommand(f"mkdir -pv '{bottlePath}'")
                self.RunCommand(f"chmod 777 -Rv '{bottlePath}'")
                self.RunCommand(f"WINEPREFIX='{bottlePath}' {chooseWine} exit")
                folderExePath = os.path.dirname(exePath.text())               
                exePathInBottle = f"c:/Program Files/{os.path.basename(folderExePath)}/{exeName}"
                exeName = os.path.splitext(os.path.basename(os.path.basename(exePath.text())))[0]
                self.RunCommand(f"mkdir -pv '{debBuildPath}/opt/apps/{debPackageName}/entries/icons/hicolor/scalable/apps/'")
                self.RunCommand(f"'{programPath}/wrestool' '{exePath.text()}' -x -t 14 > '{debBuildPath}/{programIconPath}'")
                # 拷贝文件到容器
                self.RunCommand(f"cp -rv '{folderExePath}' '{bottlePath}/drive_c/Program Files'")
                debPackageVersion = self.GetEXEVersion(exePath.text(), bottlePath)
            debDescription = f"{exeName} By Build By Wine Runner Easy Packager"
            debDepends = f"{chooseWine} | {chooseWine}-bcm | {chooseWine}-dcm | com.{chooseWine}.deepin, spark-dwine-helper | store.spark-app.spark-dwine-helper | deepin-wine-helper | com.wine-helper.deepin, fonts-wqy-microhei, fonts-wqy-zenhei"
            self.RunCommand(f"mkdir -pv '{debBuildPath}/DEBIAN'")
            self.RunCommand(f"mkdir -pv '{debBuildPath}/opt/apps/{debPackageName}/files'")
            self.RunCommand(f"mkdir -pv '{debBuildPath}/opt/apps/{debPackageName}/entries/applications'")
            self.RunCommand(f"mkdir -pv '{debBuildPath}/usr/share/applications'")
            #self.RunCommand(f"mkdir -pv '{debBuildPath}/opt/apps/{debPackageName}/entries/icons/hicolor/scalable/apps/'")
            ############ 处理容器
            # 对用户目录进行处理
            os.chdir(bottlePath)
            self.RunCommand("sed -i \"s#$USER#@current_user@#\" ./*.reg")
            os.chdir(f"{bottlePath}/drive_c/users")
            # 如果缩放文件 scale.txt 存在，需要移除以便用户自行调节缩放设置
            if os.path.exists(f"{bottlePath}/scale.txt"):
                self.RunCommand(f"rm -rfv '{bottlePath}/scale.txt'")
            # 删除因为脚本失误导致用户目录嵌套（如果存在）
            if os.path.exists(f"{bottlePath}/drive_c/users/@current_user@/@current_user@"):
                self.RunCommand(f"rm -rfv '{bottlePath}/drive_c/users/@current_user@/@current_user@'")
            self.RunCommand(f"mv -fv '{os.getlogin()}' @current_user@")
            self.RunCommand(f"rm -fv '{bottlePath}/drive_c/users/@current_user@/我的'*")
            self.RunCommand(f"rm -fv '{bottlePath}/drive_c/users/@current_user@/My '*")
            self.RunCommand(f"rm -fv '{bottlePath}/drive_c/users/@current_user@/Desktop'")
            self.RunCommand(f"rm -fv '{bottlePath}/drive_c/users/@current_user@/Downloads'")
            self.RunCommand(f"rm -fv '{bottlePath}/drive_c/users/@current_user@/Templates'")
            ########### 打包容器
            self.RunCommand(f"7z a '{bottlePackagePath}' '{bottlePath}/'*")
            ########### 生成文件内容
            buildProgramSize = getFileFolderSize(debBuildPath) / 1000
            replaceMap = [
                ["@@@Package@@@", debPackageName],
                ["@@@Version@@@", debPackageVersion],
                ["@@@Maintainer@@@", debMaintainer],
                ["@@@Depends@@@", debDepends],
                ["@@@Description@@@", debDescription],
                ["@@@Installed-Size@@@", str(int(buildProgramSize))],
                ["@@@Name@@@", exeName],
                ["@@@EXEC_PATH@@@", exePathInBottle],
                ["@@@Icon@@@", programIconPath],
                ["@@Wine@@", chooseWine]
            ]
            debControl = ReplaceText(control, replaceMap)
            debPostinst = ReplaceText(postinst, replaceMap)
            debPostrm = ReplaceText(postrm, replaceMap)
            debInfo = ReplaceText(info, replaceMap)
            debRunSh = ReplaceText(runsh, replaceMap)
            debDesktop = ReplaceText(desktopFile, replaceMap)
            ########### 写入文件
            WriteTxt(f"{debBuildPath}/opt/apps/{debPackageName}/entries/applications/{debPackageName}.desktop", debDesktop)
            WriteTxt(f"{debBuildPath}/usr/share/applications/{debPackageName}.desktop", debDesktop)
            WriteTxt(f"{debBuildPath}/opt/apps/{debPackageName}/files/run.sh", debRunSh)
            WriteTxt(f"{debBuildPath}/opt/apps/{debPackageName}/info", debInfo)
            WriteTxt(f"{debBuildPath}/DEBIAN/control", debControl)
            WriteTxt(f"{debBuildPath}/DEBIAN/postinst", debPostinst)
            WriteTxt(f"{debBuildPath}/DEBIAN/postrm", debPostrm)
            ########### 赋值权限
            self.RunCommand(f"chmod -Rv 644 '{debBuildPath}/opt/apps/{debPackageName}/info'")
            self.RunCommand(f"chmod -Rv 0755 '{debBuildPath}/DEBIAN'")
            self.RunCommand(f"chmod -Rv 755 '{debBuildPath}/opt/apps/{debPackageName}/files/'*.sh")
            self.RunCommand(f"chmod -Rv 755 '{debBuildPath}/opt/apps/{debPackageName}/entries/applications/'*.desktop")
            self.RunCommand(f"chmod -Rv 755 '{debBuildPath}/usr/share/applications/'*.desktop")
            ########### 打包 deb
            print(debPackageVersion)
            self.RunCommand(f"dpkg-deb -Z xz -z 0 -b '{debBuildPath}' '{desktopPath}/{debPackageName}_{debPackageVersion}_all.deb'")
            self.info.emit("打包完成！")
            self.disbledAll.emit(False)
            ########### 移除临时文件
            self.RunCommand(f"rm -rfv '{debBuildPath}' > /dev/null")
            self.RunCommand(f"rm -rfv '{bottlePath}' > /dev/null")
        except:
            self.RunCommand(f"rm -rfv '{debBuildPath}' > /dev/null")
            self.RunCommand(f"rm -rfv '{bottlePath}' > /dev/null")
            # 若打包出现任何错误
            traceback.print_exc()
            self.error.emit(f"打包错误，详细详细如下：{traceback.format_exc()}")
            self.showLogText.emit(traceback.format_exc())
            self.disbledAll.emit(False)

#/home/gfdgd_xi/Downloads/XPcalc.exe
def RunBuildThread():
    global buildThread
    global chooseWine
    chooseWine = wineList[wineChooser.currentIndex()]
    buildThread = RunThread()
    buildThread.showLogText.connect(ShowText)
    buildThread.error.connect(ErrorMessage)
    buildThread.info.connect(InformationMessage)
    buildThread.question.connect(QuestionMessage)
    buildThread.disbledAll.connect(DisbledAndEnabledAll)
    buildThread.cleanPressState.connect(CleanPressCompleteDownloadState)
    logText.clear()
    buildThread.start()

pressCompleteDownload = False

def PressCompleteDownload():
    global pressCompleteDownload
    pressCompleteDownload = True
    installCmpleteButton.setDisabled(True)

def BrowserExe():
    filePath = QtWidgets.QFileDialog.getOpenFileName(window, "选择 exe", get_home(), "可执行文件(*.exe);;所有文件(*.*)")
    if filePath[0] != "" or filePath[0] != None:
        exePath.setText(filePath[0])

chooseWine = ""
if __name__ == "__main__":
    programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
    iconPath = "{}/deepin-wine-runner.svg".format(programPath)
    information = json.loads(ReadTxt(f"{programPath}/information.json"))
    iconListUnBuild = json.loads(ReadTxt(f"{programPath}/IconList.json"))[0]
    iconList = json.loads(ReadTxt(f"{programPath}/IconList.json"))[1]
    for i in iconListUnBuild:
        iconList.append(i)
    app = QtWidgets.QApplication(sys.argv)
    version = information["Version"]
    window = QtWidgets.QMainWindow()
    widget = QtWidgets.QWidget()
    layout = QtWidgets.QGridLayout()
    exePath = QtWidgets.QLineEdit()
    wineChooser = QtWidgets.QComboBox()
    browserExeButton = QtWidgets.QPushButton("浏览……")
    logText = QtWidgets.QTextBrowser()
    logText.setStyleSheet("""
        background-color: black;
        color: white;
    """)
    wineChooserList = [
        "使用 Deepin Wine8 Stable 打包应用",
        "使用 Spark Wine9 wow 打包应用",
        "使用 Spark Wine9 打包应用",
        "使用 Spark Wine8 打包应用",
        "使用 Spark Wine7 Devel 打包应用",
        "使用 Deepin Wine6 Stable 打包应用",
        "使用 Deepin Wine5 Stable 打包应用",
        "使用 Deepin Wine5 打包应用",
        "使用 Deepin Wine2 打包应用",
        "使用 Spark Wine 打包应用"
    ]
    wineChooserIndex = 2
    wineList = ["deepin-wine8-stable", "spark-wine9-wow", "spark-wine9", "spark-wine8", "spark-wine7-devel", "deepin-wine6-stable", "deepin-wine6-vannila", "spark-wine8-wow", "deepin-wine5-stable", "deepin-wine5", "deepin-wine", "spark-wine"]
    for i in range(len(wineList)):
        if not os.system(f"which '{wineList[i]}'"):
            wineChooserIndex = i
            break
    chooseWine = wineList[wineChooserIndex]
    wineChooserList[wineChooserIndex] = f"{wineChooserList[wineChooserIndex]}（推荐，如无特殊需求不建议更换）"
    wineChooser.addItems(wineChooserList)
    wineChooser.setCurrentIndex(wineChooserIndex)
    controlLayout = QtWidgets.QHBoxLayout()
    buildButton = QtWidgets.QPushButton("现在打包……")
    installCmpleteButton = QtWidgets.QPushButton("安装程序执行完成")
    helpButton = QtWidgets.QPushButton("帮助")
    installUosPackingTool = QtWidgets.QPushButton("安装维护工具箱（可以安装测试 deb）")
    browserExeButton.clicked.connect(BrowserExe)
    buildButton.clicked.connect(RunBuildThread)
    installCmpleteButton.clicked.connect(PressCompleteDownload)
    helpButton.clicked.connect(ReadMe)
    def InstallUosPackingTool():
        if os.system("which spark-store"):
            QtWidgets.QMessageBox.critical(window, "提示", "未安装星火应用商店，无法继续\n星火应用商店官网：https://spark-app.store/")
            return 0
        threading.Thread(target=os.system, args=["spark-store spk://store/tools/uos-packaging-tools"]).start()
    installUosPackingTool.clicked.connect(InstallUosPackingTool)
    installCmpleteButton.setDisabled(True)
    controlLayout.addWidget(buildButton)
    controlLayout.addWidget(installCmpleteButton)
    controlLayout.addWidget(helpButton)
    controlLayout.addWidget(installUosPackingTool)
    layout.addWidget(QtWidgets.QLabel("选择 EXE："), 0, 0)
    layout.addWidget(exePath, 0, 1)
    layout.addWidget(browserExeButton, 0, 2)
    layout.addWidget(wineChooser, 1, 1)
    layout.addLayout(controlLayout, 2, 1)
    layout.addWidget(logText, 3, 0, 1, 3)
    widget.setLayout(layout)
    window.setCentralWidget(widget)
    window.setWindowTitle(f"Wine 运行器 {version}——简易打包器")
    try:
        exePath.setText(sys.argv[1])
    except:
        pass
    window.resize(int(window.frameGeometry().width() * 1.2), int(window.frameGeometry().height() * 1.1))
    window.show()
    # 设置字体
    SetFont(app)
    sys.exit(app.exec_())
