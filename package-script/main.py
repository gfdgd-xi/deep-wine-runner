#!/usr/bin/env python3
# 使用系统默认的 python3 运行
###########################################################################################
# 作者：gfdgd xi、为什么您不喜欢熊出没和阿布呢
# 版本：1.6.1
# 更新时间：2022年07月14日
# 感谢：感谢 wine 以及 deepin-wine 团队，提供了 wine 和 deepin-wine 给大家使用，让我能做这个程序
# 基于 Python3 的 tkinter 构建
###########################################################################################
#################
# 引入所需的库
#################
import os
import json
import easygui
import ttkthemes
import subprocess
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox

###################
# 程序所需事件
###################
# 读取文本文档
def readtxt(path):
    f = open(path, "r") # 设置文件对象
    str = f.read()  # 获取内容
    f.close()  # 关闭文本对象
    return str  # 返回结果

# 获取用户主目录
def get_home():
    return os.path.expanduser('~')

# 写入文本文档
def WriteTXT(path, things):
    file = open(path, 'w', encoding='UTF-8')  # 设置文件对象
    file.write(things)  # 写入文本
    file.close()  # 关闭文本对象

def DisbledOrEnabled(choose: bool):
    state = [tk.NORMAL, tk.DISABLED]
    choose = int(choose)
    e1.config(state=state[choose])
    e2.config(state=state[choose])
    e3.config(state=state[choose])
    e4.config(state=state[choose])
    e5.config(state=state[choose])
    e6.config(state=state[choose])
    e7.config(state=state[choose])
    buildDeb.config(state=state[choose])


def PackageDeb():
    DisbledOrEnabled(True)
    for i in windowFrameInputValueList:
        if i.get() == "":
            tkinter.messagebox.showinfo(title="提示", message="您未填完所有信息，无法继续")
            return
    startupWMClassName = os.path.basename(exePath.get().replace("\\", "/"))
    print(startupWMClassName)
    WriteTXT(f"{programPath}/package-hshw.sh", f"""#!/bin/bash

#最终生成的包的描述
export app_description="{debDescription.get()}"
#应用程序英文名
export app_name="{englishName.get()}"
#应用程序中文名
export app_name_zh_cn="{chineseName.get()}"
#desktop文件中的分类
export desktop_file_categories="{typeName.get()};"
#desktop文件中StartupWMClass字段。用于让桌面组件将窗口类名与desktop文件相对应。这个值为实际运行的主程序EXE的文件名，wine/crossover在程序运行后会将文件名设置为窗口类名
export desktop_file_main_exe="{startupWMClassName}"
export exec_path="{exePath.get()}"
#最终生成的包的包名,包名的命名规则以deepin开头，加官网域名（需要前后对调位置），如还不能区分再加上应用名
export deb_package_name="{packageName.get()}"
#最终生成的包的版本号，版本号命名规则：应用版本号+deepin+数字
export deb_version_string="{versionName.get()}"

export package_depends="deepin-wine6-stable:amd64 (>= 6.0.0.12-1), deepin-wine-helper (>= 5.1.25-1)"
export apprun_cmd="deepin-wine6-stable"
#export package_depends="deepin-wine5-stable:amd64 (>= 5.0.29-1), deepin-wine-helper (>= 5.1.25-1)"
#export apprun_cmd="deepin-wine5-stable"

# rm -fr final.dir/
# rm -fr icons/
# rm -fr staging.dir/

./script-packager.sh $@
""")
    os.chdir(programPath)
    RunCommand(f"./package-hshw.sh")
    DisbledOrEnabled(False)

def RunCommand(command):
    res = subprocess.Popen([command], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # 清空文本框内容
    commandReturn.config(state=tk.NORMAL)
    commandReturn.delete(1.0, "end")
    commandReturn.config(state=tk.DISABLED)
    # 实时读取程序返回
    while res.poll() is None:
        commandReturn.config(state=tk.NORMAL)
        try:
            text = res.stdout.readline().decode("utf8")
        except:
            text = ""
        commandReturn.insert("end", text)
        print(text, end="")
        commandReturn.config(state=tk.DISABLED)

def ShowHelp():
    easygui.textbox(title="帮助", msg="下面是有关打包器的各个输入框的意义以及有关的 UOS 填写标准", text=tips)

def OpenPackageFolder():
    os.system(f"xdg-open '{programPath}/package_save/uos'")

###########################
# 程序信息
###########################
programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
information = json.loads(readtxt(f"{programPath}/information.json"))
version = information["Version"]
iconPath = "{}/icon.png".format(programPath)
tips = """第一个文本框是应用程序中文名
第二个文本框是应用程序英文名
第三个文本框是最终生成的包的描述
第四个选择框是desktop文件中的分类
第五个输入框是程序在 Wine 容器的位置，以 c:\\XXX 的形式，盘符必须小写，用反斜杠，如果路径带用户名的话会自动替换为$USER
而 StartupWMClass 字段将会由程序自动生成，作用如下：
desktop文件中StartupWMClass字段。用于让桌面组件将窗口类名与desktop文件相对应。这个值为实际运行的主程序EXE的文件名，wine/crossover在程序运行后会将文件名设置为窗口类名
第六个输入框是最终生成的包的包名,包名的命名规则以deepin开头，加官网域名（需要前后对调位置），如还不能区分再加上应用名
最后一个是最终生成的包的版本号，版本号命名规则：应用版本号+deepin+数字
"""

###########################
# 窗口创建
###########################
# 读取主题
try:
    theme = not ("dark" in readtxt(get_home() + "/.gtkrc-2.0") and "gtk-theme-name=" in readtxt(get_home() + "/.gtkrc-2.0"))
except:
    print("主题读取错误，默认使用浅色主题")
    theme = True
if theme:
    win = tk.Tk()
    themes = ttkthemes.ThemedStyle(win)
    themes.set_theme("breeze")
else:
    import ttkbootstrap
    style = ttkbootstrap.Style(theme="darkly")
    win = style.master  # 创建窗口

# 变量声明
chineseName = tk.StringVar()
englishName = tk.StringVar()
debDescription = tk.StringVar()
typeName = tk.StringVar()
exePath = tk.StringVar()
packageName = tk.StringVar()
versionName = tk.StringVar()
commandReturn = tk.Text()
typeName.set("Network")
windowFrameInputValueList = [
    chineseName,
    englishName,
    debDescription,
    typeName,
    exePath,
    packageName,
    versionName
]
# Line 1
ttk.Label(win, text="程序中文名：").grid(row=0, column=0)
e1 = ttk.Entry(win, textvariable=chineseName, width=100)
e1.grid(row=0, column=1)
# Line 2
ttk.Label(win, text="程序英文名：").grid(row=1, column=0)
e2 = ttk.Entry(win, textvariable=englishName, width=100)
e2.grid(row=1, column=1)
# Line 3
ttk.Label(win, text="包描述：").grid(row=2, column=0)
e3 = ttk.Entry(win, textvariable=debDescription, width=100)
e3.grid(row=2, column=1)
# Line 4
ttk.Label(win, text="程序分类").grid(row=3, column=0)
e4 = ttk.OptionMenu(win, typeName, "Network", "Network", "Chat", "Audio", "Video", "Graphics", "Office", "Translation", "Development", "Utility", "System")
e4.grid(row=3, column=1)
# Line 5
ttk.Label(win, text="程序在 Wine 容器的位置").grid(row=4, column=0)
e5 = ttk.Entry(win, textvariable=exePath, width=100)
e5.grid(row=4, column=1)
# Line 6
ttk.Label(win, text="包名：").grid(row=5, column=0)
e6 = ttk.Entry(win, textvariable=packageName, width=100)
e6.grid(row=5, column=1)
# Line 7
ttk.Label(win, text="版本号：").grid(row=6, column=0)
e7 = ttk.Entry(win, textvariable=versionName, width=100)
e7.grid(row=6, column=1)
# Line 8
controlFrame = ttk.Frame(win)
buildDeb = ttk.Button(controlFrame, text="打包", command=PackageDeb)
debPath = ttk.Button(controlFrame, text="deb 包生成目录", command=OpenPackageFolder)
buildDeb.grid(row=0, column=1)
debPath.grid(row=0, column=0)
controlFrame.grid(row=7, column=0, columnspan=2)
# Line 9
commandReturn = tk.Text(win, width=100, height=5)
commandReturn.grid(row=8, column=0, columnspan=2)
# Menu
menu = tk.Menu()
programMenu = tk.Menu()
menu.add_cascade(label="程序", menu=programMenu)
programMenu.add_command(label="退出", command=win.destroy)

menu.add_command(label="帮助", command=ShowHelp)


# 设置控件
win.config(menu=menu)
win.iconphoto(False, tk.PhotoImage(file=iconPath))
win.title(f"Wine 打包器 {version}——基于统信 Wine 生态活动打包脚本制作")
commandReturn.config(state=tk.DISABLED)

win.mainloop()