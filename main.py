#!/usr/bin/env python3
#################
# 引入所需的库
#################
import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import os

def liulanbutton():
    path = tkinter.filedialog.askdirectory(title="选择 deepin-wine 容器", initialdir="~/.deepinwine/")
    if path != "":
        e1_text.set(path)

def liulanexebutton():
    path = tkinter.filedialog.askopenfilename(title="选择 exe 可执行文件", filetypes=[("exe 可执行文件", "*.exe"), ("所有文件", "*.*")], initialdir="~/")
    if path != "":
        e2_text.set(path)

def runexebutton():
    if e1_text.get() == "" or e2_text.get() == "":
        tkinter.messagebox.showinfo(title="提示",message="没有填写需要使用的 deepin-wine 容器或需要运行的 exe 应用")
    else:
        print("###############################")
        os.system('WINEPREFIX=' + e1_text.get() + ' ' + o1_text.get() + ' "' + e2_text.get() + '"')

# 显示“关于这个程序”窗口
def about_this_program():
    tkinter.messagebox.showinfo(title="关于这个程序",message="一个基于 Python3 的 tkinter 制作的 deepin-wine 运行器\n版本：1.0\n适用平台：Linux")

# 显示“提示”窗口
def helps():
    tkinter.messagebox.showinfo(title="提示", message="提示：\n1、使用终端运行该程序，可以看到 deepin-wine（deepin-wine5） 的提示和报错\n2、暂不支持 deepin-wine（deepin-wine5） 容器路径含有空格，如有请在空格前加“\\”进行转义")

window = tk.Tk()
window.title("deepin-wine 运行器")
e1_text = tk.StringVar()
e2_text = tk.StringVar()
o1_text = tk.StringVar()
o1_text.set("deepin-wine")
label1 = tk.Label(window, text="选择你想要使用的 deepin-wine 容器：")
e1 = tk.Entry(window, textvariable=e1_text, width=100)
button1 = tk.Button(window, text="浏览", command=liulanbutton)
label2 = tk.Label(window, text="选择要启动的 Windows 应用")
e2 = tk.Entry(window, textvariable=e2_text, width=100)
button2 = tk.Button(window, text="浏览", command=liulanexebutton)
label3 = tk.Label(window, text="选择要使用的 deepin-wine 版本")
o1 = tk.OptionMenu(window, o1_text, "deepin-wine", "deepin-wine5")
button3 = tk.Button(window, text="启动", command=runexebutton)
menu = tk.Menu(window) # 设置菜单栏
programmenu = tk.Menu(menu,tearoff=0) # 设置“程序”菜单栏
menu.add_cascade(label="程序",menu=programmenu)
programmenu.add_command(label="退出程序",command=window.quit) # 设置“退出程序”项
help = tk.Menu(menu,tearoff=0) # 设置“帮助”菜单栏
menu.add_cascade(label="帮助",menu=help)
help.add_command(label="小提示",command=helps) # 设置“小提示”项
help.add_separator() # 设置分界线
help.add_command(label="关于这个程序",command=about_this_program) # 设置“关于这个程序”项
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
window.mainloop()