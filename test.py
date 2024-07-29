import sys
import globalenv
import PyQt5.QtWidgets as QtWidgets
app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QMainWindow()
globalenv._init()
globalenv.set_value("app", app)
#import deepin_wine_packager
#modules = __import__("deepin-wine-packager")
modules = __import__("deepin-wine-easy-packager")
#import mainwindow
window.setCentralWidget(modules.window)
window.show()
app.exec_()