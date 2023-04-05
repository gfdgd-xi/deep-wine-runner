#!/usr/bin/env python3
import os
import updatekiller

if __name__ == "__main__":
    print('''                                   
   mmm  ""#                        
 m"   "   #     mmm    mmm   m mm  
 #        #    #"  #  "   #  #"  # 
 #        #    #""""  m"""#  #   # 
  "mmm"   "mm  "#mm"  "mm"#  #   # 
                                   
                                   
''')
    programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
    print("此程序可以帮助您删除程序无需的组件以节约空间")
    print("如果全部删除，将只会有核心功能")
    print("如果删除后想要恢复这样组件需要重新安装该软件包")
    delProgramList = []
    delProramCommand = "#!/bin/bash\n"
    for i in [
        [
            "含有商业软件的内容",
            [
                f"{programPath}/StartVM.sh",
	            f"{programPath}/RunVM.sh",
	            f"{programPath}/VM",
	            "/usr/share/applications/spark-deepin-wine-runner-control-vm.desktop",
	            "/usr/share/applications/spark-deepin-wine-runner-start-vm.desktop",
                f"{programPath}/BeCyIconGrabber.exe",
                f"{programPath}/geek.exe",
                f"{programPath}/窗体透明度设置工具.exe",
                f"{programPath}/UpdateGeek.sh",
                f"{programPath}/AppStore.py",
                f"{programPath}/InstallFont.py",
                f"{programPath}/InstallMsxml.py",
                f"{programPath}/InstallNetFramework.py",
                f"{programPath}/InstallOther.py",
                f"{programPath}/InstallVisualCPlusPlus.py"
            ]
        ],
        [
            "Wine 打包器（不基于生态打包脚本）", 
            [
                f"{programPath}/deepin-wine-packager.py",
                f"{programPath}/exagear",
                f"{programPath}/exagear.7z",
                f"{programPath}/exagear",
                f"{programPath}/wined3d.dll.so.7z",
                f"{programPath}/wined3d.dll.so",
                "/usr/bin/deepin-wine-package-builder",
                "/usr/share/applications/spark-deepin-wine-package-builder.desktop"
            ]
        ],
        [
            "Wine 打包器（基于生态打包脚本）", 
            [
                f"{programPath}/deepin-wine-packager-with-script.py",
                f"{programPath}/package-script.zip",
                f"{programPath}/package-script",
                "/usr/bin/deepin-wine-packager-with-script",
                "/usr/share/applications/spark-deepin-wine-packager-with-script.desktop"
            ]
        ],
        [
            "Arm 64 box86 wine 运行 DLL",
            [
                f"{programPath}/dlls-arm.7z",
                f"{programPath}/dlls-arm",
                f"{programPath}/wined3d.dll.so.7z",
                f"{programPath}/wined3d.dll.so"
            ]
        ],
        [
            "Windows 虚拟机简易安装组件",
            [
                f"{programPath}/StartVM.sh",
	            f"{programPath}/RunVM.sh",
	            f"{programPath}/VM",
	            "/usr/share/applications/spark-deepin-wine-runner-control-vm.desktop",
	            "/usr/share/applications/spark-deepin-wine-runner-start-vm.desktop"
            ]
        ],
        [
            "Wine 安装组件",
            [
                f"{programPath}/AllInstall.py",
                f"{programPath}/wine install",
                f"{programPath}/InstallWineOnDeepin23.py",
                f"{programPath}/sparkstore.list",
                f"{programPath}/InstallNewWineHQ.sh",
                f"{programPath}/wine",
                "/usr/bin/deepin-wine-runner-wine-installer",
                "/usr/bin/deepin-wine-runner-wine-install-deepin23",
                "/usr/bin/deepin-wine-runner-wine-install",
                "/usr/bin/deepin-wine-runner-winehq-install"
            ]
        ]
    ]:
        if not os.path.exists(i[1][0]):
            continue
        if input(f"是否删除组件“{i[0]}”？[Y/n]").upper() == "Y":
            delProgramList.append(i)
            for x in i[1]:
                if x == "/*" or x == "/":  # 为了防止个人疏忽，出现危险命令，所以如果有最危险的 /* 会直接跳过该命令的写入
                    continue
                delProramCommand += f"rm -rfv \"{x}\"\n"
    if len(delProgramList) == 0:
        print("您已经删除了所有可删除的组件，如果需要使用被删除的组件，请重新安装该软件安装包")
        input("按回车退出")
        exit()
    print("开始删除")
    file = open("/tmp/deepin-wine-clean.sh", "w")
    file.write(delProramCommand)
    file.close()
    os.system("pkexec bash /tmp/deepin-wine-clean.sh")
    input("按回车键退出程序")