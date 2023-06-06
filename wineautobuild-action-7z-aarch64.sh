#!/bin/bash
apt update
apt install sudo gpg wget dpkg-dev aria2 -y
sudo apt update
# 添加源
sudo wget -nc -O /usr/share/keyrings/winehq-archive.key https://dl.winehq.org/wine-builds/winehq.key
echo "deb-src [signed-by=/usr/share/keyrings/winehq-archive.key] https://dl.winehq.org/wine-builds/ubuntu/ focal main" > /etc/apt/sources.list.d/winehq-bionic.list
sudo apt update
# 编译
mkdir /wine
cd /wine
#sudo apt build-dep wget -y
#sudo apt source wget

#sudo apt source wine
sudo apt install fakeroot p7zip-full aptitude lld -y
sudo aptitude install flex bison libfreetype6-dev libjpeg-dev libpng-dev libxslt1-dev libxml2-dev libxrender-dev libgl1-mesa-dev libglu1-mesa-dev freeglut3-dev prelink libasound2-dev -y
sudo aptitude install flex bison gettext make gcc  gcc-mingw-w64 libasound2-dev libasound2-dev libpulse-dev libpulse-dev -y
sudo aptitude install libdbus-1-dev libdbus-1-dev libfontconfig1-dev libfontconfig1-dev libfreetype6-dev libfreetype6-dev libgnutls28-dev libgnutls28-dev libpng-dev libpng-dev libtiff-dev libtiff-dev libgl-dev libgl-dev libunwind-dev libunwind-dev libx11-dev libx11-dev libxml2-dev libxml2-dev libxslt1-dev libxslt1-dev libgstreamer1.0-dev -y
sudo aptitude install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgstreamer-plugins-base1.0-dev libmpg123-dev libmpg123-dev libosmesa6-dev libosmesa6-dev libudev-dev libudev-dev libvkd3d-dev libvkd3d-dev libvulkan-dev libvulkan-dev libcapi20-dev libcapi20-dev liblcms2-dev liblcms2-dev libcups2-dev libcups2-dev libgphoto2-dev libgphoto2-dev libsane-dev libsane-dev libgsm1-dev libgsm1-dev libkrb5-dev libkrb5-dev libldap2-dev libldap2-dev samba-dev ocl-icd-opencl-dev ocl-icd-opencl-dev libpcap-dev libpcap-dev libusb-1.0-0-dev libusb-1.0-0-dev libv4l-dev libv4l-dev libopenal-dev libopenal-dev libxcomposite-dev libxcomposite-dev libxcursor-dev libxcursor-dev libxi-dev libxi-dev libxrandr-dev libxrandr-dev libxinerama-dev libxinerama-dev -y
sudo apt install clang llvm -y
sudo apt install "llvm*" -y
sudo apt build-dep wine -y
# 获取数据
url=`cat /wine-url.txt`
version=`cat /wine-version.txt`
type=`cat /wine-type.txt`
cpu=$(cat /proc/cpuinfo | grep processor | wc -l)
aria2c -x 16 -s 16 $url
tar -xvf `basename $url`
#cd wine-$version
## 编译64位
mkdir build64
cd build64
sudo aptitude install libpcsclite-dev libsdl2-dev samba-dev -y
../wine-$version/configure 
make -j$cpu
mkdir ../program
make install -j$cpu DESTDIR=../program
cd ../program/usr/local/
# 打7z包
7z a /wine/wine-$type-$version-ubuntu22.04-aarch64.7z *
cd /wine
rm -rfv program

## 移除临时文件（不写了，反正 Github Action 会自动销毁）