# 用于实现窗口模块化的组件和调用封装
import os
import sys
import PyQt5.QtWidgets as QtWidgets

moduleNameList = {
    "mainwindow": {
        "Name": "运行器",
        "RepeatShow": False
    },
    "deepin-wine-easy-packager": {
        "Name": "简易打包器",
        "RepeatShow": False
    },
    "deepin-wine-packager": {
        "Name": "专业打包器",
        "RepeatShow": False
    },
    "VM.mainwindow": {
        "Name": "虚拟机管理工具",
        "RepeatShow": True
    },
    "VM.show-vm": {
        "Name": "虚拟机连接工具（VNC）",
        "RepeatShow": True
    },
    "wine.installwine": {
        "Name": "Wine 安装工具",
        "RepeatShow": True
    },
}

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