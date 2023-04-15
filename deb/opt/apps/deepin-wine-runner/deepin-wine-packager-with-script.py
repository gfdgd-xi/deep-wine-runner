#!/usr/bin/env python3
# 使用系统默认的 python3 运行
###########################################################################################
# 作者：gfdgd xi、为什么您不喜欢熊出没和阿布呢
# 版本：1.6.1
# 更新时间：2022年07月14日
# 感谢：感谢 wine 以及 deepin-wine 团队，提供了 wine 和 deepin-wine 给大家使用，让我能做这个程序
# 基于 Python3 的 tkinter 构建
###########################################################################################
#################
# 引入所需的库
#################
import os
import sys
import json
import updatekiller
import threading
import PyQt5.QtWidgets as QtWidgets

# 读取文本文档
def readtxt(path):
    f = open(path, "r") # 设置文件对象
    str = f.read()  # 获取内容
    f.close()  # 关闭文本对象
    return str  # 返回结果

def Unzip():
    os.system("mkdir -p ~")
    os.chdir(f"{homePath}")
    os.system(f"unzip -o \"{programPath}/package-script.zip\"")
    print("Unzip Done")
    ReStartProgram()

# 重启本应用程序
def ReStartProgram():
    python = sys.executable
    os.execl(python, python, * sys.argv)

programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
homePath = os.path.expanduser('~')
information = json.loads(readtxt(f"{programPath}/information.json"))
version = information["Version"]
if not os.path.exists(f"{homePath}/package-script") or not json.loads(readtxt(f"{homePath}/package-script/information.json"))["Version"] == version:
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    widgetLayout = QtWidgets.QVBoxLayout()
    widget.setWindowTitle("解压中")
    widgetLayout.addWidget(QtWidgets.QLabel("正在解压所需程序，请稍后……"))
    progress = QtWidgets.QProgressBar()
    progress.setMaximum(0)
    progress.setMinimum(0)
    progress.update()
    widgetLayout.addWidget(progress)
    widget.setLayout(widgetLayout)
    widget.show()
    # 解压流程
    QtWidgets.QProgressDialog(None)
    t = threading.Thread(target=Unzip)
    t.start()
    sys.exit(app.exec_())
os.chdir(f"{homePath}/package-script")
os.system("./package.py")
print("End")
