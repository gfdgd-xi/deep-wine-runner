#!/bin/bash
if [[ `whoami` != root ]]; then
    echo 请以 root 权限运行
    echo 按任意键退出
    read
    exit 1
fi
PCArch=`dpkg --print-architecture`
echo 使用国内源
#sudo wget https://ryanfortner.github.io/box86-debs/box86.list -O /etc/apt/sources.list.d/box86.list
#sudo bash -c "echo deb http://seafile.jyx2048.com:2345/spark-deepin-wine-runner/data/box86-debs/debian ./ > /etc/apt/sources.list.d/box86.list"
#wget -qO- http://seafile.jyx2048.com:2345/spark-deepin-wine-runner/data/box86-debs/KEY.gpg | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/box86-debs-archive-keyring.gpg 
#echo "adding key..."
#installBox=box86-generic-arm
#if [[ $PCArch == "arm64" ]]; then
#    sudo bash -c "echo deb http://seafile.jyx2048.com:2345/spark-deepin-wine-runner/data/box64-debs/debian ./ > /etc/apt/sources.list.d/box64.list"
#    wget -qO- http://seafile.jyx2048.com:2345/spark-deepin-wine-runner/data/box64-debs/KEY.gpg | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/box64-debs-archive-keyring.gpg
#    installBox="box86-generic-arm box64-generic-arm"
#    sudo dpkg --add-architecture armhf
#fi
wget http://deb.box86.wine-runner.gfdgdxi.top/sources/github.sh
bash github.sh
rm github.sh
echo " + sudo apt update"
sudo apt update
sudo apt install binfmt-support -y
sudo apt install libc6:armhf -y
sudo apt install -y box86 
sudo apt install -y box64
echo 安装完成！按回车键退出
read
