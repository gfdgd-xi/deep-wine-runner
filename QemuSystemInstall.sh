#!/bin/bash
# 如果是 Arch Linux
if [[-f /etc/arch-release ]]; then
    sudo pacman -Syu
    sudo pacman -S qemu-user qemu-user-static qemu-full
    exit
fi
sudo apt update
sudo apt install qemu-system qemu-user qemu-efi qemu-efi-aarch64 qemu-efi-arm -y
sudo apt install qemu-user-static binfmt-support qemu-system-gui -y
echo 安装完成！按回车键退出
read
