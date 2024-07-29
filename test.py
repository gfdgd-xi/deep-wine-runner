import sys
import globalenv
import PyQt5.QtWidgets as QtWidgets
app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QMainWindow()
globalenv._init()
globalenv.set_value("app", app)

import mainwindow
window.setCentralWidget(mainwindow.window)
window.show()
app.exec_()