#!/bin/bash
mkdir -p /etc/apt/sources.list.d/
cp /etc/apt/sources.list /etc/apt/sources.list.d/sources.list
sed -i "s/deb /deb-src /g" /etc/apt/sources.list.d/sources.list
cat /etc/apt/sources.list
cat /etc/apt/sources.list.d/sources.list
# 判断系统版本
cat /etc/issue | grep 12
if [[ $? == 0 ]]; then  
    echo "deb-src http://deb.debian.org/debian bookworm main" > /etc/apt/sources.list.d/debian-sources.list
fi
cat /etc/issue | grep sid
if [[ $? == 0 ]]; then  
    echo "deb-src http://deb.debian.org/debian sid main" > /etc/apt/sources.list.d/debian-sources.list
fi
apt update
apt install sudo neofetch -y
neofetch
apt build-dep qemu -y
# 如果是 Debian10 就需要安装 Python3 的依赖
apt build-dep python3.7 -y
apt build-dep . -y
exit 0