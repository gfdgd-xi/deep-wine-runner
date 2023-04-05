#!/usr/bin/env python3
import os
import sys
import updatekiller
import threading
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets

def Create():  
    # 解压容器
    # 这里参考了 deepin wine 的 run_v4.sh
    os.system(f"mkdir -p \"{sys.argv[1]}\"")
    os.system(f"7z x \"{programPath}/files-exagear.7z\" -o\"{sys.argv[1]}\"")
    os.system(f"mv \"{sys.argv[1]}/drive_c/users/@current_user@\" \"{sys.argv[1]}/drive_c/users/$USER\"")
    os.system(f"sed -i \"s#@current_user@#$USER#\" {sys.argv[1]}/*.reg")
    window.close()

def Download():
    os.system(f"aria2c -x 16 -s 16 -d \"{programPath}\" -o files-exagear.7z https://www.gitlink.org.cn/api/attachments/392364")
    window.close()

if __name__ == "__main__":
    if len(sys.argv) <= 1 or "--help" in sys.argv:
        print("帮助：")
        print("参数为要解压到的路径")
        print("--help 查看帮助")
        sys.exit(1)
    programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
    if os.path.exists(sys.argv[1]):
        exit()
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    widget = QtWidgets.QWidget()
    layout = QtWidgets.QHBoxLayout()
    label = QtWidgets.QLabel("正在下载容器，请稍后……")
    layout.addWidget(QtWidgets.QLabel(f"<img src=\"{programPath}/deepin-wine-runner.svg\" width=50>"))
    layout.addWidget(label)
    widget.setLayout(layout)
    window.setCentralWidget(widget)
    window.setWindowTitle("下载容器")
    window.setWindowIcon(QtGui.QIcon(f"{programPath}/deepin-wine-runner.svg"))
    # 下载容器
    if not os.path.exists(f"{programPath}/files-exagear.7z"):
        window.setWindowTitle("下载容器")
        label.setText("正在下载容器，请稍后……")
        window.show()
        threading.Thread(target=Download).start()
        app.exec_()
    window.setWindowTitle(f"解压容器 {sys.argv[1]}")
    label.setText(f"正在解压容器，请稍后……\n容器路径：{sys.argv[1]}")
    window.show()
    threading.Thread(target=Create).start()
    app.exec_()