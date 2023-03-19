#!/bin/bash
# 判断是否有安装 Qemu User
which qemu-i386 > /dev/null
if [[ ! $? ]]; then
    echo 您未安装 Qemu User，按回车键后退出
    read
    exit 1
fi
sudo apt purge qemu-user -y
echo 安装完成，按回车键后退出
read