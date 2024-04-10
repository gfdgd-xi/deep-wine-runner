#!/bin/bash
arch=ppc64el
libPath=/usr/lib/powerpc64le-linux-gnu/
version=1.0.0
url="https://sourceforge.net/projects/deep-wine-runner-wine-download/files/${version}-${arch}-runtime-for-qemu/${arch}-runtime-for-qemu_${version}_all.deb/download"
fileName=`basename $url`
fileName=`basename $filename`

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
sudo apt install qemu-user qemu-user-static binfmt-support -y
sudo dpkg -i /tmp/$fileName 
echo 安装完成，按回车键退出
read
