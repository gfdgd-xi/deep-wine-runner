#!/usr/bin/env python3
# 使用系统默认的 python3 运行
###########################################################################################
# 作者：gfdgd xi
# 版本：2.4.0
# 更新时间：2022年10月25日
# 感谢：感谢 wine 以及 deepin-wine 团队，提供了 wine 和 deepin-wine 给大家使用，让我能做这个程序
# 基于 Python3 构建
###########################################################################################
#################
# 引入所需的库
#################
import os
import sys
import base64
import json
import traceback
import updatekiller
import urllib.request
import req as requests
import PyQt5.QtWidgets as QtWidgets
from UI.AutoConfig import *
from Model import *
try:
    import PyQt5.QtWebEngineWidgets as QtWebEngineWidgets
    webeng = True
except:
    print("未安装此依赖库")
    webeng = False

urlSourcesList = [
    "http://www.gfdgdxi.top/deep-wine-runner-auto-configuration-script/",  # Github 源
    "https://gitee.com/gfdgd-xi/deep-wine-runner-auto-configuration-script/raw/master/",  # Gitee 源
    "https://code.gitlink.org.cn/gfdgd_xi/wine-runner-list/raw/branch/master/auto",  # Gitlink 源
    "http://gfdgdxi.msns.cn/wine-runner-list/auto/",  # 备用源1，纯 IPv6 源
    "http://gfdgdxi.free.idcfengye.com/deep-wine-runner-auto-configuration-script/",  # 备用源2
    "http://gfdgdxi.free.idcfengye.com/wine-runner-list/auto/",  # 备用源 3
    "http://127.0.0.1/wine-runner-list/auto/"  # 本地测试源
]
urlSources = urlSourcesList[0]
lists = []



all = 0
now = 0


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
            if ui.searchThings.text().upper() in i[0].upper():
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
        things = ""
        try:
            print(f"{urlSources}/{fileName}")
            file = open("/tmp/wine-runner-auto-config.wsh", "w")
            things = requests.get(f"{urlSources}/{fileName}").text
            file.write(things)
            file.close()
        except:
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(window, "错误", "无法获取配置文件")
            return
        # 判断版本以启动对应的解释器
        # 做到新旧兼容
        if "($" in things:
            print("a")
            OpenTerminal(f"env WINE='{wine}' WINEPREFIX='{wineprefix}' '{programPath}/ConfigLanguareRunner.py' '/tmp/wine-runner-auto-config.wsh' --system")
        # 执行脚本
        print(f"env WINE='{wine}' WINEPREFIX='{wineprefix}' '{programPath}/AutoShell/main.py' '/tmp/wine-runner-auto-config.wsh'")
        OpenTerminal(f"env WINE='{wine}' WINEPREFIX='{wineprefix}' '{programPath}/AutoShell/main.py' '/tmp/wine-runner-auto-config.wsh'")
        #process = QtCore.QProcess()
        #process.start(f"{programPath}/launch.sh", ["deepin-terminal", "-e", "env", f"WINE={wine}", f"WINEPREFIX={wineprefix}", f"{programPath}/ConfigLanguareRunner.py", "/tmp/wine-runner-auto-config.wsh", "--system"])
        #process.waitForFinished()
        
    def OpenFile_Triggered():
        path = QtWidgets.QFileDialog.getOpenFileName(window, "提示", homePath, "配置文件(*.sh *.wsh);;全部文件(*.*)")
        if path[0] == "":
            return
        try:
            things = ""
            with open(path) as file:
                things = file.read()
        except:
            traceback.print_exc()
        # 判断版本以启动对应的解释器
        # 做到新旧兼容
        if "($" in things:
            OpenTerminal(f"env WINE='{wine}' WINEPREFIX='{wineprefix}' '{programPath}/ConfigLanguareRunner.py' '{path[0]}' --system")
        # 执行脚本
        OpenTerminal(f"env WINEARCH='{os.getenv('WINEARCH')}' WINEDEBUG='{os.getenv('WINEDEBUG')}' WINE='{wine}' WINEPREFIX='{wineprefix}' '{programPath}/AutoShell/main.py' '{path[0]}'")
        #process = QtCore.QProcess()
        #process.start(f"{programPath}/launch.sh", ["deepin-terminal", "-e", "env", f"WINE={wine}", f"WINEPREFIX={wineprefix}", f"{programPath}/ConfigLanguareRunner.py", path[0], "--system"])
        #process.waitForFinished()

# 读取文本文档
def readtxt(path):
    f = open(path, "r") # 设置文件对象
    str = f.read()  # 获取内容
    f.close()  # 关闭文本对象
    return str  # 返回结果

def ChangeSources():
    global urlSources
    sources = [ui.actionGitee, ui.actionGithub, ui.actionGitlink, ui.action_IPv6, ui.action_2, ui.action_3, ui.action]
    for i in range(0, len(sources)):
        if sources[i].isChecked():
            urlSources = urlSourcesList[i]
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
            break

if __name__ == "__main__":
    homePath = os.path.expanduser('~')
    programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
    information = json.loads(readtxt(f"{programPath}/information.json"))
    version = information["Version"]
    wine = "deepin-wine6-stable"
    wineprefix = f"{homePath}/.wine"
    try:
        wine = sys.argv[1]
        wineprefix = sys.argv[2]
    except:
        pass
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    pinLunLayout = QtWidgets.QHBoxLayout()
    ui.setupUi(window)
    window.setWindowTitle(f"Wine 运行器 {version}——容器自动配置部署脚本")
    window.setWindowIcon(QtGui.QIcon(f"{programPath}/deepin-wine-runner.svg"))
    iconPath = "{}/deepin-wine-runner.svg".format(programPath)
    window.show()
    #ui.actionGitlink.setExclusive(True)
    sourcesGroup = QtWidgets.QActionGroup(window)
    
    sourcesGroup.addAction(ui.actionGitee)
    sourcesGroup.addAction(ui.actionGithub)
    sourcesGroup.addAction(ui.actionGitlink)
    sourcesGroup.addAction(ui.action_IPv6)
    sourcesGroup.addAction(ui.action_2)
    sourcesGroup.addAction(ui.action_3)
    sourcesGroup.addAction(ui.action)
    sourcesGroup.triggered.connect(ChangeSources)
    sourcesGroup.setExclusive(True)
    #for i in [ui.actionGitlink, ui.actionGitee, ui.actionGithub, ui.action_IPv6, ui.action]:
        #i.triggered.connect(ChangeSources)
        #pass
    # 连接信号和槽
    ui.saerchBotton.clicked.connect(Connect.SearchBotton_Clicked)
    #ui.uploadFen.clicked.connect(UploadFen)
    ui.runBotton.clicked.connect(Connect.RunBotton_Clicked)
    ui.openFile.triggered.connect(Connect.OpenFile_Triggered)
    ui.exitProgram.triggered.connect(window.close)
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