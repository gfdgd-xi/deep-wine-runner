#!/usr/bin/env python3
import os
import sys
programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
sys.path.append(f"{programPath}/..")

import os
import sys
import json
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

def Clear():
    ui.keyBoardList.model().removeRows(0, ui.keyBoardList.model().rowCount())
    model = QtCore.QStringListModel(window)
    with open(f"{programPath}/list/KeyList.json", "r") as file:
        lists = []
        for i in json.loads(file.read()):
            lists.append(f"{i[0]}（{'+'.join(i[1: -1])}），{i[-1]}")
        model.setStringList(lists)
    ui.keyBoardList.setModel(model)


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
    Clear()
    sys.exit(app.exec_())