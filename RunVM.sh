#!/bin/bash
# 使用系统默认的 bash 运行
###########################################################################################
# 作者：gfdgd xi、为什么您不喜欢熊出没和阿布呢
# 版本：1.7.0
# 更新时间：2022年07月15日
# 感谢：感谢 wine 以及 deepin-wine 团队，提供了 wine 和 deepin-wine 给大家使用，让我能做这个程序
# 基于 Python3 的 tkinter 构建
###########################################################################################
cd `dirname $0`
which VBoxManage1
if test $? == 0 ; then
    VM/VirtualMachine
    exit
fi
zenity --info --no-wrap --text="未安装 VirtualBox，请自行安装 VirtualBox 并重新运行"
#./launch.sh deepin-terminal -C "pkexec apt install virtualbox-6.1 -y && zenity --info --text=\"安装完毕，关闭此对话框和安装终端重新运行程序即可\" --no-wrap" --keep-open