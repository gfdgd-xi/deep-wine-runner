#!/usr/bin/env python3
# 使用系统默认的 python3 运行
###########################################################################################
# 作者：gfdgd xi
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
import json
import updatekiller
import req as requests
try:
    sourcesList = [
        "https://code.gitlink.org.cn/gfdgd_xi/wine-runner-list/raw/branch/master/net/list.json",
        "http://gfdgdxi.msns.cn/wine-runner-list/net/list.json"
    ]
    netList = json.loads(requests.get(sourcesList[0]).text)
except:
    netList = [
        ["Microsoft® .NET Framework 1.1 版可转散发套件", "https://download.microsoft.com/download/8/2/7/827bb1ef-f5e1-4464-9788-40ef682930fd/dotnetfx.exe"],
        ["Microsoft .NET Framework 2.0 Service Pack 1 (x86)", "https://download.microsoft.com/download/0/8/c/08c19fa4-4c4f-4ffb-9d6c-150906578c9e/NetFx20SP1_x86.exe"],
        ["3.5 SP1 Offline Installer", "https://download.visualstudio.microsoft.com/download/pr/b635098a-2d1d-4142-bef6-d237545123cb/2651b87007440a15209cac29634a4e45/dotnetfx35.exe"], 
        ["4.0 Offline Installer", "https://download.microsoft.com/download/9/5/A/95A9616B-7A37-4AF6-BC36-D6EA96C8DAAE/dotNetFx40_Full_x86_x64.exe"],
        ["4.5 Web Installer", "https://download.microsoft.com/download/B/A/4/BA4A7E71-2906-4B2D-A0E1-80CF16844F5F/dotNetFx45_Full_setup.exe"],
        ["4.5.1 Offline Installer", "https://download.microsoft.com/download/1/6/7/167F0D79-9317-48AE-AEDB-17120579F8E2/NDP451-KB2858728-x86-x64-AllOS-ENU.exe"],
        ["4.5.2 Offline Installer", "https://download.microsoft.com/download/E/2/1/E21644B5-2DF2-47C2-91BD-63C560427900/NDP452-KB2901907-x86-x64-AllOS-ENU.exe"],
        ["4.6 Offline Installer", "https://download.microsoft.com/download/6/F/9/6F9673B1-87D1-46C4-BF04-95F24C3EB9DA/enu_netfx/NDP46-KB3045557-x86-x64-AllOS-ENU_exe/NDP46-KB3045557-x86-x64-AllOS-ENU.exe"],
        ["4.6.1 Offline Installer", "https://download.microsoft.com/download/E/4/1/E4173890-A24A-4936-9FC9-AF930FE3FA40/NDP461-KB3102436-x86-x64-AllOS-ENU.exe"],
        ["4.6.2 Offline Installer", "https://download.visualstudio.microsoft.com/download/pr/8e396c75-4d0d-41d3-aea8-848babc2736a/80b431456d8866ebe053eb8b81a168b3/ndp462-kb3151800-x86-x64-allos-enu.exe"],
        ["4.7 Offline Installer", "https://download.visualstudio.microsoft.com/download/pr/2dfcc711-bb60-421a-a17b-76c63f8d1907/e5c0231bd5d51fffe65f8ed7516de46a/ndp47-kb3186497-x86-x64-allos-enu.exe"],
        ["4.7.1 Offline Installer", "https://download.visualstudio.microsoft.com/download/pr/4312fa21-59b0-4451-9482-a1376f7f3ba4/9947fce13c11105b48cba170494e787f/ndp471-kb4033342-x86-x64-allos-enu.exe"],
        ["4.7.2 Offline Installer", "https://download.visualstudio.microsoft.com/download/pr/1f5af042-d0e4-4002-9c59-9ba66bcf15f6/089f837de42708daacaae7c04b7494db/ndp472-kb4054530-x86-x64-allos-enu.exe"],
        ["4.8 Offline Installer", "https://download.visualstudio.microsoft.com/download/pr/2d6bb6b2-226a-4baa-bdec-798822606ff1/8494001c276a4b96804cde7829c04d7f/ndp48-x86-x64-allos-enu.exe"],
        ["4.8.1 Offline Installer", "https://download.visualstudio.microsoft.com/download/pr/6f083c7e-bd40-44d4-9e3f-ffba71ec8b09/3951fd5af6098f2c7e8ff5c331a0679c/ndp481-x86-x64-allos-enu.exe"],
        [".NET 5.0 Desktop Runtime (v5.0.17) - Windows x86 Installer", "https://download.visualstudio.microsoft.com/download/pr/b6fe5f2a-95f4-46f1-9824-f5994f10bc69/db5ec9b47ec877b5276f83a185fdb6a0/windowsdesktop-runtime-5.0.17-win-x86.exe"],
        [".NET 5.0 Desktop Runtime (v5.0.17) - Windows x64 Installer", "https://download.visualstudio.microsoft.com/download/pr/3aa4e942-42cd-4bf5-afe7-fc23bd9c69c5/64da54c8864e473c19a7d3de15790418/windowsdesktop-runtime-5.0.17-win-x64.exe"],
        [".NET 5.0 Desktop Runtime (v5.0.17) - Windows Arm64 Installer", "https://download.visualstudio.microsoft.com/download/pr/be25784a-4231-4c53-ba6e-869166ef523f/9602c6c0d358d31dc710fd0573fc39e0/windowsdesktop-runtime-5.0.17-win-arm64.exe"],
        [".NET Core 3.0 Desktop Runtime (v3.0.3) - Windows x86 Installer", "https://download.visualstudio.microsoft.com/download/pr/e312618d-85c4-4cad-b660-569b5522eca9/e951e76ebe011b5d3ea1289ef68e8281/windowsdesktop-runtime-3.0.3-win-x86.exe"],
        [".NET Core 3.0 Desktop Runtime (v3.0.3) - Windows x64 Installer", "https://download.visualstudio.microsoft.com/download/pr/c525a2bb-6e98-4e6e-849e-45241d0db71c/d21612f02b9cae52fa50eb54de905986/windowsdesktop-runtime-3.0.3-win-x64.exe"],
        [".NET Core 3.1 Desktop Runtime (v3.1.28) - Windows x86 Installer", "https://download.visualstudio.microsoft.com/download/pr/d2ec7ca2-017d-4d06-a6da-3707daa3c3b1/1f2e108653e3d8316e1657105ef24b93/windowsdesktop-runtime-3.1.28-win-x86.exe"],
        [".NET Core 3.1 Desktop Runtime (v3.1.28) - Windows x64 Installer", "https://download.visualstudio.microsoft.com/download/pr/5c74593e-f156-44c8-9957-f11996de72bc/d3e0e26c64a5a2d860c5c0deca975d78/windowsdesktop-runtime-3.1.28-win-x64.exe"],
        [".NET 6.0 Desktop Runtime (v6.0.8) - Windows x86 Installer", "https://download.visualstudio.microsoft.com/download/pr/61747fc6-7236-4d5e-85e5-a5df5f480f3a/02203594bf1331f0875aa6491419ffa1/windowsdesktop-runtime-6.0.8-win-x86.exe"],
        [".NET 6.0 Desktop Runtime (v6.0.8) - Windows x64 Installer", "https://download.visualstudio.microsoft.com/download/pr/b4a17a47-2fe8-498d-b817-30ad2e23f413/00020402af25ba40990c6cc3db5cb270/windowsdesktop-runtime-6.0.8-win-x64.exe"],
        [".NET 6.0 Desktop Runtime (v6.0.8) - Windows Arm64 Installer", "https://download.visualstudio.microsoft.com/download/pr/17737b16-dbb0-45f8-9684-16cce46f0835/14475e8380422840249513d58c70d8da/windowsdesktop-runtime-6.0.8-win-arm64.exe"]
    ]

def Download(wineBotton: str, id: int, wine: str):
    programName = os.path.split(netList[id][1])[1]
    os.system(f"aria2c -x 16 -s 16 -d \"/tmp/deepin-wine-runner-net\" -o \"{programName}\" \"{netList[id][1]}\"")
    return os.system(f"WINEPREFIX='{wineBotton}' {wine} '/tmp/deepin-wine-runner-net/{programName}'")

if __name__ == "__main__":
    if "--help" in sys.argv:
        print("作者：gfdgd xi")
        print("版本：1.0.0")
        print("本程序可以更方便的在 wine 容器中安装 .net framework")
        sys.exit()
    if len(sys.argv) <= 2 or sys.argv[1] == "" or sys.argv[2] == "":
        print("您未指定需要安装 .net framework 的容器和使用的 wine，无法继续")
        print("参数：")
        print("XXX 参数一 参数二 参数三(可略)")
        print("参数一为需要安装的容器，参数二为需要使用的wine，参数三为是否缓存（可略），三个参数位置不能颠倒")
        sys.exit()

    homePath = os.path.expanduser('~')
    print('''                            
        mm   m mmmmmmmmmmmmm
        #"m  # #        #   
        # #m # #mmmmm   #   
        #  # # #        #   
   #    #   ## #mmmmm   #   
                            
                            
''')
    print("请选择以下的 .net framework 进行安装（不保证能正常安装运行）")
    for i in range(0, len(netList)):
        print(f"{i} .net framework {netList[i][0]}")
    while True:
        try:
            choose = input("请输入要选择的 .net framework 版本（输入“exit”退出）：").lower()
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
    if len(sys.argv) <= 3:
        choice = True
    else:
        choice = (sys.argv[3] == "1")
    print(f"您选择了 .net framework {netList[choose][0]}")
    print(f"如果是 Offline Installer 版本，提示需要连接互联网，其实是不需要的，断网也可以安装")
    print(f"如果 Offline Installer 版本连接网络时安装失败，提示无法连接服务器或连接超时，可以尝试下载完安装包加载过程中断网以便断网安装")
    print(f"一般建议 Offline Installer 版本在下载完 exe 安装程序后在加载过程中断网以便提高安装速度")
    programName = os.path.split(netList[choose][1])[1]
    if os.path.exists(f"{homePath}/.cache/deepin-wine-runner/.netframework/{programName}") and choice:
        print("已经缓存，使用本地版本")
        os.system(f"WINEPREFIX='{sys.argv[1]}' {sys.argv[2]} '{homePath}/.cache/deepin-wine-runner/.netframework/{programName}'")
        input("安装结束，按回车键退出")
        exit()
    print("开始下载")
    os.system(f"rm -rf '{homePath}/.cache/deepin-wine-runner/.netframework/{programName}'")
    os.system(f"mkdir -p '{homePath}/.cache/deepin-wine-runner/.netframework'")
    os.system(f"aria2c -x 16 -s 16 -d \"{homePath}/.cache/deepin-wine-runner/.netframework\" -o \"{programName}\" \"{netList[choose][1]}\"")
    os.system(f"WINEPREFIX='{sys.argv[1]}' {sys.argv[2]} '{homePath}/.cache/deepin-wine-runner/.netframework/{programName}'")
    input("安装结束，按回车键退出")
