#!/usr/bin/env python3
# 使用系统默认的 python3 运行
###########################################################################################
# 作者：gfdgd xi
# 版本：2.4.0
# 更新时间：2022年10月15日
# 感谢：感谢 wine 以及 deepin-wine 团队，提供了 wine 和 deepin-wine 给大家使用，让我能做这个程序
# 基于 Python3 构建
###########################################################################################
#################
# 加入路径
#################
import os
import sys
programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
sys.path.append(f"{programPath}/../../")
#################
# 引入所需的库（正式内容）
#################
import os
import sys
import ConfigLanguareRunner
class Old:
    wine = ""
    wineprefix = ""
    def __init__(self, wine = "", wineprefix = "") -> None:
        self.wine = os.getenv("WINE") if wine == "" else wine
        self.wineprefix = os.getenv("WINEPREFIX") if wine == "" else wineprefix

    def runCommand(self, command: str) -> None:
        com = ConfigLanguareRunner.Command(command)
        print(com.GetCommandList())
        return com.Run(com.GetCommandList(), self.wineprefix, self.wine)

    def runList(self, command: list) -> None:
        return ConfigLanguareRunner.Command("").Run(command, self.wineprefix, self.wine)

class Bash:
    wine = ""
    wineprefix = ""
    def __init__(self, wine = "", wineprefix = "") -> None:
        self.wine = os.getenv("WINE") if wine == "" else wine
        self.wineprefix = os.getenv("WINEPREFIX") if wine == "" else wineprefix

    def runCommand(self, command: str) -> int:
        return os.system(f"'{programPath}/../../AutoShell/main.py' -c \"{command}\"")

    def runList(self, command: list) -> int:
        commandStr = ""
        for k in command:
            for i in k:
                commandStr += f"'{i}' "
            commandStr += ";"
        return os.system(f"'{programPath}/../../AutoShell/main.py' -c \"{commandStr}\"")
