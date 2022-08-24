import os
import PyQt5.QtCore as QtCore
shell = """# “#”后面代表注释
# 可以为了方便观看改为 bash 的高亮模式
# 安装 dll
installdll 0
installdll 1
# 安装字体
installfont 0    # 后面参数填 Wine 运行器的字体安装器提示的编号
# 安装字体（安装星火应用商店的微软核心字体）
installsparkcorefont 
# 安装 Mono
installmono
# 安装 gecko
installgecko
# 安装 vcpp
installvcpp         0    # 后面参数填 Wine 运行器的 VCPP 安装器提示的编号
# 安装 .net
installnet       # 后面参数填 Wine 运行器的 VCPP 安装器提示的编号
# 安装 MSXML
installmsxml     # 后面参数填 Wine 运行器的 MSXML 安装器提示的编号
#aaaaa
"""

class Command():
    # 可以被使用的命令
    commandList = [
        "installdll",
        "installfont",
        "installsparkcorefont",
        "installmono",
        "installgecko",
        "installvcpp",
        "installnet",
        "installmsxml"
    ]
    def __init__(self, commandString: str) -> None:
        self.commandString = commandString

    # 解析器
    # 命令字符串转可供解析的列表
    def GetCommandList(self) -> list:
        shellList = []
        shellFirstShell = self.commandString.split("\n")
        # 转换成可以执行的数组
        for l in range(0, len(shellFirstShell)):
            i = shellFirstShell[l]
            # 判断有没有注释
            if "#" in i:
                # 忽略注释
                i = i[:i.index("#")]
            # 删除前后空格
            i = i.strip()
            # 如果是空行
            if i == "":
                # 忽略此行，此行不做处理
                continue
            # 解析
            i = i.split()
            # 判断是否为合法的参数，否则提示并忽略
            if not i[0] in self.commandList:
                print(f"行{l + 1}命令{i[0]}不存在，忽略")
                continue
            shellList.append(i)
        return shellList

    # 运行器
    class Run():
        programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
        def InstallDll(self) -> int:
            import InstallDll
            return InstallDll.Download(self.wineBottonPath, InstallDll.GetNameByNumber(int(self.command[1])), InstallDll.GetUrlByNumber(int(self.command[1])))

        def InstallFont(self) -> int:
            pass
        
        def InstallMono(self) -> int:
            return os.system(f"ENTERNOTSHOW=0 '{self.programPath}/InstallMono.py' '{self.wineBottonPath}' '{self.wine}' mono")

        def InstallGecko(self) -> int:
            return os.system(f"ENTERNOTSHOW=0 '{self.programPath}/InstallMono.py' '{self.wineBottonPath}' '{self.wine}' gecko")

        def InstallVCPP(self) -> int:
            pass

        def InstallNet(self) -> int:
            pass

        def InstallMsxml(self) -> int:
            pass

        def InstallSparkCoreFont(self):
            pass

        # 可以运行的命令的映射关系
        # 可以被使用的命令的映射
        commandList = {
            "installdll": InstallDll,
            "installfont": InstallFont,
            "installsparkcorefont": InstallSparkCoreFont,
            "installmono": InstallMono,
            "installgecko": InstallGecko,
            "installvcpp": InstallVCPP,
            "installnet": InstallNet,
            "installmsxml": InstallMsxml
        }
        # 解析
        def __init__(self, command: list, wineBottonPath: str, wine: str) -> int:
            self.wineBottonPath = wineBottonPath
            self.wine = wine
            for i in command:
                self.command = i
                self.commandList[i[0]](self)
        

com = Command(shell)
com.Run(com.GetCommandList(), "/home/gfdgd_xi/.wine", "deepin-wine6-stable")