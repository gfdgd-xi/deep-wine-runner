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
sudo apt install binfmt-support -y
echo apt 源添加完毕！按回车键继续安装 Box86/Box64，若想要停止安装，则请按 Ctrl+C 或按终端右上角 ×（叉叉）退出
echo 按回车键后将会自动安装包名为 box86-generic-arm、box64-generic-arm（box64 要在 aarch64 系统才可安装）的 Box86/Box64 包（适用于通用 ARM 系统）
echo 其他特殊版本及其包名可见如下链接（如适用于 rk3399 的版本）：
echo "    - Box64：https://github.com/ryanfortner/box64-debs/"
echo "    - Box86：https://github.com/ryanfortner/box86-debs/"
echo "    - Box64（国内镜像）：https://jihulab.com/gfdgd-xi/box64-debs"
echo "    - Box64（国内镜像）：https://jihulab.com/gfdgd-xi/box86-debs"
read
sudo apt install -y $installBox
echo 安装完成！按回车键退出
read