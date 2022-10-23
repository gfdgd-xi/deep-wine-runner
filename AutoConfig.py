#!/usr/bin/env python3
# 使用系统默认的 python3 运行
###########################################################################################
# 作者：gfdgd xi、为什么您不喜欢熊出没和阿布呢
# 版本：2.1.0
# 更新时间：2022年08月25日
# 感谢：感谢 wine 以及 deepin-wine 团队，提供了 wine 和 deepin-wine 给大家使用，让我能做这个程序
# 基于 Python3 构建
###########################################################################################
#################
# 引入所需的库
#################
from fileinput import filename
import os
import sys
import json
import traceback
import req as requests
import PyQt5.QtWidgets as QtWidgets
from UI.AutoConfig import *
from Model import *

urlSources = "https://code.gitlink.org.cn/gfdgd_xi/wine-runner-list/raw/branch/master/auto"
lists = []
class ProgramRunStatusUpload():
    msgWindow = None
    starLayout = None
    fen = None
    starList = []
    sha1Value = ""
    programName = None
    def ChangeStar():
        if ProgramRunStatusUpload.fen.currentIndex() > 5:
            for i in ProgramRunStatusUpload.starList:
                i.setText(f"<img src='{programPath}/Icon/BadStar.svg' width=25>")
            return
        for i in range(ProgramRunStatusUpload.fen.currentIndex()):
            ProgramRunStatusUpload.starList[i].setText(f"<img src='{programPath}/Icon/Star.svg' width=25>")
        head = ProgramRunStatusUpload.fen.currentIndex() 
        end = len(ProgramRunStatusUpload.starList)
        for i in range(head, end):
            ProgramRunStatusUpload.starList[i].setText(f"<img src='{programPath}/Icon/UnStar.svg' width=25>")
        
    def ShowWindow(sha="", title=""):
        ProgramRunStatusUpload.starList = []
        ProgramRunStatusUpload.sha1Value = sha
        ProgramRunStatusUpload.msgWindow = QtWidgets.QMainWindow()
        msgWidget = QtWidgets.QWidget()
        msgWidgetLayout = QtWidgets.QGridLayout()
        ProgramRunStatusUpload.programName = QtWidgets.QLineEdit()
        ProgramRunStatusUpload.fen = QtWidgets.QComboBox()
        ProgramRunStatusUpload.starLayout = QtWidgets.QHBoxLayout()
        upload = QtWidgets.QPushButton(QtCore.QCoreApplication.translate("U", "上传"))
        upload.clicked.connect(ProgramRunStatusUpload.Upload)
        if title != "":
            ProgramRunStatusUpload.programName.setText(title)
            ProgramRunStatusUpload.programName.setDisabled(True)
        # 生成星星列表
        for i in [1, 1, 1, 1, 0]:
            ProgramRunStatusUpload.starList.append(QtWidgets.QLabel(f"<img src='{programPath}/Icon/{['Un', ''][i]}Star.svg' width=25>"))
            ProgramRunStatusUpload.starLayout.addWidget(ProgramRunStatusUpload.starList[-1])
        ProgramRunStatusUpload.starLayout.addItem(QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        ProgramRunStatusUpload.programName.setPlaceholderText(QtCore.QCoreApplication.translate("U", "如果这个程序和程序名确实是合法还是检测到敏感词，改为“NULL”即可"))
        ProgramRunStatusUpload.fen.addItems(["0分",
    "1分",
    "2分",
    "3分",
    "4分",
    "5分"])
        ProgramRunStatusUpload.fen.setCurrentIndex(4)
        ProgramRunStatusUpload.fen.currentIndexChanged.connect(ProgramRunStatusUpload.ChangeStar)
        msgWidgetLayout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("U", "程序名：")), 0, 0)
        msgWidgetLayout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("U", "评分：")), 1, 0)
        msgWidgetLayout.addWidget(ProgramRunStatusUpload.programName, 0, 1)
        msgWidgetLayout.addWidget(ProgramRunStatusUpload.fen, 1, 1)
        msgWidgetLayout.addLayout(ProgramRunStatusUpload.starLayout, 2, 1)
        msgWidgetLayout.addWidget(upload, 3, 1)
        msgWidget.setLayout(msgWidgetLayout)
        ProgramRunStatusUpload.msgWindow.setCentralWidget(msgWidget)
        ProgramRunStatusUpload.msgWindow.setWindowTitle(QtCore.QCoreApplication.translate("U", "上传程序运行情况"))
        ProgramRunStatusUpload.msgWindow.setWindowIcon(QtGui.QIcon(iconPath))
        ProgramRunStatusUpload.msgWindow.show()

    def Upload():
        try:
            #if ProgramRunStatusUpload.sha1Value == "":
                #ProgramRunStatusUpload.sha1Value = ProgramRunStatusUpload.GetSHA1(e2.currentText())
            QtWidgets.QMessageBox.information(None, QtCore.QCoreApplication.translate("U", "提示"), json.loads(requests.post("http://120.25.153.144:30250/bash", {
            "BashName": ProgramRunStatusUpload.programName.text(),
            "Fen": ProgramRunStatusUpload.fen.currentIndex()
            }).text)["Error"])
        except:
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(None, QtCore.QCoreApplication.translate("U", "错误"), QtCore.QCoreApplication.translate("U", "数据上传失败！"))

class ProgramRunStatusShow():
    msgWindow = None
    def ShowWindow():
        global lists
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
        try:
            fenlists = requests.get(f"http://120.25.153.144/spark-deepin-wine-runner/bashapp/{fileName}/all.json").json()
            #r = requests.get(base64.b64decode("aHR0cDovLzEyMC4yNS4xNTMuMTQ0L3NwYXJrLWRlZXBpbi13aW5lLXJ1bm5lci9hcHAv").decode("utf-8") + sha + base64.b64decode("L3RpdGxlLnR4dA==").decode("utf-8"))
            #r.encoding = "utf-8"
            #title = r.text
            tipsInfo = ""
        except:
            #traceback.print_exc()
            fenlists = [0, 0, 0, 0, 0]
            tipsInfo = "暂时无人提交此脚本运行情况，是否立即提交？"
            
        maxHead = fenlists.index(max(fenlists))
        ProgramRunStatusShow.msgWindow = QtWidgets.QMainWindow()
        msgWidget = QtWidgets.QWidget()
        msgWidgetLayout = QtWidgets.QGridLayout()
        starLayout = QtWidgets.QHBoxLayout()
        uploadButton = QtWidgets.QPushButton(QtCore.QCoreApplication.translate("U", "点此上传运行情况"))
        uploadButton.clicked.connect(lambda: ProgramRunStatusUpload.ShowWindow(fileName, fileName))
        msgWidgetLayout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("U", "综合评价：")), 0, 0)
        msgWidgetLayout.addLayout(starLayout, 0, 1)
        msgWidgetLayout.addWidget(QtWidgets.QLabel(tipsInfo), 1, 0, 1, 2)
        #msgWidgetLayout.addWidget(QtWidgets.QLabel("" if dateVersion == "" else f"数据版本：{dateVersion}"), 2, 0, 1, 2)
        msgWidgetLayout.addWidget(uploadButton, 3, 0, 1, 2)
        end = 5
        if maxHead > 5:
            for i in range(end):
                starLayout.addWidget(QtWidgets.QLabel(f"<img src='{programPath}/Icon/BadStar.svg' width=50>"))
        else:
            for i in range(maxHead):
                starLayout.addWidget(QtWidgets.QLabel(f"<img src='{programPath}/Icon/Star.svg' width=50>"))
            head = maxHead
            for i in range(head, end):
                starLayout.addWidget(QtWidgets.QLabel(f"<img src='{programPath}/Icon/UnStar.svg' width=50>"))
        msgWidget.setLayout(msgWidgetLayout)
        ProgramRunStatusShow.msgWindow.setCentralWidget(msgWidget)
        ProgramRunStatusShow.msgWindow.setWindowIcon(QtGui.QIcon(iconPath))
        #ProgramRunStatusShow.msgWindow.setWindowTitle(f"应用“{title}”的运行情况")
        ProgramRunStatusShow.msgWindow.show()

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
    ui.setupUi(window)
    window.setWindowTitle(f"Wine 运行器 {version}——容器自动配置部署脚本")
    window.setWindowIcon(QtGui.QIcon(f"{programPath}/deepin-wine-runner.svg"))
    iconPath = "{}/deepin-wine-runner.svg".format(programPath)
    window.show()
    # 连接信号和槽
    ui.saerchBotton.clicked.connect(Connect.SearchBotton_Clicked)
    ui.runBotton.clicked.connect(Connect.RunBotton_Clicked)
    ui.openFile.triggered.connect(Connect.OpenFile_Triggered)
    ui.exitProgram.triggered.connect(window.close)
    ui.getFen.clicked.connect(ProgramRunStatusShow.ShowWindow)
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