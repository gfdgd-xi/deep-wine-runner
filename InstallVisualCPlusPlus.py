#!/usr/bin/env python3
# 使用系统默认的 python3 运行
###########################################################################################
# 作者：gfdgd xi、为什么您不喜欢熊出没和阿布呢
# 版本：1.8.0
# 更新时间：2022年08月01日
# 感谢：感谢 wine 以及 deepin-wine 团队，提供了 wine 和 deepin-wine 给大家使用，让我能做这个程序
# 基于 Python3 构建
###########################################################################################
#################
# 引入所需的库
#################
import os
import sys

if "--help" in sys.argv:
    print("作者：gfdgd xi、为什么您不喜欢熊出没和阿布呢")
    print("版本：1.0.0")
    print("本程序可以更方便的在 wine 容器中安装 Visual Studio C++")
    sys.exit()
if len(sys.argv) <= 2 or sys.argv[1] == "" or sys.argv[2] == "":
    print("您未指定需要安装 Visual Studio C++ 的容器和使用的 wine，无法继续")
    print("参数：")
    print("XXX 参数一 参数二")
    print("参数一为需要安装的容器，参数二为需要使用的wine，两个参数位置不能颠倒")
    sys.exit()
netList = [
    ["2005 Service Pack 1 Redistributable Package MFC 安全更新", "https://download.microsoft.com/download/4/A/2/4A22001F-FA3B-4C13-BF4E-42EC249D51C4/vcredist_x86.EXE"],
    ["2008 (VC++ 9.0) SP1 (不再支持) ", "https://download.microsoft.com/download/5/D/8/5D8C65CB-C849-4025-8E95-C3966CAFD8AE/vcredist_x86.exe"], 
    ["2010 (VC++ 10.0) SP1 (不再支持) ", "https://download.microsoft.com/download/1/6/5/165255E7-1014-4D0A-B094-B6A430A6BFFC/vcredist_x86.exe"],
    ["2012 (VC++ 11.0) Update 4", "https://download.microsoft.com/download/1/6/B/16B06F60-3B20-4FF2-B699-5E9B7962F9AE/VSU_4/vcredist_x86.exe"],
    ["2013 (VC++ 12.0) ", "https://download.visualstudio.microsoft.com/download/pr/10912113/5da66ddebb0ad32ebd4b922fd82e8e25/vcredist_x86.exe"],
    ["2015、2017、2019 和 2022", "https://aka.ms/vs/17/release/vc_redist.x86.exe"]
]
print("请选择以下的 Visual Studio C++ 进行安装（不保证能正常安装运行）")
for i in range(0, len(netList)):
    print(f"{i} Visual Studio C++ {netList[i][0]}")
while True:
    try:
        choose = int(input("请输入要选择的 Visual Studio C++ 版本："))
    except:
        print("输入错误，请重新输入")
        continue
    if 0 <= choose and choose < len(netList):
        break
print(f"您选择了 Visual Studio C++ {netList[choose][0]}")
print("开始下载")
os.system("rm -rf /tmp/wineinstallvisualstudiocplusplus")
os.system("mkdir -p /tmp/wineinstallvisualstudiocplusplus")
os.system(f"aria2c -x 16 -s 16 -d /tmp/wineinstallvisualstudiocplusplus -o install.exe \"{netList[choose][1]}\"")
os.system(f"WINEPREFIX={sys.argv[1]} {sys.argv[2]} /tmp/wineinstallvisualstudiocplusplus/install.exe")
input("安装结束，按回车键退出")