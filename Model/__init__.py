#!/usr/bin/env python3
import os
import sys
import PyQt5.QtWidgets as QtWidgets
def OpenTerminal(command):
    if terminalEnd[terminal][1]:
        os.system(f"\"{terminal}\" \"{terminalEnd[terminal][0]}\" \"{command}\"")
        return
    os.system(f"\"{terminal}\" \"{terminalEnd[terminal][0]}\" {command}")
programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
# 对终端的获取
# 为什么 openkylin 只有 mate-terminal
# 优先为深度终端
terminal = ""
terminalList = [
    "deepin-terminal",
    "gxde-terminal",
    "mate-terminal",
    "gnome-terminal",
    "xfce4-terminal"
]
terminalEnd = {
    f"{programPath}/../launch.sh\" \"deepin-terminal": ["-e", 0],
    f"{programPath}/../launch.sh\" \"gxde-terminal": ["-e", 0],
    "mate-terminal": ["-e", 1],
    "gnome-terminal": ["--", 0],
    "xfce4-terminal": ["-e", 1]
}
for i in terminalList:
    if not os.system(f"which {i}"):
        if i == "deepin-terminal":
            i = f"{programPath}/../launch.sh\" \"deepin-terminal"
        if i == "deepin-terminal-gtk":
            i = f"{programPath}/../launch.sh\" \"gxde-terminal"
        terminal = i
        break
if terminal == "":
    print("无法识别到以下的任意一个终端")
    print(" ".join(terminalList))
    app = QtWidgets.QApplication(sys.argv)
    QtWidgets.QMessageBox.critical(None, "错误", "无法识别到以下的任意一个终端\n" + " ".join(terminalList))
    exit()

# 转包
class TurnDeb():
    debPath = ""
    def __init__(self, debPath):
        self.debPath = debPath

    def ToRpm(self):
        if os.system("which alien"):
            raise NameError("无法找到 alien 命令，请先安装 alien")
        if os.system("which fakeroot"):
            raise NameError("无法找到 fakeroot 命令，请先安装 fakeroot")
        os.system(f"fakeroot alien -r '{self.debPath}' -c")

    def ToTarZst(self):
        if os.system("debtap"):
            raise NameError("无法找到 debtap 命令，请先安装 debtap")
        os.system(f"debtap -Q '{self.debPath}'")
