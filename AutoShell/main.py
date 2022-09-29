#!/usr/bin/env python3
import os
import sys
import time
import json
import platform

# 读取文本文档
def readtxt(path):
    f = open(path, "r") # 设置文件对象
    str = f.read()  # 获取内容
    f.close()  # 关闭文本对象
    return str  # 返回结果
programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
information = json.loads(readtxt(f"{programPath}/../information.json"))
version = information["Version"]
thankText = ""
for i in information["Thank"]:
    thankText += f"{i}\n"
programEnv = [
    ["WINEPREFIX", f"{os.path.expanduser('~')}/.wine"],
    ["WINE", "deepin-wine6-stable"],
    ["DANGER", "0"],
    ["PROGRAMPATH", programPath],
    ["VERSION", version],
    ["THANK", thankText.replace("\n", "\\n")],
    ["MAKER", "gfdgd xi、为什么您不喜欢熊出没和阿布呢"],
    ["COPYRIGHT", f"©2020~{time.strftime('%Y')} gfdgd xi、为什么您不喜欢熊出没和阿布呢"],
    ["PLATFORM", platform.system()],
    ["DEBUG", str(int("--debug" in sys.argv))]
]
'''programEnv = [
    ["($WINEPREFIX)", f"{os.path.expanduser('~')}/.wine"],
    ["($WINE)", "deepin-wine6-stable"],
    ["($DANGER)", "0"],
    ["($HOME)", os.path.expanduser('~')],
    ["($PROGRAMPATH)", programPath],
    ["($VERSION)", version],
    ["($THANK)", thankText],
    ["($MAKER)", "gfdgd xi、为什么您不喜欢熊出没和阿布呢"],
    ["($COPYRIGHT)", f"©2020~{time.strftime('%Y')} gfdgd xi、为什么您不喜欢熊出没和阿布呢"],
    ["?", "0"],
    ["PLATFORM)", platform.system()],
    ["DEBUG)", str(int("--debug" in sys.argv))]
]'''
optionAll = 0
if "--debug" in sys.argv:
    optionAll += 1
if "--system" in sys.argv:
    programEnv.append(["DANGER", "1"])
    optionAll += 1
if os.getenv("WINE") != None:
    programEnv.append(["WINE", os.getenv("WINE")])
if os.getenv("WINEPREFIX") != None:
    programEnv.append(["WINE", os.getenv("WINEPREFIX")])
# 生成可以使用的参数
commandEnv = ""
for i in programEnv:
    commandEnv += f"{i[0]}=\"{i[1]}\" "
commandEnv += f"PATH=\"$PATH:{programPath}/command\" "
if len(sys.argv) - optionAll < 2:
    print("Wine 运行器自动配置文件解析器交互环境（基于 Bash）")
    print(f"版本：{version}")
    print(f"©2020~{time.strftime('%Y')} gfdgd xi、为什么您不喜欢熊出没和阿布呢")
    print("--------------------------------------------------------------")
    os.system(f"{commandEnv} bash")