#!/bin/bash

#sudo apt install squashfs-tools

mkdir -p ~/temp
cd ~/temp
echo "正在下载supersu"
aria2c -x 16 -s 16 -d ~/temp http://supersuroot.org/downloads/SuperSU-v2.82-201705271822.zip
cd ..
mkdir -p ~/temp/work/dabao/extract/DEBIAN
echo "正在解压supersu" 
unzip ~/temp/SuperSU-v2.82-201705271822.zip -d ~/temp/work/su
WORKDIR=~/temp/work
cd "$WORKDIR" 
echo "正在下载uengine-android-image"
apt download uengine-android-image
echo "正在解压uengine-android-image" 
cd dabao
dpkg-deb -x $WORKDIR/uengine-android-image*.deb extract/
dpkg-deb -e $WORKDIR/uengine-android-image*.deb extract/DEBIAN
cd ..
cp dabao/extract/usr/share/uengine/android.img android.img

echo "正在解压android镜像" 
sudo unsquashfs android.img

sudo mkdir -p ./squashfs-root/system/app/SuperSU
sudo mkdir -p ./squashfs-root/system/bin/.ext/

echo "正在将supersu安装到android镜像" 
sudo cp ./su/common/Superuser.apk ./squashfs-root/system/app/SuperSU/SuperSU.apk
sudo cp ./su/common/install-recovery.sh ./squashfs-root/system/etc/install-recovery.sh
sudo cp ./su/common/install-recovery.sh ./squashfs-root/system/bin/install-recovery.sh  
sudo cp ./su/x64/su ./squashfs-root/system/xbin/su
sudo cp ./su/x64/su ./squashfs-root/system/bin/.ext/.su
sudo cp ./su/x64/su ./squashfs-root/system/xbin/daemonsu
sudo cp ./su/x64/supolicy ./squashfs-root/system/xbin/supolicy
sudo cp ./su/x64/libsupol.so ./squashfs-root/system/lib64/libsupol.so
sudo cp ./squashfs-root/system/bin/app_process64 ./squashfs-root/system/bin/app_process_init
sudo cp ./squashfs-root/system/bin/app_process64 ./squashfs-root/system/bin/app_process64_original
sudo cp ./squashfs-root/system/xbin/daemonsu ./squashfs-root/system/bin/app_process
sudo cp ./squashfs-root/system/xbin/daemonsu ./squashfs-root/system/bin/app_process64

sudo chmod +x ./squashfs-root/system/app/SuperSU/SuperSU.apk
sudo chmod +x ./squashfs-root/system/etc/install-recovery.sh
sudo chmod +x ./squashfs-root/system/bin/install-recovery.sh
sudo chmod +x ./squashfs-root/system/xbin/su
sudo chmod +x ./squashfs-root/system/bin/.ext/.su
sudo chmod +x ./squashfs-root/system/xbin/daemonsu
sudo chmod +x ./squashfs-root/system/xbin/supolicy
sudo chmod +x ./squashfs-root/system/lib64/libsupol.so
sudo chmod +x ./squashfs-root/system/bin/app_process_init
sudo chmod +x ./squashfs-root/system/bin/app_process64_original
sudo chmod +x ./squashfs-root/system/bin/app_process
sudo chmod +x ./squashfs-root/system/bin/app_process64

echo "正在打包android镜像" 
sudo rm android.img
sudo mksquashfs squashfs-root android.img -b 131072 -comp xz -Xbcj ia64


cp android.img dabao/extract/usr/share/uengine/android.img

echo "正在打包uengine-android-image" 
cd dabao/extract
find usr -type f -print0 |xargs -0 md5sum >md5sums
cd ..
mkdir build
dpkg-deb -b extract/ build/

cp build/*.deb ~/

echo "正在清理垃圾" 
sudo rm -rf ~/temp

echo "已在用户主目录生成新的安装包，安装后重启即可生效" 