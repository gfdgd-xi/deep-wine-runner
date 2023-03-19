#!/bin/bash
echo 开始安装 qemu-user-static
pkexec apt update
# binfmt-support 是非常重要的
pkexec apt install qemu-user-static binfmt-support -y