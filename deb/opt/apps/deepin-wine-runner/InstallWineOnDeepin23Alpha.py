#!/usr/bin/env python3
# 使用系统默认的 python3 运行
###########################################################################################
# 作者：gfdgd xi、为什么您不喜欢熊出没和阿布呢
# 版本：2.5.0
# 更新时间：2022年11月15日
# 感谢：感谢 wine 以及 deepin-wine 团队，提供了 wine 和 deepin-wine 给大家使用，让我能做这个程序
# 基于 Python3 构建
###########################################################################################
#################
# 引入所需的库
#################
import os
import webbrowser
import updatekiller

def YesOrNo():
    if input().replace(" ", "").upper() == "N":
        return False
    return True

def InstallWineSpark(wine):
    print(f"开始安装 {wine}")
    #os.system("pkexec apt update")
    if not os.system(f"pkexec aptss install {wine} -y"):
        print(f"{wine} 安装失败！")
        PressEnter()
    else:
        print("安装完成")

def InstallWine(wine):
    print(f"开始安装 {wine}")
    os.system("pkexec apt update")
    if not os.system(f"pkexec apt install {wine} -y"):
        print(f"{wine} 安装失败！")
        PressEnter()
    else:
        print("安装完成")

def CheckSparkStore():
    return os.system("which spark-store > /dev/null") + os.system("which aptss > /dev/null")

def InstallSparkStore():
    if not CheckSparkStore:
        return
    print("按下回车键后打开星火应用商店官网，手动安装完星火应用商店后再次按下回车以继续")
    webbrowser.open_new_tab("https://spark-app.store/")
    PressEnter()
    print("安装星火应用商店后按下回车……")
    PressEnter()
    while True:
        if not os.system("which spark-store > /dev/null"):
            if not os.system("which aptss > /dev/null"):
                break
            print("您暂未安装最新版本的星火应用商店，请更新版本后按下回车")
            PressEnter()
            continue
        print("您暂未安装星火应用商店，请在安装后按下回车")    
        PressEnter()
        continue

def InstallDeepinAppStore():
    print("开始安装官方应用商店")
    if not os.system("pkexec apt install deepin-app-store -y"):
        print("安装失败！按回车键后退出")
        PressEnter()
        exit()
    else:
        print("安装完成")

def PressEnter():
    input("按回车键后继续……")

if __name__ == "__main__":
    print('''                            
m     m   "                 
#  #  # mmm    m mm    mmm  
" #"# #   #    #"  #  #"  # 
 ## ##"   #    #   #  #"""" 
 #   #  mm#mm  #   #  "#mm" 
                            
                            
''')
    print("后续操作需要有 root 权限")
    programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
    # 敢这样浪不还是 Alpha 源有官方应用商店
    if os.system("which deepin-home-appstore-client > /dev/null"):
        print("暂未安装官方应用商店，安装后才能继续，是否安装？[Y/N]")
        if YesOrNo:
            InstallDeepinAppStore()
    deepinWineList = [
        #"deepin-wine",
        #"deepin-wine5-stable",
        "deepin-wine6-stable"
    ]
    for i in deepinWineList:
        if not os.system(f"which {i} > /dev/null"):
            print(f"{i} 已安装")
            continue
        print(f"是否安装 {i}？[Y/N]")
        if YesOrNo:
            InstallWine(i)
    sparkWineList = [
        #"deepin-wine",
        #"deepin-wine5",
        #"spark-wine7-devel"
    ]
    for i in sparkWineList:
        if not os.system(f"which {i} > /dev/null"):
            continue
        print(f"是否安装 {i}？[Y/N]")
        if YesOrNo:
            InstallSparkStore()
            InstallWineSpark(i)
    print("按回车键退出")
    PressEnter()
    exit()
