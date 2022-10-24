#!/usr/bin/env python3
import os
import sys

# 读取文本文档
def readtxt(path: "路径")->"读取文本文档":
    f = open(path, "r")  # 设置文件对象
    str = f.read()  # 获取内容
    f.close()  # 关闭文本对象
    return str  # 返回结果


def ChangeDeepinWineOpenFileDialogDefult()->"":
    info = readtxt("/opt/deepinwine/tools/run_v3.sh")
    all = ""
    for line in info.split('\n'):
        if "export ATTACH_FILE_DIALOG=" in line:
            if "#" in line:
                return False
            line = "#" + line
        all = all + line + "\n"
    return all[0: -1]

def ChangeDeepinWineOpenFileDialogDeepinDialog()->"":
    info = readtxt("/opt/deepinwine/tools/run_v3.sh")
    all = ""
    for line in info.split('\n'):
        if "export ATTACH_FILE_DIALOG=" in line:
            if "#" not in line:
                return False
            line = line.replace("#", "")
        all = all + line + "\n"
    return all[0: -1]

# 写入文本文档
def write_txt(path: "路径", things: "内容")->"写入文本文档":
    file = open(path, 'w', encoding='UTF-8')  # 设置文件对象
    file.write(things)  # 写入文本
    file.close()  # 关闭文本对象

def Help():
    print("参数帮助：")
    print("deepin\t使用 deepin 默认文管")
    print("defult\t使用 wine 默认文管")
    print("recovery\t恢复默认设置")
    print("--help\t查看帮助")

if len(sys.argv) <= 1:
    print("参数错误！")
    Help()
    sys.exit(1)
if not sys.argv[1] == "deepin" and not sys.argv[1] == "defult" and not sys.argv[1] == "recovery" or sys.argv[1] == "--help":
    Help()
    sys.exit(1)
things = ""
if sys.argv[1] == "deepin":
    things = ChangeDeepinWineOpenFileDialogDeepinDialog()
elif sys.argv[1] == "defult":
    things = ChangeDeepinWineOpenFileDialogDefult()
elif sys.argv[1] == "recovery":
    os.system("sudo apt reinstall deepin-wine-helper:i386")
    sys.exit(0)
else:
    print("参数错误！")
    Help()
    sys.exit(1)
if things == False or things == "":
    print("无法更新配置：配置不准重复更新")
    sys.exit(1)
write_txt("/opt/deepinwine/tools/run_v3.sh", things)
sys.exit(0)
