#!/bin/bash
export PATH=/opt/apps/deepin-wine-runner-qemu-system-extra/files/usr/local/bin:$PATH
echo 推荐使用 Wine 运行器的虚拟机管理工具调用 Qemu,如果安装了 Wine 运行器输入命令 
echo /opt/apps/deepin-wine-runner/StartVM.sh
echo 启动虚拟机管理工具
echo Wine 运行器地址：https://gitee.com/gfdgd-xi/deep-wine-runner
echo ==========================
echo 也可以通过命令调用，输入 qemu-system-x86_64 开始吧
echo 可输入命令 qemu-commands-list 查看支持的命令
echo 当前 Qemu 版本：
qemu-system-x86_64 --version
echo ©2020~`date +%Y` gfdgd xi
echo ==========================
if [ $# -eq 0 ]; then
    echo 进入交互环境：
    bash
else
    bash -c $@
fi
exit $?