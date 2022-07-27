import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("wine运行器1.6.0")
root.geometry("1275x900")

frame_up = tk.Frame(root)
frame_left = tk.Frame(frame_up)#快速启动区
frame_left.config(bd=30)
#
frame_left_1 = tk.Frame(frame_left)#左侧标题
left_title = tk.Label(frame_left_1,text="快速启动")
left_title.config(font=("幼圆",24))
left_title.pack(anchor="w")
frame_left_1.grid(row=0,sticky="w" + "e")
#
frame_left_2 = tk.Frame(frame_left)#容器路径
##
label_l_1 = tk.Label(frame_left_2,text="请选择容器的路径:")
label_l_1.config(font=("幼圆",16))
label_l_1.grid(row=0,column=0,sticky='w')
##
combo_l_1 = ttk.Combobox(frame_left_2, width=50)
combo_l_1.grid(row=1,column=0)
##
button_l_1 = tk.Button(frame_left_2,text="浏览")
button_l_1.config(font=("幼圆",12),padx=20,pady=3)
button_l_1.grid(row=1,column=1)
##
frame_left_2.grid(row=1)
#
frame_left_3 = tk.Frame(frame_left)#程序路径
label_l_2 = tk.Label(frame_left_3,text="请选择待执行程序:")
label_l_2.config(font=("幼圆",16))
label_l_2.grid(row=0,column=0,sticky='w')
##
combo_l_2 = ttk.Combobox(frame_left_3, width=50)
combo_l_2.grid(row=1,column=0)
##
button_l_2 = tk.Button(frame_left_3,text="浏览")
button_l_2.config(font=("幼圆",12),padx=20,pady=3)
button_l_2.grid(row=1,column=1)
##
frame_left_3.grid(row=2)
#
frame_left_4 = tk.Frame(frame_left)#wine的版本
##
label_l_3 = tk.Label(frame_left_4,text="请选择wine的版本")
label_l_3.config(font=("幼圆",16))
label_l_3.grid(row=0,column=0,sticky='w')
##
OptionList = ["deppin-wine5","wine"]
variable = tk.StringVar(frame_left_4)
variable.set(OptionList[0])
choose_1 = tk.OptionMenu(frame_left_4,variable,*OptionList)
choose_1.grid(row=1,column=0)
##
label_l_4 = tk.Label(frame_left_4,text=" "*4)#占位用字符串
label_l_4.grid(row=1,column=1)
##
button_l_3 = tk.Button(frame_left_4,text="运行程序")
button_l_3.config(font=("幼圆",12),padx=21,pady=3)
button_l_3.grid(row=1,column=2)
##
label_l_5 = tk.Label(frame_left_4,text=" "*13)#占位用字符串
label_l_5.grid(row=1,column=3)
##
button_l_4 = tk.Button(frame_left_4,text="终止程序")
button_l_4.config(font=("幼圆",12),padx=21,pady=3)
button_l_4.grid(row=1,column=4)
##
frame_left_4.grid(row=3)
#
frame_left.grid(row=0,column=0)#第一行第一列

frame_right = tk.Frame(frame_up)#高级配置区
frame_right.config(bd=30)
#
frame_right_1 = tk.Frame(frame_right)
right_title = tk.Label(frame_right_1,text="高级功能")
right_title.config(font=("幼圆",24))
right_title.pack(anchor="w")
frame_right_1.grid(row=0,sticky="w" + "e")
#
frame_right_2 = tk.Frame(frame_right)
##
label_r_1 = tk.Label(frame_right_2,text="创建快捷方式(Desktop文件):")
label_r_1.config(font=("幼圆",16))
label_r_1.grid(row=0,column=0)
##
frame_right_2.grid(row=1,sticky='w')
#
frame_right_3 = tk.Frame(frame_right)
##
label_r_2 = tk.Label(frame_right_3,text="名称:")
label_r_2.config(font=("幼圆",14))
label_r_2.grid(row=0,column=0)
##
entry1 = tk.Entry(frame_right_3,width=15)
entry1.grid(row=0,column=1)
##
empty1 = tk.Label(frame_right_3,text=" "*5)
empty1.grid(row=0,column=2)
##
button_r_1 = tk.Button(frame_right_3,text="创建到桌面")
button_r_1.config(font=("幼圆",12),padx=20,pady=3)
button_r_1.grid(row=0,column=3)
##
empty2 = tk.Label(frame_right_3,text=" "*5)
empty2.grid(row=0,column=4)
##
button_r_2 = tk.Button(frame_right_3,text="创建到开始菜单")
button_r_2.config(font=("幼圆",12),padx=20,pady=3)
button_r_2.grid(row=0,column=5)
##
frame_right_3.grid(row=2,sticky='w')
#
frame_right_4 = tk.Frame(frame_right)
##
label_r_2 = tk.Label(frame_right_4,text="管理该程序:")
label_r_2.config(font=("幼圆",16))
label_r_2.grid(row=0,column=0)
##
frame_right_4.grid(row=3,sticky='w')
#
frame_right_5 = tk.Frame(frame_right)
##
button_r_3 = tk.Button(frame_right_5,text="卸载程序")
button_r_3.config(font=("幼圆",12),padx=20,pady=3)
button_r_3.grid(column=0)
##
empty3 = tk.Label(frame_right_5,text=" "*5)
empty3.grid(row=0,column=1)
##
button_r_4 = tk.Button(frame_right_5,text="提取图标")
button_r_4.config(font=("幼圆",12),padx=20,pady=3)
button_r_4.grid(row=0,column=2)
##
frame_right_5.grid(row=4,sticky='w')
#
frame_right_6 = tk.Frame(frame_right)
##
label_r_3 = tk.Label(frame_right_6,text="管理该wine")
label_r_3.config(font=("幼圆",16))
label_r_3.grid(row=0,column=0)
##
frame_right_6.grid(row=5,sticky='w')
#
frame_right_7 = tk.Frame(frame_right)
##
button_r_5 = tk.Button(frame_right_7,text="配置容器")
button_r_5.config(font=("幼圆",12),padx=20,pady=3)
button_r_5.grid(row=0,column=0)
##
empty4 = tk.Label(frame_right_7,text=" "*5)
empty4.grid(row=0,column=1)
##
button_r_6 = tk.Button(frame_right_7,text="安装字体")
button_r_6.config(font=("幼圆",12),padx=20,pady=3)
button_r_6.grid(row=0,column=2)
##
frame_right_7.grid(row=6,sticky='w')
#
frame_right.grid(row=0,column=1,sticky='n')#第一行第二列

frame_up.grid(row=0,sticky='w')

frame_down = tk.Frame(root,bd=30)
returnText = tk.Text(frame_down,width=120)
returnText.insert("end", "此可以查看到 Wine 应用安装时的程序返回值")
returnText.config(state=tk.DISABLED)
returnText.grid(row=0,column=0,sticky='e'+'w')
frame_down.grid(row=1,sticky='w')

root.mainloop()