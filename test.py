import os
import sys
import globalenv
import PyQt5.QtWidgets as QtWidgets
app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QMainWindow()
# globalenv 的 init 是必须的，这样才能正确的 import Wine 运行器的窗口
globalenv._init()
globalenv.set_value("app", app)  # 用于将该部分的 app 给子模块的 Qt 控件调用以解决 UI 异常以及其它问题
#import deepin_wine_packager
#modules = __import__("deepin-wine-packager")
#modules = __import__("deepin-wine-easy-packager")  
#import mainwindow
# 使用 __import__ 可以引入带 - 文件名的模块
import wine.installwine
window.setCentralWidget(wine.installwine.window)
window.show()
app.exec_()