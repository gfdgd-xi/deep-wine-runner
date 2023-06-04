#!/bin/bash
dpkg --add-architecture i386
apt update
apt install sudo gpg wget dpkg-dev -y
sudo apt update
# 添加源
sudo wget -nc -O /usr/share/keyrings/winehq-archive.key https://dl.winehq.org/wine-builds/winehq.key
echo "deb-src [signed-by=/usr/share/keyrings/winehq-archive.key] https://dl.winehq.org/wine-builds/ubuntu/ focal main" > /etc/apt/sources.list.d/winehq-bionic.list
echo "deb-src http://repo.huaweicloud.com/debian buster main" > /etc/apt/sources.list.d/debian10-s.list
sudo apt update
# 编译
mkdir /wine
cd /wine
#sudo apt build-dep wget -y
#sudo apt source wget
sudo apt build-dep wine -y
sudo apt source wine
sudo apt install fakeroot -y
sudo apt install flex bison gettext make gcc gcc-multilib gcc-mingw-w64 libasound2-dev libasound2-dev:i386 libpulse-dev libpulse-dev:i386 libdbus-1-dev libdbus-1-dev:i386 libfontconfig1-dev libfontconfig1-dev:i386 libfreetype6-dev libfreetype6-dev:i386 libgnutls28-dev libgnutls28-dev:i386 libjpeg62-turbo-dev libjpeg62-turbo-dev:i386 libpng-dev libpng-dev:i386 libtiff-dev libtiff-dev:i386 libgl-dev libgl-dev:i386 libunwind-dev libunwind-dev:i386 libx11-dev libx11-dev:i386 libxml2-dev libxml2-dev:i386 libxslt1-dev libxslt1-dev:i386 libgstreamer1.0-dev libgstreamer1.0-dev:i386 libgstreamer-plugins-base1.0-dev libgstreamer-plugins-base1.0-dev:i386 libmpg123-dev libmpg123-dev:i386 libosmesa6-dev libosmesa6-dev:i386 libudev-dev libudev-dev:i386 libvkd3d-dev libvkd3d-dev:i386 libvulkan-dev libvulkan-dev:i386 libcapi20-dev libcapi20-dev:i386 liblcms2-dev liblcms2-dev:i386 libcups2-dev libcups2-dev:i386 libgphoto2-dev libgphoto2-dev:i386 libsane-dev libsane-dev:i386 libgsm1-dev libgsm1-dev:i386 libkrb5-dev libkrb5-dev:i386 libldap2-dev libldap2-dev:i386 samba-dev ocl-icd-opencl-dev ocl-icd-opencl-dev:i386 libpcap-dev libpcap-dev:i386 libusb-1.0-0-dev libusb-1.0-0-dev:i386 libv4l-dev libv4l-dev:i386 libopenal-dev libopenal-dev:i386 libxcomposite-dev libxcomposite-dev:i386 libxcursor-dev libxcursor-dev:i386 libxi-dev libxi-dev:i386 libxrandr-dev libxrandr-dev:i386 libxinerama-dev libxinerama-dev:i386 -y
sudo apt install flex:i386 bison:i386 qt4-qmake:i386 libfreetype6-dev:i386 libjpeg-dev:i386 libpng-dev:i386 libxslt1-dev:i386 libxml2-dev:i386 libxrender-dev:i386 libgl1-mesa-dev:i386 libglu1-mesa-dev:i386 freeglut3-dev:i386 prelink:i386 libasound2-dev:i386 g++-multilib gcc-multilib g++-multilib -y
cd */
dpkg-buildpackage -b -nc
# 移除无用包
rm ../*dbg*.deb -vrf
rm ../*dbgsym*.deb -vrf