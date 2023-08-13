#!/usr/bin/env python3
# 读取设置单独用一个 py 文件
import os
import json
import PyQt5.QtGui as QtGui

# 获取用户主目录
def get_home():
    return os.path.expanduser('~')

# 读取文本文档
def readtxt(path):
    f = open(path, "r") # 设置文件对象
    str = f.read()  # 获取内容
    f.close()  # 关闭文本对象
    return str  # 返回结果

defultProgramList = {
    "Architecture": "Auto",
    "Debug": True,
    "DefultWine": "deepin-wine6 stable",
    "DefultBotton" : get_home() + "/.wine",
    "TerminalOpen": False,
    "WineOption": "",
    "WineBottonDifferent": False,
    "CenterWindow": False,
    "Theme": "",
    "MonoGeckoInstaller": False,
    "AutoWine": True,
    "RuntimeCache": True,
    "MustRead": False,
    "BuildByBottleName": False,
    "AutoPath": False,
    "QemuUnMountHome": False,
    "Chinese": True,
    "FontSize": 1
}

def SetFont(app):
    defaultFont = app.font()
    size = setting["FontSize"]
    font = QtGui.QFont(defaultFont)
    if size == 1:
        app.setFont(defaultFont)    
        return
    font.setPixelSize(int(defaultFont.pixelSize() / size))
    font.setPointSize(int(defaultFont.pointSize() / size))
    app.setFont(font)

try:
    setting = json.loads(readtxt(get_home() + "/.config/deepin-wine-runner/WineSetting.json"))
except:
    setting = defultProgramList