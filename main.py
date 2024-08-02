#   库的引用
import os
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
import importlib
import sys

class RunnerWindow:
    programPath = os.path.split(os.path.realpath(__file__))[0]  # 获取当前程序目录
    import globalenv
    recycleTime = 0
    def __init__(self, app: QtWidgets.QApplication, moduleName: str) -> None:
        self.globalenv._init()  # globalenv 的 init 是必须的，这样才能正确的 import Wine 运行器的窗口
        self.globalenv.set_value("app", app)   # 用于将该部分的 app 给子模块的 Qt 控件调用以解决 UI 异常以及其它问题
        # 因为 Python 有不允许重复 import 的特性从而导致多次返回的控件实际指向同一对象，所以要通过特殊的方式绕过这一限制
        # 将使用指向程序所在文件夹的超链接以改变库名称从而实现每次引入时命名控件不同
        # 通过嵌套多个 local.local.local 以解决问题
        # 同理可以利用该特性使用 globalenv 传值
        if (not os.path.exists(f"{self.programPath}/local")):
            # 没有存在该超链接，不启用该机制
            self.globalenv.set_value("app", app)
            self.mainwindow = __import__(moduleName, fromlist=["mainwindow"])
            return
        while True:
            self.recycleTime += 1
            testModuleName = "local." * self.recycleTime + moduleName
            if (not testModuleName in sys.modules):
                self.mainwindow = __import__(testModuleName, fromlist=["mainwindow"])  # 设置 fromlist 就不会返回最上层节点，及 local
                break
    
    def Win(self) -> QtWidgets.QMainWindow:
        # 输出窗口
        return self.mainwindow.window
           

#   创建界面
class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.counter_a = 1
        self.counter_b = 1
        self.counter_c = 1
        self.widgetList = list()
        self.initUI()

    def initUI(self):
        self.setMinimumSize(800, 600)
        self.setWindowTitle("增减测试")
        self.mainLayout = QtWidgets.QHBoxLayout()
        self.setLayout(self.mainLayout)

        #   左侧区域
        self.leftWidget = LeftWidget()
        self.mainLayout.addWidget(self.leftWidget)

        self.leftWidget.btn1.clicked.connect(self.addA)
        self.leftWidget.btn2.clicked.connect(self.addB)
        self.leftWidget.btn3.clicked.connect(self.addC)
        self.leftWidget.btn4.clicked.connect(self.delCurrent)
        self.leftWidget.list1.itemClicked.connect(self.switchWidget)

        #   右侧区域
        self.rightWidget = RightWidget()
        self.mainLayout.addWidget(self.rightWidget)

    #   新增a类界面
    def addA(self):
        self.newTab = "a类页面#{0}".format(self.counter_a)
        self.counter_a += 1
        self.leftWidget.list1.addItem(self.newTab)

        self.newWidget = RunnerWindow(app, "mainwindow").Win()
        print(self.newWidget)
        self.widgetList.append(self.newWidget)
        self.rightWidget.addWidget(self.newWidget)

    #   新增b类界面
    def addB(self):
        self.newTab = "b类页面#{0}".format(self.counter_b)
        self.counter_b += 1
        self.leftWidget.list1.addItem(self.newTab)

        self.newWidget = RunnerWindow(app, "deepin-wine-packager").Win()
        self.widgetList.append(self.newWidget)
        self.rightWidget.addWidget(self.newWidget)

    #   新增c类界面
    def addC(self):
        self.newTab = "c类页面#{0}".format(self.counter_c)
        self.counter_c += 1
        self.leftWidget.list1.addItem(self.newTab)
        self.newWidget = RunnerWindow(app, "VM.mainwindow").Win()
        self.widgetList.append(self.newWidget)
        self.rightWidget.addWidget(self.newWidget)

    #   删除_本页面
    def delCurrent(self):
        self.row = self.leftWidget.list1.currentRow()
        self.leftWidget.list1.takeItem(self.row)
        self.rightWidget.removeWidget(self.widgetList[self.row])

    #   切换页面
    def switchWidget(self):
        self.row = self.leftWidget.list1.currentRow()
        self.rightWidget.setCurrentIndex(self.row)

#   左侧区域
class LeftWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setFixedWidth(100)
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)

        #   左侧标题
        self.lab1 = QtWidgets.QLabel("页面导航区")
        self.mainLayout.addWidget(self.lab1)

        #   左侧页面列表
        self.list1 = QtWidgets.QListWidget()
        self.mainLayout.addWidget(self.list1)

        #   新增a类按钮
        self.btn1 = QtWidgets.QPushButton("新增a类界面")
        self.mainLayout.addWidget(self.btn1)

        #   新增b类按钮
        self.btn2 = QtWidgets.QPushButton("新增b类界面")
        self.mainLayout.addWidget(self.btn2)

        #   新增c类按钮
        self.btn3 = QtWidgets.QPushButton("新增c类界面")
        self.mainLayout.addWidget(self.btn3)

        #   删_页面按钮
        self.btn4 = QtWidgets.QPushButton("删除_本页面")
        self.mainLayout.addWidget(self.btn4)

#   右侧区域
class RightWidget(QtWidgets.QStackedWidget):
    def __init__(self):
        super().__init__()
        #self.initUI()

    #def initUI(self):

#   运行程序
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = Window()
    mainWindow.show()
    sys.exit(app.exec())