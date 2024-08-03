#   库的引用
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore

import sys

#   创建界面
class WinWelcome(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.mainLayout)

        #   标签1
        self.lab1 = QtWidgets.QLabel("欢迎使用Wine运行器！")
        self.lab1.setStyleSheet("font-size:20px")
        self.mainLayout.addWidget(self.lab1)

        #   文本栏
        self.txt = QtWidgets.QTextBrowser()
        self.introduction = "Wine运行器\n用于运行一般的Windows程序及安装包（exe、msi文件）\n\nWine打包器\n将特定的Windows程序打包为deb格式，以便存储或分享\n\n虚拟机\n可用于运行无法通过Wine运行的程序，或在龙架构上运行x86程序\n请注意，虚拟机可解决兼容性问题，但性能开销较大"
        self.txt.setText(self.introduction)
        self.mainLayout.addWidget(self.txt)
        
        #   标签2
        self.lab2 = QtWidgets.QLabel("请根据您的需求，在左下角打开相应页面")
        self.mainLayout.addWidget(self.lab2)

#   测试界面
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    winWelcome = WinWelcome()
    winWelcome.show()
    sys.exit(app.exec())