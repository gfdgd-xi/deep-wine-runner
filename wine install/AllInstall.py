#!/usr/bin/env python3
# 使用系统默认的 python3 运行
###########################################################################################
# 作者：gfdgd xi
# 版本：1.4.0
# 更新时间：2021年07月27日
# 感谢：感谢 wine 以及 deepin-wine 团队，提供了 wine 和 deepin-wine 给大家使用，让我能做这个程序
# 基于 Python3 的 tkinter 构建
###########################################################################################
#################
# 引入所需的库
#################
import os

###################
# 程序功能
###################
print("请保证你能有 root 权限以便安装")
print("如果有请按回车，否则按 [Ctrl+C] 退出", end=' ')
input()
os.system("sudo apt update")
print("请问是否要更新操作系统？[Y/N]", end=' ')
choose = input().upper()
if not choose == "N":
    os.system("sudo apt upgrade -y")
print("请问是否要安装原版 wine（wine64）？[Y/N]", end=' ')
choose = input().upper()
if not choose == "N":
    os.system("sudo apt install wine -y")
print("请问是否要安装 deepin-wine？[Y/N]", end=' ')
choose = input().upper()
if not choose == "N":
    os.system("sudo apt install deepin-wine -y")
print("请问是否要安装 deepin-wine5（需要添加星火应用商店的源）？[Y/N]", end=' ')
choose = input().upper()
if not choose == "N":
    if os.path.exists("/etc/apt/sources.list.d/sparkstore-temp.list"):
        os.system("sudo rm -v /etc/apt/sources.list.d/sparkstore-temp.list")
    if not os.path.exists("/etc/apt/sources.list.d/sparkstore.list"):
        os.system("sudo touch /etc/apt/sources.list.d/sparkstore-temp.list")
        os.system("echo 'deb [by-hash=force] https://d.store.deepinos.org.cn / ' | sudo tee '/etc/apt/sources.list.d/sparkstore-temp.list'")
        os.system("sudo apt update")
    os.system("sudo apt install deepin-wine5 -y")
    if os.path.exists("/etc/apt/sources.list.d/sparkstore-temp.list"):
        os.system("sudo rm -v /etc/apt/sources.list.d/sparkstore-temp.list")
        os.system("sudo apt update")
print("请问是否要安装 deepin-wine5-stable？[Y/N]", end=' ')
choose = input().upper()
if not choose == "N":
    os.system("sudo apt install deepin-wine5-stable -y")
print("请问是否要安装 deepin-wine6-stable？[Y/N]", end=' ')
choose = input().upper()
if not choose == "N":
    os.system("sudo apt install deepin-wine6-stable -y")
print("全部完成！")