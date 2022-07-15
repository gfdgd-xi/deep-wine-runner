#!/bin/bash
cd `dirname $0`
which VBoxManage
if test $? == 0 ; then
    VM/VirtualMachine
    exit
fi
echo 未安装 VirtualBox，开始安装，安装结束重新运行即可
./launch.sh deepin-terminal -C "pkexec apt install virtualbox-6.1 -y && zenity --info --text=\"安装完毕，关闭此对话框和安装终端重新运行程序即可\" --no-wrap" --keep-open