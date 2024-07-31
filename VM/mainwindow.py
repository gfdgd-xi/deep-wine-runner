import sys
import ui_mainwindow
import PyQt5.QtWidgets as QtWidgets

app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QMainWindow()
ui = ui_mainwindow.Ui_MainWindow()
ui.setupUi(window)
window.show()
sys.exit(app.exec_())