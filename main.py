#!/usr/bin/env python3
#########################################################################
# 作者：gfdgd xi
# 版本：1.1.1
# 感谢：感谢 deepin-wine 团队，提供了 deepin-wine 给大家使用，让我能做这个程序
# 基于 Python3 的 tkinter 构建
#########################################################################
#################
# 引入所需的库
#################
import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import os
import threading

###################
# 程序所需事件
###################
# 读取文本文档
def readtxt(path):
    f = open(path, "r") # 设置文件对象
    str = f.read() # 获取内容
    f.close() # 关闭文本对象
    return str # 返回结果

# 写入文本文档
def write_txt(path, things):
    file = open(path, 'a+', encoding='UTF-8') # 设置文件对象
    file.write(things) # 写入文本
    file.close() # 关闭文本对象

# 获取用户桌面目录
def get_desktop_path():
    for line in open(get_home() + "/.config/user-dirs.dirs"): # 以行来读取配置文件
        desktop_index = line.find("XDG_DESKTOP_DIR=\"") # 寻找是否有对应项，有返回 0，没有返回 -1
        if desktop_index != -1: # 如果有对应项
            break # 结束循环
    if desktop_index == -1: # 如果是提前结束，值一定≠-1，如果是没有提前结束，值一定＝-1
        return -1
    else:
        get = line[17:-2] # 截取桌面目录路径
        get_index = get.find("$HOME") # 寻找是否有对应的项，需要替换内容
        if get != -1: # 如果有
            get = get.replace("$HOME", get_home()) # 则把其替换为用户目录（～）
        return get # 返回目录

# 获取用户主目录
def get_home():
    return os.path.expanduser('~')

# 第一个浏览按钮事件
def liulanbutton():
    path = tkinter.filedialog.askdirectory(title="选择 deepin-wine 容器", initialdir="~/.deepinwine/")
    if path != "":
        e1_text.set(path)

# 第二个浏览按钮事件
def liulanexebutton():
    path = tkinter.filedialog.askopenfilename(title="选择 exe 可执行文件", filetypes=[("exe 可执行文件", "*.exe"), ("所有文件", "*.*")], initialdir="~/")
    if path != "":
        e2_text.set(path)

# 
def runexebutton():
    run = threading.Thread(target = runexebutton_threading)
    run.start()

# 运行可执行文件的线程
def runexebutton_threading():
    if e1_text.get() == "" or e2_text.get() == "": # 判断文本框是否有内容
        tkinter.messagebox.showinfo(title="提示",message="没有填写需要使用的 deepin-wine 容器或需要运行的 exe 应用")
    else: # 如果都有
        print("###############################")
        os.system("WINEPREFIX='" + e1_text.get() + "' " + o1_text.get() + " '" + e2_text.get() + "'") # 运行

# 显示“关于这个程序”窗口
def about_this_program():
    tkinter.messagebox.showinfo(title="关于这个程序",message="一个基于 Python3 的 tkinter 制作的 deepin-wine（deepin-wine5） 运行器\n版本：1.1\n适用平台：Linux\ntkinter 版本：" + str(tk.TkVersion))

# 显示“提示”窗口
def helps():
    tkinter.messagebox.showinfo(title="提示", message="提示：\n1、使用终端运行该程序，可以看到 deepin-wine（deepin-wine5） 以及程序本身的提示和报错")

# 生成 shell 文件在桌面
# （第四个按钮的事件）
def make_desktop_on_desktop():
    if e3_text.get() == "" or e2_text.get() == "" or e1_text.get() == "": # 判断文本框是否有内容
        tkinter.messagebox.showinfo(title="提示",message="没有填写需要使用的 deepin-wine 容器或需要运行的 exe 应用或保存的文件名")
    else: # 如果都有
        if os.path.exists(get_desktop_path() + "/" + e3_text.get() + ".sh"): # 判断目录是否有该文件，如果有
            choose = tkinter.messagebox.askokcancel(title="提示",message="文件已经存在，是否覆盖？")  # 询问用户是否覆盖
            if choose: # 如要覆盖
                os.remove(get_desktop_path() + "/" + e3_text.get() + ".sh") # 删除该文件
            else: # 如不覆盖
                return # 结束
        os.mknod(get_desktop_path() + "/" + e3_text.get() + ".sh") # 创建文本文档
        write_txt(get_desktop_path() + "/" + e3_text.get() + ".sh", "#!/bin/bash\n" + "WINEPREFIX='" + e1_text.get() + "' " + o1_text.get() + " '" + e2_text.get() + "'") # 写入文本文档
        os.system("chmod 777 '" + get_desktop_path() + "/" + e3_text.get() + ".sh" + "'") # 赋予可执行权限
        tkinter.messagebox.showinfo(title="提示", message="生成完成！") # 显示完成对话框

###########################
# 窗口创建
###########################
window = tk.Tk() # 创建窗口
window.title("deepin-wine 运行器") # 设置标题
# 设置变量以修改和获取值项
e1_text = tk.StringVar()
e2_text = tk.StringVar()
o1_text = tk.StringVar()
e3_text = tk.StringVar()
o1_text.set("deepin-wine")
# 创建控件
label1 = tk.Label(window, text="选择你想要使用的 deepin-wine 容器：") # 创建标签控件
e1 = tk.Entry(window, textvariable=e1_text, width=100) # 创建文本框控件
button1 = tk.Button(window, text="浏览", command=liulanbutton) # 创建按钮控件
label2 = tk.Label(window, text="选择要启动的 Windows 应用") # 创建标签控件
e2 = tk.Entry(window, textvariable=e2_text, width=100) # 创建文本框控件
button2 = tk.Button(window, text="浏览", command=liulanexebutton) # 创建按钮控件
label3 = tk.Label(window, text="选择要使用的 deepin-wine 版本") # 创建标签控件
o1 = tk.OptionMenu(window, o1_text, "deepin-wine", "deepin-wine5") # 创建选择框控件
button3 = tk.Button(window, text="启动", command=runexebutton) # 创建按钮控件
label4 = tk.Label(window, text="设置文件名，以便把上方填写的信息写入到 shell 文件里") # 创建标签控件
e3 = tk.Entry(window, textvariable=e3_text, width=100) # 创建文本框控件
button5 = tk.Button(window, text="创建用于运行的 shell 文件到桌面", command=make_desktop_on_desktop) # 创建按钮控件
menu = tk.Menu(window) # 设置菜单栏
programmenu = tk.Menu(menu,tearoff=0) # 设置“程序”菜单栏
menu.add_cascade(label="程序",menu=programmenu)
programmenu.add_command(label="退出程序",command=window.quit) # 设置“退出程序”项
help = tk.Menu(menu,tearoff=0) # 设置“帮助”菜单栏
menu.add_cascade(label="帮助",menu=help)
help.add_command(label="小提示",command=helps) # 设置“小提示”项
help.add_separator() # 设置分界线
help.add_command(label="关于这个程序",command=about_this_program) # 设置“关于这个程序”项
# 添加控件
window.config(menu=menu) # 显示菜单栏
label1.pack()
e1.pack()
button1.pack()
label2.pack()
e2.pack()
button2.pack()
label3.pack()
o1.pack()
button3.pack()
label4.pack()
e3.pack()
button5.pack()
# 启动窗口
window.mainloop()
