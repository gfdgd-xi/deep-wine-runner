#!/bin/bash
if [[ `whoami` != root ]]; then
    echo 请以 root 权限运行
    echo 按任意键退出
    read
    exit 1
fi
PCArch=`dpkg --print-architecture`
if [[ $PCArch != "aarch64" ]] && [[ $PCArch != "arm64" ]]; then
    echo 非 ARM 架构，无法继续
    echo 按任意键退出
    read
    exit 1
fi
which box86
if [[ $? == 0 ]]; then
    echo 已安装，结束
    echo 按回车键退出
    read 
    exit 1
fi
#sudo wget https://ryanfortner.github.io/box86-debs/box86.list -O /etc/apt/sources.list.d/box86.list
sudo bash -c "echo deb http://jihulab.com/gfdgd-xi/box64-debs/-/raw/master/debian ./ > /etc/apt/sources.list.d/box86.list"
wget -qO- https://ryanfortner.github.io/box86-debs/KEY.gpg | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/box86-debs-archive-keyring.gpg 
echo "adding key..."
installBox=box86-generic-arm
if [[ $PCArch == "arm64" ]]; then
    sudo bash -c "echo deb http://jihulab.com/gfdgd-xi/box86-debs/-/raw/master/debian ./ > /etc/apt/sources.list.d/box64.list"
    wget -qO- https://ryanfortner.github.io/box64-debs/KEY.gpg | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/box64-debs-archive-keyring.gpg
    installBox="box86-generic-arm box64-generic-arm"
    sudo dpkg --add-architecture armhf
fi
echo " + sudo apt update"
sudo apt update
sudo apt install -y $installBox
echo 安装完成！按回车键退出
read