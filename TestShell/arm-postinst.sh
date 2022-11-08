#!/bin/bash

#DEB_PATH=/opt/apps/aaa
DEB_PATH=.
if [ -f $DEB_PATH/files/wined3d.dll.so ] && [ -d "/usr/lib/nvidia" ];then
	mv $DEB_PATH/files/wined3d.dll.so $DEB_PATH/files/dlls
fi

KUNPENG="0x48"
cpu_vendor=$(lscpu | grep Vendor | awk '{print $3}')
KIRIN=`cat /proc/cpuinfo | grep Kirin`
if [ ! -z "$KIRIN" ];then
        mv $DEB_PATH/files/*.so $DEB_PATH/files/dlls
fi

## check if the cpu support arm32 instruction or not, 126 means unsupported
/opt/deepin-box86/box86 -v
CHECK_ARM32=$?

IMAGE_VER=10deepin3
IMAGE_DIR=/opt/deepin-wine-exagear-images/debian-buster
ARCHIVE_FILE=files.7z

download_image() {
	pushd /var/cache/apt/archives >/dev/null
	apt download deepin-wine-exagear-images
	dpkg -x deepin-wine-exagear-images*.deb /
	rm deepin-wine-exagear-images*.deb
	echo $IMAGE_VER > $IMAGE_DIR/VERSION 
	popd >/dev/null
}

move_box86_runsh() {
    if [[ -f $DEB_PATH/files/run_with_exagear.sh ]]; then
        echo 单图标
        mv $DEB_PATH/files/run_with_exagear.sh $DEB_PATH/files/run.sh
    else
        echo 多图标
        for shell_path in $(ls $DEB_PATH/files/*_with_exagear.sh)
            do
            name=${shell_path#$DEB_PATH/files/}
            name=${name%_with_exagear.sh}
            mv $shell_path $DEB_PATH/files/$name.sh
            done
    fi
}

move_exagear_runsh() {
    if [[ -f $DEB_PATH/files/run_with_exagear.sh ]]; then
        echo 单图标
        mv $DEB_PATH/files/run_with_box86.sh $DEB_PATH/files/run.sh
    else
        echo 多图标
        for shell_path in $(ls $DEB_PATH/files/*_with_box86.sh)
            do
            name=${shell_path#$DEB_PATH/files/}
            name=${name%_with_box86.sh}
            mv $shell_path $DEB_PATH/files/$name.sh
            done
    fi
}

if [[ "$KUNPENG" == "$cpu_vendor" ]] || [[ $CHECK_ARM32 != 0 ]];then
	echo "use exagear as emulator..."
	if [ ! -d /opt/exagear/bin ];then
		mkdir /opt/exagear/bin -p
	fi

	if [ ! -e /opt/exagear/bin/ubt_x32a64_al ];then
		cp $DEB_PATH/files/exa/ubt_x32a64_al /opt/exagear/bin/ubt_x32a64_al
	fi

	if [ ! -e /opt/exagear/bin/ubt_x64a64_al ];then
		cp $DEB_PATH/files/exa/ubt_x64a64_al /opt/exagear/bin/ubt_x64a64_al
	fi
    move_exagear_runsh
	mv $DEB_PATH/files/exa/wineserver /opt/deepin-wine6-stable/bin/wineserver
else
	echo "use box86 as emulator..."
    move_box86_runsh
	mv $DEB_PATH/files/run_with_box86.sh $DEB_PATH/files/run.sh
fi

true
