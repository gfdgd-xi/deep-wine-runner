#!/usr/bin/env python3
import sys
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtWebEngineWidgets as QtWebEngineWidgets



app = QtWidgets.QApplication(sys.argv)
web = QtWebEngineWidgets.QWebEngineView()
#web.urlChanged.connect()
web.loadFinished.connect(lambda: exit())
web.setUrl(QtCore.QUrl("http://120.25.153.144/spark-deepin-wine-runner/open/Install.php?Version=a"))
#web.show()
app.exec_()
