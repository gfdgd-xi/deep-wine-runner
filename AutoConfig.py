#!/usr/bin/env python3
import os
import sys
import json
import traceback
import requests
import PyQt5.QtWidgets as QtWidgets
from UI.AutoConfig import *

urlSources = "https://code.gitlink.org.cn/gfdgd_xi/wine-runner-list/raw/branch/master/auto"
lists = []

class Connect:
    def SearchBotton_Clicked():
        nmodel = QtGui.QStandardItemModel(window)
        if ui.searchThings.text() == "":
            # 显示全部内容
            for i in lists:
                nmodel.appendRow(QtGui.QStandardItem(i[0]))
            ui.searchList.setModel(nmodel)
            return
        for i in lists:
            # 显示筛选的内容
            if ui.searchThings.text() in i[0]:
                nmodel.appendRow(QtGui.QStandardItem(i[0]))
        ui.searchList.setModel(nmodel)

    def RunBotton_Clicked():
        # 获取选中项
        try:
            choose = ui.searchList.selectionModel().selectedIndexes()[0].data()
        except:
            QtWidgets.QMessageBox.critical(window, "错误", "您未选择任何配置文件")
            return
        fileName = ""
        for i in lists:
            print(i)
            if i[0] == choose:
                fileName = i[1]
                break
        # 下载脚本
        try:
            print(f"{urlSources}/{fileName}")
            file = open("/tmp/wine-runner-auto-config.wsh", "w")
            file.write(requests.get(f"{urlSources}/{fileName}").text)
            file.close()
        except:
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(window, "错误", "无法获取配置文件")
            return
        # 执行脚本
        process = QtCore.QProcess()
        process.start(f"{programPath}/launch.sh", ["deepin-terminal", "-e", "env", "WINE=deepin-wine6-stable", "WINEPREFIX=/home/gfdgd_xi/.deepinwine", f"{programPath}/ConfigLanguareRunner.py", "/tmp/wine-runner-auto-config.wsh"])
        process.waitForFinished()
        


if __name__ == "__main__":
    programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    window.show()
    # 连接信号和槽
    ui.saerchBotton.clicked.connect(Connect.SearchBotton_Clicked)
    ui.runBotton.clicked.connect(Connect.RunBotton_Clicked)
    # 解析云列表
    try:
        # 获取列表
        lists = json.loads(requests.get(f"{urlSources}/list.json").text)
        # 解释列表并显示在 GUI 上
        nmodel = QtGui.QStandardItemModel(window)
        for i in lists:
            nmodel.appendRow(QtGui.QStandardItem(i[0]))
        ui.searchList.setModel(nmodel)
    except:
        traceback.print_exc()
        QtWidgets.QMessageBox.critical(window, "提示", "无法连接服务器")
    app.exec_()