#!/bin/bash
# 如果是 Fedora
if [[-f /etc/fedora-release ]]; then
    sudo yum update -y
    sudo yum install qemu
    echo 安装完成！按回车键退出
    read
    exit
fi
# 如果是 Arch Linux
if [[-f /etc/arch-release ]]; then
    sudo pacman -Syu
    sudo pacman -S qemu-user qemu-user-static qemu-full  --noconfirm
    echo 安装完成！按回车键退出
    read
    exit
fi
sudo apt update
sudo apt install qemu-system qemu-user qemu-efi qemu-efi-aarch64 qemu-efi-arm -y
sudo apt install qemu-user-static binfmt-support qemu-system-gui -y
echo 安装完成！按回车键退出
read
