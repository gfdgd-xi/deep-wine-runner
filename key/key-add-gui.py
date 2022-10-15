#!/usr/bin/env python3
import os
import sys
programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
sys.path.append(f"{programPath}/..")

import dbus
import threading
from UI.KeyAddGui import *
import PyQt5.QtWidgets as QtWidgets

class Check:
    def VersionCheck():
        try:
            bus = dbus.SessionBus()
            bus.get_object("com.deepin.daemon.Keybinding", "/com/deepin/daemon/Keybinding").List()
            int("a")
            return True
        except:
            print("无法检测到 Deepin/UOS 快捷键服务")
            return False
    def CheckThreading():
        if Check.VersionCheck():
            ui.startServer.setDisabled(True)
            ui.stopServer.setDisabled(True)
            ui.setAutoStart.setDisabled(True)
            ui.setUnautoStart.setDisabled(True)
            ui.editButton.setDisabled(True)
            ui.keyBoardList.setDisabled(True)
            ui.saveButton.setDisabled(True)

class Click:
    def AddButton():
        os.system(f"'{programPath}/keyboard-add-gui.py'")

    

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    # 连接槽
    ui.addButton.clicked.connect(Click.AddButton)
    ui.startServer.triggered.connect(lambda: threading.Thread(target=os.system, args=[f"nohup '{programPath}/key-get.py' &"]).start())
    ui.stopServer.triggered.connect(lambda: threading.Thread(target=os.system, args=[f"'{programPath}/stop.sh'"]).start())
    ui.setAutoStart.triggered.connect(lambda: threading.Thread(target=os.system, args=[f"'{programPath}/start-auto-server.sh'"]).start())
    ui.setUnautoStart.triggered.connect(lambda: threading.Thread(target=os.system, args=[f"'{programPath}/stop-auto-server.sh'"]).start())
    window.show()
    threading.Thread(target=Check.CheckThreading).start()
    sys.exit(app.exec_())