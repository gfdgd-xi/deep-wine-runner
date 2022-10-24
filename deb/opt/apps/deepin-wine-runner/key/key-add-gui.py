#!/usr/bin/env python3
import os
import sys
import traceback
programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
sys.path.append(f"{programPath}/..")

import os
import sys
import json
import dbus
import threading
from UI.KeyAddGui import *
import PyQt5.QtWidgets as QtWidgets

keyListDebianMap = [[], ["shift"], ["ctrl"], ["alt"], ["ctrl", "alt"], ["ctrl", "shift"], ["alt", "shift"]]
keyList = ["无快捷键", "shift", "ctrl", "alt", "ctrl+alt", "ctrl+shift", "alt+shift"]

class Check:
    def VersionCheck():
        try:
            bus = dbus.SessionBus()
            bus.get_object("com.deepin.daemon.Keybinding", "/com/deepin/daemon/Keybinding").List()
            #int("a")
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
            ui.delectButton.setDisabled(True)

def Clear():
    #ui.keyBoardList.model().removeRows(0, ui.keyBoardList.model().rowCount())
    
    model = QtCore.QStringListModel(window)
    try:
        with open(f"{programPath}/list/KeyList.json", "r") as file:
            lists = []
            for i in json.loads(file.read()):
                #lists.append(f"{i[0]}（{'+'.join(i[0: -1])}），{i[-1]}")
                choice = i
                #ui.localKeyboardChoose.setCurrentIndex(keyListDebianMap.index(choice[:-2]))
                newList = []
                newList.append([keyListDebianMap.index(choice[:-2]), choice[-2]])
                # 解析命令
                command = choice[-1]
                # 筛掉路径
                command = command[command[1:].index("'") + 2:].strip()
                # 筛出其中一个快捷键
                newList.append([command[command.index(" ") - 1]])
                command = command[command.index(" ") + 2:]
                # 读 exe
                newList.insert(0, command[:command.index("'")])
                command = command[command.index("'") + 1: ].strip()
                # 读最后的快捷键
                newList[2].insert(0, int(command))
                print(newList)
                lists.append(f"{newList[0]}（{'+'.join(keyListDebianMap[newList[1][0]])}+{newList[1][1]}）=>（{'+'.join(keyListDebianMap[newList[2][0]])}+{newList[2][1]}）")
            model.setStringList(lists)
        ui.keyBoardList.setModel(model)
    except:
        traceback.print_exc()

class Click:
    def AddButton():
        os.system(f"'{programPath}/keyboard-add-gui.py'")
        Clear()

    def EditButton():
        os.system(f"'{programPath}/keyboard-add-gui.py' {ui.keyBoardList.currentIndex().row()}")
        Clear()

    def DeleteButton():
        try:
            with open(f"{programPath}/list/KeyList.json", "r") as file:
                lists = json.loads(file.read())
            del lists[ui.keyBoardList.currentIndex().row()]
            with open(f"{programPath}/list/KeyList.json", "w") as file:
                file.write(json.dumps(lists))
            Clear()
        except:
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(window, "错误", traceback.format_exc())
    

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    # 连接槽
    ui.addButton.clicked.connect(Click.AddButton)
    ui.editButton.clicked.connect(Click.EditButton)
    ui.delectButton.clicked.connect(Click.DeleteButton)
    ui.startServer.triggered.connect(lambda: threading.Thread(target=os.system, args=[f"nohup '{programPath}/key-get.py' &"]).start())
    ui.stopServer.triggered.connect(lambda: threading.Thread(target=os.system, args=[f"'{programPath}/stop.sh'"]).start())
    ui.setAutoStart.triggered.connect(lambda: threading.Thread(target=os.system, args=[f"pkexec '{programPath}/start-auto-server.sh'"]).start())
    ui.setUnautoStart.triggered.connect(lambda: threading.Thread(target=os.system, args=[f"pkexec '{programPath}/stop-auto-server.sh'"]).start())
    window.show()
    threading.Thread(target=Check.CheckThreading).start()
    Clear()
    sys.exit(app.exec_())