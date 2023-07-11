#!/bin/bash
CURRENT_DIR=$(cd $(dirname $0); pwd)
cd $CURRENT_DIR
if [[ ! -f $CURRENT_DIR/usr/ ]]; then
    echo 运行库未安装，按回车键退出
    read
    exit
fi
rm -rfv lib
rm -rfv lib64
rm -rfv usr
chmod 777 -Rv .
echo 删除完成！按回车键退出
read