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
mount --bind /dev ./dev
mount --bind  /dev/pts ./dev/pts
mount -t proc /proc ./proc
mount --bind /etc/resolv.conf ./etc/resolv.conf
mount -t sysfs /sys ./sys
mount --bind /dev/shm  ./dev/shm
chmod 777 -R root
xhost +
# 挂载 Wine 运行器目录
mount -o bind `dirname $0` ./opt/apps/deepin-wine-runner/
# 挂载字体
mount -o bind /usr/share/fonts ./usr/share/fonts
# 配置用户
if [ ! -d "home/$2" ]; then
    # 新建用户，且密码为 123456，以便读写
    chroot . echo -e "123456\n123456\n\n\n\n\n\n\n\n\n" | adduser "$2"
fi
# 挂载用户目录到 /root（默认 $HOME 路径）
if [[ $2 == "root" ]]; then
    mount --bind root "$1/root/"
else
    mount --bind "/home/$2" "$1/root/"
fi

# 如果参数 3 存在
chroot "--userspec=$2:$2" . "${@:3}"