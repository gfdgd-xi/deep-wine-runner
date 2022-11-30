#!/usr/bin/env python3
import os
import sys
import json
import traceback
import req as requests
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets
from Model import *

sources = [
    "https://code.gitlink.org.cn/gfdgd_xi/deepin-wine-runner-ubuntu-image/raw/branch/master/Sandbox"
]
sourceIndex = 0

def ReadTXT(path: str) -> str:
    with open(path, "r") as file:
        things = file.read()
    return things

def WriteTXT(path: str, text: str) -> None:
    with open(path, "w") as file:
        file.write(text)

def CheckVersion(arch: str) -> bool:
    information = requests.get(f"{sources[sourceIndex]}/{arch}/lists.json").json()[0]
    try:
        ReadTXT()
    except:
        traceback.print_exc()
        QtWidgets.QMessageBox.critical(None, "错误", traceback.format_exc())


if __name__ == "__main__":
    programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
    app = QtWidgets.QApplication(sys.argv)
    if os.system("which qemu-i386-static"):
        if QtWidgets.QMessageBox.question(None, "提示", "检测到您未安装 qemu-user-static，是否安装？") == QtWidgets.QMessageBox.Yes:
            OpenTerminal(f"pkexec bash '{programPath}/ShellList/InstallQemuUserStatic.sh'")
        exit()
    while True:
        archList = requests.get(f"{sources[sourceIndex]}/lists.json").json()
        choose = QtWidgets.QInputDialog.getItem(None, "选择", "选择要安装/更新的镜像对应的架构", archList, 0, False)
        if not choose[1]:
            QtWidgets.QMessageBox.information(None, "提示", "用户取消操作")
            break