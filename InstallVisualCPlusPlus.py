#!/usr/bin/env python3
# 使用系统默认的 python3 运行
###########################################################################################
# 作者：gfdgd xi、为什么您不喜欢熊出没和阿布呢
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
import requests
try:
    netList = json.loads(requests.get("https://code.gitlink.org.cn/gfdgd_xi/wine-runner-list/raw/branch/master/vscpp/list.json").text)
except:
    netList = [
        ["VC6 运行库", "https://code.gitlink.org.cn/gfdgd_xi/wine-runner-list/raw/branch/master/vscpp/VC6RedistSetup_deu.exe"],
        ["2005 Service Pack 1 Redistributable Package MFC 安全更新", "https://download.microsoft.com/download/4/A/2/4A22001F-FA3B-4C13-BF4E-42EC249D51C4/vcredist_x86.EXE", "vcredist05_x86.exe"],
        ["2008 (VC++ 9.0) SP1 (不再支持) X86", "https://download.microsoft.com/download/5/D/8/5D8C65CB-C849-4025-8E95-C3966CAFD8AE/vcredist_x86.exe", "vcredist08_x86.exe"], 
        ["2008 (VC++ 9.0) SP1 (不再支持) X64", "https://download.microsoft.com/download/5/D/8/5D8C65CB-C849-4025-8E95-C3966CAFD8AE/vcredist_x64.exe", "vcredist08_x86.exe"], 
        ["2010 (VC++ 10.0) SP1 (不再支持) X86", "https://download.microsoft.com/download/1/6/5/165255E7-1014-4D0A-B094-B6A430A6BFFC/vcredist_x86.exe", "vcredist10_x86.exe"],
        ["2010 (VC++ 10.0) SP1 (不再支持) X64", "https://download.microsoft.com/download/1/6/5/165255E7-1014-4D0A-B094-B6A430A6BFFC/vcredist_x86.exe", "vcredist10_x64.exe"],
        ["2012 (VC++ 11.0) Update 4 X86", "https://download.microsoft.com/download/1/6/B/16B06F60-3B20-4FF2-B699-5E9B7962F9AE/VSU_4/vcredist_x86.exe", "vcredist12_x86.exe"],
        ["2012 (VC++ 11.0) Update 4 X64", "https://download.microsoft.com/download/1/6/B/16B06F60-3B20-4FF2-B699-5E9B7962F9AE/VSU_4/vcredist_x64.exe", "vcredist12_x64.exe"],
        ["2013 (VC++ 12.0) X86", "https://aka.ms/highdpimfc2013x86enu", "vcredist13_x86.exe"],
        ["2013 (VC++ 12.0) X64", "https://aka.ms/highdpimfc2013x64enu", "vcredist13_x64.exe"],
        ["2015、2017、2019 和 2022 X86", "https://aka.ms/vs/17/release/vc_redist.x86.exe", "vc_redist15.x86.exe"],
        ["2015、2017、2019 和 2022 X64", "https://aka.ms/vs/17/release/vc_redist.x64.exe", "vc_redist15.x64.exe"],
        ["2015、2017、2019 和 2022 ARM64", "https://aka.ms/vs/17/release/vc_redist.arm64.exe", "vc_redist15.arm64.exe"]
    ]
def Download(wineBotton: str, id: int, wine: str) -> int:
    try:
        os.remove(f"/tmp/deepin-wine-runner-vcpp/{netList[id][2]}")
    except:
        pass
    os.system(f"aria2c -x 16 -s 16 -d '/tmp/deepin-wine-runner-vcpp' -o '{netList[id][2]}' \"{netList[id][1]}\"")
    os.system(f"WINEPREFIX='{wineBotton}' {wine} '/tmp/deepin-wine-runner-vcpp/{netList[id][2]}'")

if __name__ == "__main__":
    if "--help" in sys.argv:
        print("作者：gfdgd xi、为什么您不喜欢熊出没和阿布呢")
        print("版本：1.0.0")
        print("本程序可以更方便的在 wine 容器中安装 Visual Studio C++")
        sys.exit()
    if len(sys.argv) <= 2 or sys.argv[1] == "" or sys.argv[2] == "":
        print("您未指定需要安装 Visual Studio C++ 的容器和使用的 wine，无法继续")
        print("参数：")
        print("XXX 参数一 参数二 参数三(可略)")
        print("参数一为需要安装的容器，参数二为需要使用的wine，参数三为是否缓存（可略），三个参数位置不能颠倒")
        sys.exit()

    homePath = os.path.expanduser('~')
    print('''                            
 m    m   mmm               
 "m  m" m"   "   m      m   
  #  #  #        #      #   
  "mm"  #     """#""""""#"""
   ##    "mmm"   #      #   
                            
                            
''')

    print("请选择以下的 Visual Studio C++ 进行安装（不保证能正常安装运行）")
    for i in range(0, len(netList)):
        print(f"{i} Visual Studio C++ {netList[i][0]}")
    while True:
        try:
            choose = input("请输入要选择的 Visual Studio C++ 版本（输入“exit”退出）：").lower()
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
    print(f"您选择了 Visual Studio C++ {netList[choose][0]}")
    if os.path.exists(f"{homePath}/.cache/deepin-wine-runner/vcpp/{netList[choose][2]}"):
        print("已经缓存，使用本地版本")
        os.system(f"WINEPREFIX='{sys.argv[1]}' {sys.argv[2]} '{homePath}/.cache/deepin-wine-runner/vcpp/{netList[choose][2]}'")
        input("安装结束，按回车键退出")
        exit()
    print("开始下载")
    os.system(f"rm -rf '{homePath}/.cache/deepin-wine-runner/vcpp/{netList[choose][2]}'")
    os.system(f"mkdir -p '{homePath}/.cache/deepin-wine-runner/vcpp'")
    os.system(f"aria2c -x 16 -s 16 -d '{homePath}/.cache/deepin-wine-runner/vcpp' -o '{netList[choose][2]}' \"{netList[choose][1]}\"")
    os.system(f"WINEPREFIX='{sys.argv[1]}' {sys.argv[2]} '{homePath}/.cache/deepin-wine-runner/vcpp/{netList[choose][2]}'")
    input("安装结束，按回车键退出")