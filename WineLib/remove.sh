#!/bin/bash
CURRENT_DIR=$(cd $(dirname $0); pwd)
cd $CURRENT_DIR
if [[ ! -f $CURRENT_DIR/usr/lib/ld-linux-x86-64.so.2 ]]; then
    echo 运行库未安装，按回车键退出
    read
    exit
fi
sudo rm -rfv lib
sudo rm -rfv lib64
sudo rm -rfv usr
sudo chmod 777 -Rv .
echo 删除完成！按回车键退出
read