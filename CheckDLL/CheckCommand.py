#!/usr/bin/env python3
# 使用系统默认的 python3 运行
#################################################################################################################
# 作者：gfdgd xi
# 版本：2.5.0
# 更新时间：2022年11月18日
# 感谢：感谢 wine、deepin-wine 以及星火团队，提供了 wine、deepin-wine、spark-wine-devel 给大家使用，让我能做这个程序
# 基于 Python3 的 PyQt5 构建
#################################################################################################################
#################
# 引入所需的库
#################
import os
import sys
import json

if len(sys.argv) <= 1:
    print("参数不足")
    sys.exit(1)

if "--help" in sys.argv:
    print("帮助：")
    print("[exe path] [option]")
    print("--json  以 json 格式输出")
    print("-w [wine botton] [wine program path]")

jsonPrint = "--json" in sys.argv
if jsonPrint:
    del sys.argv[sys.argv.index("--json")]
lists = []
programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
checkDll = False
if "-w" in sys.argv:
    wineCommand = sys.argv.index("-w")
    wineBotton = os.getenv("HOME")
    wineProgram = "deepin-wine6-stable"
    checkDll = True
    try:
        wineBotton = sys.argv[wineCommand + 1]
        wineProgram = sys.argv[wineCommand + 2]
    except:
        pass
badChar = [
    "(", "?", "*", "!", ")", "&", "'", "\""
]
with open(sys.argv[1], "rb") as file:
    while True:
        things = file.readline()
        if things == b"":
            break
        for n in [".dll", ".DLL"]:
            if n.encode() in things:
                # 提取 DLL 名称
                for i in str(things[1: -2]).split("\\x"):
                    charBad = False
                    for b in badChar:
                        if b in i:
                            charBad = True
                    if n in i and not charBad and i[0] != "/":
                        name = i[2: ].replace(",{M", "").replace("+", "")
                        # 文件路径合法性检测

                        try:
                            dllName = name[:name.index(".dll") + 4]
                        except:
                            try:
                                dllName = name[:name.index(".DLL") + 4]
                            except:
                                dllName = name

                        if dllName.lower() == ".dll":
                            continue
                        if dllName in lists:
                            continue
                        if checkDll:
                            if jsonPrint:
                                if os.system(f"WINEPREFIX='{wineBotton}' {wineProgram} '{programPath}/Check.exe' '{dllName}' > /dev/null 2>&1"):
                                    lists.append(dllName)
                                    continue
                            else:
                                os.system(f"WINEPREFIX='{wineBotton}' {wineProgram} '{programPath}/Check.exe' '{dllName}'")
                                lists.append(dllName)
                        elif jsonPrint:
                            lists.append(dllName)
                            continue
                        else:
                            print(dllName)
                            lists.append(dllName)
if jsonPrint:
    print(json.dumps(lists))