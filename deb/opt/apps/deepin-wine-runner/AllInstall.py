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

def AddSparkStoreSource():
    # Download and install key
    os.system("mkdir -p /tmp/spark-store-install")
    os.system("wget -O /tmp/spark-store-install/spark-store.asc https://d.store.deepinos.org.cn/dcs-repo.gpg-key.asc")
    os.system("sudo gpg --dearmor /tmp/spark-store-install/spark-store.asc")
    os.system("cp -f /tmp/spark-store-install/spark-store.asc.gpg /etc/apt/trusted.gpg.d/spark-store.gpg")
    # Run apt update to avoid users being fucked up by the non-exist dependency problem
    os.system("sudo apt update -o Dir::Etc::sourcelist=\"sources.list.d/sparkstore.list\"     -o Dir::Etc::sourceparts=\"-\" -o APT::Get::List-Cleanup=\"0\"")

def InstallSparkWine(wine):
    #if os.path.exists("/usr/local/bin/ss-apt-fast"):
        #os.system("sudo apt install apt-fast -y")
        #os.system(f"sudo ss-apt-fast install \"{wine}\" -y")
        #return
    #os.system("sudo ss-apt-fast update")
    if not os.system("which aptss"):
        os.system(f"sudo aptss install \"{wine}\" -y")
    elif not os.system("which ss-apt-fast"):
        os.system("sudo ss-apt-fast update")
        os.system(f"sudo ss-apt-fast install \"{wine}\" -y")
    elif not os.system("which apt-fast"):
        os.system(f"sudo apt-fast install \"{wine}\" -y")
    else:
        os.system(f"sudo apt install \"{wine}\" -y")

###################
# 程序功能
###################
print('''                            
m     m   "                 
#  #  # mmm    m mm    mmm  
" #"# #   #    #"  #  #"  # 
 ## ##"   #    #   #  #"""" 
 #   #  mm#mm  #   #  "#mm" 
                            
                            
''')
print("请保证你能有 root 权限以便安装")
print("如果有请按回车，否则按 [Ctrl+C] 退出", end=' ')
input()
os.system("sudo apt update")
print("请问是否要更新操作系统？[Y/N]", end=' ')
choose = input().upper()
if not choose == "N":
    os.system("sudo apt upgrade -y")
if os.system("which wine > /dev/null"):
    print("请问是否要安装原版 wine（wine64）？[Y/N]", end=' ')
    choose = input().upper()
    if not choose == "N":
        os.system("sudo apt install wine -y")
if os.system("which deepin-wine > /dev/null"):
    print("请问是否要安装 deepin-wine？[Y/N]", end=' ')
    choose = input().upper()
    if not choose == "N":
        os.system("sudo apt install deepin-wine -y")
if os.system("which deepin-wine5 > /dev/null"):
    print("请问是否要安装 deepin-wine5（需要安装最新版星火应用商店）？[Y/N]", end=' ')
    choose = input().upper()
if os.system("which deepin-wine5-stable > /dev/null"):
    print("请问是否要安装 deepin-wine5-stable？[Y/N]", end=' ')
    choose = input().upper()
    if not choose == "N":
        os.system("sudo apt install deepin-wine5-stable -y")
if os.system("which deepin-wine6-stable > /dev/null"):
    print("请问是否要安装 deepin-wine6-stable？[Y/N]", end=' ')
    choose = input().upper()
    if not choose == "N":
        os.system("sudo apt install deepin-wine6-stable -y")
if os.system("which spark-wine7-devel > /dev/null"):
    print("请问是否要安装 spark-wine7-devel（需要安装最新版星火应用商店）？[Y/N]", end=' ')
    choose = input().upper()
    if not choose == "N":
        InstallSparkWine("spark-wine7-devel")
if os.system("which ukylin-wine > /dev/null"):
    print("请问是否要安装 ukylin-wine（需要添加 ukylin 源，但因为可能会导致系统问题，将不会自动添加）？[Y/N]", end=" ")
    choose = input().upper()
    if not choose == "N":
        os.system("sudo apt install ukylin-wine -y")
print("全部完成！")