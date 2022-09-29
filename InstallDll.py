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
import traceback
import req as requests
def exit():
    if __name__ == "__main__":
        input("按回车键退出")
        sys.exit()
    sys.exit()
# 获取云列表
url = "https://code.gitlink.org.cn/gfdgd_xi/wine-runner-list/raw/branch/master/dlls"
print("获取列表中……", end="")
try:
    lists = json.loads(requests.get(f"{url}/list.json").text)
except:
    print("\r列表获取失败！")
    exit()
print("\r列表获取成功！")

def GetUrlByNumber(dllID: int) -> str:
    dllName = lists[dllID][0]
    return f"{url}/{lists[int(dllID)][1]}/{lists[int(dllID)][2]}/{lists[int(dllID)][0]}"

def GetNameByNumber(dllID: int) -> str:
    return lists[dllID][0]

def GetUrlByName(dllName: str):
    for i in range(0, len(lists)):
        if dllName == lists[i][0]:
            return f"{url}/{lists[i][1]}/{lists[i][2]}/{lists[i][0]}"

def Download(wineBotton, dllName, urlPart, wine: str) -> bool:
    try:
        os.remove(f"{wineBotton}/drive_c/windows/system32/{dllName}")
    except:
        pass
    os.system(f"aria2c -x 16 -s 16 -d '{wineBotton}/drive_c/windows/system32' -o '{dllName}' '{urlPart}'")
    #print(f"WINEPREFIX='{wineBotton}' {wine} reg add 'HKEY_CURRENT_USER\Software\Wine\DllOverrides' /v {os.path.splitext(dllName)[0]} /d native /f")
    os.system(f"WINEPREFIX='{wineBotton}' {wine} reg add 'HKEY_CURRENT_USER\Software\Wine\DllOverrides' /v {os.path.splitext(dllName)[0]} /d native /f")
    return 0

def exit():
    input("按回车键退出")
    sys.exit()

if __name__ == "__main__":
    if "--help" in sys.argv:
        print("作者：gfdgd xi、为什么您不喜欢熊出没和阿布呢")
        print("版本：1.0.0")
        print("本程序可以更方便的在 wine 容器中安装指定应用")
        sys.exit()
    if len(sys.argv) <= 1 or sys.argv[1] == "":
        print("您未指定需要安装的容器，无法继续")
        print("参数：")
        print("XXX 参数一")
        print("参数一为需要安装的容器")
        sys.exit()
    print('''                     
 mmmm   ""#    ""#   
 #   "m   #      #   
 #    #   #      #   
 #    #   #      #   
 #mmm"    "mm    "mm 
                     
                     
''')
    wineBotton = sys.argv[1]
    wine = sys.argv[2]
    if not os.path.exists(f"{wineBotton}/drive_c/windows/Fonts"):
        input("您选择的不是 Wine 容器")
        exit()
    # 判断是不是 wine 容器
    if not os.path.exists(f"{wineBotton}/drive_c/windows/system32"):
        print("这不是 Wine 容器")
        exit()
    # 获取用户希望安装的DLL

    while True:
        print()
        print("您可以输入DLL名称进行搜索，输入前面编号或DLL全称即可安装(推荐是编号，可以选系统版本)")
        print("输入exit即可退出")
        urlPart = ""
        while True:
            dllName = input(">")
            if dllName.lower() == "exit":
                exit()
            if dllName in lists:
                url = dllName
                break
            try:
                dllName = lists[int(dllName)][0]
                urlPart = GetUrlByNumber(int(dllName))
                f"{url}/{lists[int(dllName)][1]}/{lists[int(dllName)][2]}/{lists[int(dllName)][0]}"
                break
            except:
                pass
            right = False
            for i in range(0, len(lists)):
                if dllName == lists[i][0]:
                    right = True
                    urlPart = f"{url}/{lists[i][1]}/{lists[i][2]}/{lists[i][0]}"
                    break
                if dllName in lists[i][0]:
                    print(i, lists[i][0], f"平台：{lists[i][1]}", f"架构：{lists[i][2]}")
            if right:
                break
        if os.path.exists(f"{wineBotton}/drive_c/windows/system32/{dllName}"):
            if input(f"{dllName} 已存在，是否覆盖？(一般不推荐)[Y/N]").upper() == "N":
                continue
            try:
                os.remove(f"{wineBotton}/drive_c/windows/system32/{dllName}")
            except:
                print("文件移除失败！")
                traceback.print_exc()
                continue
        # 下载 DLL
        print(f"正在下载{dllName}，请稍后")
        print(f"下载链接：{urlPart}")
        if Download(wineBotton, dllName, urlPart, wine):
            print("下载失败！请重试")
