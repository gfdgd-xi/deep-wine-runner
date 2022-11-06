#!/usr/bin/env python3
# 使用系统默认的 python3 运行
###########################################################################################
# 作者：gfdgd xi、为什么您不喜欢熊出没和阿布呢
# 版本：2.1.0
# 更新时间：2022年10月05日
# 感谢：感谢 wine 以及 deepin-wine 团队，提供了 wine 和 deepin-wine 给大家使用，让我能做这个程序
# 基于 Python3 构建
###########################################################################################
#################
# 引入所需的库
#################
import os
import sys
import json
import req as requests
try:
    sourcesList = [
        "https://code.gitlink.org.cn/gfdgd_xi/wine-runner-list/raw/branch/master/vb/list.json",
        "http://gfdgdxi.msns.cn/wine-runner-list/vb/list.json"
    ]
    netList = json.loads(requests.get().text)
except:
    netList = [
        ["Visual Basic 1(DOS application)", "https://code.gitlink.org.cn/gfdgd_xi/wine-runner-list/raw/branch/master/vb/vbrun100.exe", "vbrun100.exe"],
        ["Visual Basic 2(DOS application)", "https://code.gitlink.org.cn/gfdgd_xi/wine-runner-list/raw/branch/master/vb/vbrun200.exe", "vbrun200.exe"],
        ["Visual Basic 3", "https://code.gitlink.org.cn/gfdgd_xi/wine-runner-list/raw/branch/master/vb/vb3run.exe", "vb3run.exe"], 
        ["Visual Basic 4", "https://code.gitlink.org.cn/gfdgd_xi/wine-runner-list/raw/branch/master/vb/vb4run.exe", "vb4run.exe"], 
        ["Visual Basic 6", "https://code.gitlink.org.cn/gfdgd_xi/wine-runner-list/raw/branch/master/vb/vbrun60sp4.exe", "vbrun60sp4.exe"]
    ]
def Download(wineBotton: str, id: int, wine: str) -> int:
    try:
        os.remove(f"/tmp/deepin-wine-runner-vb/{netList[id][2]}")
    except:
        pass
    os.system(f"aria2c -x 16 -s 16 -d '/tmp/deepin-wine-runner-vb' -o '{netList[id][2]}' \"{netList[id][1]}\"")
    return os.system(f"WINEPREFIX='{wineBotton}' {wine} '/tmp/deepin-wine-runner-vb/{netList[id][2]}'")

if __name__ == "__main__":
    if "--help" in sys.argv:
        print("作者：gfdgd xi、为什么您不喜欢熊出没和阿布呢")
        print("版本：1.0.0")
        print("本程序可以更方便的在 wine 容器中安装 Visual Basic Runtime")
        sys.exit()
    if len(sys.argv) <= 2 or sys.argv[1] == "" or sys.argv[2] == "":
        print("您未指定需要安装 Visual Basic Runtime 的容器和使用的 wine，无法继续")
        print("参数：")
        print("XXX 参数一 参数二 参数三(可略)")
        print("参数一为需要安装的容器，参数二为需要使用的wine，参数三为是否缓存（可略），三个参数位置不能颠倒")
        sys.exit()

    homePath = os.path.expanduser('~')
    print('''              
 m    m mmmmm 
 "m  m" #    #
  #  #  #mmmm"
  "mm"  #    #
   ##   #mmmm"
              
              
''')

    print("请选择以下的 Visual Basic Runtime 进行安装（不保证能正常安装运行）")
    for i in range(0, len(netList)):
        print(f"{i} Visual Basic Runtime {netList[i][0]}")
    while True:
        try:
            choose = input("请输入要选择的 Visual Basic Runtime 版本（输入“exit”退出）：").lower()
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
    print(f"您选择了 Visual Basic Runtime {netList[choose][0]}")
    if os.path.exists(f"{homePath}/.cache/deepin-wine-runner/vb/{netList[choose][2]}"):
        print("已经缓存，使用本地版本")
        os.system(f"WINEPREFIX='{sys.argv[1]}' {sys.argv[2]} '{homePath}/.cache/deepin-wine-runner/vb/{netList[choose][2]}'")
        input("安装结束，按回车键退出")
        exit()
    print("开始下载")
    os.system(f"rm -rf '{homePath}/.cache/deepin-wine-runner/vb/{netList[choose][2]}'")
    os.system(f"mkdir -p '{homePath}/.cache/deepin-wine-runner/vb'")
    os.system(f"aria2c -x 16 -s 16 -d '{homePath}/.cache/deepin-wine-runner/vb' -o '{netList[choose][2]}' \"{netList[choose][1]}\"")
    os.system(f"WINEPREFIX='{sys.argv[1]}' {sys.argv[2]} '{homePath}/.cache/deepin-wine-runner/vb/{netList[choose][2]}'")
    input("安装结束，按回车键退出")