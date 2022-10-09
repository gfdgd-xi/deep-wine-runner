#!/usr/bin/env python3
import os
import sys
import traceback
programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
sys.path.append(f"{programPath}/..")

import dbus
import threading
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


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    # 连接槽
    ui.addButton.clicked.connect(Click.AddButton)
    ui.localKeyboardChoose.currentIndexChanged.connect(Click.LocalValueChange)
    ui.localKey.textChanged.connect(Click.LocalKeyChange)
    window.show()
    # 添加选项
    ui.localKeyboardChoose.addItems(keyList)
    ui.wineKeyboardChoose.addItems(keyList)
    #threading.Thread(target=Check.CheckThreading).start()
    sys.exit(app.exec_())