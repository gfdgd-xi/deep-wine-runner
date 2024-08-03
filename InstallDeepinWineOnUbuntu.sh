#!/bin/bash
which git > /dev/null
if [[ $? != 0 ]]; then
	sudo apt install git -y
fi
cd /tmp
if [ -d /tmp/deepin-wine-for-ubuntu ]; then
	rm -rf /tmp/deepin-wine-for-ubuntu
fi
git clone https://gitee.com/wszqkzqk/deepin-wine-for-ubuntu.git
cd deepin-wine-for-ubuntu
bash install.sh
echo 安装完成，按回车键退出
read
