#!/usr/bin/env python3
import os
import sys
import time
import subprocess
import threading
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

def check_window():
    # 使用 wmctrl 命令列出所有窗口，并使用 grep 过滤出特定的 WMCLASS
    windows = subprocess.getoutput(f'wmctrl -lx | grep "{target_wmclass}"')
    # 如果窗口存在，则关闭提示
    if windows.replace("\n", "").replace(" ", "") != "":
        # 提取窗口ID
        window_id = windows.replace("  ", " ").split(" ")[0]

        print(f"Window with WMCLASS '{target_wmclass}' found")
        return 1
    else:
        print(f"Window with WMCLASS '{target_wmclass}' not found.")


def check_wmclass():
    if timeout:
        time.sleep(timeout)
        window.close()
        return
    # 循环检测窗口是否存在的函数
    # 每隔一段时间检测一次窗口是否存在
    showtimeout = 60  # 为防止因为应用无法打开而无法正常关闭窗口，于是设置 time out
    while True:
        if check_window():
            break
        # 等待一段时间后再次检测
        time.sleep(1)
        AppInfoShowerRefresh()
        showtimeout -= 1
        if showtimeout <= 0:
            break
    window.close()


timeout = 0
if os.getenv("WAYLAND_DISPLAY"):
    timeout = 3

if os.system("which wmctrl"):
    print("No wmctrl installed. Do not check wmclass")
    timeout = 3

target_wmclass = os.getenv("WINE_WMCLASS")

def GetRecommendWindowSize(window: QMainWindow):
    # 计算屏幕分辨率
    screen = QGuiApplication.primaryScreen()
    width = screen.geometry().width()
    height = screen.geometry().height()
    # 如果为竖状屏幕
    if width < height:
        temp = height
        height = width
        width = temp
    return [int(width / 4), window.geometry().height()]

def SetWindowSize(window: QMainWindow):
    # 计算比例
    size = GetRecommendWindowSize(window)
    window.resize(size[0], size[1])

def MoveCenter(window: QMainWindow):
    # 计算屏幕分辨率
    screen = QGuiApplication.primaryScreen()
    width = screen.geometry().width()
    height = screen.geometry().height()
    print(window.geometry().height())
    # 计算窗口坐标
    window.move(int(width / 2 - window.geometry().width() / 2),
                int(height / 2.8 - window.geometry().height() / 2)
                )

def AppInfoShowerRefresh():
    global appInfoShowerTime
    appInfoShower.setText(f"<h3 align='center'>星火Windows应用兼容助手</h3><p align='center'>正在为您启动以下应用：{os.getenv('WINE_APP_NAME')} {'.' * (appInfoShowerTime % 3 + 1)}</p>")

    appInfoShowerTime += 1

programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string

app = QApplication(sys.argv)
# 构建窗口
window = QMainWindow()
widget = QWidget()
layout = QGridLayout()

appInfoShower = QLabel()
appInfoShowerTime = 0
AppInfoShowerRefresh()

backgroundImgPath = f"{programPath}/back.jpg"
# GXDE 彩蛋
if os.path.exists("/usr/share/gxde-resources/spark-dwine-helper.png"):
    backgroundImgPath = "/usr/share/gxde-resources/spark-dwine-helper.png"

window.setWindowTitle("星火Windows应用兼容助手")
layout.addWidget(QLabel(f""), 1, 0)
layout.addWidget(appInfoShower, 2, 0)
layout.addWidget(QLabel(f"<hr>由 Wine 运行器提供支持"), 4, 0)
widget.setLayout(layout)
window.setCentralWidget(widget)
window.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint)
window.show()
SetWindowSize(window)

layout.addWidget(QLabel(f"<p align='center'><img width='{window.geometry().width()}' src='{backgroundImgPath}'></p>"), 0, 0)
threading.Thread(target=check_wmclass).start()
MoveCenter(window)
app.exec_()