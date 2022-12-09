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
echo $3
# 挂载必备目录
cd "$1"
# 拷贝 Qemu Static
cp -r /usr/bin/qemu-*-static ./usr/bin
# 挂载目录
mount --bind /dev ./dev
#mount --bind  /dev/pts ./dev/pts
mount -t proc /proc ./proc
mount --bind /etc/resolv.conf ./etc/resolv.conf
mount -t sysfs /sys ./sys
#mount --bind /dev/shm  ./dev/shm
chmod 777 -R root
xhost +

# 如果参数 3 存在
chroot . ${@:3}
