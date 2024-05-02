#!/usr/bin/env python3
import os
import sys
import time
import subprocess
import threading
import PyQt5.QtWidgets as QtWidgets

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
    while True:
        if check_window():
            break
        # 等待一段时间后再次检测
        time.sleep(1)
    window.close()


timeout = 0
if os.getenv("WAYLAND_DISPLAY"):
    timeout = 3

if os.system("which wmctrl"):
    print("No wmctrl installed. Do not check wmclass")
    timeout = 3

target_wmclass = os.getenv("WINE_WMCLASS")


app = QtWidgets.QApplication(sys.argv)
# 构建窗口
window = QtWidgets.QMainWindow()
window.setCentralWidget(QtWidgets.QLabel(f"正在为您启动以下应用：{os.getenv('WINE_APP_NAME')}"))
window.show()
threading.Thread(target=check_wmclass).start()
app.exec_()