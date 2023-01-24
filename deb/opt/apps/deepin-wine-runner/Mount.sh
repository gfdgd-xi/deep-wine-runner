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
# 此部分将会由 pardus-chroot 来处理
#mount --bind /dev ./dev
#mount --bind  /dev/pts ./dev/pts
#mount -t proc /proc ./proc
#mount --bind /etc/resolv.conf ./etc/resolv.conf
#mount -t sysfs /sys ./sys
#mount --bind /dev/shm  ./dev/shm
chmod 777 -R root tmp
xhost +
# 挂载 Wine 运行器目录
mount -o bind `dirname $0` ./opt/apps/deepin-wine-runner/
# 挂载字体
mount -o bind /usr/share/fonts ./usr/share/fonts
# 配置用户
if [ ! -d "home/$2" ]; then
    # 新建用户，且密码为 123456，以便读写
    "$programPath/pardus-chroot" . bash /opt/apps/deepin-wine-runner/ChangePassword.sh "$2"
fi
# 挂载用户目录到 /root（默认 $HOME 路径）
if [[ $2 == "root" ]]; then
    mount --bind root "$1/root/"
else
    mount --bind "/home/$2" "$1/home/$2"
fi
# 挂载此内容以可以跨架构运行程序
mount binfmt_misc -t binfmt_misc /proc/sys/fs/binfmt_misc
# 如果参数 3 存在
"$programPath/pardus-chroot" "--userspec=$2:$2" . env "HOME=/home/$2" ${@:3}
