#!/bin/bash
echo 网址：http://deb.wine.wine-runner.gfdgdxi.top/
if [[ ! -f /etc/apt/sources.list.d/gfdgdxi-list-winehq.list ]]; then
    echo 未添加源，现在开始添加！
    sudo apt update
    sudo apt install wget gpg
    if [[ -f /tmp/github.sh ]]; then
        rm -v /tmp/github.sh
    fi
    cd /tmp
    wget http://deb.wine.wine-runner.gfdgdxi.top/sources/github.sh
    bash github.sh
    rm github.sh
    echo 添加完成，现在安装 Wine！
else
    echo 已添加源，忽略，现在安装 Wine！
    sudo apt update
fi
sudo apt install winehq-devel -y
echo 安装完成，按回车键退出！
read