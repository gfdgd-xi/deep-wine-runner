#!/usr/bin/env python3
# 读取设置单独用一个 py 文件
import os
import json
import base64
import shutil
import getpass
import datetime
import traceback
import subprocess
import PyQt5.QtGui as QtGui

# 获取用户主目录
def get_home():
    return os.path.expanduser('~')

# 读取文本文档
def readtxt(path):
    f = open(path, "r") # 设置文件对象
    str = f.read()  # 获取内容
    f.close()  # 关闭文本对象
    return str  # 返回结果

defultProgramList = {
    "Architecture": "Auto",
    "Debug": True,
    "DefultWine": "deepin-wine8-stable",
    "DefultBotton" : get_home() + "/.wine",
    "TerminalOpen": False,
    "WineOption": "",
    "WineBottonDifferent": False,
    "CenterWindow": False,
    "Theme": "",
    "MonoGeckoInstaller": False,
    "AutoWine": True,
    "RuntimeCache": True,
    "MustRead": False,
    "BuildByBottleName": False,
    "AutoPath": False,
    "QemuUnMountHome": False,
    "Chinese": True,
    "FontSize": 1
}

programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
try:
    setting = json.loads(readtxt(get_home() + "/.config/deepin-wine-runner/WineSetting.json"))
    information = json.loads(readtxt(f"{programPath}/information.json"))
except:
    setting = defultProgramList

def SetFont(app):
    defaultFont = app.font()
    size = setting["FontSize"]
    font = QtGui.QFont(defaultFont)
    if size == 1:
        app.setFont(defaultFont)    
        return
    font.setPixelSize(int(defaultFont.pixelSize() / size))
    font.setPointSize(int(defaultFont.pointSize() / size))
    app.setFont(font)

def getFileFolderSize(fileOrFolderPath):
    """get size for file or folder"""
    totalSize = 0
    try:
        if not os.path.exists(fileOrFolderPath):
            return totalSize
        if os.path.isfile(fileOrFolderPath):
            totalSize = os.path.getsize(fileOrFolderPath)  # 5041481
            return totalSize
        if os.path.islink(fileOrFolderPath):
            return 0
        if os.path.isdir(fileOrFolderPath):
            with os.scandir(fileOrFolderPath) as dirEntryList:
                for curSubEntry in dirEntryList:
                    curSubEntryFullPath = os.path.join(fileOrFolderPath, curSubEntry.name)
                    if curSubEntry.is_dir():
                        curSubFolderSize = getFileFolderSize(curSubEntryFullPath)  # 5800007
                        totalSize += curSubFolderSize
                    elif curSubEntry.is_file():
                        curSubFileSize = os.path.getsize(curSubEntryFullPath)  # 1891
                        totalSize += curSubFileSize
                return totalSize
    except:
        return totalSize

def FileToBase64(filePath):
    src = ""
    with open(filePath, "rb") as f:
        base64Byte = base64.b64encode(f.read())
        src += base64Byte.decode("utf-8")
    return src

class SaveLog():
    userName = getpass.getuser()
    time = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    kernelVersion = subprocess.getoutput("uname -a")
    wineRunnerVersion = information["Version"]
    architecture = subprocess.getoutput("arch")
    cpuInfo = subprocess.getoutput("lscpu")
    lsmod = subprocess.getoutput("lsmod")
    lshw = subprocess.getoutput("lshw")
    cpu = subprocess.getoutput("cat /proc/cpuinfo | grep 'model name' | head -n 1 | awk -F: '{print $2}'")
    gpu = subprocess.getoutput("lspci | grep -i 'VGA\|3D\|2D'")
    

    def __init__(self, chooseWineName, chooseWineCommand, runCommand, binPath, logOut, description, imgPath=[]) -> None:
        self.chooseWineName = chooseWineName
        self.chooseWineCommand = chooseWineCommand
        self.runCommand = runCommand
        self.binPath = binPath
        self.logOut = logOut
        self.description = description
        self.imgPath = imgPath
        # 读取可执行文件信息
        if os.path.exists(binPath):
            try:
                self.binSize = f"{str(int(getFileFolderSize(binPath) / 1024 / 1024))}MB"
            except:
                self.binSize = "Error"
                traceback.print_exc()
            os.system(f"'{programPath}/wrestool' '{binPath}' -x -t 14 > '/tmp/wine-runner-log-icon.png'")
            # 如果提取成功
            if os.path.exists("/tmp/wine-runner-log-icon.png"):
                # 转换成 base64 编码
                self.binIcon = "data:image/jpg;base64," + FileToBase64("/tmp/wine-runner-log-icon.png")
                self.binIconPath = "/tmp/wine-runner-log-icon.png"
            else:
                self.binIcon = "Not Found"
                self.binIconPath = "Not Found"
        else:
            self.binSize = "Not Found"
            self.binIcon = "Not Found"
            self.binIconPath = "Not Found"
        try:
            self.memoryInfo = readtxt("/proc/meminfo")
        except:
            traceback.print_exc()
            self.memoryInfo = traceback.format_exc()

    def To7z(self, savePath):
        os.system("rm -rfv /tmp/wine-runner-log")
        os.system("mkdir -v /tmp/wine-runner-log")
        self.ToHtml("/tmp/wine-runner-log/index.html", toZip=True)
        shutil.copy(self.binIconPath, f"/tmp/wine-runner-log/{os.path.basename(self.binIconPath)}")
        lists = ["wine-runner-log-icon.png", "index.html"]
        for i in self.imgPath:
            name = os.path.basename(i)
            if os.path.basename(i) in lists:
                while name in lists:
                    name = os.path.splitext(name)[0] + "-copy" + os.path.splitext(name)[1]
                lists.append(name)
            else:
                lists.append(name)
            shutil.copy(i, f"/tmp/wine-runner-log/{name}")
        os.system(f"7z a '{savePath}' /tmp/wine-runner-log")


    def ToHtml(self, savePath, toZip=False):
        print(self.userName, self.time)
        # 对文本进行处理
        description = ""
        logOut = ""
        cpuInfo = ""
        memoryInfo = ""
        imgPath = ""
        lsmod = ""
        lshw = ""
        for i in self.description.splitlines():
            description += f'<span class="line code">{i}</span>\n'
        for i in self.logOut.splitlines():
            logOut += f'<span class="line code">{i}</span>\n'
        for i in self.cpuInfo.splitlines():
            cpuInfo += f'<span class="line code">{i}</span>\n'
        for i in self.memoryInfo.splitlines():
            memoryInfo += f'<span class="line code">{i}</span>\n'
        for i in self.lsmod.splitlines():
            lsmod += f'<span class="line code">{i}</span>\n'
        for i in self.lshw.splitlines():
            lshw += f'<span class="line code">{i}</span>\n'
        text = readtxt(f"{programPath}/Resources/LogTemplate/template.html")
        if toZip:
            binIcon = os.path.basename(self.binIconPath)
            # 重名排除
            lists = ["wine-runner-log-icon.png", "index.html"]
            for i in self.imgPath:
                name = os.path.basename(i)
                if os.path.basename(i) in lists:
                    while name in lists:
                        name = os.path.splitext(name)[0] + "-copy" + os.path.splitext(name)[1]
                    lists.append(name)
                else:
                    lists.append(name)
                imgPath += f'<p align="center"><img src="{name}" class="imgShow"></p>\n'
        else:
            binIcon = self.binIcon
            for i in self.imgPath:
                try:
                    path = "data:image/jpg;base64," + FileToBase64(i)
                except:
                    traceback.print_exc()
                    path = "Error"
                imgPath += f'   <p align="center"><img src="{path}" class="imgShow"></p>\n'

        replaceMap = {
            "%UserName%": self.userName,
            "%Time%": self.time,
            "%KernelVersion": self.kernelVersion,
            "%ChooseWineName%": self.chooseWineName,
            "%ChooseWineCommand%": self.chooseWineCommand,
            "%RunCommand%": self.runCommand,
            "%BinPath%": self.binPath,
            "%WineRunnerVersion%": self.wineRunnerVersion,
            "%BinSize%": self.binSize,
            "%BinIcon%": binIcon,
            "%CPUInfo%": cpuInfo,
            "%Architecture%": self.architecture,
            "%MemoryInfo%": memoryInfo,
            "%LogOut%": logOut,
            "%Description%": description,
            "%ImgPath%": imgPath,
            "%Lsmod%": lsmod,
            "%Lshw%": lshw,
            "%CPU%": self.cpu,
            "%GPU%": self.gpu
        }
        for i in replaceMap.keys():
            text = text.replace(i, replaceMap[i])
        with open(savePath, "w") as file:
            file.write(text)




SaveLog("a", "b", "c", "/opt/apps/deepin-wine-runner/geek.exe", "e", "f", ["/tmp/wine-runner-log/wine-runner-log-icon.png"]).To7z("/tmp/a.7z")