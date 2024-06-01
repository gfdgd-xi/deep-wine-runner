#!/bin/bash
echo lat只能在loongarch架构安装
# 检查是否有 aptss
aptPath=apt
if [[ -f /usr/bin/aptss ]]; then
    aptPath=aptss
fi
# 判断新旧世界
if [[ `dpkg --print-architecture` == "loong64" ]]; then
    # 新世界
    sudo $aptPath update
    sudo $aptPath install lat lat-runtime-i386 lat-runtime-amd64
    echo 按回车键退出
    read
    exit
fi
# 旧世界
sudo $aptPath update
sudo $aptPath install lat i386-runtime-base i386-runtime-extra
echo 按回车键退出
read
exit