#!/bin/bash
if [ ` whoami ` != "root" ]; then 
    echo "Only root can run me" 
    exit 1 
fi
if [ ! -d "$1" ]; then
    echo "路径不存在！"
    exit 1
fi
programPath=`dirname $0`
echo $0
echo $1
echo $2
echo $3
# 挂载必备目录
cd "$1"
# 拷贝 Qemu Static
cp -r /usr/bin/qemu-*-static ./usr/bin
# 挂载目录
# 这里将由 pardus-chroot 处理
#mount --bind /dev ./dev
#mount --bind  /dev/pts ./dev/pts
#mount -t proc /proc ./proc
#mount --bind /etc/resolv.conf ./etc/resolv.conf
#mount -t sysfs /sys ./sys
#mount --bind /dev/shm  ./dev/shm
chmod 777 -R root tmp
xhost +
# 挂载此内容以可以跨架构运行程序
mount binfmt_misc -t binfmt_misc /proc/sys/fs/binfmt_misc
# 如果参数 3 存在
"$programPath/pardus-chroot" . ${@:3}
