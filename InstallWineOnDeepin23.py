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

def InstallWithDeepinSource(program):
    os.system(f"sudo cp '{programPath}/deepin.list' /etc/apt/sources.list.d/deepin20-withwinerunner.list")
    os.system(f"sudo dpkg --add-architecture i386")
    os.system(f"sudo apt update")
    os.system(f"sudo apt install {program}")
    os.system(f"sudo rm /etc/apt/sources.list.d/deepin20-withwinerunner.list")
    os.system(f"sudo apt update")
    os.system(f"sudo dpkg --remove-architecture i386")
    os.system(f"sudo apt update")

def InstallWithSparkStoreSource(program):
    os.system(f"sudo cp '{programPath}/sparkstore.list' /etc/apt/sources.list.d/sparkstore-withwinerunner.list")
    os.system(f"sudo cp '{programPath}/deepin.list' /etc/apt/sources.list.d/deepin20-withwinerunner.list")
    os.system(f"sudo dpkg --add-architecture i386")
    os.system(f"sudo mkdir /tmp/spark-store-install")
    os.system(f"sudo rm -rf /tmp/spark-store-install/spark-store.asc")
    os.system(f"sudo wget -O /tmp/spark-store-install/spark-store.asc https://d.store.deepinos.org.cn/dcs-repo.gpg-key.asc")
    os.system(f"sudo gpg --dearmor /tmp/spark-store-install/spark-store.asc")
    os.system(f"sudo apt update")
    os.system(f"sudo apt install {program}")
    os.system(f"sudo rm /etc/apt/sources.list.d/sparkstore-withwinerunner.list")
    os.system(f"sudo rm /etc/apt/sources.list.d/deepin20-withwinerunner.list")
    os.system(f"sudo apt update")
    os.system(f"sudo dpkg --remove-architecture i386")
    os.system(f"sudo apt update")

def Repair():
    print("修复中……")
    os.system(f"rm -f /etc/apt/sources.list.d/sparkstore-withwinerunner.list")
    os.system(f"rm -f /etc/apt/sources.list.d/deepin20-withwinerunner.list")
    print("修复完成！")

if __name__ == "__main__":
    print('''                            
m     m   "                 
#  #  # mmm    m mm    mmm  
" #"# #   #    #"  #  #"  # 
 ## ##"   #    #   #  #"""" 
 #   #  mm#mm  #   #  "#mm" 
                            
                            
''')
    programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
    print("能不用这个就不用这个！！！真心建议！！！\n")
    print("下面的安装过程皆需要换源等操作，安装过程千万不要中断，以及千万不要 apt upgrade，感谢\n")
    print("如果真一不小心中断了，可以在下面输入“repair”进行修复")
    print("所有操作均需要 Root 权限，请知悉\n")
    print("千万不要中断且 apt upgrade、千万不要中断且 apt upgrade、千万不要中断且 apt upgrade，重要的事情说三遍")
    print("以及无法保证安装的 Wine 能使用、无法保证安装的 Wine 能使用、无法保证安装的 Wine 能使用，重要的事情说三遍")
    repair = input("按回车后继续")
    if repair.lower() == "repair":
        Repair()
        exit()
    for i in [
        ["原版 Wine（Wine64）", "wine"],
        ["deepin-wine5-stable", "deepin-wine5-stable"],
        ["deepin-wine6-stable", "deepin-wine6-stable"]
    ]:
        if not os.system(f"which {i[1]} > /dev/null"):
            continue
        choose = input(f"安装{i[0]}?（添加深度源）[Y/N]").upper()
        if choose == "Y":
            print("安装中……")
            InstallWithDeepinSource(i[1])
            print("安装完成！")
    #exit()
    for i in [
        ["deepin-wine", "deepin-wine"],
        ["spark-wine7-devel", "spark-wine7-devel"]
    ]:
        if not os.system(f"which {i[1]} > /dev/null"):
            continue
        choose = input(f"安装{i[0]}?（添加深度、星火源）[Y/N]").upper()
        if choose == "Y":
            InstallWithSparkStoreSource(i[1])
    input("按回车键后退出……")
    exit()