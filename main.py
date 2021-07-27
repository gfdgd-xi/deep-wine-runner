#!/usr/bin/env python3
# 使用系统默认的 python3 运行
###########################################################################################
# 作者：gfdgd xi
# 版本：1.3.2
# 更新时间：2021年07月27日
# 感谢：感谢 wine 以及 deepin-wine 团队，提供了 wine 和 deepin-wine 给大家使用，让我能做这个程序
# 基于 Python3 的 tkinter 构建
###########################################################################################
#################
# 引入所需的库
#################
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog
import tkinter.messagebox
import os
import sys
import time
import json
import shutil
import threading
import webbrowser

###################
# 程序所需事件
###################

# 打开程序官网
def OpenProgramURL():
    webbrowser.open_new_tab(programUrl)

# 读取文本文档
def readtxt(path):
    f = open(path, "r") # 设置文件对象
    str = f.read()  # 获取内容
    f.close()  # 关闭文本对象
    return str  # 返回结果

# 写入文本文档
def write_txt(path, things):
    file = open(path, 'w', encoding='UTF-8')  # 设置文件对象
    file.write(things)  # 写入文本
    file.close()  # 关闭文本对象

# 获取用户桌面目录
def get_desktop_path():
    for line in open(get_home() + "/.config/user-dirs.dirs"):  # 以行来读取配置文件
        desktop_index = line.find("XDG_DESKTOP_DIR=\"")  # 寻找是否有对应项，有返回 0，没有返回 -1
        if desktop_index != -1:  # 如果有对应项
            break  # 结束循环
    if desktop_index == -1:  # 如果是提前结束，值一定≠-1，如果是没有提前结束，值一定＝-1
        return -1
    else:
        get = line[17:-2]  # 截取桌面目录路径
        get_index = get.find("$HOME")  # 寻找是否有对应的项，需要替换内容
        if get != -1:  # 如果有
            get = get.replace("$HOME", get_home())  # 则把其替换为用户目录（～）
        return get  # 返回目录

# 获取用户主目录
def get_home():
    return os.path.expanduser('~')

# 第一个浏览按钮事件
def liulanbutton():
    
    path = tkinter.filedialog.askdirectory(title="选择 wine 容器", initialdir=json.loads(readtxt(get_home() + "/.config/deepin-wine-runner/WineBotton.json"))["path"])
    if path != "" and path != "()":
        e1.set(path)
        write_txt(get_home() + "/.config/deepin-wine-runner/WineBotton.json", json.dumps({"path": path}))  # 写入配置文件

# 第二个浏览按钮事件
def liulanexebutton():
    path = tkinter.filedialog.askopenfilename(title="选择 exe 可执行文件", filetypes=[("exe 可执行文件", "*.exe"), ("EXE 可执行文件", "*.EXE"), ("所有文件", "*.*")], initialdir=json.loads(readtxt(get_home() + "/.config/deepin-wine-runner/FindExe.json"))["path"])
    if path != "" and path != "()":
        e2.set(path)  # 显示路径
        write_txt(get_home() + "/.config/deepin-wine-runner/FindExe.json", json.dumps({"path": os.path.dirname(path)}))  # 写入配置文件
        

# 使用多线程运行可执行文件
def runexebutton():
    run = threading.Thread(target=runexebutton_threading)
    run.start()

def DisableButton(things):
    a = {True: tk.DISABLED, False: tk.NORMAL}
    button1.configure(state=a[things])
    button2.configure(state=a[things])
    button3.configure(state=a[things])
    e1.configure(state=a[things])
    e2.configure(state=a[things])
    o1.configure(state=a[things])

# 运行可执行文件的线程
def runexebutton_threading():
    DisableButton(True)
    if e1.get() == "" or e2.get() == "":  # 判断文本框是否有内容
        tkinter.messagebox.showinfo(title="提示", message="没有填写需要使用的 wine 容器或需要运行的 exe 应用")
    else:  # 如果都有
        os.system("WINEPREFIX='" + e1.get() + "' " + wine[o1_text.get()] + " '" + e2.get() + "'")  # 运行
    findExeHistory.append(e1.get())  # 将记录写进数组
    wineBottonHistory.append(e2.get())  # 将记录写进数组
    print(ListToDictionary(findExeHistory))
    write_txt(get_home() + "/.config/deepin-wine-runner/FindExeHistory.json", str(json.dumps(ListToDictionary(findExeHistory))))  # 将历史记录的数组转换为字典并写入
    write_txt(get_home() + "/.config/deepin-wine-runner/WineBottonHistory.json", str(json.dumps(ListToDictionary(wineBottonHistory))))  # 将历史记录的数组转换为字典并写入
    e1['value'] = findExeHistory
    e2['value'] = wineBottonHistory
    DisableButton(False)

# 显示“关于这个程序”窗口
def about_this_program():
    global about
    tkinter.messagebox.showinfo(title="关于这个程序", message=about)

# 显示“提示”窗口
def helps():
    global tips
    tkinter.messagebox.showinfo(title="提示", message=tips)

# 显示更新内容窗口
def UpdateThings():
    tkinter.messagebox.showinfo(title="更新内容", message=updateThings)

# 生成 shell 文件在桌面
# （第四个按钮的事件）
def make_desktop_on_desktop():
    if combobox1.get() == "" or e2.get() == "" or e1.get() == "":  # 判断文本框是否有内容
        tkinter.messagebox.showinfo(title="提示", message="没有填写需要使用的 wine 容器或需要运行的 exe 应用或保存的文件名")
    else:  # 如果都有
        if os.path.exists(get_desktop_path() + "/" + combobox1.get() + ".sh"): # 判断目录是否有该文件，如果有
            choose = tkinter.messagebox.askokcancel(title="提示", message="文件已经存在，是否覆盖？")  # 询问用户是否覆盖
            if choose:   # 如要覆盖
                os.remove(get_desktop_path() + "/" + combobox1.get() + ".sh")  # 删除该文件
            else:  # 如不覆盖
                return  # 结束
        os.mknod(get_desktop_path() + "/" + combobox1.get() + ".sh")  # 创建文本文档
        write_txt(get_desktop_path() + "/" + combobox1.get() + ".sh", "#!/bin/bash\n" + "WINEPREFIX='" + e1.get() + "' " + wine[o1_text.get()] + " '" + e2.get() + "'") # 写入文本文档
        os.system("chmod 777 '" + get_desktop_path() + "/" + combobox1.get() + ".sh" + "'")  # 赋予可执行权限
        shellHistory.append(combobox1.get())  # 将记录写进数组
        write_txt(get_home() + "/.config/deepin-wine-runner/ShellHistory.json", str(json.dumps(ListToDictionary(shellHistory))))  # 将历史记录的数组转换为字典并写入
        combobox1['value'] = shellHistory
        tkinter.messagebox.showinfo(title="提示", message="生成完成！")  # 显示完成对话框

# 数组转字典
def ListToDictionary(list):
    dictionary = {}
    for i in range(len(list)):
        dictionary[i] = list[i]
    return dictionary

def CleanProgramHistory():
    if tkinter.messagebox.askokcancel(title="警告", message="删除后将无法恢复，你确定吗？\n删除后软件将会自动重启。"):
        shutil.rmtree(get_home() + "/.config/deepin-wine-runner")
        ReStartProgram()

# 重启本应用程序
def ReStartProgram():
    python = sys.executable
    os.execl(python, python, * sys.argv)



###########################
# 加载配置
###########################
if not os.path.exists(get_home() + "/.config/deepin-wine-runner"):  # 如果没有配置文件夹
    os.mkdir(get_home() + "/.config/deepin-wine-runner")  # 创建配置文件夹
if not os.path.exists(get_home() + "/.config/deepin-wine-runner/ShellHistory.json"):  # 如果没有配置文件
    write_txt(get_home() + "/.config/deepin-wine-runner/ShellHistory.json", json.dumps({}))  # 创建配置文件
if not os.path.exists(get_home() + "/.config/deepin-wine-runner/FindExeHistory.json"):  # 如果没有配置文件
    write_txt(get_home() + "/.config/deepin-wine-runner/FindExeHistory.json", json.dumps({}))  # 创建配置文件
if not os.path.exists(get_home() + "/.config/deepin-wine-runner/WineBottonHistory.json"):  # 如果没有配置文件
    write_txt(get_home() + "/.config/deepin-wine-runner/WineBottonHistory.json", json.dumps({}))  # 创建配置文件
if not os.path.exists(get_home() + "/.config/deepin-wine-runner/FindExe.json"):  # 如果没有配置文件
    write_txt(get_home() + "/.config/deepin-wine-runner/FindExe.json", json.dumps({"path": "~"}))  # 写入（创建）一个配置文件
if not os.path.exists(get_home() + "/.config/deepin-wine-runner/WineBotton.json"):  # 如果没有配置文件
    write_txt(get_home() + "/.config/deepin-wine-runner/WineBotton.json", json.dumps({"path": "~/.deepinwine"}))  # 写入（创建）一个配置文件

###########################
# 设置变量
###########################
# 如果要添加其他 wine，请在字典添加其名称和执行路径
# 在数组添加其名称
wineName = ["deepin-wine", "deepin-wine","deepin-wine5", "wine", "wine64", "deepin-wine5 stable", "deepin-wine6 stable 32 位"]
wine = {"deepin-wine": "deepin-wine", "deepin-wine5": "deepin-wine5", "wine": "wine", "wine64": "wine64", "deepin-wine5 stable": "deepin-wine5-stable", "deepin-wine6 stable": "deepin-wine6-stable"}
shellHistory = list(json.loads(readtxt(get_home() + "/.config/deepin-wine-runner/ShellHistory.json")).values())
findExeHistory = list(json.loads(readtxt(get_home() + "/.config/deepin-wine-runner/FindExeHistory.json")).values())
wineBottonHistory = list(json.loads(readtxt(get_home() + "/.config/deepin-wine-runner/WineBottonHistory.json")).values())


###########################
# 程序信息
###########################
programUrl = "https://gitee.com/gfdgd-xi/deep-wine-runner"
version = "1.3.2"
goodRunSystem = "Linux"
about = '''一个基于 Python3 的 tkinter 制作的 wine 运行器
版本：{}
适用平台：{}
tkinter 版本：{}
程序官网：{}
©2020-{} gfdgd xi'''.format(version, goodRunSystem, tk.TkVersion, programUrl, time.strftime("%Y"))
tips = '''提示：
1、使用终端运行该程序，可以看到 wine 以及程序本身的提示和报错
2、wine 32 位和 64 位的容器互不兼容'''
updateThingsString = '''1、修改了 wine 选项的说明和 wine 的启动方式'''
title = "wine 运行器 {}".format(version)
updateTime = "2021年07月27日"
updateThings = "{} 更新内容：\n{}\n更新时间：{}".format(version, updateThingsString, updateTime, time.strftime("%Y"))


###########################
# 窗口创建
###########################
window = tk.Tk()  # 创建窗口
window.title(title)  # 设置标题
# 设置变量以修改和获取值项
o1_text = tk.StringVar()
combobox1 = tk.StringVar()
o1_text.set("deepin-wine")
# 创建控件
button1 = ttk.Button(window, text="浏览", command=liulanbutton)  # 创建按钮控件
button2 = ttk.Button(window, text="浏览", command=liulanexebutton)  # 创建按钮控件
button3 = ttk.Button(window, text="启动", command=runexebutton)  # 创建按钮控件
button5 = ttk.Button(window, text="创建用于运行的 shell 文件到桌面", command=make_desktop_on_desktop)  # 创建按钮控件
label1 = ttk.Label(window, text="选择你想要使用的 wine 容器：")  # 创建标签控件
label2 = ttk.Label(window, text="选择要启动的 Windows 应用")  # 创建标签控件
label3 = ttk.Label(window, text="选择要使用的 wine 版本")  # 创建标签控件
label4 = ttk.Label(window, text="设置文件名，以便把上方填写的信息写入到 shell 文件里")  # 创建标签控件
e1 = ttk.Combobox(window, width=100)  # 创建文本框控件
e2 = ttk.Combobox(window, width=100)  # 创建文本框控件
combobox1 = ttk.Combobox(window, width=100)
o1 = ttk.OptionMenu(window, o1_text, *wineName)  # 创建选择框控件
menu = tk.Menu(window)  # 设置菜单栏
programmenu = tk.Menu(menu, tearoff=0)  # 设置“程序”菜单栏
menu.add_cascade(label="程序", menu=programmenu)
programmenu.add_command(label="清空软件历史记录", command=CleanProgramHistory)
programmenu.add_separator()  # 设置分界线
programmenu.add_command(label="退出程序", command=window.quit)  # 设置“退出程序”项
help = tk.Menu(menu, tearoff=0)  # 设置“帮助”菜单栏
menu.add_cascade(label="帮助", menu=help)
help.add_command(label="程序官网", command=OpenProgramURL)  # 设置“程序官网”项
help.add_separator()
help.add_command(label="小提示", command=helps)  # 设置“小提示”项
help.add_command(label="更新内容", command=UpdateThings)  # 设置“更新内容”项
help.add_command(label="关于这个程序", command=about_this_program)  # 设置“关于这个程序”项
# 设置控件
e1['value'] = findExeHistory
e2['value'] = wineBottonHistory
combobox1['value'] = shellHistory
# 添加控件
window.config(menu=menu)  # 显示菜单栏
label1.grid(row=0, column=0)
label2.grid(row=1, column=0)
label3.grid(row=2, column=0)
label4.grid(row=4, column=0)
e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
#combobox1.grid(row=4, column=1)
combobox1.grid(row=4, column=1)
button1.grid(row=0, column=2)
button2.grid(row=1, column=2)
button3.grid(row=3, column=0, columnspan=3)
button5.grid(row=5, column=0, columnspan=3)
o1.grid(row=2, column=1)
# 启动窗口
window.mainloop()
