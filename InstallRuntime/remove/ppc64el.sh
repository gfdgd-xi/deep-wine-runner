#!/bin/bash
arch=ppc64el
libPath=/usr/lib/powerpc64le-linux-gnu/
package=$arch-runtime-for-qemu

if [[ ! -d $libPath ]]; then
    echo "未安装 $arch 运行库，按回车键退出"
    read
    exit 1
fi
sudo apt purge $package -y
echo 卸载完成，按回车键退出
read