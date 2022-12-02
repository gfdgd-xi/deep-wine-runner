#!/bin/bash
if [ ` whoami ` != "root" ]; then 
    echo "Only root can run me" 
    exit 1 
fi
if [ ! -d "$1" ]; then
    echo "路径不存在！"
    exit 1
fi
echo $0
echo $1
echo $2
#echo $3
# 挂载必备目录
cd "$1"
umount ./dev
umount ./dev/pts
umount ./proc
umount ./etc/resolv.conf
umount ./sys
umount ./dev/shm
# 挂载 Wine 运行器目录
umount ./opt/apps/deepin-wine-runner/
# 挂载字体
umount ./usr/share/fonts
# 挂载用户目录到 /root（默认 $HOME 路径）
umount ./root