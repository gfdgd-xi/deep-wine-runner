#!/usr/bin/env python3
# 使用系统默认的 python3 运行
###########################################################################################
# 作者：gfdgd xi、为什么您不喜欢熊出没和阿布呢
# 版本：1.5.1
# 更新时间：2022年07月04日
# 感谢：感谢 wine 以及 deepin-wine 团队，提供了 wine 和 deepin-wine 给大家使用，让我能做这个程序
# 基于 Python3 的 tkinter 构建
###########################################################################################
#################
# 引入所需的库
#################
import os
import sys
import pyquery

if "--help" in sys.argv:
    print("作者：gfdgd xi、为什么您不喜欢熊出没和阿布呢")
    print("版本：1.0.0")
    print("本程序可以更方便的在 wine 容器中安装 mono、gecko")
    sys.exit()
if len(sys.argv) <= 3 or sys.argv[1] == "" or sys.argv[2] == "" or sys.argv[3] == "":
    print("您未指定需要安装 gecko 或者 mono 的容器和使用的 wine，无法继续")
    print("参数：")
    print("XXX 参数一 参数二 参数三")
    print("参数一为需要安装的容器，参数二为需要使用的wine，参数三为安装gecko或mono（gecko/mono），三个参数位置不能颠倒")
    sys.exit()
# 获取最新版本的版本号
programVersionList = pyquery.PyQuery(url=f"http://mirrors.ustc.edu.cn/wine/wine/wine-{sys.argv[3]}/")
programVersion = programVersionList("a:last-child").attr.href
# 获取最新版本安装包的URL
programUrl = pyquery.PyQuery(url=f"http://mirrors.ustc.edu.cn/wine/wine/wine-{sys.argv[3]}/{programVersion}")
programDownloadUrl = ""
programFileName = ""
for i in programUrl("a").items():
    if i.attr.href[-4:] == ".msi":
        programDownloadUrl = f"http://mirrors.ustc.edu.cn/wine/wine/wine-{sys.argv[3]}/{programVersion}{i.attr.href}"
        programFileName = i.attr.href
        break

if programDownloadUrl == "":
    print("无法获取链接，无法继续")
    sys.exit()
print(f"当前选择的程序获取路径：{programDownloadUrl}")
print("开始下载")
os.system("rm -rf /tmp/winegeckomonoinstall")
os.system("mkdir -p /tmp/winegeckomonoinstall")
os.system(f"aria2c -x 16 -s 16 -d /tmp/winegeckomonoinstall -o install.msi \"{programDownloadUrl}\"")
print("开始安装")
os.system(f"WINEPREFIX={sys.argv[1]} {sys.argv[2]} msiexec /i /tmp/winegeckomonoinstall/install.msi")
print("安装结束")