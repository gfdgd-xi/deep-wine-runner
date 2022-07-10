#!/usr/bin/env python3
# 使用系统默认的 python3 运行
###########################################################################################
# 作者：gfdgd xi、为什么您不喜欢熊出没和阿布呢
# 版本：1.6.0
# 更新时间：2022年07月10日
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
import easygui
import requests
import threading
import traceback
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
    #winetricksOpen.configure(state=a[things])
    getProgramIcon.configure(state=a[things])
    uninstallProgram.configure(state=a[things])
    trasButton.configure(state=a[things])

def CheckProgramIsInstall(program):
    return not bool(os.system(f"which '{program}'"))

# 运行可执行文件的线程
def runexebutton_threading():
    DisableButton(True)
    if not CheckProgramIsInstall(wine[o1_text.get()]):
        if not tkinter.messagebox.askyesno(title="提示", message="检查到您未安装这个 wine，是否继续使用这个 wine 运行？"):
            DisableButton(False)
            return
    if e2.get() == "":  # 判断文本框是否有内容
        tkinter.messagebox.showinfo(title="提示", message="没有填写需要使用的 exe 应用")
        DisableButton(False)
        return
    else:  # 如果都有
        if e1.get() == "":
            wineBottonPath = setting["DefultBotton"]
        else:
            wineBottonPath = e1.get()
        option = ""
        if setting["Architecture"] != "Auto":
            option += f"WINEARCH={setting['Architecture']} "
        if not setting["Debug"]:
            option += "WINEDEBUG=-all "
        if setting["TerminalOpen"]:
            res = subprocess.Popen([f"'{programPath}/launch.sh' deepin-terminal -C \"WINEPREFIX='" + wineBottonPath + "' " + option + wine[o1_text.get()] + " '" + e2.get() + "' " + setting["WineOption"] + "\" --keep-open"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        else:
            res = subprocess.Popen(["WINEPREFIX='" + wineBottonPath + "' " + option + wine[o1_text.get()] + " '" + e2.get() + "' " + setting["WineOption"]], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
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
    if not CheckProgramIsInstall(wine[o1_text.get()]):
        if not tkinter.messagebox.askyesno(title="提示", message="检查到您未安装这个 wine，是否继续使用这个 wine 写入？"):
            DisableButton(False)
            return
    else:  # 如果都有
        if os.path.exists(get_home() + "/.local/share/applications/" + combobox1.get() + ".desktop"): # 判断目录是否有该文件，如果有
            choose = tkinter.messagebox.askokcancel(title="提示", message="文件已经存在，是否覆盖？")  # 询问用户是否覆盖
            if choose:   # 如要覆盖
                os.remove(get_home() + "/.local/share/applications/" + combobox1.get() + ".desktop")  # 删除该文件
            else:  # 如不覆盖
                return  # 结束
        if e1.get() == "":
            wineBottonPath = setting["DefultBotton"]
        else:
            wineBottonPath = e1.get()
        option = ""
        if setting["Architecture"] != "Auto":
            option += f"WINEARCH={setting['Architecture']} "
        if not setting["Debug"]:
            option += "WINEDEBUG=-all "
        write_txt(get_home() + "/.local/share/applications/" + combobox1.get() + ".desktop", f'''[Desktop Entry]
Name={combobox1.get()}
Exec=env WINEPREFIX='{wineBottonPath}' {option} {wine[o1_text.get()]} '{e2.get()}' {setting["WineOption"]}
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
    if not CheckProgramIsInstall(wine[o1_text.get()]):
        if not tkinter.messagebox.askyesno(title="提示", message="检查到您未安装这个 wine，是否继续使用这个 wine 写入？"):
            DisableButton(False)
            return
    else:  # 如果都有
        if os.path.exists(get_desktop_path() + "/" + combobox1.get() + ".desktop"): # 判断目录是否有该文件，如果有
            choose = tkinter.messagebox.askokcancel(title="提示", message="文件已经存在，是否覆盖？")  # 询问用户是否覆盖
            if choose:   # 如要覆盖
                os.remove(get_desktop_path() + "/" + combobox1.get() + ".desktop")  # 删除该文件
            else:  # 如不覆盖
                return  # 结束
        if e1.get() == "":
            wineBottonPath = setting["DefultBotton"]
        else:
            wineBottonPath = e1.get()
        os.mknod(get_desktop_path() + "/" + combobox1.get() + ".desktop")
        option = ""
        if setting["Architecture"] != "Auto":
            option += f"WINEARCH={setting['Architecture']} "
        if not setting["Debug"]:
            option += "WINEDEBUG=-all "
        write_txt(get_desktop_path() + "/" + combobox1.get() + ".desktop", f'''[Desktop Entry]
Name={combobox1.get()}
Exec=env WINEPREFIX='{wineBottonPath}' {option} {wine[o1_text.get()]} '{e2.get()}' {setting["WineOption"]}
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
        wineBottonPath = setting["DefultBotton"]
    else:
        wineBottonPath = e1.get()
    os.system("xdg-open \"" + wineBottonPath.replace("\'", "\\\'") + "\"")

def OpenWineFontPath():
    if e1.get() == "":
        wineBottonPath = setting["DefultBotton"]
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

def RunWineProgram(wineProgram, history = False, Disbled = True):
    DisableButton(True)
    if not CheckProgramIsInstall(wine[o1_text.get()]):
        if not tkinter.messagebox.askyesno(title="提示", message="检查到您未安装这个 wine，是否继续使用这个 wine 运行？"):
            DisableButton(False)
            return
    if e1.get() == "":
        wineBottonPath = setting["DefultBotton"]
    else:
        wineBottonPath = e1.get()
    option = ""
    if setting["Architecture"] != "Auto":
        option += f"WINEARCH={setting['Architecture']} "
    if not setting["Debug"]:
        option += "WINEDEBUG=-all "
    if setting["TerminalOpen"]:
        res = subprocess.Popen([f"'{programPath}/launch.sh' deepin-terminal -C \"WINEPREFIX='" + wineBottonPath + "' " + option + wine[o1_text.get()] + " '" + wineProgram + "' " + setting["WineOption"] + "\" --keep-open"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    else:
        res = subprocess.Popen(["WINEPREFIX='" + wineBottonPath + "' " + option + wine[o1_text.get()] + " '" + wineProgram + "' " + setting["WineOption"]], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
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
    if Disbled:
        DisableButton(False)

def RunWinetricks():
    DisableButton(True)
    if not CheckProgramIsInstall(wine[o1_text.get()]):
        if not tkinter.messagebox.askyesno(title="提示", message="检查到您未安装这个 wine，是否继续使用这个 wine 运行？"):
            DisableButton(False)
            return
    wineBottonPath = setting["DefultBotton"]
    if not e1.get() == "":
        wineBottonPath = e1.get()
    option = ""
    if setting["Architecture"] != "Auto":
        option += f"WINEARCH={setting['Architecture']} "
    if not setting["Debug"]:
        option += "WINEDEBUG=-all "
    if setting["TerminalOpen"]:
        res = subprocess.Popen([f"'{programPath}/launch.sh' deepin-terminal -C \"WINEPREFIX='{wineBottonPath}' {option} WINE=" + subprocess.getoutput(f"which {wine[o1_text.get()]}").replace(" ", "").replace("\n", "") + " winetricks --gui\" --keep-open"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    else:    
        res = subprocess.Popen([f"WINEPREFIX='{wineBottonPath}' {option} WINE='" + subprocess.getoutput(f"which {wine[o1_text.get()]}").replace(" ", "").replace("\n", "") + "' winetricks --gui"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        #res = subprocess.Popen(["WINEPREFIX='" + option + wineBottonPath + "' winetricks"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
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
        wineBottonPath = setting["DefultBotton"]
    else:
        wineBottonPath = e1.get()
    os.system(f"'{programPath}/launch.sh' deepin-terminal -C \"'{programPath}/InstallMono.py' '{wineBottonPath}' {wine[o1_text.get()]} {program}\" --keep-open")
    DisableButton(False)

def InstallNetFramework():
    DisableButton(True)
    if e1.get() == "":
        wineBottonPath = setting["DefultBotton"]
    else:
        wineBottonPath = e1.get()
    os.system(f"'{programPath}/launch.sh' deepin-terminal -C \"'{programPath}/InstallNetFramework.py' '{wineBottonPath}' {wine[o1_text.get()]}\" --keep-open")
    DisableButton(False)

def InstallVisualStudioCPlusPlus():
    DisableButton(True)
    if e1.get() == "":
        wineBottonPath = setting["DefultBotton"]
    else:
        wineBottonPath = e1.get()
    os.system(f"'{programPath}/launch.sh' deepin-terminal -C \"'{programPath}/InstallVisualCPlusPlus.py' '{wineBottonPath}' {wine[o1_text.get()]}\" --keep-open")
    DisableButton(False)

def InstallMSXML():
    DisableButton(True)
    if e1.get() == "":
        wineBottonPath = setting["DefultBotton"]
    else:
        wineBottonPath = e1.get()
    os.system(f"'{programPath}/launch.sh' deepin-terminal -C \"'{programPath}/InstallMsxml.py' '{wineBottonPath}' {wine[o1_text.get()]}\" --keep-open")
    DisableButton(False)

def InstallOther():
    DisableButton(True)
    if e1.get() == "":
        wineBottonPath = setting["DefultBotton"]
    else:
        wineBottonPath = e1.get()
    os.system(f"'{programPath}/launch.sh' deepin-terminal -C \"'{programPath}/InstallOther.py' '{wineBottonPath}' {wine[o1_text.get()]}\" --keep-open")
    DisableButton(False)

def BuildExeDeb():
    if e1.get() == "":
        wineBottonPath = setting["DefultBotton"]
    else:
        wineBottonPath = e1.get()
    threading.Thread(target=os.system, args=[f"python3 '{programPath}/deepin-wine-packager.py' '{wineBottonPath}' '{wine[o1_text.get()]}'"]).start()

def SetDeepinFileDialogDeepin():
    code = os.system(f"pkexec \"{programPath}/deepin-wine-venturi-setter.py\" deepin")
    if code != 0:
        if code == 1:
            tkinter.messagebox.showerror(title="错误", message="无法更新配置：配置不准重复配置")
            return
        tkinter.messagebox.showerror(title="错误", message="配置失败")

def SetDeepinFileDialogDefult():
    code = os.system(f"pkexec \"{programPath}/deepin-wine-venturi-setter.py\" defult")
    if code != 0:
        if code == 1:
            tkinter.messagebox.showerror(title="错误", message="无法更新配置：配置不准重复配置")
            return
        tkinter.messagebox.showerror(title="错误", message="配置失败")

def SetDeepinFileDialogRecovery():
    threading.Thread(target=os.system, args=[f"'{programPath}/launch.sh' deepin-terminal -C 'pkexec \"{programPath}/deepin-wine-venturi-setter.py\" recovery' --keep-open"]).start()

def DeleteWineBotton():
    if not tkinter.messagebox.askokcancel(title="提示", message="你确定要删除容器吗？删除后将无法恢复！\n如果没有选择 wine 容器，将会自动删除默认的容器！"):
        return
    if e1.get() == "":
        wineBottonPath = setting["DefultBotton"]
    else:
        wineBottonPath = e1.get()
    try:
        shutil.rmtree(wineBottonPath)
        tkinter.messagebox.showinfo(title="提示", message="删除完毕！")
    except:
        traceback.print_exc()
        tkinter.messagebox.showerror(title="错误", message=traceback.format_exc())

def ThankWindow():
    easygui.textbox(title="特别谢明", msg="感谢以下的大佬在 deepin 论坛、公众号等平台提供的 Wine 适配解决方案，现在将这些 Wine 适配方案加入此 Wine 运行器，对此有由衷的感谢！如果有侵犯到您的权利和意愿，请尽快与开发者联系删除在此程序内相关的内容：", text=thankText)

def InstallWineFont():
    threading.Thread(target=os.system, args=[f"'{programPath}/launch.sh' deepin-terminal -C 'echo 这些字体来自星火应用商店 && sudo ss-apt-fast install ms-core-fonts winfonts -y' --keep-open"]).start()

def WineRunnerBugUpload():
    threading.Thread(target=os.system, args=[programPath + "/deepin-wine-runner-update-bug"]).start()

class UpdateWindow():
    data = {}
    def ShowWindow():
        update = tk.Toplevel()
        update.title("检查更新")
        update.resizable(0, 0)
        update.iconphoto(False, tk.PhotoImage(file=iconPath))
        versionLabel = ttk.Label(update, text="当前版本：{}\n最新版本：未知\n更新内容：".format(version))
        updateText = tk.Text(update)
        controlFrame = ttk.Frame(update)
        ok = ttk.Button(controlFrame, text="更新（更新过程中会关闭所有Python应用，包括这个应用）", command=UpdateWindow.Update)
        cancel = ttk.Button(controlFrame, text="取消", command=update.destroy)
        try:
            UpdateWindow.data = json.loads(requests.get("http://120.25.153.144/spark-deepin-wine-runner/update.json").text)
            versionLabel = ttk.Label(update, text="当前版本：{}\n最新版本：{}\n更新内容：".format(version, UpdateWindow.data["Version"]))
            if UpdateWindow.data["Version"] == version:
                updateText.insert("0.0", "此为最新版本，无需更新")
                ok.configure(state=tk.DISABLED)
            else:
                updateText.insert("0.0", UpdateWindow.data["New"].replace("\\n", "\n"))
        except:
            traceback.print_exc()
            tkinter.messagebox.showerror(title="错误", message="无法连接服务器！")
        updateText.configure(state=tk.DISABLED)
        versionLabel.pack(anchor=tk.W)
        updateText.pack()
        controlFrame.pack(anchor=tk.E)
        cancel.grid(row=0, column=0)
        ok.grid(row=0, column=1)
        update.mainloop()
    def Update():
        if not os.path.exists("/tmp/uengine-runner/update"):
            os.makedirs("/tmp/spark-deepin-wine-runner/update")
        try:            
            write_txt("/tmp/spark-deepin-wine-runner/update.sh", f"""#!/bin/bash
echo 删除多余的安装包
rm -rfv /tmp/spark-deepin-wine-runner/update/*
echo 关闭“UEngine 运行器”以及其它“Python 应用”
killall python3
echo 下载安装包
wget -P /tmp/spark-deepin-wine-runner/update {UpdateWindow.data["Url"][0], iconPath}
echo 安装安装包
dpkg -i /tmp/spark-deepin-wine-runner/update/*.deb
echo 修复依赖关系
apt install -f -y
notify-send -i "{iconPath}" "更新完毕！"
zenity --info --text=\"更新完毕！\" --ellipsize
""")
        except:
            traceback.print_exc()
            easygui.textbox(title="错误", msg="更新出现错误，无法继续更新！", text=traceback.format_exc())
        os.system(f"'{programPath}/launch.sh' deepin-terminal -e pkexec bash /tmp/spark-deepin-wine-runner/update.sh")

class GetDllFromWindowsISO:
    wineBottonPath = get_home() + "/.wine"
    isoPath = None#ttk.Entry()
    dllList = None
    message = None
    dllFound = None
    dllControl = None
    foundButton = None
    saveDll = None
    setWineBotton = None
    browser = None
    mount = False
    mountButton = None
    def ShowWindow():
        DisableButton(True)
        GetDllFromWindowsISO.message = tk.Toplevel()
        if not e1.get() == "":
            GetDllFromWindowsISO.wineBottonPath = e1.get()
        ttk.Label(GetDllFromWindowsISO.message, text=f"""提示：
    目前本提取功能只支持 Windows XP 以及 Windows Server 2003 等老系统的官方安装镜像，只支持读取 i386 安装方法的安装镜像，不支持读取 wim、ghost 安装方式
    以及不要拷贝/替换太多的 dll，否则可能会导致 wine 容器异常
    最后，拷贝/替换 dll 后，建议点击下面“设置 wine 容器”按钮==》函数库 进行设置
当前选择的 Wine 容器：{GetDllFromWindowsISO.wineBottonPath}""").grid(row=0, column=0, columnspan=3, sticky=tk.W)
        ttk.Label(GetDllFromWindowsISO.message, text="ISO镜像：").grid(row=1, column=0, sticky=tk.W)
        GetDllFromWindowsISO.isoPath = ttk.Combobox(GetDllFromWindowsISO.message, width=100)
        GetDllFromWindowsISO.browser = ttk.Button(GetDllFromWindowsISO.message, text="浏览……", command=GetDllFromWindowsISO.Browser)
        isoControl = ttk.Frame(GetDllFromWindowsISO.message)
        GetDllFromWindowsISO.mountButton = ttk.Button(isoControl, text="读取/挂载ISO镜像", command=GetDllFromWindowsISO.MountDisk)
        ttk.Button(isoControl, text="关闭/卸载ISO镜像", command=GetDllFromWindowsISO.UmountDisk).grid(row=0, column=1)
        ttk.Label(GetDllFromWindowsISO.message, text="查找DLL\n（为空则代表不查找，\n将显示全部内容）：").grid(row=3, column=0)
        GetDllFromWindowsISO.dllFound = ttk.Combobox(GetDllFromWindowsISO.message, width=100)
        GetDllFromWindowsISO.foundButton = ttk.Button(GetDllFromWindowsISO.message, text="查找", command=GetDllFromWindowsISO.Found)
        GetDllFromWindowsISO.dllList = tk.Listbox(GetDllFromWindowsISO.message, width=100)
        GetDllFromWindowsISO.dllControl = ttk.Frame(GetDllFromWindowsISO.message)
        GetDllFromWindowsISO.saveDll = ttk.Button(GetDllFromWindowsISO.dllControl, text="保存到 wine 容器中", command=GetDllFromWindowsISO.CopyDll)
        GetDllFromWindowsISO.setWineBotton = ttk.Button(GetDllFromWindowsISO.dllControl, text="设置 wine 容器", command=lambda: threading.Thread(target=RunWineProgram, args=["winecfg", False, False]).start())
        # 设置控件
        GetDllFromWindowsISO.DisbledDown(True)
        GetDllFromWindowsISO.isoPath['value'] = isoPath
        GetDllFromWindowsISO.dllFound['value'] = isoPathFound  
        # 显示控件
        GetDllFromWindowsISO.isoPath.grid(row=1, column=1)
        GetDllFromWindowsISO.browser.grid(row=1, column=2)
        GetDllFromWindowsISO.mountButton.grid(row=0, column=0)
        isoControl.grid(row=2, column=0, columnspan=3)
        GetDllFromWindowsISO.dllFound.grid(row=3, column=1)
        GetDllFromWindowsISO.foundButton.grid(row=3, column=2)
        GetDllFromWindowsISO.dllList.grid(row=4, column=0, columnspan=3)
        GetDllFromWindowsISO.dllControl.grid(row=5, column=0, columnspan=3)
        GetDllFromWindowsISO.saveDll.grid(row=0, column=0)
        GetDllFromWindowsISO.setWineBotton.grid(row=0, column=1)
        # 设置
        GetDllFromWindowsISO.message.protocol('WM_DELETE_WINDOW', GetDllFromWindowsISO.ExitWindow)
        GetDllFromWindowsISO.message.title("从 ISO 提取 DLL")
        # 显示
        GetDllFromWindowsISO.message.mainloop()

    def DisbledUp(state):
        nd = [tk.NORMAL, tk.DISABLED]
        GetDllFromWindowsISO.isoPath.configure(state=nd[int(state)])
        GetDllFromWindowsISO.browser.configure(state=nd[int(state)])
        GetDllFromWindowsISO.mountButton.configure(state=nd[int(state)])


    def DisbledDown(state):
        nd = [tk.NORMAL, tk.DISABLED]
        GetDllFromWindowsISO.dllList.configure(state=nd[int(state)])
        GetDllFromWindowsISO.dllFound.configure(state=nd[int(state)])
        #GetDllFromWindowsISO.dllControl.configure(state=nd[int(state)])
        GetDllFromWindowsISO.saveDll.configure(state=nd[int(state)])
        GetDllFromWindowsISO.setWineBotton.configure(state=nd[int(state)])
        GetDllFromWindowsISO.foundButton.configure(state=nd[int(state)])

    def Browser():
        path = tkinter.filedialog.askopenfilename(title="选择 ISO 镜像文件", 
            filetypes=[("ISO 镜像文件", "*.iso"), ("ISO 镜像文件", "*.ISO"), ("所有文件", "*.*")], 
            initialdir=json.loads(readtxt(get_home() + "/.config/deepin-wine-runner/FindISO.json"))["path"])
        if path == None or path == "":
            return
        GetDllFromWindowsISO.isoPath.set(path)
        write_txt(get_home() + "/.config/deepin-wine-runner/FindISO.json", json.dumps({"path": os.path.dirname(path)}))  # 写入配置文件

    def Found():
        found = GetDllFromWindowsISO.dllFound.get()
        GetDllFromWindowsISO.dllList.configure(state=tk.NORMAL)
        GetDllFromWindowsISO.dllList.delete(0, tk.END)
        try:
            if found == "":
                for i in os.listdir("/tmp/wine-runner-getdll/i386"):
                    if i[-3:] == "dl_":
                        GetDllFromWindowsISO.dllList.insert("end", i[:-1] + "l")    
                return
            for i in os.listdir("/tmp/wine-runner-getdll/i386"):
                if found in i[:-1] + "l":
                    GetDllFromWindowsISO.dllList.insert("end", i[:-1] + "l")  
            isoPathFound.append(found)  # 将记录写进数组
            write_txt(get_home() + "/.config/deepin-wine-runner/ISOPathFound.json", str(json.dumps(ListToDictionary(isoPathFound))))  # 将历史记录的数组转换为字典并写入
            GetDllFromWindowsISO.dllFound['value'] = isoPathFound  
        except:
            traceback.print_exc()
            tkinter.messagebox.showerror(title="错误", message=traceback.format_exc())


    def ExitWindow():
        if GetDllFromWindowsISO.mount:
            tkinter.messagebox.showinfo(title="提示", message="请关闭/卸载镜像后再关闭本窗口")
            return
        DisableButton(False)
        GetDllFromWindowsISO.message.destroy()

    def MountDisk():
        if not os.path.exists(GetDllFromWindowsISO.isoPath.get()):
            tkinter.messagebox.showerror(title="错误", message="您选择的 ISO 镜像文件不存在")
            return
        if os.path.exists("/tmp/wine-runner-getdll"):
            try:
                os.rmdir("/tmp/wine-runner-getdll")
            except:
                # 如果无法删除可能是挂载了文件
                os.system("pkexec umount /tmp/wine-runner-getdll")
                try:
                    os.rmdir("/tmp/wine-runner-getdll")
                except:
                    traceback.print_exc()
                    tkinter.messagebox.showerror(title="错误", message=traceback.format_exc())
                    return
        os.makedirs("/tmp/wine-runner-getdll")
        GetDllFromWindowsISO.dllList.configure(state=tk.NORMAL)
        os.system(f"pkexec mount '{GetDllFromWindowsISO.isoPath.get()}' /tmp/wine-runner-getdll")
        GetDllFromWindowsISO.dllList.delete(0, tk.END)
        try:
            for i in os.listdir("/tmp/wine-runner-getdll/i386"):
                if i[-3:] == "dl_":
                    GetDllFromWindowsISO.dllList.insert("end", i[:-1] + "l")     
        except:
            traceback.print_exc()
            tkinter.messagebox.showerror(title="错误", message=f"镜像内容读取/挂载失败，报错如下：\n{traceback.format_exc()}")
            return
        GetDllFromWindowsISO.DisbledDown(False)  
        GetDllFromWindowsISO.DisbledUp(True)
        GetDllFromWindowsISO.mount = True
        isoPath.append(GetDllFromWindowsISO.isoPath.get())  # 将记录写进数组
        write_txt(get_home() + "/.config/deepin-wine-runner/ISOPath.json", str(json.dumps(ListToDictionary(isoPath))))  # 将历史记录的数组转换为字典并写入
        GetDllFromWindowsISO.isoPath['value'] = isoPath

    def UmountDisk():
        os.system("pkexec umount /tmp/wine-runner-getdll")
        GetDllFromWindowsISO.dllList.configure(state=tk.NORMAL)
        try:
            shutil.rmtree("/tmp/wine-runner-getdll")
        except:
            traceback.print_exc()
            tkinter.messagebox.showerror(title="错误", message=f"关闭/卸载镜像失败，报错如下：\n{traceback.format_exc()}")
            return
        GetDllFromWindowsISO.DisbledDown(True)
        GetDllFromWindowsISO.DisbledUp(False)
        GetDllFromWindowsISO.mount = False

    def CopyDll():
        for i in GetDllFromWindowsISO.dllList.curselection():
            choose = GetDllFromWindowsISO.dllList.get(i)
            if os.path.exists(f"{GetDllFromWindowsISO.wineBottonPath}/drive_c/windows/system32/{choose}"):
                if not tkinter.messagebox.askyesno(title="提示", message=f"DLL {choose} 已经存在，是否覆盖？"):
                    continue
            print(i)
            try:
                shutil.copy(f"/tmp/wine-runner-getdll/i386/{choose[:-1]}_", f"{GetDllFromWindowsISO.wineBottonPath}/drive_c/windows/system32/{choose}")
                tkinter.messagebox.showinfo(title="提示", message="提取成功！")
            except:
                traceback.print_exc()
                tkinter.messagebox.showerror(title="错误", message=traceback.format_exc())
            
class ProgramSetting():
    wineBottonA = None
    wineDebug = None
    defultWine = None
    defultBotton = None
    terminalOpen = None
    wineOption = None
    wineBottonDifferent = None
    def ShowWindow():
        message = tk.Toplevel()
        ProgramSetting.wineBottonA = tk.StringVar()
        ProgramSetting.wineDebug = tk.IntVar()
        ProgramSetting.wineDebug.set(int(setting["Debug"]))
        ProgramSetting.defultWine = tk.StringVar()
        ttk.Label(message, text="选择 Wine 容器版本：").grid(row=0, column=0, sticky=tk.W)
        ttk.OptionMenu(message, ProgramSetting.wineBottonA, setting["Architecture"], "Auto", "win32", "win64").grid(row=0, column=1)
        ttk.Label(message, text="wine DEBUG 信息输出：").grid(row=1, column=0, sticky=tk.W)
        ttk.Checkbutton(message, text="开启 DEBUG 输出", variable=ProgramSetting.wineDebug).grid(row=1, column=1)
        ttk.Label(message, text="默认 Wine：").grid(row=2, column=0, sticky=tk.W)
        ttk.OptionMenu(message, ProgramSetting.defultWine, setting["DefultWine"], *list(wine)).grid(row=2, column=1)  # 创建选择框控件
        ttk.Label(message, text="默认 Wine 容器：").grid(row=3, column=0, sticky=tk.W)
        ProgramSetting.defultBotton = tk.StringVar()
        ProgramSetting.defultBotton.set(setting["DefultBotton"])
        ttk.Entry(message, width=30, text=setting["DefultBotton"], textvariable=ProgramSetting.defultBotton).grid(row=3, column=1)
        ttk.Button(message, text="浏览", command=ProgramSetting.Browser).grid(row=3, column=2)
        ProgramSetting.terminalOpen = tk.IntVar()
        ProgramSetting.terminalOpen.set(setting["TerminalOpen"])
        ttk.Label(message, text="使用终端打开：").grid(row=4, column=0)
        ttk.Checkbutton(message, text="使用终端打开（deepin 终端）", variable=ProgramSetting.terminalOpen).grid(row=4, column=1, columnspan=2)
        ttk.Label(message, text="自定义 wine 参数：").grid(row=5, column=0)
        ProgramSetting.wineOption = tk.StringVar()
        ProgramSetting.wineOption.set(setting["WineOption"])
        #ttk.Label(message, text="容器创建规则：").grid(row=6, column=0)
        #ProgramSetting.wineBottonDifferent = tk.IntVar()
        #ProgramSetting.wineBottonDifferent.set(setting["WineBottonDifferent"])
        ttk.Checkbutton(message, text="为每一个可执行文件创建单独的容器（如果勾选的话，上面默认 Wine 容器选项将会指定这些产生的 Wine 容器默认存放目录）", variable=ProgramSetting.wineBottonDifferent)
        ttk.Entry(message, width=40, textvariable=ProgramSetting.wineOption).grid(row=5, column=1, columnspan=2)
        ttk.Button(message, text="保存", command=ProgramSetting.Save).grid(row=6, column=0, columnspan=3, sticky=tk.E)
        # 设置
        message.title(f"设置 wine 运行器 {version}")
        # 显示
        message.mainloop()

    def Browser():
        path = tkinter.filedialog.askdirectory(title="选择 Wine 容器", initialdir=json.loads(readtxt(get_home() + "/.config/deepin-wine-runner/WineBotton.json"))["path"])
        if path == "" or path == None or path == "()" or path == ():
            return
        ProgramSetting.defultBotton.set(path)

    def Save():
        # 写入容器位数设置
        setting["Architecture"] = ProgramSetting.wineBottonA.get()
        setting["Debug"] = bool(ProgramSetting.wineDebug.get())
        setting["DefultWine"] = ProgramSetting.defultWine.get()
        setting["DefultBotton"] = ProgramSetting.defultBotton.get()
        setting["TerminalOpen"] = bool(ProgramSetting.terminalOpen.get())
        setting["WineOption"] = ProgramSetting.wineOption.get()
        setting["WineBottonDifferent"] = bool(ProgramSetting.wineBottonDifferent.get())
        try:
            write_txt(get_home() + "/.config/deepin-wine-runner/WineSetting.json", json.dumps(setting))
        except:
            traceback.print_exc()
            tkinter.messagebox.showerror(title="错误", message=traceback.format_exc())
            return
        tkinter.messagebox.showinfo(title="提示", message="保存完毕！")

###########################
# 加载配置
###########################
defultProgramList = {
    "Architecture": "Auto",
    "Debug": True,
    "DefultWine": "deepin-wine6 stable",
    "DefultBotton" : get_home() + "/.wine",
    "TerminalOpen": False,
    "WineOption": "",
    "WineBottonDifferent": False
}
if not os.path.exists(get_home() + "/.config/deepin-wine-runner"):  # 如果没有配置文件夹
    os.mkdir(get_home() + "/.config/deepin-wine-runner")  # 创建配置文件夹
if not os.path.exists(get_home() + "/.config/deepin-wine-runner/ShellHistory.json"):  # 如果没有配置文件
    write_txt(get_home() + "/.config/deepin-wine-runner/ShellHistory.json", json.dumps({}))  # 创建配置文件
if not os.path.exists(get_home() + "/.config/deepin-wine-runner/FindExeHistory.json"):  # 如果没有配置文件
    write_txt(get_home() + "/.config/deepin-wine-runner/FindExeHistory.json", json.dumps({}))  # 创建配置文件
if not os.path.exists(get_home() + "/.config/deepin-wine-runner/WineBottonHistory.json"):  # 如果没有配置文件
    write_txt(get_home() + "/.config/deepin-wine-runner/WineBottonHistory.json", json.dumps({}))  # 创建配置文件
if not os.path.exists(get_home() + "/.config/deepin-wine-runner/ISOPath.json"):  # 如果没有配置文件
    write_txt(get_home() + "/.config/deepin-wine-runner/ISOPath.json", json.dumps({}))  # 写入（创建）一个配置文件
if not os.path.exists(get_home() + "/.config/deepin-wine-runner/ISOPathFound.json"):  # 如果没有配置文件
    write_txt(get_home() + "/.config/deepin-wine-runner/ISOPathFound.json", json.dumps({}))  # 写入（创建）一个配置文件
if not os.path.exists(get_home() + "/.config/deepin-wine-runner/FindExe.json"):  # 如果没有配置文件
    write_txt(get_home() + "/.config/deepin-wine-runner/FindExe.json", json.dumps({"path": "~"}))  # 写入（创建）一个配置文件
if not os.path.exists(get_home() + "/.config/deepin-wine-runner/FindISO.json"):  # 如果没有配置文件
    write_txt(get_home() + "/.config/deepin-wine-runner/FindISO.json", json.dumps({"path": "~"}))  # 写入（创建）一个配置文件
if not os.path.exists(get_home() + "/.config/deepin-wine-runner/WineBotton.json"):  # 如果没有配置文件
    write_txt(get_home() + "/.config/deepin-wine-runner/WineBotton.json", json.dumps({"path": "~/.deepinwine"}))  # 写入（创建）一个配置文件
if not os.path.exists(get_home() + "/.config/deepin-wine-runner/WineSetting.json"):  # 如果没有配置文件
    write_txt(get_home() + "/.config/deepin-wine-runner/WineSetting.json", json.dumps(defultProgramList))  # 写入（创建）一个配置文件

###########################
# 设置变量
###########################
# 如果要添加其他 wine，请在字典添加其名称和执行路径
try:
    wine = {"deepin-wine": "deepin-wine", "deepin-wine5": "deepin-wine5", "wine": "wine", "wine64": "wine64", "deepin-wine5 stable": "deepin-wine5-stable", "deepin-wine6 stable": "deepin-wine6-stable", "spark-wine7-devel": "spark-wine7-devel", "ukylin-wine": "ukylin-wine"}
    shellHistory = list(json.loads(readtxt(get_home() + "/.config/deepin-wine-runner/ShellHistory.json")).values())
    findExeHistory = list(json.loads(readtxt(get_home() + "/.config/deepin-wine-runner/FindExeHistory.json")).values())
    wineBottonHistory = list(json.loads(readtxt(get_home() + "/.config/deepin-wine-runner/WineBottonHistory.json")).values())
    isoPath = list(json.loads(readtxt(get_home() + "/.config/deepin-wine-runner/ISOPath.json")).values())
    isoPathFound = list(json.loads(readtxt(get_home() + "/.config/deepin-wine-runner/ISOPathFound.json")).values())
    setting = json.loads(readtxt(get_home() + "/.config/deepin-wine-runner/WineSetting.json"))
    change = False
    for i in ["Architecture", "Debug", "DefultWine", "DefultBotton", "TerminalOpen", "WineOption", "WineBottonDifferent"]:
        if not i in setting:
            change = True
            setting[i] = defultProgramList[i]
    if change:
        write_txt(get_home() + "/.config/deepin-wine-runner/WineSetting.json", json.dumps(setting))
except:
    root = tk.Tk()
    root.withdraw()
    tkinter.messagebox.showerror(title="错误", message="无法读取配置，无法继续")
    sys.exit(1)

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
updateThingsString = '''※1、新增程序感谢、谢明以及程序的建议和问题反馈和内置更新程序
※2、支持 winetricks 指定 Wine 打开
※3、新增窗口透明工具，感谢@a2035274 和 @虚幻的早晨 在论坛的讨论
※4、支持在指定容器、Wine 安装 MSXML
※5、支持启用/关闭 opengl（感谢@zhangs 在论坛发帖）以及支持安装/卸载 winbind
※6、添加云沙箱的网站链接快捷方式
※7、支持从星火应用商店源安装 Windows 常见字体
8、优化窗口布局以及默认显示位置
9、支持打开指定容器、Wine 的资源管理器
'''
title = "wine 运行器 {}".format(version)
updateTime = "2022年07月10日"
updateThings = "{} 更新内容：\n{}\n更新时间：{}".format(version, updateThingsString, updateTime, time.strftime("%Y"))
thankText = ""
for i in information["Thank"]:
    thankText += f"{i}\n"


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
win.title(title)  # 设置标题
window = tk.Frame()
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
#openWineBotton = ttk.Button(controlFrame, text="打开Wine容器目录", command=OpenWineBotton)
#installWineFont = ttk.Button(controlFrame, text="安装字体", command=OpenWineFontPath)
uninstallProgram = ttk.Button(controlFrame, text="卸载程序", command=UninstallProgram)
wineConfig = ttk.Button(controlFrame, text="配置wine容器", command=ConfigWineBotton)
sparkWineSetting = ttk.Button(controlFrame, text="星火wine设置", command=lambda: threading.Thread(target=os.system, args=["/opt/durapps/spark-dwine-helper/spark-dwine-helper-settings/settings.sh"]).start())
getProgramIcon = ttk.Button(controlFrame, text="获取选择的程序图标", command=lambda: threading.Thread(target=RunWineProgram, args=[f"{programPath}/Run.bat' '{programPath}/BeCyIconGrabber.exe' '{e2.get()}"]).start())
trasButton = ttk.Button(controlFrame, text="窗口透明度工具", command=lambda: threading.Thread(target=RunWineProgram, args=[programPath + "/窗体透明度设置工具.exe"]).start())
#winetricksOpen = ttk.Button(controlFrame, text="使用winetricks打开指定容器(只能使用wine和wine64)", command=lambda: threading.Thread(target=RunWinetricks).start())
button5 = ttk.Button(sendFrame, text="创建用于运行的 desktop 文件到桌面", command=make_desktop_on_desktop)  # 创建按钮控件
saveDesktopFileOnLauncher = ttk.Button(sendFrame, text="创建用于运行的 desktop 文件到启动器", command=make_desktop_on_launcher)  # 创建按钮控件
label1 = ttk.Label(window, text="选择你想要使用的 wine 容器：")  # 创建标签控件
label2 = ttk.Label(window, text="选择要启动的 Windows 应用")  # 创建标签控件
label3 = ttk.Label(window, text="选择要使用的 wine 版本：")  # 创建标签控件
label4 = ttk.Label(window, text="设置标题，以便把上方填写的信息写入到desktop文件里")  # 创建标签控件
e1 = ttk.Combobox(window, width=100)  # 创建文本框控件
e2 = ttk.Combobox(window, width=100)  # 创建文本框控件
combobox1 = ttk.Combobox(window, width=100)
o1 = ttk.OptionMenu(window, o1_text, setting["DefultWine"], *list(wine))  # 创建选择框控件
returnText = tk.Text(window, width=150)
menu = tk.Menu(window, background="white")  # 设置菜单栏
programmenu = tk.Menu(menu, tearoff=0, background="white")  # 设置“程序”菜单栏
menu.add_cascade(label="程序", menu=programmenu)
programmenu.add_command(label="安装 wine", command=InstallWine)
programmenu.add_separator()  # 设置分界线
programmenu.add_command(label="设置程序", command=ProgramSetting.ShowWindow)
programmenu.add_command(label="清空软件历史记录", command=CleanProgramHistory)
programmenu.add_separator()  # 设置分界线
programmenu.add_command(label="退出程序", command=window.quit)  # 设置“退出程序”项
wineOption = tk.Menu(menu, tearoff=0, background="white")  # 设置“Wine”菜单栏
menu.add_cascade(label="Wine", menu=wineOption)
wineOption.add_command(label="打开 Wine 容器目录", command=OpenWineBotton)
wineOption.add_command(label="安装常见字体", command=InstallWineFont)
wineOption.add_command(label="安装自定义字体", command=OpenWineFontPath)
wineOption.add_command(label="删除选择的 Wine 容器", command=DeleteWineBotton)
wineOption.add_separator()
wineOption.add_command(label="打包 wine 应用", command=BuildExeDeb)
wineOption.add_separator()
wineOption.add_command(label="从镜像获取DLL（只支持Windows XP、Windows Server 2003官方安装镜像）", command=GetDllFromWindowsISO.ShowWindow)
wineOption.add_separator()
wineOption.add_command(label="在指定wine、指定容器安装 .net framework", command=lambda: threading.Thread(target=InstallNetFramework).start())
wineOption.add_command(label="在指定wine、指定容器安装 Visual Studio C++", command=lambda: threading.Thread(target=InstallVisualStudioCPlusPlus).start())
wineOption.add_command(label="在指定wine、指定容器安装 MSXML", command=lambda: threading.Thread(target=InstallMSXML).start())
wineOption.add_command(label="在指定wine、指定容器安装 gecko", command=lambda: threading.Thread(target=InstallMonoGecko, args=["gecko"]).start())
wineOption.add_command(label="在指定wine、指定容器安装 mono", command=lambda: threading.Thread(target=InstallMonoGecko, args=["mono"]).start())
wineOption.add_command(label="在指定wine、指定容器安装其它运行库", command=lambda: threading.Thread(target=InstallOther).start())
wineOption.add_separator()
wineOption.add_command(label="打开指定wine、指定容器的控制面板", command=lambda: threading.Thread(target=RunWineProgram, args=["control"]).start())
wineOption.add_command(label="打开指定wine、指定容器的浏览器", command=lambda: threading.Thread(target=RunWineProgram, args=["iexplore' 'https://www.deepin.org"]).start())
wineOption.add_command(label="打开指定wine、指定容器的注册表", command=lambda: threading.Thread(target=RunWineProgram, args=["regedit"]).start())
wineOption.add_command(label="打开指定wine、指定容器的任务管理器", command=lambda: threading.Thread(target=RunWineProgram, args=["taskmgr"]).start())
wineOption.add_command(label="打开指定wine、指定容器的资源管理器", command=lambda: threading.Thread(target=RunWineProgram, args=["explorer"]).start())
wineOption.add_command(label="打开指定wine、指定容器的关于 wine", command=lambda: threading.Thread(target=RunWineProgram, args=["winver"]).start())
wineOption.add_separator()
wineOption.add_command(label="设置 run_v3.sh 的文管为 Deepin 默认文管", command=SetDeepinFileDialogDeepin)
wineOption.add_command(label="设置 run_v3.sh 的文管为 Wine 默认文管", command=SetDeepinFileDialogDefult)
wineOption.add_command(label="重新安装 deepin-wine-helper", command=SetDeepinFileDialogRecovery)
wineOption.add_separator()
wineOption.add_command(label="使用winetricks打开指定容器", command=lambda: threading.Thread(target=RunWinetricks).start())
wineOption.add_separator()
opengl = tk.Menu()
opengl.add_command(label="开启 opengl", command=lambda: threading.Thread(target=RunWineProgram, args=[f"regedit.exe' /s '{programPath}/EnabledOpengl.reg"]).start())
opengl.add_command(label="禁用 opengl", command=lambda: threading.Thread(target=RunWineProgram, args=[f"regedit.exe' /s '{programPath}/DisabledOpengl.reg"]).start())
wineOption.add_cascade(label="启用/禁用 opengl", menu=opengl)
winbind = tk.Menu()
winbind.add_command(label="安装 winbind", command=lambda: os.system(f"'{programPath}/launch.sh' deepin-terminal -C 'pkexec apt install winbind -y' --keep-open"))
winbind.add_command(label="卸载 winbind", command=lambda: os.system(f"'{programPath}/launch.sh' deepin-terminal -C 'pkexec apt purge winbind -y' --keep-open"))
wineOption.add_cascade(label="安装/卸载 winbind", menu=winbind)
safeWebsize = tk.Menu(menu, tearoff=0, background="white")
menu.add_cascade(label="云沙箱", menu=safeWebsize)
safeWebsize.add_command(label="360 沙箱云", command=lambda: webbrowser.open_new_tab("https://ata.360.net/"))
safeWebsize.add_command(label="微步云沙箱", command=lambda: webbrowser.open_new_tab("https://s.threatbook.cn/"))
safeWebsize.add_command(label="VIRUSTOTAL", command=lambda: webbrowser.open_new_tab("https://www.virustotal.com/"))

help = tk.Menu(menu, tearoff=0, background="white")  # 设置“帮助”菜单栏

menu.add_cascade(label="帮助", menu=help)
help.add_command(label="程序官网", command=OpenProgramURL)  # 设置“程序官网”项
help.add_separator()
help.add_command(label="小提示", command=helps)  # 设置“小提示”项
help.add_command(label="更新内容", command=UpdateThings)  # 设置“更新内容”项
help.add_command(label="谢明名单", command=ThankWindow)
help.add_separator()
help.add_command(label="更新这个程序", command=UpdateWindow.ShowWindow)
help.add_command(label="反馈这个程序的建议和问题", command=WineRunnerBugUpload)
help.add_command(label="关于这个程序", command=about_this_program)  # 设置“关于这个程序”项
help.add_separator()
moreProgram = tk.Menu(menu, tearoff=0, background="white")  
help.add_cascade(label="更多生态适配应用", menu=moreProgram)
moreProgram.add_command(label="运行 Android 应用：UEngine 运行器", command=lambda: webbrowser.open_new_tab("https://gitee.com/gfdgd-xi/uengine-runner"))
# 设置窗口
win.iconphoto(False, tk.PhotoImage(file=iconPath))
win.config(bg="white")
# 设置控件
e1.set(setting["DefultBotton"])
if len(sys.argv) > 1 and sys.argv[1]:
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
combobox1.grid(row=4, column=1)
button1.grid(row=0, column=2)
button2.grid(row=1, column=2)
controlFrame.grid(row=3, column=0, columnspan=3)
button3.grid(row=0, column=0)
killProgram.grid(row=0, column=1)
#openWineBotton.grid(row=0, column=2)
#installWineFont.grid(row=0, column=3)
uninstallProgram.grid(row=0, column=2)
wineConfig.grid(row=0, column=3)
sparkWineSetting.grid(row=0, column=4)
getProgramIcon.grid(row=0, column=5)
#winetricksOpen.grid(row=0, column=8)
trasButton.grid(row=0, column=6)
sendFrame.grid(row=5, column=0, columnspan=3)
button5.grid(row=0, column=0)
saveDesktopFileOnLauncher.grid(row=0, column=1)
o1.grid(row=2, column=1)
returnText.grid(row=6, column=0, columnspan=3)
# 启动窗口
window.pack(fill=tk.BOTH, expand = True)
# 窗口居中
win.update()
win.geometry(f"{win.winfo_width()}x{win.winfo_height()}+{win.winfo_screenwidth() // 2 - win.winfo_width() // 2}+{win.winfo_screenheight() // 2 - win.winfo_height() // 2}")
# 显示窗口
win.mainloop()
