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
import traceback
import pyquery

if "--help" in sys.argv:
    print("作者：gfdgd xi、为什么您不喜欢熊出没和阿布呢")
    print("版本：1.0.0")
    print("本程序可以更方便的在 wine 容器中安装 mono、gecko")
    sys.exit()
if len(sys.argv) <= 3 or sys.argv[1] == "" or sys.argv[2] == "" or sys.argv[3] == "":
    print("您未指定需要安装 gecko 或者 mono 的容器和使用的 wine，无法继续")
    print("参数：")
    print("XXX 参数一 参数二 参数三 参数四(可略)")
    print("参数一为需要安装的容器，参数二为需要使用的wine，参数三为安装gecko或mono（gecko/mono），参数四为是否缓存（可略），四个参数位置不能颠倒")
    sys.exit()

if sys.argv[3] == "mono":
    print('''                            
 m    m                     
 ##  ##  mmm   m mm    mmm  
 # ## # #" "#  #"  #  #" "# 
 # "" # #   #  #   #  #   # 
 #    # "#m#"  #   #  "#m#" 
                            
                            
''')
else:
    print('''                                   
   mmm                #            
 m"   "  mmm    mmm   #   m   mmm  
 #   mm #"  #  #"  "  # m"   #" "# 
 #    # #""""  #      #"#    #   # 
  "mmm" "#mm"  "#mm"  #  "m  "#m#" 
                                   
                                   
''')
homePath = os.path.expanduser('~')
try:
    exitInputShow = int(os.getenv("ENTERNOTSHOW"))
except:
    exitInputShow = True
try:
    # 获取最新版本的版本号
    programVersionList = pyquery.PyQuery(url=f"http://mirrors.ustc.edu.cn/wine/wine/wine-{sys.argv[3]}/")
except:
    print("无法连接下载服务器，将使用本地缓存")
    if not os.path.exists(f"{homePath}/.cache/deepin-wine-runner/{sys.argv[3]}/install.msi") or not os.path.exists(f"{homePath}/.cache/deepin-wine-runner/{sys.argv[3]}/information.txt"):
        print("无本地缓存数据，无法进行、结束")
        if exitInputShow:
            input("按回车键退出")
        exit()
    file = open(f"{homePath}/.cache/deepin-wine-runner/{sys.argv[3]}/information.txt", "r")
    version = file.read().replace("\n", "")    
    print("安装版本:", version)
    os.system(f"WINEPREFIX='{sys.argv[1]}' '{sys.argv[2]}' msiexec /i \"{homePath}/.cache/deepin-wine-runner/{sys.argv[3]}/install.msi\"")
    if exitInputShow:
        input("安装结束，按回车键退出")
    exit()
programVersion = programVersionList("a:last-child").attr.href
# 获取最新版本安装包的URL
programUrl = pyquery.PyQuery(url=f"http://mirrors.ustc.edu.cn/wine/wine/wine-{sys.argv[3]}/{programVersion}")
programDownloadUrl = ""
programFileName = ""
for i in programUrl("a").items():
    if i.attr.href[-4:] == ".msi":
        programDownloadUrl = f"http://mirrors.ustc.edu.cn/wine/wine/wine-{sys.argv[3]}/{programVersion}{i.attr.href}"
        programFileName = i.attr.href
        break

if programDownloadUrl == "":
    print("无法获取链接，无法继续")
    sys.exit()
print(f"当前选择的程序获取路径：{programDownloadUrl}")
if not os.path.exists(f"{homePath}/.cache/deepin-wine-runner/{sys.argv[3]}"):
    os.makedirs(f"{homePath}/.cache/deepin-wine-runner/{sys.argv[3]}")
if len(sys.argv) <= 4:
    choice = True
else:
    choice = (sys.argv[3] == "1")
if os.path.exists(f"{homePath}/.cache/deepin-wine-runner/{sys.argv[3]}/install.msi") and os.path.exists(f"{homePath}/.cache/deepin-wine-runner/{sys.argv[3]}/information.txt") and choice:
    print("版本号校验")
    file = open(f"{homePath}/.cache/deepin-wine-runner/{sys.argv[3]}/information.txt", "r")
    version = file.read().replace("\n", "")
    if version == programVersion.replace("\n", ""):
        print("缓存版本:", version.replace("/", ""))
        print("已经缓存，使用本地版本")
        file.close()
        os.system(f"WINEPREFIX='{sys.argv[1]}' '{sys.argv[2]}' msiexec /i \"{homePath}/.cache/deepin-wine-runner/{sys.argv[3]}/install.msi\"")
        if exitInputShow:
            input("安装结束，按回车键退出")
        exit()

file = open(f"{homePath}/.cache/deepin-wine-runner/{sys.argv[3]}/information.txt", "w+")  
print("开始下载")
os.system(f"rm -rf \"{homePath}/.cache/deepin-wine-runner/{sys.argv[3]}/install.msi\"")
os.system("mkdir -p /tmp/winegeckomonoinstall")
os.system(f"aria2c -x 16 -s 16 -d \"{homePath}/.cache/deepin-wine-runner/{sys.argv[3]}\" -o install.msi \"{programDownloadUrl}\"")
print("开始安装")
os.system(f"WINEPREFIX='{sys.argv[1]}' '{sys.argv[2]}' msiexec /i \"{homePath}/.cache/deepin-wine-runner/{sys.argv[3]}/install.msi\"")
try:
    if sys.argv[4] == "1":
        print("写入缓存")
        file.write(programVersion)
        file.close()
    else:
        print("删除临时文件")
        os.system(f"rm -rf \"{homePath}/.cache/deepin-wine-runner/{sys.argv[3]}\"")
except:
    print("写入缓存")
    file.write(programVersion)
    file.close()
if exitInputShow:
    input("安装结束，按回车键退出")