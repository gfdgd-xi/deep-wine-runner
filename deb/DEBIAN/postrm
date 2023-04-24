#!/bin/bash
# 使用系统默认的 sh 运行
#################################################################################################################
# 作者：gfdgd xi
# 版本：2.2.0
# 更新时间：2022年09月24日
# 感谢：感谢 wine、deepin-wine 以及星火团队，提供了 wine、deepin-wine、spark-wine-devel 给大家使用，让我能做这个程序
# 基于 sh
#################################################################################################################
# 删除软件残留，简单粗暴一点直接全部删掉，防止出现警告
# 加判断是为了怕 reinstall 后程序就再也打不开了（除非卸载后重新安装）
if [ "$1" = "remove" ] || [ "$1" = "purge" ]; then
	rm -rf /opt/apps/deepin-wine-runner/
fi
# 删除软件缓存（留着也没什么用了）
# 缓存目录：~/.cache/deepin-wine-runner
if [ "$1" = "remove" ] || [ "$1" = "purge" ]; then

	echo "清理程序缓存"

	for username in $(ls /home); do
		echo /home/$username
		if [ -d "/home/$username/.cache/deepin-wine-runner/" ]; then
			rm -rf "/home/$username/.cache/deepin-wine-runner/"
		fi
	done
	# 清理 root 用户的缓存文件
	echo /root
	if [ -d "/root/.cache/deepin-wine-runner/" ]; then
		rm -rf "/root/.cache/deepin-wine-runner/"
	fi
else
	echo "非卸载，跳过清理"
fi
# 删除软件配置文件（只限“purge”）
# 配置目录：~/.config/deepin-wine-runner
if [ "$1" = "purge" ]; then

	echo "清理程序配置文件"

	for username in $(ls /home); do
		echo /home/$username
		if [ -d "/home/$username/.config/deepin-wine-runner/" ]; then
			rm -rf "/home/$username/.config/deepin-wine-runner/"
		fi
	done
	# 清理 root 用户的配置文件
	echo /root
	if [ -d "/root/.config/deepin-wine-runner/" ]; then
		rm -rf "/root/.config/deepin-wine-runner/"
	fi
else
	echo "非 purge，跳过清理"
fi
