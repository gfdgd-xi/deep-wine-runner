#!/bin/bash
pkexec apt update
pkexec apt install qemu-system qemu-user qemu-user-static -y
echo 安装完成！按回车键退出
read
