#!/usr/bin/env python3
import os
import sys
programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
sys.path.append(f"{programPath}/..")

import os
import sys
import dbus
import json
import threading
import traceback
from UI.KeyAddKeyboardGui import *
import PyQt5.QtWidgets as QtWidgets

keyList = ["无快捷键", "shift", "ctrl", "alt", "ctrl+alt", "ctrl+shift", "alt+shift"]
keyListDeepinMap = ["", "<Shift>", "<Control>", "<Alt>", "<Control><Alt>", "<Control><Shift>", "<Alt><Shift>"]
keyListDebianMap = [[], ["shift"], ["ctrl"], ["alt"], ["ctrl", "alt"], ["ctrl", "shift"], ["alt", "shift"]]

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

class Click:
    def LocalValueChange():
        ui.wineKeyboardChoose.setCurrentIndex(ui.localKeyboardChoose.currentIndex())

    def LocalKeyChange():
        ui.wineKey.setText(ui.localKey.text())

    def AddButton():
        # 完整性检测
        if ui.exeName.text() == "" or ui.localKey.text() == "" or ui.wineKey.text() == "":
            QtWidgets.QMessageBox.critical(window, "错误", "您的信息暂未填写完整")
            return
        if ui.localKey.text()[0] == " " or ui.wineKey.text()[0] == " ":
            QtWidgets.QMessageBox.critical(window, "错误", "映射快捷键的第一位不能为空格")
            return
        # Deepin/UOS 的情况
        if Check.VersionCheck():
            # 接入 dbus
            try:
                bus = dbus.SessionBus()
                bus.get_object("com.deepin.daemon.Keybinding", "/com/deepin/daemon/Keybinding").Add(
                    ui.exeName.text(), 
                    f"'{programPath}/sendkeys.sh' {ui.wineKey.text()[0]} '{ui.exeName.text()}' {ui.wineKeyboardChoose.currentIndex()}",
                    f"{keyListDeepinMap[ui.localKeyboardChoose.currentIndex()]}{ui.localKey.text()[0]}"
                )
                QtWidgets.QMessageBox.information(window, "提示", "添加成功！")
            except:
                traceback.print_exc()
                QtWidgets.QMessageBox.critical(window, "错误", traceback.format_exc())
            return
        keyboardList = []
        if os.path.exists(f"{programPath}/list/KeyList.json"):
            try:
                with open(f"{programPath}/list/KeyList.json") as file:
                    keyboardList = json.loads(file.read())
            except:
                traceback.print_exc()
                QtWidgets.QMessageBox.critical(window, "错误", traceback.format_exc())
                return
        print(keyboardList)
        addList = []
        addList = keyListDebianMap[ui.localKeyboardChoose.currentIndex()][:]
        print(keyListDebianMap)
        print(addList)
        addList.append(ui.localKey.text()[0])
        print(1, addList)
        addList.append(f"'{programPath}/sendkeys.sh' {ui.wineKey.text()[0]} '{ui.exeName.text()}' {ui.wineKeyboardChoose.currentIndex()}")
        print(2, addList)
        print(addList)
        try:
            keyboardList[int(sys.argv[1])] = addList
        except:
            keyboardList.append(addList)
        try:
            with open(f"{programPath}/list/KeyList.json", "w") as file:
                file.write(json.dumps(keyboardList))
            QtWidgets.QMessageBox.information(window, "提示", "添加成功！")
        except:
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(window, "错误", traceback.format_exc())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    # 添加选项
    ui.localKeyboardChoose.addItems(keyList)
    ui.wineKeyboardChoose.addItems(keyList)
    # 读取程序参数
    try:
        with open(f"{programPath}/list/KeyList.json") as file:
            keyboardList = json.loads(file.read())
        choice = keyboardList[int(sys.argv[1])]
        ui.localKeyboardChoose.setCurrentIndex(keyListDebianMap.index(choice[:-2]))
        ui.localKey.setText(choice[-2])
        # 解析命令
        command = choice[-1]
        # 筛掉路径
        command = command[command[1:].index("'") + 2:].strip()
        # 筛出其中一个快捷键
        ui.wineKey.setText(command[command.index(" ") - 1])
        command = command[command.index(" ") + 2:]
        # 读 exe
        ui.exeName.setText(command[:command.index("'")])
        command = command[command.index("'") + 1: ].strip()
        # 读最后的快捷键
        ui.wineKeyboardChoose.setCurrentIndex(int(command))
    except:
        pass
    # 连接槽
    ui.addButton.clicked.connect(Click.AddButton)
    ui.localKeyboardChoose.currentIndexChanged.connect(Click.LocalValueChange)
    ui.localKey.textChanged.connect(Click.LocalKeyChange)
    window.show()
    #threading.Thread(target=Check.CheckThreading).start()
    sys.exit(app.exec_())