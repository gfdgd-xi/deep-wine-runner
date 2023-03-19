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
#sudo wget https://itai-nelken.github.io/weekly-box86-debs/debian/box86.list -O /etc/apt/sources.list.d/box86.list
echo deb https://code.gitlink.org.cn/gfdgd_xi/weekly-box86-debs/raw/branch/main/debian / > /etc/apt/sources.list.d/box86.list
echo "adding key..."
wget -qO- https://code.gitlink.org.cn/gfdgd_xi/weekly-box86-debs/raw/branch/main/debian/KEY.gpg | sudo apt-key add -
installBox=box86
if [[ $PCArch == "arm64" ]]; then
    installBox="box86 box64"
    sudo dpkg --add-architecture armhf
fi
echo " + sudo apt update"
sudo apt update
sudo apt install -y $installBox
echo 安装完成！按回车键退出
read