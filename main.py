#!/usr/bin/env python3
# 使用系统默认的 python3 运行
###########################################################################################
# 作者：gfdgd xi、为什么您不喜欢熊出没和阿布呢
# 版本：1.5.2
# 更新时间：2022年07月05日
# 感谢：感谢 wine 以及 deepin-wine 团队，提供了 wine 和 deepin-wine 给大家使用，让我能做这个程序
# 基于 Python3 的 tkinter 构建
###########################################################################################
#################
# 引入所需的库
#################
import os
import sys
import time
import json
import shutil
import threading
import ttkthemes
import webbrowser
import subprocess
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog
import tkinter.messagebox
import PIL.Image as Image
import PIL.ImageTk as ImageTk

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
    wineConfig.configure(state=a[things])
    e1.configure(state=a[things])
    e2.configure(state=a[things])
    o1.configure(state=a[things])
    winetricksOpen.configure(state=a[things])
    getProgramIcon.configure(state=a[things])
    uninstallProgram.configure(state=a[things])

# 运行可执行文件的线程
def runexebutton_threading():
    DisableButton(True)
    if e2.get() == "":  # 判断文本框是否有内容
        tkinter.messagebox.showinfo(title="提示", message="没有填写需要使用的 exe 应用")
        DisableButton(False)
        return
    else:  # 如果都有
        if e1.get() == "":
            wineBottonPath = get_home() + "/.wine"
        else:
            wineBottonPath = e1.get()
        res = subprocess.Popen(["WINEPREFIX='" + wineBottonPath + "' " + wine[o1_text.get()] + " '" + e2.get() + "'"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # 清空文本框内容
        returnText.config(state=tk.NORMAL)
        returnText.delete(1.0, "end")
        returnText.config(state=tk.DISABLED)
        # 实时读取程序返回
        while res.poll() is None:
            returnText.config(state=tk.NORMAL)
            try:
                text = res.stdout.readline().decode("utf8")
            except:
                text = ""
            returnText.insert("end", text)
            print(text)
            returnText.config(state=tk.DISABLED)
    findExeHistory.append(wineBottonPath)  # 将记录写进数组
    wineBottonHistory.append(e2.get())  # 将记录写进数组
    write_txt(get_home() + "/.config/deepin-wine-runner/FindExeHistory.json", str(json.dumps(ListToDictionary(findExeHistory))))  # 将历史记录的数组转换为字典并写入
    write_txt(get_home() + "/.config/deepin-wine-runner/WineBottonHistory.json", str(json.dumps(ListToDictionary(wineBottonHistory))))  # 将历史记录的数组转换为字典并写入
    e1['value'] = findExeHistory
    e2['value'] = wineBottonHistory
    DisableButton(False)

# 显示“关于这个程序”窗口
def about_this_program()->"显示“关于这个程序”窗口":
    global about
    global title
    global iconPath
    mess = tk.Toplevel()
    message = ttk.Frame(mess)
    mess.resizable(0, 0)
    mess.title("关于 {}".format(title))
    mess.iconphoto(False, tk.PhotoImage(file=iconPath))
    img = ImageTk.PhotoImage(Image.open(iconPath))
    label1 = ttk.Label(message, image=img)
    label2 = ttk.Label(message, text=about)
    button1 = ttk.Button(message, text="确定", command=mess.withdraw)
    label1.pack()
    label2.pack()
    button1.pack(side="bottom")
    message.pack()
    mess.mainloop()

# 显示“提示”窗口
def helps():
    global tips
    tkinter.messagebox.showinfo(title="提示", message=tips)

# 显示更新内容窗口
def UpdateThings():
    tkinter.messagebox.showinfo(title="更新内容", message=updateThings)

# 生成 desktop 文件在启动器
def make_desktop_on_launcher():
    if combobox1.get() == "" or e2.get() == "":  # 判断文本框是否有内容
        tkinter.messagebox.showinfo(title="提示", message="没有填写需要使用 exe 应用或保存的文件名")
    else:  # 如果都有
        if os.path.exists(get_home() + "/.local/share/applications/" + combobox1.get() + ".desktop"): # 判断目录是否有该文件，如果有
            choose = tkinter.messagebox.askokcancel(title="提示", message="文件已经存在，是否覆盖？")  # 询问用户是否覆盖
            if choose:   # 如要覆盖
                os.remove(get_home() + "/.local/share/applications/" + combobox1.get() + ".desktop")  # 删除该文件
            else:  # 如不覆盖
                return  # 结束
        if e1.get() == "":
            wineBottonPath = get_home() + "/.wine"
        else:
            wineBottonPath = e1.get()
        write_txt(get_home() + "/.local/share/applications/" + combobox1.get() + ".desktop", f'''[Desktop Entry]
Name={combobox1.get()}
Exec=env WINEPREFIX='{wineBottonPath}' {wine[o1_text.get()]} '{e2.get()}'
Icon={iconPath}
Type=Application
StartupNotify=true''') # 写入文本文档
        shellHistory.append(combobox1.get())  # 将记录写进数组
        write_txt(get_home() + "/.config/deepin-wine-runner/ShellHistory.json", str(json.dumps(ListToDictionary(shellHistory))))  # 将历史记录的数组转换为字典并写入
        combobox1['value'] = shellHistory
        tkinter.messagebox.showinfo(title="提示", message="生成完成！")  # 显示完成对话框

# 生成 desktop 文件在桌面
# （第四个按钮的事件）
def make_desktop_on_desktop():
    if combobox1.get() == "" or e2.get() == "":  # 判断文本框是否有内容
        tkinter.messagebox.showinfo(title="提示", message="没有填写需要使用的 exe 应用或保存的文件名")
    else:  # 如果都有
        if os.path.exists(get_desktop_path() + "/" + combobox1.get() + ".desktop"): # 判断目录是否有该文件，如果有
            choose = tkinter.messagebox.askokcancel(title="提示", message="文件已经存在，是否覆盖？")  # 询问用户是否覆盖
            if choose:   # 如要覆盖
                os.remove(get_desktop_path() + "/" + combobox1.get() + ".desktop")  # 删除该文件
            else:  # 如不覆盖
                return  # 结束
        if e1.get() == "":
            wineBottonPath = get_home() + "/.wine"
        else:
            wineBottonPath = e1.get()
        os.mknod(get_desktop_path() + "/" + combobox1.get() + ".desktop")
        write_txt(get_desktop_path() + "/" + combobox1.get() + ".desktop", f'''[Desktop Entry]
Name={combobox1.get()}
Exec=env WINEPREFIX='{wineBottonPath}' {wine[o1_text.get()]} '{e2.get()}'
Icon={iconPath}
Type=Application
StartupNotify=true''') # 写入文本文档
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

def KillProgram():
    os.system(f"killall {wine[o1_text.get()]} -9")
    os.system("killall winedbg -9")

def InstallWine():
    threading.Thread(target=os.system, args=[f"'{programPath}/launch.sh' deepin-terminal -e \"{programPath}/AllInstall.py\""]).start()

def OpenWineBotton():
    if e1.get() == "":
        wineBottonPath = get_home() + "/.wine"
    else:
        wineBottonPath = e1.get()
    os.system("xdg-open \"" + wineBottonPath.replace("\'", "\\\'") + "\"")

def OpenWineFontPath():
    if e1.get() == "":
        wineBottonPath = get_home() + "/.wine"
    else:
        wineBottonPath = e1.get()
    tkinter.messagebox.showinfo(title="提示", message="如果安装字体？只需要把字体文件复制到此字体目录\n按下“OK”按钮可以打开字体目录")
    os.system("xdg-open \"" + wineBottonPath.replace("\'", "\\\'") + "/drive_c/windows/Fonts\"")

def UninstallProgram():
    threading.Thread(target=UninstallProgram_threading).start()

def UninstallProgram_threading():
    threading.Thread(target=RunWineProgram, args=[programPath + "/geek.exe"]).start()

def ConfigWineBotton():
    threading.Thread(target=RunWineProgram, args=["winecfg"]).start()

def RunWineProgram(wineProgram, history = False):
    DisableButton(True)
    if e1.get() == "":
        wineBottonPath = get_home() + "/.wine"
    else:
        wineBottonPath = e1.get()
    print("WINEPREFIX='" + wineBottonPath + "' " + wine[o1_text.get()] + " '" + wineProgram + "'")
    res = subprocess.Popen(["WINEPREFIX='" + wineBottonPath + "' " + wine[o1_text.get()] + " '" + wineProgram + "'"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # 清空文本框内容
    returnText.config(state=tk.NORMAL)
    returnText.delete(1.0, "end")
    returnText.config(state=tk.DISABLED)
    # 实时读取程序返回
    while res.poll() is None:
        returnText.config(state=tk.NORMAL)
        try:
            text = res.stdout.readline().decode("utf8")
        except:
            text = ""
        returnText.insert("end", text)
        print(text)
        returnText.config(state=tk.DISABLED)
    if history:
        findExeHistory.append(wineBottonPath)  # 将记录写进数组
        wineBottonHistory.append(e2.get())  # 将记录写进数组
        write_txt(get_home() + "/.config/deepin-wine-runner/FindExeHistory.json", str(json.dumps(ListToDictionary(findExeHistory))))  # 将历史记录的数组转换为字典并写入
        write_txt(get_home() + "/.config/deepin-wine-runner/WineBottonHistory.json", str(json.dumps(ListToDictionary(wineBottonHistory))))  # 将历史记录的数组转换为字典并写入
        e1['value'] = findExeHistory
        e2['value'] = wineBottonHistory
    DisableButton(False)

def RunWinetricks():
    DisableButton(True)
    wineBottonPath = get_home() + "/.wine"
    if not e1.get() == "":
        wineBottonPath = e1.get()
    print("WINEPREFIX='" + wineBottonPath + "' winetricks")
    res = subprocess.Popen(["WINEPREFIX='" + wineBottonPath + "' winetricks"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # 清空文本框内容
    returnText.config(state=tk.NORMAL)
    returnText.delete(1.0, "end")
    returnText.config(state=tk.DISABLED)
    # 实时读取程序返回
    while res.poll() is None:
        returnText.config(state=tk.NORMAL)
        try:
            text = res.stdout.readline().decode("utf8")
        except:
            text = ""
        returnText.insert("end", text)
        print(text)
        returnText.config(state=tk.DISABLED)
    DisableButton(False)

def InstallMonoGecko(program):
    DisableButton(True)
    if e1.get() == "":
        wineBottonPath = get_home() + "/.wine"
    else:
        wineBottonPath = e1.get()
    os.system(f"'{programPath}/launch.sh' deepin-terminal -C \"'{programPath}/InstallMono.py' '{wineBottonPath}' {wine[o1_text.get()]} {program}\" --keep-open")
    DisableButton(False)

def InstallNetFramework():
    DisableButton(True)
    if e1.get() == "":
        wineBottonPath = get_home() + "/.wine"
    else:
        wineBottonPath = e1.get()
    os.system(f"'{programPath}/launch.sh' deepin-terminal -C \"'{programPath}/InstallNetFramework.py' '{wineBottonPath}' {wine[o1_text.get()]}\" --keep-open")
    DisableButton(False)

def InstallVisualStudioCPlusPlus():
    DisableButton(True)
    if e1.get() == "":
        wineBottonPath = get_home() + "/.wine"
    else:
        wineBottonPath = e1.get()
    os.system(f"'{programPath}/launch.sh' deepin-terminal -C \"'{programPath}/InstallVisualCPlusPlus.py' '{wineBottonPath}' {wine[o1_text.get()]}\" --keep-open")
    DisableButton(False)

def BuildExeDeb():
    if e1.get() == "":
        wineBottonPath = get_home() + "/.wine"
    else:
        wineBottonPath = e1.get()
    threading.Thread(target=os.system, args=[f"python3 '{programPath}/deepin-wine-packager.py' '{wineBottonPath}' '{wine[o1_text.get()]}'"]).start()

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
wine = {"deepin-wine": "deepin-wine", "deepin-wine5": "deepin-wine5", "wine": "wine", "wine64": "wine64", "deepin-wine5 stable": "deepin-wine5-stable", "deepin-wine6 stable": "deepin-wine6-stable", "spark-wine7-devel": "spark-wine7-devel", "ukylin-wine": "ukylin-wine"}
shellHistory = list(json.loads(readtxt(get_home() + "/.config/deepin-wine-runner/ShellHistory.json")).values())
findExeHistory = list(json.loads(readtxt(get_home() + "/.config/deepin-wine-runner/FindExeHistory.json")).values())
wineBottonHistory = list(json.loads(readtxt(get_home() + "/.config/deepin-wine-runner/WineBottonHistory.json")).values())


###########################
# 程序信息
###########################
programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
iconPath = "{}/icon.png".format(programPath)
programUrl = "https://gitee.com/gfdgd-xi/deep-wine-runner\nhttps://github.com/gfdgd-xi/deep-wine-runner\nhttps://www.gitlink.org.cn/gfdgd_xi/deep-wine-runner"
information = json.loads(readtxt(f"{programPath}/information.json"))
version = information["Version"]
goodRunSystem = "Linux"
about = '''一个基于 Python3 的 tkinter 制作的 wine 运行器
版本：{}
适用平台：{}
tkinter 版本：{}
程序官网：{}
©2020-{} gfdgd xi、为什么您不喜欢熊出没和阿布呢'''.format(version, goodRunSystem, tk.TkVersion, programUrl, time.strftime("%Y"))
tips = '''提示：
1、使用终端运行该程序，可以看到 wine 以及程序本身的提示和报错;
2、wine 32 位和 64 位的容器互不兼容;
3、所有的 wine 和 winetricks 均需要自行安装（可以从 菜单栏=>程序 里面进行安装）
4、本程序支持带参数运行 wine 程序（之前版本也可以），只需要按以下格式即可：
exe路径\' 参数 \'
即可（单引号需要输入）
5、wine 容器如果没有指定，则会默认为 ~/.wine'''
updateThingsString = '''※1、支持打开 spark-wine7-devel 的专门缩放设置（如未安装则此按钮禁用）
※2、支持提取选择的 exe 文件的图标
※3、支持向指定的 wine 容器安装 mono、gecko、.net framework（此功能在菜单栏“Wine”中，卸载只需要使用程序的卸载按钮打开 Geek Uninstaller 即可）
※4、支持指定特定的 wine 容器调用 winetricks
※5、在没有指定 wine 容器的情况下，将自动设置为 ~/.wine
6、新增 ukylin-wine
7、将默认选择的 wine 改为 deepin-wine6 stable
8、支持打开指定容器的 winecfg、winver、regedit、taskmgr
9、双击使用 wine 运行器打开 exe（不知道能不能生效）
'''
title = "wine 运行器 {}".format(version)
updateTime = "2022年07月05日"
updateThings = "{} 更新内容：\n{}\n更新时间：{}".format(version, updateThingsString, updateTime, time.strftime("%Y"))


###########################
# 窗口创建
###########################
win = tk.Tk()  # 创建窗口
win.title(title)  # 设置标题
window = ttk.Frame()
# 设置变量以修改和获取值项
o1_text = tk.StringVar()
combobox1 = tk.StringVar()
o1_text.set("deepin-wine6 stable")
# 创建控件
controlFrame = ttk.Frame(window)
sendFrame = ttk.Frame(window)
button1 = ttk.Button(window, text="浏览", command=liulanbutton)  # 创建按钮控件
button2 = ttk.Button(window, text="浏览", command=liulanexebutton)  # 创建按钮控件
button3 = ttk.Button(controlFrame, text="启动", command=runexebutton)  # 创建按钮控件
killProgram = ttk.Button(controlFrame, text="停止", command=KillProgram)
openWineBotton = ttk.Button(controlFrame, text="打开Wine容器目录", command=OpenWineBotton)
installWineFont = ttk.Button(controlFrame, text="安装字体", command=OpenWineFontPath)
uninstallProgram = ttk.Button(controlFrame, text="卸载程序", command=UninstallProgram)
wineConfig = ttk.Button(controlFrame, text="配置wine容器", command=ConfigWineBotton)
sparkWineSetting = ttk.Button(controlFrame, text="星火wine设置", command=lambda: threading.Thread(target=os.system, args=["/opt/durapps/spark-dwine-helper/spark-dwine-helper-settings/settings.sh"]).start())
getProgramIcon = ttk.Button(controlFrame, text="获取选择的程序图标", command=lambda: threading.Thread(target=RunWineProgram, args=[f"{programPath}/Run.bat' '{programPath}/BeCyIconGrabber.exe' '{e2.get()}"]).start())
winetricksOpen = ttk.Button(controlFrame, text="使用winetricks打开指定容器(只能使用wine和wine64)", command=lambda: threading.Thread(target=RunWinetricks).start())
button5 = ttk.Button(sendFrame, text="创建用于运行的 desktop 文件到桌面", command=make_desktop_on_desktop)  # 创建按钮控件
saveDesktopFileOnLauncher = ttk.Button(sendFrame, text="创建用于运行的 desktop 文件到启动器", command=make_desktop_on_launcher)  # 创建按钮控件
label1 = ttk.Label(window, text="选择你想要使用的 wine 容器：")  # 创建标签控件
label2 = ttk.Label(window, text="选择要启动的 Windows 应用")  # 创建标签控件
label3 = ttk.Label(window, text="选择要使用的 wine 版本")  # 创建标签控件
label4 = ttk.Label(window, text="设置标题，以便把上方填写的信息写入到desktop文件里")  # 创建标签控件
e1 = ttk.Combobox(window, width=100)  # 创建文本框控件
e2 = ttk.Combobox(window, width=100)  # 创建文本框控件
combobox1 = ttk.Combobox(window, width=100)
o1 = ttk.OptionMenu(window, o1_text, "deepin-wine6 stable", *list(wine))  # 创建选择框控件
returnText = tk.Text(window)
menu = tk.Menu(window, background="white")  # 设置菜单栏
programmenu = tk.Menu(menu, tearoff=0, background="white")  # 设置“程序”菜单栏
menu.add_cascade(label="程序", menu=programmenu)
programmenu.add_command(label="安装 wine", command=InstallWine)
programmenu.add_separator()  # 设置分界线
programmenu.add_command(label="清空软件历史记录", command=CleanProgramHistory)
programmenu.add_separator()  # 设置分界线
programmenu.add_command(label="退出程序", command=window.quit)  # 设置“退出程序”项
wineOption = tk.Menu(menu, tearoff=0, background="white")  # 设置“Wine”菜单栏
menu.add_cascade(label="Wine", menu=wineOption)
wineOption.add_command(label="打包 wine 应用", command=BuildExeDeb)
wineOption.add_separator()
wineOption.add_command(label="在指定wine、指定容器安装 .net framework", command=lambda: threading.Thread(target=InstallNetFramework).start())
wineOption.add_command(label="在指定wine、指定容器安装 Visual Studio C++", command=lambda: threading.Thread(target=InstallVisualStudioCPlusPlus).start())
wineOption.add_command(label="在指定wine、指定容器安装 gecko", command=lambda: threading.Thread(target=InstallMonoGecko, args=["gecko"]).start())
wineOption.add_command(label="在指定wine、指定容器安装 mono", command=lambda: threading.Thread(target=InstallMonoGecko, args=["mono"]).start())
wineOption.add_command(label="打开指定wine、指定容器的注册表", command=lambda: threading.Thread(target=RunWineProgram, args=["regedit"]).start())
wineOption.add_command(label="打开指定wine、指定容器的任务管理器", command=lambda: threading.Thread(target=RunWineProgram, args=["taskmgr"]).start())
wineOption.add_command(label="打开指定wine、指定容器的关于 wine", command=lambda: threading.Thread(target=RunWineProgram, args=["winver"]).start())
help = tk.Menu(menu, tearoff=0, background="white")  # 设置“帮助”菜单栏
menu.add_cascade(label="帮助", menu=help)
help.add_command(label="程序官网", command=OpenProgramURL)  # 设置“程序官网”项
help.add_separator()
help.add_command(label="小提示", command=helps)  # 设置“小提示”项
help.add_command(label="更新内容", command=UpdateThings)  # 设置“更新内容”项
help.add_command(label="关于这个程序", command=about_this_program)  # 设置“关于这个程序”项
# 设置窗口
win.iconphoto(False, tk.PhotoImage(file=iconPath))
themes = ttkthemes.ThemedStyle(win)
themes.set_theme("breeze")
win.config(bg="white")
# 设置控件
if len(sys.argv) > 1 and sys.argv[1]:
    e1.set(f"{get_home()}/.wine")
    e2.set(sys.argv[1])
menu.configure(activebackground="dodgerblue")
programmenu.configure(activebackground="dodgerblue")
wineOption.configure(activebackground="dodgerblue")
help.configure(activebackground="dodgerblue")
e1['value'] = findExeHistory
e2['value'] = wineBottonHistory
combobox1['value'] = shellHistory
returnText.insert("end", "此可以查看到 Wine 应用安装时的程序返回值")
returnText.config(state=tk.DISABLED)
if not os.path.exists("/opt/durapps/spark-dwine-helper/spark-dwine-helper-settings/settings.sh"):
    sparkWineSetting.config(state=tk.DISABLED)
# 添加控件
win.config(menu=menu)  # 显示菜单栏
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
controlFrame.grid(row=3, column=0, columnspan=3)
button3.grid(row=0, column=0)
killProgram.grid(row=0, column=1)
openWineBotton.grid(row=0, column=2)
installWineFont.grid(row=0, column=3)
uninstallProgram.grid(row=0, column=4)
wineConfig.grid(row=0, column=5)
sparkWineSetting.grid(row=0, column=6)
getProgramIcon.grid(row=0, column=7)
winetricksOpen.grid(row=0, column=8)
sendFrame.grid(row=5, column=0, columnspan=3)
button5.grid(row=0, column=0)
saveDesktopFileOnLauncher.grid(row=0, column=1)
o1.grid(row=2, column=1)
returnText.grid(row=6, column=0, columnspan=3)
# 启动窗口
window.pack()
win.mainloop()
