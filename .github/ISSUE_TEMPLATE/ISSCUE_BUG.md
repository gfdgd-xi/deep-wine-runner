---
name: 程序bug
about: 反馈程序的故障
---
需要把下面的替换成自己的信息，下面为例子

# 故障表现（最好带图、日志）
按右上角叉叉可以关闭运行器  
![图片.png](https://storage.deepin.org/thread/202308132203366743_图片.png)  
## 日志（终端输入 `deepin-wine-runner` 输出的内容）
```
gfdgd_xi@gfdgdxi-PC:~$ deepin-wine-runner
/usr/bin/deepin-terminal
/usr/bin/deepin-wine6-stable
/usr/bin/deepin-wine
/usr/bin/qemu-i386-static
/usr/bin/qemu-i386
/usr/bin/qemu-x86_64
['', '']
/usr/bin/qemu-i386
/usr/bin/qemu-x86_64
['', '']
{'基于 UOS box86 的 deepin-wine6-stable': "WINEPREDLL='/opt/apps/deepin-wine-runner/dlls-arm' WINEDLLPATH=/opt/deepin-wine6-stable/lib BOX86_NOSIGSEGV=1 /opt/deepin-box86/box86 /opt/deepin-wine6-stable/bin/wine ", '基于 UOS exagear 的 deepin-wine6-stable': "WINEPREDLL='/opt/apps/deepin-wine-runner/dlls-arm' WINEDLLPATH=/opt/deepin-wine6-stable/lib /opt/exagear/bin/ubt_x64a64_al --path-prefix /home/gfdgd_xi/.deepinwine/debian-buster --utmp-paths-list /home/gfdgd_xi/.deepinwine/debian-buster/.exagear/utmp-list --vpaths-list /home/gfdgd_xi/.deepinwine/debian-buster/.exagear/vpaths-list --opaths-list /home/gfdgd_xi/.deepinwine/debian-buster/.exagear/opaths-list --smo-mode fbase --smo-severity smart --fd-limit 8192 --foreign-ubt-binary /opt/exagear/bin/ubt_x32a64_al -- /opt/deepin-wine6-stable/bin/wine ", '使用 Flatpak 安装的 Wine': 'flatpak run org.winehq.Wine', 'deepin-wine6 stable': 'deepin-wine6-stable', 'deepin-wine5 stable': 'deepin-wine5-stable', 'spark-wine': 'spark-wine', 'spark-wine7-devel': 'spark-wine7-devel', 'spark-wine8': 'spark-wine8', 'deepin-wine': 'deepin-wine', 'deepin-wine5': 'deepin-wine5', 'wine': 'wine', 'wine64': 'wine64', 'ukylin-wine': 'ukylin-wine', 'mono（这不是 wine，但可以实现初步调用运行 .net 应用）': 'mono', '基于 linglong 的 deepin-wine6-stable（不推荐）': "ll-cli run '' --exec '/bin/deepin-wine6-stable'", '/opt/apps/deepin-wine-runner/wine/wine-ce-8.13-amd64/bin/wine': '/opt/apps/deepin-wine-runner/wine/wine-ce-8.13-amd64/bin/wine', '/opt/apps/deepin-wine-runner/wine/wine-ce-8.13-amd64/bin/wine-aarch64': '/opt/apps/deepin-wine-runner/wine/wine-ce-8.13-amd64/bin/wine-aarch64', '/opt/apps/deepin-wine-runner/wine/wine-ce-8.13-riscv64/bin/wine': '/opt/apps/deepin-wine-runner/wine/wine-ce-8.13-riscv64/bin/wine', '/opt/apps/deepin-wine-runner/wine/wine-ce-8.13-riscv64/bin/wine-i386': '/opt/apps/deepin-wine-runner/wine/wine-ce-8.13-riscv64/bin/wine-i386', '/opt/apps/deepin-wine-runner/wine/wine-ce-8.13-riscv64/bin/wine-aarch64': '/opt/apps/deepin-wine-runner/wine/wine-ce-8.13-riscv64/bin/wine-aarch64', '/opt/apps/deepin-wine-runner/wine/wine-ce-8.13-riscv64/bin/wine-x86_64': '/opt/apps/deepin-wine-runner/wine/wine-ce-8.13-riscv64/bin/wine-x86_64', '/home/gfdgd_xi/.deepinwine/wine-ce-8.13-amd64/bin/wine': '/home/gfdgd_xi/.deepinwine/wine-ce-8.13-amd64/bin/wine'}
[['cmd', 'cmd'], ['cmd', 'cmd.exe'], ['cmd', 'wineBottonPath/drive_c/windows/system32/cmd.exe'], ['Internet Explorer', 'iexplore'], ['Internet Explorer', 'iexplore.exe'], ['Internet Explorer', 'wineBottonPath/drive_c/Program Files/Internet Explorer/iexplore.exe'], ['Internet Explorer', 'wineBottonPath/drive_c/Program Files (x86)/Internet Explorer/iexplore.exe'], ['微信', 'wineBottonPath/drive_c/Program Files/Tencent/WeChat/WeChat.exe'], ['微信', 'wineBottonPath/drive_c/Program Files (x86)/Tencent/WeChat/WeChat.exe'], ['UltraISO', 'wineBottonPath/drive_c/Program Files/UltraISO/UltraISO.exe'], ['UltraISO', 'wineBottonPath/drive_c/Program Files (x86)/UltraISO/UltraISO.exe'], ['迅雷', 'wineBottonPath/drive_c/Program Files/Thunder Network/MiniThunder/Bin/ThunderMini.exe'], ['迅雷', 'wineBottonPath/drive_c/Program Files (x86)/Thunder Network/MiniThunder/Bin/ThunderMini.exe'], ['Microsoft Office Word', 'wineBottonPath/drive_c/Program Files/Microsoft Office/Office12/WINWORD.EXE'], ['Microsoft Office Word', 'wineBottonPath/drive_c/Program Files (x86)/Microsoft Office/Office12/WINWORD.EXE'], ['腾讯会议', 'wineBottonPath/drive_c/Program Files/Tencent/WeMeet/wemeetapp.exe'], ['腾讯会议', 'wineBottonPath/drive_c/Program Files (x86)/Tencent/WeMeet/wemeetapp.exe'], ['腾讯课堂', 'wineBottonPath/drive_c/Program Files/Tencent/EDU/bin/TXEDU.exe'], ['腾讯课堂', 'wineBottonPath/drive_c/Program Files (x86)/Tencent/EDU/bin/TXEDU.exe'], ['QQ', 'wineBottonPath/drive_c/Program Files/Tencent/QQ/Bin/QQ.exe'], ['QQ', 'wineBottonPath/drive_c/Program Files (x86)/Tencent/QQ/Bin/QQ.exe'], ['TIM', 'wineBottonPath/drive_c/Program Files/Tencent/TIM/Bin/TIM.exe'], ['TIM', 'wineBottonPath/drive_c/Program Files (x86)/Tencent/TIM/Bin/TIM.exe']]
lock
libpng warning: iCCP: known incorrect sRGB profile
libpng warning: iCCP: known incorrect sRGB profile
libpng warning: iCCP: known incorrect sRGB profile
libpng warning: iCCP: known incorrect sRGB profile
libpng warning: iCCP: known incorrect sRGB profile
libpng warning: iCCP: known incorrect sRGB profile
libpng warning: iCCP: known incorrect sRGB profile
libpng warning: iCCP: known incorrect sRGB profile
create icon [font] engine failed.[theme:bloom-dark] nonCache[theme].size[0] (No such file or directory)
create icon [floppy_unmount] engine failed.[theme:bloom-dark] nonCache[theme].size[1] (No such file or directory)
create icon [3floppy_unmount] engine failed.[theme:bloom-dark] nonCache[theme].size[2] (No such file or directory)
检测到库 riscv64
检测到库 arm64
检测到库 armhf
检测到库 i386
检测到库 s390x
检测到库 mips64el
检测到库 ppc64el
检测到库 amd64
版本号为：3.4.0
普通版本
qt.qpa.xcb: QXcbConnection: XCB error: 5 (BadAtom), sequence: 390, resource id: 0, major code: 20 (GetProperty), minor code: 0
```

# 系统版本
- 系统：Deepin 23
- 硬件：
    ![图片.png](https://storage.deepin.org/thread/202308132200482953_图片.png)
- 其他补充信息

# 之前做过什么操作
在终端里输入了内容
```bash
sudo apt upgrade
```
更新了系统

# 复现步骤
1. 打开运行器，然后点击右上角叉叉可以关闭

# 推测故障原因（可选）
Qt 默认有一套配置好的退出事件

