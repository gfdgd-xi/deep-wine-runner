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
    print("本程序可以更方便的在 wine 容器中安装 .net framework")
    sys.exit()
if len(sys.argv) <= 2 or sys.argv[1] == "" or sys.argv[2] == "":
    print("您未指定需要安装 .net framework 的容器和使用的 wine，无法继续")
    print("参数：")
    print("XXX 参数一 参数二 参数三(可略)")
    print("参数一为需要安装的容器，参数二为需要使用的wine，参数三为是否缓存（可略），三个参数位置不能颠倒")
    sys.exit()

homePath = os.path.expanduser('~')
os.system("toilet .NET")
netList = [
    ["3.5 SP1 Offline Installer", "https://download.visualstudio.microsoft.com/download/pr/b635098a-2d1d-4142-bef6-d237545123cb/2651b87007440a15209cac29634a4e45/dotnetfx35.exe"], 
    ["4.0 Offline Installer", "https://download.microsoft.com/download/9/5/A/95A9616B-7A37-4AF6-BC36-D6EA96C8DAAE/dotNetFx40_Full_x86_x64.exe"],
    ["4.5 Web Installer", "https://download.microsoft.com/download/B/A/4/BA4A7E71-2906-4B2D-A0E1-80CF16844F5F/dotNetFx45_Full_setup.exe"],
    ["4.5.1 Offline Installer", "https://download.microsoft.com/download/1/6/7/167F0D79-9317-48AE-AEDB-17120579F8E2/NDP451-KB2858728-x86-x64-AllOS-ENU.exe"],
    ["4.5.2 Offline Installer", "https://download.microsoft.com/download/E/2/1/E21644B5-2DF2-47C2-91BD-63C560427900/NDP452-KB2901907-x86-x64-AllOS-ENU.exe"],
    ["4.6 Offline Installer", "https://download.microsoft.com/download/6/F/9/6F9673B1-87D1-46C4-BF04-95F24C3EB9DA/enu_netfx/NDP46-KB3045557-x86-x64-AllOS-ENU_exe/NDP46-KB3045557-x86-x64-AllOS-ENU.exe"],
    ["4.6.1 Offline Installer", "https://download.microsoft.com/download/E/4/1/E4173890-A24A-4936-9FC9-AF930FE3FA40/NDP461-KB3102436-x86-x64-AllOS-ENU.exe"],
    ["4.6.2 Offline Installer", "https://download.visualstudio.microsoft.com/download/pr/8e396c75-4d0d-41d3-aea8-848babc2736a/80b431456d8866ebe053eb8b81a168b3/ndp462-kb3151800-x86-x64-allos-enu.exe"],
    ["4.7 Offline Installer", "https://download.visualstudio.microsoft.com/download/pr/2dfcc711-bb60-421a-a17b-76c63f8d1907/e5c0231bd5d51fffe65f8ed7516de46a/ndp47-kb3186497-x86-x64-allos-enu.exe"],
    ["4.7.1 Offline Installer", "https://download.visualstudio.microsoft.com/download/pr/4312fa21-59b0-4451-9482-a1376f7f3ba4/9947fce13c11105b48cba170494e787f/ndp471-kb4033342-x86-x64-allos-enu.exe"],
    ["4.7.2 Offline Installer", "https://download.visualstudio.microsoft.com/download/pr/1f5af042-d0e4-4002-9c59-9ba66bcf15f6/089f837de42708daacaae7c04b7494db/ndp472-kb4054530-x86-x64-allos-enu.exe"],
    ["4.8 Offline Installer", "https://download.visualstudio.microsoft.com/download/pr/2d6bb6b2-226a-4baa-bdec-798822606ff1/8494001c276a4b96804cde7829c04d7f/ndp48-x86-x64-allos-enu.exe"]
]
print("请选择以下的 .net framework 进行安装（不保证能正常安装运行）")
for i in range(0, len(netList)):
    print(f"{i} .net framework {netList[i][0]}")
while True:
    try:
        choose = input("请输入要选择的 .net framework 版本（输入“exit”退出）：").lower()
        if choose == "exit":
            break
        choose = int(choose)
    except:
        print("输入错误，请重新输入")
        continue
    if 0 <= choose and choose < len(netList):
        break

if choose == "exit":
    exit()
if len(sys.argv) <= 3:
    choice = True
else:
    choice = (sys.argv[3] == "1")
print(f"您选择了 .net framework {netList[choose][0]}")
print(f"如果是 Offline Installer 版本，提示需要连接互联网，其实是不需要的，断网也可以安装")
print(f"如果 Offline Installer 版本连接网络时安装失败，提示无法连接服务器或连接超时，可以尝试下载完安装包加载过程中断网以便断网安装")
print(f"一般建议 Offline Installer 版本在下载完 exe 安装程序后在加载过程中断网以便提高安装速度")
programName = os.path.split(netList[choose][1])[1]
if os.path.exists(f"{homePath}/.cache/deepin-wine-runner/.netframework/{programName}") and choice:
    print("已经缓存，使用本地版本")
    os.system(f"WINEPREFIX={sys.argv[1]} {sys.argv[2]} '{homePath}/.cache/deepin-wine-runner/.netframework/{programName}'")
    input("安装结束，按回车键退出")
    exit()
print("开始下载")
os.system(f"rm -rf '{homePath}/.cache/deepin-wine-runner/.netframework/{programName}'")
os.system(f"mkdir -p '{homePath}/.cache/deepin-wine-runner/.netframework'")
os.system(f"aria2c -x 16 -s 16 -d \"{homePath}/.cache/deepin-wine-runner/.netframework\" -o \"{programName}\" \"{netList[choose][1]}\"")
os.system(f"WINEPREFIX={sys.argv[1]} {sys.argv[2]} '{homePath}/.cache/deepin-wine-runner/.netframework/{programName}'")
input("安装结束，按回车键退出")