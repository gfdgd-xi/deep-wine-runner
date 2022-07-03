#!/usr/bin/env python3
# 使用系统默认的 python3 运行
###########################################################################################
# 作者：gfdgd xi
# 版本：1.5.0
# 更新时间：2022年07月03日
# 感谢：感谢 wine 以及 deepin-wine 团队，提供了 wine 和 deepin-wine 给大家使用，让我能做这个程序
# 基于 Python3 的 tkinter 构建
###########################################################################################
#################
# 引入所需的库
#################
import os

def AddSparkStoreSource():
    # Download and install key
    os.system("mkdir -p /tmp/spark-store-install")
    os.system("wget -O /tmp/spark-store-install/spark-store.asc https://d.store.deepinos.org.cn/dcs-repo.gpg-key.asc")
    os.system("sudo gpg --dearmor /tmp/spark-store-install/spark-store.asc")
    os.system("cp -f /tmp/spark-store-install/spark-store.asc.gpg /etc/apt/trusted.gpg.d/spark-store.gpg")
    # Run apt update to avoid users being fucked up by the non-exist dependency problem
    os.system("sudo apt update -o Dir::Etc::sourcelist=\"sources.list.d/sparkstore.list\"     -o Dir::Etc::sourceparts=\"-\" -o APT::Get::List-Cleanup=\"0\"")

def InstallSparkWine(wine):
    if os.path.exists("/usr/local/bin/ss-apt-fast"):
        os.system("sudo apt install apt-fast -y")
        os.system(f"sudo ss-apt-fast install \"{wine}\" -y")
        return
    os.system(f"sudo apt install \"{wine}\" -y")

###################
# 程序功能
###################
#print("请按回车：")
#input()
#os.system("clear")
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
    if not os.path.exists("/etc/apt/sources.list.d/sparkstore.list"):
        AddSparkStoreSource()
    InstallSparkWine("deepin-wine5")
print("请问是否要安装 deepin-wine5-stable？[Y/N]", end=' ')
choose = input().upper()
if not choose == "N":
    os.system("sudo apt install deepin-wine5-stable -y")
print("请问是否要安装 deepin-wine6-stable？[Y/N]", end=' ')
choose = input().upper()
if not choose == "N":
    os.system("sudo apt install deepin-wine6-stable -y")
print("请问是否要安装 spark-wine7-devel（需要添加星火应用商店的源）？[Y/N]", end=' ')
choose = input().upper()
if not choose == "N":
    if not os.path.exists("/etc/apt/sources.list.d/sparkstore.list"):
        AddSparkStoreSource()
    InstallSparkWine("spark-wine7-devel")
print("全部完成！")