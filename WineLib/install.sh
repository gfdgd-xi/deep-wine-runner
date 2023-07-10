#!/bin/bash
CURRENT_DIR=$(cd $(dirname $0); pwd)
cd $CURRENT_DIR
if [[ -f $CURRENT_DIR/usr/lib/ld-linux-x86-64.so.2 ]]; then
    echo 运行库已安装，按回车键退出
    exit
fi
aria2c -x 16 -s 16 -d /tmp https://jihulab.com/gfdgd-xi/bwrapruntime/-/raw/main/library.tar.xz
if [[ $? != 0 ]]; then
    echo 安装包下载失败！按回车键退出
    read
fi
sudo chmod 777 -Rv .
tar -xvf /tmp/library.tar.xz
rm -vf /tmp/library.tar.xz
echo 安装完成！按回车键退出
read