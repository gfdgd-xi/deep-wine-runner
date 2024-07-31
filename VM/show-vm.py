#!/usr/bin/env python3
import os
import sys
import time
import random
import requests
import threading
import webbrowser
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
sys.path.append(f"{programPath}/../")
sys.path.append(f"{programPath}/")
import globalenv

# 尝试引入 QtWebEngine
isWebengineInstalled = False
try:
    from PyQt5.QtWebEngineWidgets import *
    isWebengineInstalled = True
except:
    pass

def CheckService():
    pass

class NoVNCService(QThread):
    serviceStop = pyqtSignal()
    def run(self):
        os.system(f"'{programPath}/novnc/utils/novnc_proxy' --listen localhost:6789 --vnc localhost:5905 --file-only")
        # 显示关闭服务
        self.serviceStop.emit()
        pass

class CheckConnect(QThread):
    connected = pyqtSignal()
    def run(self):
        while True:
            time.sleep(0.5)
            try:
                requests.get("http://localhost:6789/vnc.html", timeout=0.5)
                self.connected.emit()
                break
            except:
                pass

def ShowVNCShower():
    global webEngine
    if (isWebengineInstalled):
        webEngine = QWebEngineView(window)
        webEngine.settings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
        webEngine.setUrl(QUrl("http://localhost:6789/vnc.html"))
        window.setCentralWidget(webEngine)
        return
    webEngine = QPushButton("点击使用浏览器打开连接页")
    webEngine.clicked.connect(lambda: webbrowser.open_new_tab("http://localhost:6789/vnc.html"))
    window.setCentralWidget(webEngine)

def ShowRestartButton():
    # 显示重启服务按钮
    RestartServiceButtonInit()
    window.setCentralWidget(restartServiceButton)

def RunService():
    global vnc
    global socket
    # 设置加载文本
    LoadingLabelInit()
    window.setCentralWidget(loadingLabel)
    socket = CheckConnect()
    vnc = NoVNCService()
    vnc.serviceStop.connect(ShowRestartButton)
    socket.connected.connect(ShowVNCShower)
    socket.start()
    try:
        # 如果服务已经启用，则不重复启用
        requests.get("http://localhost:6789/vnc.html", timeout=0.5)
    except:
        vnc.start()
    
def LoadingLabelInit():
    global loadingLabel
    loadingLabel = QLabel("加载中...")
    window.setCentralWidget(loadingLabel)

def RestartServiceButtonInit():
    global restartServiceButton
    restartServiceButton = QPushButton("重启服务")
    restartServiceButton.clicked.connect(RunService)

# 尝试启动服务
if (__name__ == "__main__"):
    app = QApplication(sys.argv)
else:
    app = globalenv.get_value("app")
    
window = QMainWindow()
LoadingLabelInit()
RunService()
window.setWindowTitle("虚拟机连接")
window.show()
if (__name__ == "__main__"):
    window.resize(int(window.frameGeometry().width() * 5),
                  int(window.frameGeometry().height() * 5))
    sys.exit(app.exec_())