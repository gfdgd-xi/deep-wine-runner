#!/usr/bin/env python3
import os
import sys
import base64
import traceback
import req as requests
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets

class ProgramRunStatusShow():
    msgWindow = None
    def ShowWindow():
        try:
            #fenlists = requests.get(base64.b64decode("aHR0cDovLzEyMC4yNS4xNTMuMTQ0L3NwYXJrLWRlZXBpbi13aW5lLXJ1bm5lci9iYXNoYXBwLw==").decode("utf-8") + fileName + base64.b64decode("L2FsbC5qc29u").decode("utf-8")).json()
            fenlists = []
            for i in range(6):
                fenlists.append(int(requests.get(base64.b64decode("aHR0cDovLzEyMC4yNS4xNTMuMTQ0L3NwYXJrLWRlZXBpbi13aW5lLXJ1bm5lci9GZW4=").decode("utf-8") + f"{i}/data.txt").text))
            tipsInfo = ""
        except:
            traceback.print_exc()
            fenlists = [0, 0, 0, 0, 0]
            tipsInfo = "暂时无人提交此脚本运行情况，是否立即提交？"
            
        maxHead = fenlists.index(max(fenlists))
        allNumber = 0
        for i in fenlists:
            allNumber += i
        try:
            tipsInfo = ""
            for i in range(len(fenlists)):
                tipsInfo += f"有 {fenlists[i] / allNumber * 100}% 的用户选择了 {i} 分（{fenlists[i]}/{allNumber}）\n"
            maxNumber = max(fenlists) / allNumber * 100
            #if tipsInfo == "":
            #    tipsInfo = f"有{maxNumber}%的用户选择了这个评分"
        except:
            pass
        ProgramRunStatusShow.msgWindow = QtWidgets.QMainWindow()
        msgWidget = QtWidgets.QWidget()
        msgWidgetLayout = QtWidgets.QGridLayout()
        starLayout = QtWidgets.QHBoxLayout()
        uploadButton = QtWidgets.QPushButton(QtCore.QCoreApplication.translate("U", "点此上传运行情况"))
        uploadButton.clicked.connect(ProgramRunStatusUpload.ShowWindow)
        msgWidgetLayout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("U", "综合评价：")), 0, 0)
        msgWidgetLayout.addLayout(starLayout, 0, 1)
        msgWidgetLayout.addWidget(QtWidgets.QLabel(tipsInfo), 1, 0, 1, 2)
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
        ProgramRunStatusShow.msgWindow.setWindowTitle(f"程序运行情况")
        ProgramRunStatusShow.msgWindow.show()

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
        
    def ShowWindow():
        ProgramRunStatusUpload.starList = []
        ProgramRunStatusUpload.msgWindow = QtWidgets.QMainWindow(ProgramRunStatusShow.msgWindow)
        msgWidget = QtWidgets.QWidget()
        msgWidgetLayout = QtWidgets.QGridLayout()
        ProgramRunStatusUpload.fen = QtWidgets.QComboBox()
        ProgramRunStatusUpload.starLayout = QtWidgets.QHBoxLayout()
        upload = QtWidgets.QPushButton(QtCore.QCoreApplication.translate("U", "上传"))
        upload.clicked.connect(ProgramRunStatusUpload.Upload)
        # 生成星星列表
        for i in [1, 1, 1, 1, 1]:
            ProgramRunStatusUpload.starList.append(QtWidgets.QLabel(f"<img src='{programPath}/Icon/{['Un', ''][i]}Star.svg' width=25>"))
            ProgramRunStatusUpload.starLayout.addWidget(ProgramRunStatusUpload.starList[-1])
        ProgramRunStatusUpload.starLayout.addItem(QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        ProgramRunStatusUpload.fen.addItems(["0分", "1分", "2分", "3分", "4分", "5分"])
        ProgramRunStatusUpload.fen.setCurrentIndex(5)
        ProgramRunStatusUpload.fen.currentIndexChanged.connect(ProgramRunStatusUpload.ChangeStar)
        msgWidgetLayout.addWidget(QtWidgets.QLabel(QtCore.QCoreApplication.translate("U", "评分：")), 1, 0)
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
            QtWidgets.QMessageBox.information(ProgramRunStatusUpload.msgWindow, QtCore.QCoreApplication.translate("U", "提示"), requests.get(f"http://120.25.153.144/spark-deepin-wine-runner/Install.php?Version=Fen{ProgramRunStatusUpload.fen.currentIndex()}").json()["Error"])
        except:
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(ProgramRunStatusUpload.msgWindow, QtCore.QCoreApplication.translate("U", "错误"), QtCore.QCoreApplication.translate("U", "数据上传失败！"))

if __name__ == "__main__":
    programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
    iconPath = "{}/deepin-wine-runner.svg".format(programPath)
    app = QtWidgets.QApplication(sys.argv)
    ProgramRunStatusShow.ShowWindow()
    app.exec_()
