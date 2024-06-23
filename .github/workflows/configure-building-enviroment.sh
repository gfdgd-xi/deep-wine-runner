#!/bin/bash
sed -i "/deb-src/s/# //g" /etc/apt/sources.list
sudo apt update
sudo apt build-dep qemu -y
# 如果是 Debian10 就需要安装 Python3 的依赖
sudo apt build-dep python3.7 -y
exit 0