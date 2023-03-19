#!/bin/bash
arch=mips64el
libPath=/usr/lib/mips64el-linux-gnuabi64
version=1.0.0
url="https://code.gitlink.org.cn/gfdgd_xi/runtime-for-qemu/raw/branch/master/$arch-runtime-for-qemu_${version}_all.deb"
fileName=`basename $url`

if [[ -d $libPath ]]; then
    echo "已安装 $arch 运行库，按回车键退出"
    read
    exit 1
fi
if [[ -f /tmp/$fileName ]]; then
    rm "/tmp/$fileName"
fi
aria2c -x 16 -s 16 -c $url -d /tmp -o $fileName
sudo apt update
sudo dpkg -i /tmp/$fileName 
echo 安装完成，按回车键退出
read