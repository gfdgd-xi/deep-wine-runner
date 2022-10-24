#!/bin/bash
# 使用系统默认的 Bash
#################################################################################################################
# 作者：gfdgd xi、为什么您不喜欢熊出没和阿布呢
# 版本：2.4.0
# 更新时间：2022年10月11日
# 感谢：感谢 wine、deepin-wine 以及星火团队，提供了 wine、deepin-wine、spark-wine-devel 给大家使用，让我能做这个程序
# 基于 Bash 制作
#################################################################################################################
cd `dirname $0`
programPath=$(cd "$(dirname "$0")";pwd)
echo $programPath
if [[ -f "/etc/xdg/autostart/deepin-wine-runner-keyboard.desktop" ]]; then
	# 判断是否自启动，已经自启动就不再考虑
	echo "文件已存在，取消"
	exit 1
fi
sudo cp -rv desktop/deepin-wine-runner-keyboard.desktop /etc/xdg/autostart/deepin-wine-runner-keyboard.desktop
sudo ./replace.py /etc/xdg/autostart/deepin-wine-runner-keyboard.desktop @programPath@ "$programPath"