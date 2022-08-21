# 本来是用C++写的，但在非deepin/UOS编译/运行就是下载不了https文件，只能用python重写
import sys
import PyQt5.QtWidgets as QtWidgets

import mainwindowui

# 继承至界面文件的主窗口类
class MyMainWindow(mainwindowui.Ui_MainWindow):
    def __init__(self, parent=None):
        #pass
        super(MyMainWindow, self).__init__(parent)
        #self.setupUi(self)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    app.exec_()