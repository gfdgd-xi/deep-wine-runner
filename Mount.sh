#!/bin/bash
if [ ` whoami ` != "root" ]; then 
    echo "Only root can run me" 
    exit 1 
fi
if [ ! -d "$1" ]; then
    echo "路径不存在！"
    exit 1
fi
# 挂载用户目录
mkdir -p "$1/home/$USER"
mount -o bind ~ "$1/home/$USER"
# 挂载 Wine 运行器目录
#mount -o bind `dirname $0` "$1/opt/apps/deepin-wine-runner/wine"
mount -o bind `dirname $0` "$1/opt/apps/deepin-wine-runner/"
# 挂载必备目录
cd "$1"
mount --bind /dev ./dev
mount --bind  /dev/pts ./dev/pts
mount -t proc /proc ./proc
mount --bind /etc/resolv.conf ./etc/resolv.conf
mount -t sysfs /sys ./sys
mount --bind /dev/shm  ./dev/shm
# 如果参数 2 存在
chroot . "${@:2}"