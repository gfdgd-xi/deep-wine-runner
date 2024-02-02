Summary: 它同时还内置了基于Qemu/VirtualBox制作的、专供小白使用的Windows虚拟机安装工具，可以做到只需下载系统镜像并点击安装即可，无需考虑虚拟机的安装、创建、分区等操作，也能在非 X86 架构安装 X86 架构的 Windows 操作系统（但是效率较低）。
Name: spark-deepin-wine-runner
Version: 3.6.1
Release: 200
License: GPLv3+
AutoReqProv: no
URL: https://gitee.com/gfdgd-xi/deep-wine-runner 

Requires: python3
Requires: python3-pillow
Requires: python3-pillow-tk
Requires: python3-pyquery
Requires: aria2
Requires: curl
Requires: unrar
Requires: unzip
Requires: python3-pyqt6
Requires: python3-psutil
Requires: python3-requests
Requires: deepin-terminal
Requires: python3-dbus
Requires: python3-pip
Requires: p7zip
Requires: sudo
Requires: python3-pyperclip
Requires: bubblewrap
Requires: zenity
Requires: tree
Requires: dpkg
Requires: fakeroot
Requires: python3-pyqt6-webengine
Requires: qemu

%define __os_install_post %{nil}
%description
Wine运行器是一个能让Linux用户更加方便地运行Windows应用的程序。原版的 Wine 只能使用命令操作，且安装过程较为繁琐，对小白不友好。于是该运行器为了解决该痛点，内置了对Wine图形化的支持、Wine 安装器、微型应用商店、各种Wine工具、自制的Wine程序打包器、运行库安装工具等。
它同时还内置了基于Qemu/VirtualBox制作的、专供小白使用的Windows虚拟机安装工具，可以做到只需下载系统镜像并点击安装即可，无需考虑虚拟机的安装、创建、分区等操作，也能在非 X86 架构安装 X86 架构的 Windows 操作系统（但是效率较低，可以运行些老系统）。
而且对于部分 Wine 应用适配者来说，提供了图形化的打包工具，以及提供了一些常用工具以及运行库的安装方式，以及能安装多种不同的 Wine 以测试效果，能极大提升适配效率。
且对于 Deepin23 用户做了特别优化，以便能在缺少 i386 运行库的情况下运行 Wine32。同时也为非 X86 架构用户提供了 Box86/64、Qemu User 的安装方式

%prep
%build
git clone https://gitlink.org.cn/gfdgd_xi/deep-wine-runner --depth=1 | true
cd deep-wine-runner
git pull
make package-deb -j4
%install
cd deep-wine-runner
dpkg -x spark-deepin-wine-runner.deb ~/rpmbuild/BUILDROOT/*
chmod 0755 -Rv ~/rpmbuild/BUILDROOT/*/opt
chmod 777 -Rv ~/rpmbuild/BUILDROOT/*/opt/apps/deepin-wine-runner
chmod 0755 -Rv ~/rpmbuild/BUILDROOT/*/usr
chmod 0555 -Rv ~/rpmbuild/BUILDROOT/*/usr/bin

chmod 0555 ~/rpmbuild/BUILDROOT/*/usr/lib
#fakeroot chown root:root ~/rpmbuild/BUILDROOT/*/usr -Rv
#%dir %attr(0755, root, root) "/usr"

%post
#!/bin/sh
# 使用系统默认的 sh 运行
#################################################################################################################
# 作者：gfdgd xi
# 版本：3.0.0
# 更新时间：2022年10月02日
# 感谢：感谢 wine、deepin-wine 以及星火团队，提供了 wine、deepin-wine、spark-wine-devel 给大家使用，让我能做这个程序
# 基于 sh
#################################################################################################################
# 非强制性的必应组件，所以成功不成功都行
# 程序版本号
version=3.4.1
echo 安装组件
python3 -m pip install --upgrade PyQt5 --trusted-host https://repo.huaweicloud.com -i https://repo.huaweicloud.com/repository/pypi/simple --break-system-packages > /dev/null 2>&1 | true
python3 -m pip install --upgrade PyQtWebEngine --trusted-host https://repo.huaweicloud.com -i https://repo.huaweicloud.com/repository/pypi/simple > /dev/null 2>&1 | true
python3 -m pip install --upgrade pynput --trusted-host https://repo.huaweicloud.com -i https://repo.huaweicloud.com/repository/pypi/simple --break-system-packages > /dev/null 2>&1 | true
python3 -m pip install --upgrade xpinyin --trusted-host https://repo.huaweicloud.com -i https://repo.huaweicloud.com/repository/pypi/simple --break-system-packages > /dev/null 2>&1 | true
# 用于解决老版本 pip 没 --break-system-packages 参数的问题
python3 -m pip install --upgrade pynput --trusted-host https://repo.huaweicloud.com -i https://repo.huaweicloud.com/repository/pypi/simple > /dev/null 2>&1 | true
python3 -m pip install --upgrade xpinyin --trusted-host https://repo.huaweicloud.com -i https://repo.huaweicloud.com/repository/pypi/simple > /dev/null 2>&1 | true
# 修改 box86/64 国内源错误数据
if [[ -f /etc/apt/sources.list.d/box64.list ]]; then
	sed -i 's/http:\/\/seafile.jyx2048.com:2345/http:\/\/gfdgdxi.v5.idcfengye.com/g' /etc/apt/sources.list.d/box64.list
fi
if [[ -f /etc/apt/sources.list.d/box86.list ]]; then
	sed -i 's/http:\/\/seafile.jyx2048.com:2345/http:\/\/gfdgdxi.v5.idcfengye.com/g' /etc/apt/sources.list.d/box86.list
fi
echo 执行完成
echo 移除旧组件
if [ -d /opt/apps/deepin-wine-runner/arm-package ]; then
	rm -rf /opt/apps/deepin-wine-runner/arm-package
fi
if [ -d /opt/apps/deepin-wine-runner/dlls-arm ]; then
	rm -rf /opt/apps/deepin-wine-runner/dlls-arm
fi
if [ -d /opt/apps/deepin-wine-runner/exa ]; then
	rm -rf /opt/apps/deepin-wine-runner/exa
fi
if [ -d /opt/apps/deepin-wine-runner/dxvk ]; then
	rm -rf /opt/apps/deepin-wine-runner/dxvk
fi
echo 移除完成
# 如果为非 X86 PC，可以删除掉一些无用组件（主要是用不了）
if [[ `arch` != "x86_64" ]]; then
	echo 非X86架构，删除对非X86架构无用的组件
	# 删除虚拟机功能
	#rm -rf /opt/apps/deepin-wine-runner/StartVM.sh
	#rm -rf /opt/apps/deepin-wine-runner/RunVM.sh
	#rm -rf /opt/apps/deepin-wine-runner/VM
	#rm -rf /usr/share/applications/spark-deepin-wine-runner-control-vm.desktop
	#rm -rf /usr/share/applications/spark-deepin-wine-runner-start-vm.desktop
	# 删除安装 wine 功能
	rm -rf "/opt/apps/deepin-wine-runner/wine install"
	# 这个注释掉的理论可用，不移除
	#rm -rf "/opt/apps/deepin-wine-runner/wine"
	rm -rf /usr/bin/deepin-wine-runner-wine-installer
	rm -rf /usr/bin/deepin-wine-runner-wine-install-deepin23
	rm -rf /usr/bin/deepin-wine-runner-wine-install
	rm -rf /usr/bin/deepin-wine-runner-winehq-install
	rm -rf /opt/apps/deepin-wine-runner/InstallWineOnDeepin23.py
	rm -rf /opt/apps/deepin-wine-runner/sparkstore.list
	rm -rf /opt/apps/deepin-wine-runner/AllInstall.py
	rm -rf /opt/apps/deepin-wine-runner/InstallNewWineHQ.sh
fi
# 处理 VM 工具
vmPath=/opt/apps/deepin-wine-runner/VM/VirtualMachine-`dpkg --print-architecture`
echo 当前架构为：`dpkg --print-architecture`
if [ -f $vmPath ]; then
	echo 虚拟机工具有该架构的预编译文件
	# 移除辅助文件
	rm -f /opt/apps/deepin-wine-runner/VM/VirtualMachine
	# 移动
	mv $vmPath /opt/apps/deepin-wine-runner/VM/VirtualMachine
	rm -f /opt/apps/deepin-wine-runner/VM/VirtualMachine-*
else
	echo 虚拟机工具无该架构的预编译文件
	rm -f /opt/apps/deepin-wine-runner/VM/VirtualMachine-*
fi
echo 处理完成！
# 修复 3.3.0.1 Box86 源挂了的问题
if [ -f /etc/apt/sources.list.d/box86.list ]; then
	bash -c "echo deb http://seafile.jyx2048.com:2345/spark-deepin-wine-runner/data/box86-debs/debian ./ > /etc/apt/sources.list.d/box86.list"
fi
# Gitlink 源挂了
# 到时候切换 gpg 源会方便很多
#if [ -r /etc/apt/sources.list.d/better-dde.list ]; then
#	if [ -d /usr/share/deepin-installer ]; then
#		# 用于修复 Deepin Community Live CD Install 版签名过期的问题
#		wget -P /tmp/gfdgd-xi-sources https://code.gitlink.org.cn/gfdgd_xi/gfdgd-xi-apt-mirrors/raw/branch/master/gpg.asc
#		rm -rfv /etc/apt/trusted.gpg.d/gfdgdxi-list.gpg | true
#		cp -v /tmp/gfdgd-xi-sources/gpg.asc.gpg /etc/apt/trusted.gpg.d/gfdgdxi-list.gpg
#   	# 用于修复 2022.11.25 Better DDE 导致的 Deepin Community Live CD Install 版问题
#		# 移除 Better DDE 源
#    	rm -rfv /etc/apt/sources.list.d/better-dde.list
#		apt update > /dev/null 2>&1 | true
#	fi
#fi
# 设置目录权限，让用户可读可写，方便后续删除组件
chmod 777 -R /opt/apps/deepin-wine-runner > /dev/null 2>&1 | true
# 向服务器返回安装数加1（不显示内容且忽略错误）
python3 /opt/apps/deepin-wine-runner/Download.py $version > /dev/null 2>&1 | true

%postun
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


%files
/usr/
/opt/

