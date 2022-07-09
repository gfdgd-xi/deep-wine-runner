#!/usr/bin/env python3
import os
import sys

if "--help" in sys.argv:
    print("作者：gfdgd xi、为什么您不喜欢熊出没和阿布呢")
    print("版本：1.0.0")
    print("本程序可以更方便的在 wine 容器中安装 MSXML")
    sys.exit()
if len(sys.argv) <= 2 or sys.argv[1] == "" or sys.argv[2] == "":
    print("您未指定需要安装 MSXML 的容器和使用的 wine，无法继续")
    print("参数：")
    print("XXX 参数一 参数二")
    print("参数一为需要安装的容器，参数二为需要使用的wine，两个参数位置不能颠倒")
    sys.exit()

msxmlList = [
    ["MSXML 4.0 SP2", "https://www.gitlink.org.cn/api/attachments/390679?gfdgd_xi"],
    ["MSXML 4.0 SP3", "https://www.gitlink.org.cn/api/attachments/390678?gfdgd_xi"],
    ["MSXML 6.0", "https://www.gitlink.org.cn/api/attachments/390681?gfdgd_xi"]    
]
print("请选择以下的 MSXML 进行安装（不保证能正常安装运行）")
for i in range(0, len(msxmlList)):
    print(f"{i}、{msxmlList[i][0]}")
while True:
    try:
        choose = int(input("请输入要选择要安装的 MSXML："))
    except:
        print("输入错误，请重新输入")
        continue
    if 0 <= choose and choose < len(msxmlList):
        break
print(f"您选择了 {msxmlList[choose][0]}")
print("开始下载")
os.system("rm -rfv /tmp/wineinstallmsxml")
os.system("mkdir -p /tmp/wineinstallmsxml")
os.system(f"aria2c -x 16 -s 16 -d /tmp/wineinstallmsxml -o install.msi \"{msxmlList[choose][1]}\"")
print("开始安装")
os.system(f"WINEPREFIX={sys.argv[1]} {sys.argv[2]} msiexec /i /tmp/wineinstallmsxml/install.msi")
print("安装结束")
sys.exit()