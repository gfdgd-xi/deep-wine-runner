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
import json
import os
import sys
import ttkthemes
import threading
import tkinter as tk
import tkinter.ttk as ttk

# 读取文本文档
def readtxt(path):
    f = open(path, "r") # 设置文件对象
    str = f.read()  # 获取内容
    f.close()  # 关闭文本对象
    return str  # 返回结果

def Unzip():
    os.system("mkdir -p ~")
    os.chdir(f"{homePath}")
    os.system(f"unzip -o \"{programPath}/package-script.zip\"")
    window.quit()
    print("Unzip Done")
    ReStartProgram()

# 重启本应用程序
def ReStartProgram():
    python = sys.executable
    os.execl(python, python, * sys.argv)

programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
homePath = os.path.expanduser('~')
information = json.loads(readtxt(f"{programPath}/information.json"))
version = information["Version"]
if not os.path.exists(f"{homePath}/package-script") or not json.loads(readtxt(f"{homePath}/package-script/information.json"))["Version"] == version:
    print("未检测到指定文件，解压文件")
    # 读取主题
    try:
        theme = not ("dark" in readtxt(homePath + "/.gtkrc-2.0") and "gtk-theme-name=" in readtxt(homePath + "/.gtkrc-2.0"))
    except:
        print("主题读取错误，默认使用浅色主题")
        theme = True
    if theme:
        window = tk.Tk()
        themes = ttkthemes.ThemedStyle(window)
        themes.set_theme("breeze")
    else:
        import ttkbootstrap
        style = ttkbootstrap.Style(theme="darkly")
        window = style.master  # 创建窗口
    window.title("解压中")
    ttk.Label(window, text="正在解压所需程序，请稍后……").pack()
    progress = ttk.Progressbar(window, mode='indeterminate')
    progress.start()
    progress.pack()
    # 解压流程
    t = threading.Thread(target=Unzip)
    t.start()
    window.mainloop()
os.chdir(f"{homePath}/package-script")
os.system("python3 main.py")
print("End")
