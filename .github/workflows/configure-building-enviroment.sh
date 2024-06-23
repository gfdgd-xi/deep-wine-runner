#!/bin/bash
sed -i "/deb-src/s/# //g" /etc/apt/sources.list
apt update
apt install sudo -y
apt build-dep qemu -y
# 如果是 Debian10 就需要安装 Python3 的依赖
apt build-dep python3.7 -y
apt build-dep . -y
exit 0