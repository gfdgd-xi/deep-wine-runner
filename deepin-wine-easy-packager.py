import os
import sys
import json
import random
import xpinyin
import traceback
import subprocess
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets

def ShowText(text: str):
    if text.replace(" ", "").replace("\n", "") == "":
        return
    logText.append(text)
    
def ErrorMessage(text: str):
    QtWidgets.QMessageBox.critical(window, "错误", text)

def InformationMessage(text: str):
    QtWidgets.QMessageBox.information(window, "提示", text)

def QuestionMessage(text: str):
    if QtWidgets.QMessageBox.question(window, "提示", text) == QtWidgets.QMessageBox.Yes:
        return True
    return False

def DisbledAndEnabledAll(choose: bool):
    pass

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
                    for k in str(things[1: -2]).split("\\x00"):
                        things = k
                        if things == b"":
                            break
                        if "c:" in things:
                            lnkList.append([filePath, things])
                            print(things)
    return lnkList

def ReplaceText(string: str, lists: list):
    for i in lists:
        string = string.replace(i[0], i[1])
    return string

control = '''Package: @@@Package@@@
Version: @@@Version@@@
Architecture: i386
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
START_SHELL_PATH="/opt/deepinwine/tools/spark_run_v4.sh"
export MIME_TYPE=""
#####没什么用
export DEB_PACKAGE_NAME="@@@Package@@@"
####这里写包名才能在启动的时候正确找到files.7z,似乎也和杀残留进程有关
export APPRUN_CMD="@@@Package@@@"
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
fi'''

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

def WriteTxt(path, things):
    with open(path, "w") as file:
        file.write(things)

def ReadTxt(path):
    things = ""
    with open(path, "r") as file:
        things = file.read()
    return things

class RunThread(QtCore.QThread):
    showLogText = QtCore.pyqtBoundSignal(str)
    error = QtCore.pyqtBoundSignal(str)
    info = QtCore.pyqtBoundSignal(str)
    question = QtCore.pyqtBoundSignal(str)
    disbledAll = QtCore.pyqtBoundSignal(bool)

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
    
    def run(self):
        try:
            if not self.question.emit("在此过程中，需要回答一系列的问题以进行打包，点击确定继续"):
                self.disbledAll.emit(False)
                return
            bottlePath = f"/tmp/deepin-wine-runner-bottle{random.randint(0, 10000)}"
            # 清空容器以保证能正常使用
            if os.path.exists(bottlePath):
                self.RunCommand(f"rm -rfv '{bottlePath}'")
            ############# 后面将全部调用 deepin wine6 stable 进行操作
            exeName = os.path.basename(exePath.text())
            # 暂定
            debPackageName = "spark-" + xpinyin.Pinyin().get_pinyin(os.path.splitext(exeName)[0].replace(" ", "")).lower().replace("--", "-").replace(" ", "")
            debPackageVersion = "1.0.0"
            debMaintainer = os.getlogin()
            debBuildPath = f"/tmp/deepin-wine-packager-builder-{debPackageName}"
            bottlePackagePath = f"{debBuildPath}/opt/apps/{debPackageName}/files/files.7z"
            desktopPath = get_desktop_path()
            self.RunCommand(f"mkdir -pv '{debBuildPath}/DEBIAN'")
            self.RunCommand(f"mkdir -pv '{debBuildPath}/opt/apps/{debPackageName}/files'")
            self.RunCommand(f"mkdir -pv '{debBuildPath}/opt/apps/{debPackageName}/entries/applications'")
            self.RunCommand(f"mkdir -pv '{debBuildPath}/opt/apps/{debPackageName}/entries/icons'")
            ############## 运行 EXE
            if self.question.emit("请问此可执行文件是安装包还是绿色软件？是安装包请按 Yes，绿色软件按 No"):
                # 清空无益处的 lnk 文件
                lnkPath = f"{bottlePath}/drive_c/ProgramData/Microsoft/Windows/Start Menu/Programs"
                self.RunCommand(f"rm -rfv '{lnkPath}'")
                # 安装包
                self.RunCommand(f"WINEPREFIX='{bottlePath}' deepin-wine6-stable '{exePath.text()}'")
                # 安装锁，先不写
                # 识别 lnk
                lnkList = GetLnkDesktop(lnkPath)
                if len(lnkList) <= 0:
                    self.info.error("无法识别到任何 lnk 快捷方式")
                    self.disbledAll.emit(False)
                    return
                # 选择最优 lnk
                secondChooseList = []
                for k in lnkList:
                    lnkPath = k[0].lower()
                    if "卸载" in lnkPath or "uninstall" in lnkPath or "update" in lnkPath:
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
                folderExePath = os.path.dirname(rightLnk[1].replace("\\", "/").replace("c:/", bottlePath))
                exePathInBottle = rightLnk[1]
                exeName = os.path.splitext(os.path.basename(folderExePath))[0]
                programIconPath = ""
            else:
                # 绿色软件
                folderExePath = os.path.dirname(exePath.text())               
                exePathInBottle = f"c:/Program Files/{os.path.basename(folderExePath)}/{exeName}"
                exeName = os.path.splitext(os.path.basename(os.path.basename(exePath.text())))[0]
                programIconPath = ""
                # 拷贝文件到容器
                self.RunCommand(f"cp -rv '{folderExePath}/..' '{bottlePath}/Program Files'")
            debDescription = f"{exeName} By Deepin Wine 6 Stable And Build By Wine Runner"
            debDepends = "deepin-wine6-stable, spark-dwine-helper | store.spark-app.spark-dwine-helper, fonts-wqy-microhei, fonts-wqy-zenhei"
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
            buildProgramSize = 0
            replaceMap = [
                ["@@@Package@@@", debPackageName],
                ["@@@Version@@@", debPackageVersion],
                ["@@@Maintainer@@@", debMaintainer],
                ["@@@Depends@@@", debDepends],
                ["@@@Description@@@", debDescription],
                ["@@@Installed-Size@@@", buildProgramSize],
                ["@@@Name@@@", exeName],
                ["@@@EXEC_PATH@@@", exePathInBottle],
                ["@@@Icon@@@", programIconPath]
            ]
            debControl = ReplaceText(control, replaceMap)
            debPostrm = ReplaceText(postrm, replaceMap)
            debInfo = ReplaceText(info, replaceMap)
            debRunSh = ReplaceText(runsh, replaceMap)
            debDesktop = ReplaceText(desktopFile, replaceMap)
            ########### 写入文件
            WriteTxt(f"{debBuildPath}/opt/apps/{debPackageName}/entries/applications/{debPackageName}.desktop", debDesktop)
            WriteTxt(f"{debBuildPath}/opt/apps/{debPackageName}/files/run.sh", debRunSh)
            WriteTxt(f"{debBuildPath}/opt/apps/{debPackageName}/info", debInfo)
            WriteTxt(f"{debBuildPath}/DEBIAN/control", debControl)
            WriteTxt(f"{debBuildPath}/DEBIAN/postrm", debPostrm)
            ########### 打包 deb
            self.RunCommand(f"dpkg -b '{debBuildPath}' '{desktopPath}/{debPackageName}_{debPackageVersion}_i386.deb'")
            self.info.emit("打包完成！")
            self.disbledAll.emit(False)
        except:
            # 若打包出现任何错误
            traceback.print_exc()
            self.error.emit(f"打包错误，详细详细如下：{traceback.format_exc()}")
            self.showLogText.emit(traceback.format_exc())
            self.disbledAll.emit(False)

def RunBuildThread():
    global buildThread
    buildThread = RunThread()
    buildThread.showLogText.connect(ShowText)
    buildThread.error.connect(ErrorMessage)
    buildThread.info.connect(InformationMessage)
    buildThread.question.connect(QuestionMessage)
    buildThread.disbledAll.connect(DisbledAndEnabledAll)
    buildThread.start()

if __name__ == "__main__":
    programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
    iconPath = "{}/deepin-wine-runner.svg".format(programPath)
    information = json.loads(ReadTxt(f"{programPath}/information.json"))
    app = QtWidgets.QApplication(sys.argv)
    version = information["Version"]
    window = QtWidgets.QMainWindow()
    widget = QtWidgets.QWidget()
    layout = QtWidgets.QGridLayout()
    exePath = QtWidgets.QLineEdit()
    browserExeButton = QtWidgets.QPushButton("浏览……")
    logText = QtWidgets.QTextBrowser()
    logText.setStyleSheet("""
        background-color: black;
        color: white;
    """)
    buildButton = QtWidgets.QPushButton("现在打包……")
    buildButton.clicked.connect(RunBuildThread)
    layout.addWidget(QtWidgets.QLabel("选择 EXE："), 0, 0)
    layout.addWidget(exePath, 0, 1)
    layout.addWidget(browserExeButton, 0, 2)
    layout.addWidget(buildButton, 1, 1)
    layout.addWidget(logText, 2, 0, 1, 3)
    widget.setLayout(layout)
    window.setCentralWidget(widget)
    window.setWindowTitle(f"Wine 运行器 {version}——简易打包器")
    window.show()
    sys.exit(app.exec_())