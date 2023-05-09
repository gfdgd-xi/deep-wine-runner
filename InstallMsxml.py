#!/usr/bin/env python3
# 使用系统默认的 python3 运行
###########################################################################################
# 作者：gfdgd xi
# 版本：2.1.0
# 更新时间：2022年08月25日
# 感谢：感谢 wine 以及 deepin-wine 团队，提供了 wine 和 deepin-wine 给大家使用，让我能做这个程序
# 基于 Python3 构建
###########################################################################################
#################
# 引入所需的库
#################
import os
import sys
import json
import updatekiller
import req as requests
try:
    sourcesList = [
        "http://msxml.wine-runner.gfdgdxi.top/list.json",
        "https://code.gitlink.org.cn/gfdgd_xi/wine-runner-list/raw/branch/master/msxml/list.json"
    ]
    change = False
    for i in sourcesList:
        try:
            msxmlList = json.loads(requests.get(i).text)
            change = True
            break
        except:
            pass
    if not change:
        msxmlList = json.loads(requests.get(sourcesList[0]).text)
except:
    print("使用离线列表")
    msxmlList = [
        ["MSXML 4.0 SP2", "http://msxml.wine-runner.gfdgdxi.top/msxml6.0.msi", "msxml6.0.msi"],
        ["MSXML 4.0 SP3", "http://msxml.wine-runner.gfdgdxi.top/msxml4.0SP3.msi", "msxml4.0SP3.msi"],
        ["MSXML 6.0", "http://msxml.wine-runner.gfdgdxi.top/msxml6_x64.msi", "msxml6_x64.msi"],
        ["MSXML 3.0", "http://msxml.wine-runner.gfdgdxi.top/msxml3.msi", "msxml3.msi"]    
    ]


def Download(wineBotton: str, id: int, wine: str):
    os.system(f"aria2c -x 16 -s 16 -d \"/tmp/deepin-wine-runner-msxml/\" -o \"{msxmlList[id][2]}\" \"{msxmlList[id][1]}\"")
    return os.system(f"WINEPREFIX='{wineBotton}' {wine} msiexec /i \"/tmp/deepin-wine-runner-msxml/{msxmlList[id][2]}\"")

if __name__ == "__main__":
    if "--help" in sys.argv:
        print("作者：gfdgd xi")
        print("版本：1.0.0")
        print("本程序可以更方便的在 wine 容器中安装 MSXML")
        sys.exit()
    if len(sys.argv) <= 2 or sys.argv[1] == "" or sys.argv[2] == "":
        print("您未指定需要安装 MSXML 的容器和使用的 wine，无法继续")
        print("参数：")
        print("XXX 参数一 参数二 参数三(可略)")
        print("参数一为需要安装的容器，参数二为需要使用的wine，参数三为是否缓存（可略），三个参数位置不能颠倒")
        sys.exit()

    homePath = os.path.expanduser('~')
    print('''                                   
 m    m  mmmm  m    m m    m m     
 ##  ## #"   "  #  #  ##  ## #     
 # ## # "#mmm    ##   # ## # #     
 # "" #     "#  m""m  # "" # #     
 #    # "mmm#" m"  "m #    # #mmmmm
                                   
                                   
''')

    print("请选择以下的 MSXML 进行安装（不保证能正常安装运行）")
    for i in range(0, len(msxmlList)):
        print(f"{i}、{msxmlList[i][0]}")
    while True:
        try:
            choose = input("请输入要选择要安装的 MSXML（输入“exit”退出）：")
            if choose.lower() == "exit":
                break
            choose = int(choose)
        except:
            print("输入错误，请重新输入")
            continue
        if 0 <= choose and choose < len(msxmlList):
            break
    try:
        if choose.lower() == "exit":
            exit()
    except:
        pass
    print(f"您选择了 {msxmlList[choose][0]}")
    if len(sys.argv) <= 3:
        choice = True
    else:
        choice = (sys.argv[3] == "1")
    if os.path.exists(f"{homePath}/.config/deepin-wine-runner/MSXML/{msxmlList[choose][2]}") and choice:
        print("已经缓存，使用本地版本")
        os.system(f"WINEPREFIX='{sys.argv[1]}' {sys.argv[2]} msiexec /i \"{homePath}/.config/deepin-wine-runner/MSXML/{msxmlList[choose][2]}\"")
        input("安装结束，按回车键退出")
        exit()
    print("开始下载")
    os.system(f"rm -rfv \"{homePath}/.config/deepin-wine-runner/MSXML/{msxmlList[choose][2]}\"")
    os.system(f"mkdir -p \"{homePath}/.config/deepin-wine-runner/MSXML/\"")
    os.system(f"aria2c -x 16 -s 16 -d \"{homePath}/.config/deepin-wine-runner/MSXML\" -o \"{msxmlList[choose][2]}\" \"{msxmlList[choose][1]}\"")
    print("开始安装")
    os.system(f"WINEPREFIX='{sys.argv[1]}' {sys.argv[2]} msiexec /i \"{homePath}/.config/deepin-wine-runner/MSXML/{msxmlList[choose][2]}\"")
    input("安装结束，按回车键退出")