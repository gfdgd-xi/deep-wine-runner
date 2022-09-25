#!/bin/bash
# 使用系统默认的 bash 运行
###########################################################################################
# 作者：gfdgd xi、为什么您不喜欢熊出没和阿布呢
# 版本：2.2.0
# 更新时间：2022年09月25日
# 感谢：感谢 wine 以及 deepin-wine 团队，提供了 wine 和 deepin-wine 给大家使用，让我能做这个程序
# 基于 Python3 构建
###########################################################################################
#################
# 引入所需的库
#################
echo                                           
echo 'm     m   "                  m    m  mmmm '
echo '#  #  # mmm    m mm    mmm   #    # m"  "m'
echo '" #"# #   #    #"  #  #"  #  #mmmm# #    #'
echo ' ## ##"   #    #   #  #""""  #    # #    #'
echo ' #   #  mm#mm  #   #  "#mm"  #    #  #mm#"'
echo '                                        # '
                                          

ubuntuSource=(
    "echo deb [arch=amd64,i386 signed-by=/usr/share/keyrings/winehq-archive.key] https://mirrors.tuna.tsinghua.edu.cn/wine-builds/ubuntu/ jammy main | sudo tee /etc/apt/sources.list.d/winehq.list"
    "sudo wget -nc -P /etc/apt/sources.list.d/ https://dl.winehq.org/wine-builds/ubuntu/dists/impish/winehq-impish.sources" 
    "echo deb [arch=amd64,i386 signed-by=/usr/share/keyrings/winehq-archive.key] https://mirrors.tuna.tsinghua.edu.cn/wine-builds/ubuntu/ focal main | sudo tee /etc/apt/sources.list.d/winehq.list"
    "echo deb [arch=amd64,i386 signed-by=/usr/share/keyrings/winehq-archive.key] https://mirrors.tuna.tsinghua.edu.cn/wine-builds/ubuntu/ bionic main | sudo tee /etc/apt/sources.list.d/winehq.list"
)
debianSource=(
    "echo deb [arch=amd64,i386 signed-by=/usr/share/keyrings/winehq-archive.key] https://mirrors.tuna.tsinghua.edu.cn/wine-builds/debian/ buster main | sudo tee /etc/apt/sources.list.d/winehq.list"
    "echo deb [arch=amd64,i386 signed-by=/usr/share/keyrings/winehq-archive.key] https://mirrors.tuna.tsinghua.edu.cn/wine-builds/debian/ bullseye main | sudo tee /etc/apt/sources.list.d/winehq.list"
    "sudo wget -nc -P /etc/apt/sources.list.d/ https://dl.winehq.org/wine-builds/debian/dists/bookworm/winehq-bookworm.sources"
)
# 选择发行版
echo "WineHQ 官网：https://wiki.winehq.org/"
echo "国内镜像源：https://mirrors-i.tuna.tsinghua.edu.cn/help/wine-builds/"
echo
echo "选择发行版："
echo "0. Debian"
echo "1. Ubuntu"
read system
# 选择版本
echo "选择系统版本"
if [ $system = "0" ]; then
    echo "0. Debian 10 (Buster)"
    echo "1. Debian 11 (Bullseye)"
    echo "2. Debian Testing (Bookworm)"
fi
if [ $system = "1" ]; then
    echo "0. Ubuntu 22.04"
    echo "1. Ubuntu 21.10"
    echo "2. Ubuntu 20.04，Linux Mint 20.x"
    echo "3. Ubuntu 18.04，Linux Mint 19.x"
fi
read systemVersion
# 选择 Wine
echo "选择 Wine："
echo "0. 稳定分支"
echo "1. 开发分支"
echo "2. Staging 分支"
read programVersion
# 初步配置
sudo apt-key del "D43F 6401 4536 9C51 D786 DDEA 76F1 A20F F987 672F"
sudo dpkg --add-architecture i386
sudo wget -nc -O /usr/share/keyrings/winehq-archive.key https://dl.winehq.org/wine-builds/winehq.key
# 检测 apt-fast 或 ss-apt-fast 是否存在
apt="apt"
which apt-fast > /dev/null
if [ $? == 0 ]; then
    apt="apt-fast"
fi
which ss-apt-fast > /dev/null
if [ $? == 0 ]; then
    apt="ss-apt-fast"
fi
which aptss > /dev/null
if [ $? == 0 ]; then
    apt="aptss"
fi
# 添加源
if [ $system = "0" ]; then
    bash -c "${debianSource[$systemVersion]}"
fi
if [ $system = "1" ]; then
    bash -c "${ubuntuSource[$systemVersion]}"
fi
sudo $apt update
# 安装 Wine 
wineInstall=("sudo $apt install --install-recommends winehq-stable" "sudo $apt install --install-recommends winehq-devel" "sudo $apt install --install-recommends winehq-staging")
${wineInstall[$programVersion]}
echo "按回车键退出"
read