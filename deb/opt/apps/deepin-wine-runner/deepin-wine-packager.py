#!/usr/bin/env python3
#########################################################################
# 作者：gfdgd xi、为什么您不喜欢熊出没和阿布
# 版本：1.5.2
# 感谢：感谢 deepin-wine 团队，提供了 deepin-wine 给大家使用，让我能做这个程序
# 基于 Python3 的 tkinter 构建
#########################################################################
#################
# 引入所需的库
#################
import os
import sys
import json
import shutil
import random
import pathlib
import ttkthemes
import threading
import traceback
import subprocess
from PIL import Image
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
import tkinter.filedialog as filedialog

#################
# 程序所需事件
#################

def button1_cl():
    path = filedialog.askdirectory(title="选择 wine 容器", initialdir="~/.deepinwine")
    if path != "":
        e6_text.set(path)

def button2_cl():
    path = filedialog.askopenfilename(filetypes=[("PNG图标", "*.png"), ("SVG图标", "*.svg"), ("全部文件", "*.*")], title="选择图标文件", initialdir="~")
    if path != "":
        e9_text.set(path)

def button4_cl():
    path = filedialog.asksaveasfilename(filetypes=[("deb 文件", "*.deb"), ("所有文件", "*.*")], title="保存 deb 包", initialdir="~", initialfile="{}_{}_i386.deb".format(e1_text.get(), e2_text.get()))
    if path != "":
        e12_text.set(path)

def disabled_or_NORMAL_all(choose):
    chooses = {True: tk.NORMAL, False: tk.DISABLED}
    a = chooses[choose]
    label1.configure(state=a)
    label2.configure(state=a)
    label3.configure(state=a)
    label4.configure(state=a)
    label5.configure(state=a)
    label6.configure(state=a)
    label7.configure(state=a)
    label8.configure(state=a)
    label9.configure(state=a)
    label10.configure(state=a)
    label12.configure(state=a)
    label14.configure(state=a)
    label15.configure(state=a)
    e1.configure(state=a)
    e2.configure(state=a)
    e3.configure(state=a)
    e4.configure(state=a)
    e5.configure(state=a)
    e6.configure(state=a)
    e7.configure(state=a)
    e8.configure(state=a)
    e9.configure(state=a)
    e10.configure(state=a)
    e12.configure(state=a)
    e15.configure(state=a)
    button1.config(state=a)
    button2.config(state=a)
    button4.config(state=a)
    button5.config(state=a)
    option1.config(state=a)

def make_deb():
    clean_textbox1_things()
    disabled_or_NORMAL_all(False)
    if e1_text.get() == "" or e2_text.get() == "" or e3_text.get() == "" or e4_text.get() == "" or e5_text.get() == "" or e6_text.get() == "" or e7_text.get() == "" or e8_text.get() == "" or e12_text.get() == "":
        messagebox.showinfo(title="提示", message="必填信息没有填写完整，无法继续构建 deb 包")
        disabled_or_NORMAL_all(True)
        label13_text_change("必填信息没有填写完整，无法继续构建 deb 包")
        return
    thread = threading.Thread(target=make_deb_threading)
    thread.start()

def label13_text_change(thing):
    label13_text.set("当前 deb 打包情况：{}".format(thing))

def make_deb_threading():
    #####################################
    # 程序创建的 deb 构建临时文件夹目录树：
    # /XXX
    # ├── DEBIAN
    # │   └── control
    # └── opt
    # └── apps
    #     └── XXX
    #         ├── entries
    #         │   ├── applications
    #         │   │   └── XXX.desktop
    #         │   └── icons
    #         │       └── hicolor
    #         │           └── scalable
    #         │               └── apps
    #         │                   └── XXX.png（XXX.svg）
    #         ├── files
    #         │   ├── files.7z
    #         │   └── run.sh
    #         └── info
    #
    # 11 directories, 6 files
    #####################################
    try:
        #####################
        # 判断文件是否存在
        #####################
        label13_text_change("正在检查文件是否存在并为后面步骤准备……")
        a = ""
        if e6_text.get() == "/":
            b = e6_text.get()[:-1]
        else:
            b = e6.get()
        if e9_text.get() != "":
            # 获取图片格式（不太准）
            try:
                im = Image.open(e9_text.get())
                imms = im.format.lower()
            except: # 未知（就直接设置为 svg 后缀）
                imms = ".svg"
            a = "/opt/apps/{}/entries/icons/hicolor/scalable/apps/{}.{}".format(e1_text.get(), e1_text.get(), imms)
            if not os.path.exists(e9_text.get()):
                messagebox.showerror(title="提示", message="图标的路径填写错误，无法进行构建 deb 包")
                disabled_or_NORMAL_all(True)
                label13_text_change("图标的路径填写错误，无法进行构建 deb 包")
                return
        if not os.path.exists(e6_text.get()):
            messagebox.showerror(title="提示", message="路径填写错误，无法继续构建 deb 包")
            disabled_or_NORMAL_all(True)
            label13_text_change("图标的路径填写错误，无法进行构建 deb 包")
            return
        #############
        # 删除文件
        #############
        label13_text_change("正在删除对构建 deb 包有影响的文件……")
        debPackagePath = f"/tmp/{random.randint(0, 9999)}"
        run_command(f"rm -rfv /tmp/{debPackagePath}")
        ###############
        # 创建目录
        ###############
        label13_text_change("正在创建目录……")
        os.makedirs("{}/DEBIAN".format(debPackagePath))
        os.makedirs("{}/opt/apps/{}/entries/applications".format(debPackagePath, e1_text.get()))
        os.makedirs("{}/opt/apps/{}/entries/icons/hicolor/scalable/apps".format(debPackagePath, e1_text.get()))
        os.makedirs("{}/opt/apps/{}/files".format(debPackagePath, e1_text.get()))
        ###############
        # 创建文件
        ###############
        label13_text_change("正在创建文件……")
        os.mknod("{}/DEBIAN/control".format(debPackagePath))
        os.mknod("{}/opt/apps/{}/entries/applications/{}.desktop".format(debPackagePath, e1_text.get(), e1_text.get()))
        os.mknod("{}/opt/apps/{}/files/run.sh".format(debPackagePath, e1_text.get()))
        os.mknod("{}/opt/apps/{}/info".format(debPackagePath, e1_text.get()))
        ###############
        # 压缩容器
        ###############
        label13_text_change("正在打包 wine 容器")
        run_command("7z a {}/opt/apps/{}/files/files.7z {}/*".format(debPackagePath, e1_text.get(), b))
        ###############
        # 复制图片
        ###############
        label13_text_change("正在复制文件……")
        run_command(f"cp -rv '{programPath}/dlls' {debPackagePath}/opt/apps/{e1_text.get()}/files/")
        if e9_text.get() != "":
            shutil.copy(e9_text.get(), "{}/opt/apps/{}/entries/icons/hicolor/scalable/apps/{}.{}".format(debPackagePath, e1_text.get(), e1_text.get(), imms))
        ################
        # 获取文件大小
        ################
        label13_text_change("正在计算文件大小……")
        size = getFileFolderSize(debPackagePath) / 1024
        ################
        # 写入文本文档
        ################
        label13_text_change("正在写入文件……")
        if not bool(chooseWineHelperValue.get()):
            write_txt("{}/DEBIAN/control".format(debPackagePath), '''Package: {}
Version: {}
Architecture: i386
Maintainer: {}
Depends: {}, deepin-wine-helper (>= 5.1.30-1), fonts-wqy-microhei, fonts-wqy-zenhei
Section: non-free/otherosfs
Priority: optional
Multi-Arch: foreign
Description: {}
'''.format(e1_text.get(), e2_text.get(), e4_text.get(), wineVersion.get(), e3_text.get()))
        else:
            write_txt("{}/DEBIAN/control".format(debPackagePath), '''Package: {}
Version: {}
Architecture: i386
Maintainer: {}
Depends: {}, spark-dwine-helper (>= 1.6.2), fonts-wqy-microhei, fonts-wqy-zenhei
Section: non-free/otherosfs
Priority: optional
Multi-Arch: foreign
Description: {}
'''.format(e1_text.get(), e2_text.get(), e4_text.get(), wineVersion.get(), e3_text.get()))
        write_txt("{}/opt/apps/{}/entries/applications/{}.desktop".format(debPackagePath, e1_text.get(), e1_text.get()), '#!/usr/bin/env xdg-open\n[Desktop Entry]\nEncoding=UTF-8\nType=Application\nX-Created-By={}\nCategories={};\nIcon={}\nExec="/opt/apps/{}/files/run.sh" {}\nName={}\nComment={}\nMimeType={}\nGenericName={}\nTerminal=false\nStartupNotify=false\n'.format(e4_text.get(), option1_text.get(), a, e1_text.get(), e15_text.get(), e8_text.get(), e3_text.get(), e10_text.get(), e1_text.get()))
        if not bool(chooseWineHelperValue.get()):
            write_txt("{}/opt/apps/{}/files/run.sh".format(debPackagePath, e1_text.get()), '''#!/bin/sh

#   Copyright (C) 2016 Deepin, Inc.
#
#   Author:     Li LongYu <lilongyu@linuxdeepin.com>
#               Peng Hao <penghao@linuxdeepin.com>

version_gt() {{ test "$(echo "$@" | tr " " "\\n" | sort -V | head -n 1)" != "$1"; }}

BOTTLENAME="{}"
APPVER="{}"
EXEC_PATH="{}"
START_SHELL_PATH="/opt/deepinwine/tools/run_v4.sh"
export MIME_TYPE=""
export DEB_PACKAGE_NAME="{}"
export APPRUN_CMD="{}"
DISABLE_ATTACH_FILE_DIALOG=""
EXPORT_ENVS=""

export SPECIFY_SHELL_DIR=`dirname $START_SHELL_PATH`

ARCHIVE_FILE_DIR="/opt/apps/$DEB_PACKAGE_NAME/files"

export WINEDLLPATH=/opt/$APPRUN_CMD/lib:/opt/$APPRUN_CMD/lib64

export WINEPREDLL="$ARCHIVE_FILE_DIR/dlls"

if [ -z "$DISABLE_ATTACH_FILE_DIALOG" ];then
    export ATTACH_FILE_DIALOG=1
fi

if [ -n "$EXPORT_ENVS" ];then
    export $EXPORT_ENVS
fi

if [ -n "$EXEC_PATH" ];then
    if [ -z "${{EXEC_PATH##*.lnk*}}" ];then
        $START_SHELL_PATH $BOTTLENAME $APPVER "C:/windows/command/start.exe" "/Unix" "$EXEC_PATH" "$@"
    else
        $START_SHELL_PATH $BOTTLENAME $APPVER "$EXEC_PATH" "$@"
    fi
else
    $START_SHELL_PATH $BOTTLENAME $APPVER "uninstaller.exe" "$@"
fi
'''.format(e5_text.get(), e2_text.get(), e7_text.get(), e1_text.get(), wineVersion.get()))
        else:
            write_txt("{}/opt/apps/{}/files/run.sh".format(debPackagePath, e1_text.get()), '''#!/bin/sh

#   Copyright (C) 2016 Deepin, Inc.
#
#   Author:     Li LongYu <lilongyu@linuxdeepin.com>
#               Peng Hao <penghao@linuxdeepin.com>

#######################函数段。下文调用的额外功能会在此处声明

Get_Dist_Name()
{{
    if grep -Eqii "Deepin" /etc/issue || grep -Eq "Deepin" /etc/*-release; then
        DISTRO='Deepin'
    elif grep -Eqi "UnionTech" /etc/issue || grep -Eq "UnionTech" /etc/*-release; then
        DISTRO='UniontechOS'
    else
	 DISTRO='OtherOS'
	fi
}}

####获得发行版名称

version_gt() {{ test "$(echo "$@" | tr " " "\n" | sort -V | head -n 1)" != "$1"; }}

BOTTLENAME="{}"
APPVER="{}"
EXEC_PATH="{}"
START_SHELL_PATH="/opt/deepinwine/tools/spark_run_v4.sh"
export MIME_TYPE=""
export DEB_PACKAGE_NAME="{}"
export APPRUN_CMD="{}"
EXPORT_ENVS=""

export SPECIFY_SHELL_DIR=`dirname $START_SHELL_PATH`

ARCHIVE_FILE_DIR="/opt/apps/$DEB_PACKAGE_NAME/files"

export WINEDLLPATH=/opt/$APPRUN_CMD/lib:/opt/$APPRUN_CMD/lib64

export WINEPREDLL="$ARCHIVE_FILE_DIR/dlls"

DISABLE_ATTACH_FILE_DIALOG=""

Get_Dist_Name

if [ "$DISTRO" != "Deepin" ] && [ "$DISTRO" != "UniontechOS" ];then
DISABLE_ATTACH_FILE_DIALOG="1"
echo "非deepin/UOS，默认关闭系统自带的文件选择工具，使用Wine的"
echo "如果你想改变这个行为，请到/opt/apps/$DEB_PACKAGE_NAME/files/$0处修改"
echo "To打包者：如果你要打开自带请注意在适配的发行版上进行测试"
echo "To用户：打包者没有打开这个功能，这证明启用这个功能可能造成运行问题。如果你要修改这个行为，请确保你有一定的动手能力"
fi

if [ -z "$DISABLE_ATTACH_FILE_DIALOG" ];then
    export ATTACH_FILE_DIALOG=1
fi

if [ -n "$EXPORT_ENVS" ];then
    export $EXPORT_ENVS
fi

if [ -n "$EXEC_PATH" ];then
    if [ -z "${{EXEC_PATH##*.lnk*}}" ];then
        $START_SHELL_PATH $BOTTLENAME $APPVER "C:/windows/command/start.exe" "/Unix" "$EXEC_PATH" "$@"
    else
        $START_SHELL_PATH $BOTTLENAME $APPVER "$EXEC_PATH" "$@"
    fi
else
    $START_SHELL_PATH $BOTTLENAME $APPVER "uninstaller.exe" "$@"
fi
'''.format(e5_text.get(), e2_text.get(), e7_text.get(), e1_text.get(), wineVersion.get()))
        write_txt("{}/opt/apps/{}/info".format(debPackagePath, e1_text.get()), '{\n    "appid": "' + e1_text.get() + '",\n    "name": "' + e8_text.get() + '",\n    "version": "' + e2_text.get() + '",\n    "arch": ["i386"],\n    "permissions": {\n        "autostart": false,\n        "notification": false,\n        "trayicon": true,\n        "clipboard": true,\n        "account": false,\n        "bluetooth": false,\n        "camera": false,\n        "audio_record": false,\n        "installed_apps": false\n    }\n}')
        ################
        # 修改文件权限
        ################
        label13_text_change("正在修改文件权限……")
        run_command("chmod -Rv 644 {}/opt/apps/{}/files/run.sh".format(debPackagePath, e1_text.get()))
        run_command("chmod -Rv 644 {}/opt/apps/{}/info".format(debPackagePath, e1_text.get()))
        run_command("chmod -Rv 755 {}/opt/apps/{}/files/run.sh".format(debPackagePath, e1_text.get()))
        ################
        # 构建 deb 包
        ################
        label13_text_change("正在构建 deb 包……")
        run_command("dpkg -b {} {}".format(debPackagePath, e12_text.get()))
        ################
        # 完成构建
        ################
        label13_text_change("完成构建！")
        disabled_or_NORMAL_all(True)
    except Exception as e:
        messagebox.showerror(title="错误", message="程序出现错误，错误信息：\n{}".format(traceback.format_exc()))
        traceback.print_exc()
        label13_text_change("deb 包构建出现错误：{}".format(repr(e)))
        chang_textbox1_things(traceback.format_exc())
        disabled_or_NORMAL_all(True)

# 写入文本文档
def write_txt(path, things):
    file = open(path, 'a+', encoding='UTF-8')  # 设置文件对象
    file.write(things)  # 写入文本
    file.close()  # 关闭文本对象

def chang_textbox1_things(things):
    textbox1.configure(state=tk.NORMAL)
    textbox1.insert('end', things)
    textbox1.configure(state=tk.DISABLED)

def clean_textbox1_things():
    textbox1.configure(state=tk.NORMAL)
    textbox1.delete('1.0','end')
    textbox1.configure(state=tk.DISABLED)

def run_command(command):
    res = subprocess.Popen([command], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # 实时读取程序返回
    while res.poll() is None:
        try:
            text = res.stdout.readline().decode("utf8")
        except:
            text = ""
        print(text)
        chang_textbox1_things(text)


def getFileFolderSize(fileOrFolderPath):
    """get size for file or folder"""
    totalSize = 0
    if not os.path.exists(fileOrFolderPath):
        return totalSize
    if os.path.isfile(fileOrFolderPath):
        totalSize = os.path.getsize(fileOrFolderPath)  # 5041481
        return totalSize
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

# 显示“提示”窗口
def helps():
    messagebox.showinfo(title="提示", message=tips)

# 读取文本文档
def readtxt(path):
    f = open(path, "r") # 设置文件对象
    str = f.read()  # 获取内容
    f.close()  # 关闭文本对象
    return str  # 返回结果

###############
# 程序信息
###############
# 如果要添加其他 wine，请在字典添加其名称和执行路径
wine = {"deepin-wine": "deepin-wine", "deepin-wine5": "deepin-wine5", "wine": "wine", "wine64": "wine64", "deepin-wine5 stable": "deepin-wine5-stable", "deepin-wine6 stable": "deepin-wine6-stable", "spark-wine7-devel": "spark-wine7-devel", "ukylin-wine": "ukylin-wine"}
programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
iconPath = "{}/icon.png".format(programPath)
information = json.loads(readtxt(f"{programPath}/information.json"))
version = information["Version"]
tips = """提示：
1、deb 打包软件包名要求：
软件包名只能含有小写字母(a-z)、数字(0-9)、加号(+)和减号(-)、以及点号(.)，软件包名最短长度两个字符；它必须以字母开头
2、如果要填写路径，有“浏览……”按钮的是要填本计算机对应文件的路径，否则就是填写安装到其他计算机使用的路径
3、输入 wine 的容器路径时最后面请不要输入“/”
4、输入可执行文件的运行路径时是以“C:/XXX/XXX.exe”的格式进行输入，默认是以 C： 为开头，不用“\”做命令的分隔，而是用“/”
5、.desktop 的图标只支持 PNG 格式和 SVG 格式，其他格式无法显示图标"""

###############
# 窗口创建
###############
window = tk.Tk()
# 设置变量以修改和获取值项
wineVersion = tk.StringVar()
wineVersion.set("deepin-wine6 stable")
e1_text = tk.StringVar()
e2_text = tk.StringVar()
e3_text = tk.StringVar()
e4_text = tk.StringVar()
e5_text = tk.StringVar()
e6_text = tk.StringVar()
e7_text = tk.StringVar()
e8_text = tk.StringVar()
e9_text = tk.StringVar()
e10_text = tk.StringVar()
e12_text = tk.StringVar()
e15_text = tk.StringVar()
label13_text = tk.StringVar()
option1_text = tk.StringVar()
option1_text.set("Network")
label13_text.set("当前 deb 打包情况：暂未打包")
# 创建控件
label1 = ttk.Label(window, text="要打包的 deb 包的包名（※必填）")
label2 = ttk.Label(window, text="要打包的 deb 包的版本号（※必填）")
label3 = ttk.Label(window, text="要打包的 deb 包的说明（※必填）")
label4 = ttk.Label(window, text="要打包的 deb 包的维护者（※必填）")
label5 = ttk.Label(window, text="要解压的 wine 容器的容器名（※必填）")
label6 = ttk.Label(window, text="要解压的 wine 容器（※必填）")
label7 = ttk.Label(window, text="要解压的 wine 容器里需要运行的可执行文件路径（※必填）")
label8 = ttk.Label(window, text="要显示的 .desktop 文件的名称（※必填）")
label9 = ttk.Label(window, text="要显示的 .desktop 文件的图标（选填）")
label10 = ttk.Label(window, text="要显示的 .desktop 文件的 MimeType 内容（选填）")
label12 = ttk.Label(window, text="打包 deb 的保存路径（※必填）")
label13 = ttk.Label(window, textvariable=label13_text)
label14 = ttk.Label(window, text="要显示的 .desktop 文件的分类（※必填）")
label15 = ttk.Label(window,text="要解压的 wine 容器里需要运行的可执行文件的参数（选填）")
wineFrame = ttk.Frame(window)
chooseWineVersionTips = ttk.Label(window,text="选择打包的 wine 版本（必选）")
chooseWineVersion = ttk.OptionMenu(wineFrame, wineVersion, "deepin-wine6 stable", *list(wine))  # 创建选择框控件
chooseWineHelperValue = tk.IntVar()
chooseWineHelper = ttk.Checkbutton(wineFrame, text="使用星火wine helper（如不勾选默认为deepin-wine-helper）", variable=chooseWineHelperValue)
e1 = ttk.Entry(window, textvariable=e1_text, width=100)
e2 = ttk.Entry(window, textvariable=e2_text, width=100)
e3 = ttk.Entry(window, textvariable=e3_text, width=100)
e4 = ttk.Entry(window, textvariable=e4_text, width=100)
e5 = ttk.Entry(window, textvariable=e5_text, width=100)
e6 = ttk.Entry(window, textvariable=e6_text, width=100)
e7 = ttk.Entry(window, textvariable=e7_text, width=100)
e8 = ttk.Entry(window, textvariable=e8_text, width=100)
e9 = ttk.Entry(window, textvariable=e9_text, width=100)
e10 = ttk.Entry(window, textvariable=e10_text, width=100)
e12 = ttk.Entry(window, textvariable=e12_text, width=100)
e15 = ttk.Entry(window, textvariable=e15_text, width=100)
button1 = ttk.Button(window, text="浏览……", command=button1_cl)
button2 = ttk.Button(window, text="浏览……", command=button2_cl)
button4 = ttk.Button(window, text="浏览……", command=button4_cl)
button5 = ttk.Button(window, text="打包……", command=make_deb)
option1 = ttk.OptionMenu(window, option1_text, "Network", "Chat", "Audio", "Video", "Graphics", "Office", "Translation", "Development", "Utility")
textbox1 = tk.Text(window, width=100, height=4)
textbox1.configure(state=tk.DISABLED)
menu = tk.Menu(window)  # 设置菜单栏
programmenu = tk.Menu(menu, tearoff=0)  # 设置“程序”菜单栏
menu.add_cascade(label="程序", menu=programmenu)
programmenu.add_command(label="退出程序", command=window.quit)  # 设置“退出程序”项
help = tk.Menu(menu, tearoff=0) # 设置“帮助”菜单栏
menu.add_cascade(label="帮助", menu=help)
help.add_command(label="小提示", command=helps)  # 设置“小提示”项
# 设置窗口
style = ttkthemes.ThemedStyle(window)
style.set_theme("breeze")
window.title(f"wine 应用打包器 {version}")
window.iconphoto(False, tk.PhotoImage(file=iconPath))
# 控件配置
try:
    e6_text.set(sys.argv[1])
    e5_text.set(pathlib.PurePath(sys.argv[1]).name)
    wineVersion.set(sys.argv[2])
except:
    pass
# 添加控件
window.config(menu=menu)  # 显示菜单栏
label1.grid(row=0, column=0)
e1.grid(row=0, column=1)
label2.grid(row=1, column=0)
e2.grid(row=1, column=1)
label3.grid(row=2, column=0)
e3.grid(row=2, column=1)
label4.grid(row=3, column=0)
e4.grid(row=3, column=1)
label5.grid(row=4, column=0)
e5.grid(row=4, column=1)
label6.grid(row=5, column=0)
e6.grid(row=5, column=1)
button1.grid(row=5, column=2)
label7.grid(row=6, column=0)
e7.grid(row=6, column=1)
label14.grid(row=7, column=0)
option1.grid(row=7, column=1)
label15.grid(row=8, column=0)
e15.grid(row=8, column=1)
label8.grid(row=9, column=0)
e8.grid(row=9, column=1)
label9.grid(row=10, column=0)
e9.grid(row=10, column=1)
button2.grid(row=10, column=2)
label10.grid(row=11, column=0)
e10.grid(row=11, column=1)
chooseWineVersionTips.grid(row=12, column=0)
wineFrame.grid(row=12, column=1)
chooseWineVersion.grid(row=0, column=0)
chooseWineHelper.grid(row=0, column=1)
label12.grid(row=13, column=0)
e12.grid(row=13, column=1)
button4.grid(row=13, column=2)
button5.grid(row=14, column=1)
label13.grid(row=15, column=0, columnspan=3)
textbox1.grid(row=16, column=0, columnspan=3)
window.mainloop()
