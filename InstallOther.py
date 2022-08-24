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
import json
import requests

if "--help" in sys.argv:
    print("作者：gfdgd xi、为什么您不喜欢熊出没和阿布呢")
    print("版本：1.0.0")
    print("本程序可以更方便的在 wine 容器中安装运行库")
    sys.exit()
if len(sys.argv) <= 2 or sys.argv[1] == "" or sys.argv[2] == "":
    print("您未指定需要安装的容器和使用的 wine，无法继续")
    print("参数：")
    print("XXX 参数一 参数二 参数三(可略)")
    print("参数一为需要安装的容器，参数二为需要使用的wine，参数三为是否缓存（可略），三个参数位置不能颠倒")
    sys.exit()

homePath = os.path.expanduser('~')
print('''                                   
  mmmm    m    #                   
 m"  "m mm#mm  # mm    mmm    m mm 
 #    #   #    #"  #  #"  #   #"  "
 #    #   #    #   #  #""""   #    
  #mm#    "mm  #   #  "#mm"   #    
                                   
                                   
''')
try:
    msxmlList = json.loads(requests.get("https://code.gitlink.org.cn/gfdgd_xi/wine-runner-list/raw/branch/master/other/list.json").text)
except:
    msxmlList = [
        ["Windows Script 5.7 for Windows XP", "https://download.microsoft.com/download/f/f/e/ffea3abf-b55f-4924-b5a5-bde0805ad67c/scripten.exe", "exe", "scripten.exe"],
        ["Windows Management Instrumentation 1.50.1131", "https://www.gitlink.org.cn/api/attachments/390680", "exe", "WMITools.exe"]  
    ]
print("请选择以下的应用进行安装（不保证能正常安装运行）")
for i in range(0, len(msxmlList)):
    print(f"{i}、{msxmlList[i][0]}")
while True:
    try:
        choose = input("请输入要选择要安装的应用（输入“exit”退出）：").lower()
        choose = int(choose)
    except:
        print("输入错误，请重新输入")
        continue
    if 0 <= choose and choose < len(msxmlList):
        break
if choose == "exit":
    exit()
if len(sys.argv) <= 3:
    choice = True
else:
    choice = (sys.argv[3] == "1")
print(f"您选择了{msxmlList[choose][0]}")
if os.path.exists(f"{homePath}/.cache/deepin-wine-runner/other/{msxmlList[choose][3]}") and choice:
    print("已经缓存，使用本地版本")
    if msxmlList[choose][2] == "msi":
        os.system(f"WINEPREFIX={sys.argv[1]} {sys.argv[2]} msiexec /i '{homePath}/.cache/deepin-wine-runner/other/{msxmlList[choose][3]}'")
        input("安装结束，按回车键退出")
        sys.exit()
    if msxmlList[choose][2] == "exe":
        os.system(f"WINEPREFIX={sys.argv[1]} {sys.argv[2]} '{homePath}/.cache/deepin-wine-runner/other/{msxmlList[choose][3]}'")
        input("安装结束，按回车键退出")
        sys.exit()
print("开始下载")
os.system(f"rm -rf '{homePath}/.cache/deepin-wine-runner/other/{msxmlList[choose][3]}'")
os.system(f"mkdir -p '{homePath}/.cache/deepin-wine-runner/other'")
if msxmlList[choose][2] == "msi":
    os.system(f"aria2c -x 16 -s 16 -d '{homePath}/.cache/deepin-wine-runner/other' -o '{msxmlList[choose][3]}' \"{msxmlList[choose][1]}\"")
    print("开始安装")
    os.system(f"WINEPREFIX={sys.argv[1]} {sys.argv[2]} msiexec /i '{homePath}/.cache/deepin-wine-runner/other/{msxmlList[choose][3]}'")
    print("安装结束")
    sys.exit()
if msxmlList[choose][2] == "exe":
    os.system(f"aria2c -x 16 -s 16 -d '{homePath}/.cache/deepin-wine-runner/other' -o '{msxmlList[choose][3]}' \"{msxmlList[choose][1]}\"")
    print("开始安装")
    os.system(f"WINEPREFIX={sys.argv[1]} {sys.argv[2]} '{homePath}/.cache/deepin-wine-runner/other/{msxmlList[choose][3]}'")
    input("安装结束，按回车键退出")
    sys.exit()