#!/bin/bash
# $1=arm64
# $2=buster

function getd23debootstrap() {
    git clone https://github.com/deepin-community/debootstrap --depth=1
    cd debootstrap
    sudo apt build-dep . -y
    dpkg-buildpackage -b
    sudo apt install ../*.deb -y
}

sudo apt update
sudo apt install debootstrap qemu-user-static git -y
bottlePath=./system-bottle
if [[ $2 == "beige" ]]; then
    getd23debootstrap
fi
sudo debootstrap --arch=$1 $2 $bottlePath $3
sudo bash .github/workflows/pardus-chroot $bottlePath
# 配置 git
sudo chroot $bottlePath apt update
sudo chroot $bottlePath apt install git -y
sudo chroot $bottlePath git clone https://github.com/gfdgd-xi/deep-wine-runner-qemu-system --depth=1
# 修改版本号
sudo sed -i "s/) UNRELEASED; urgency=medium/~$2) UNRELEASED; urgency=medium/g" $bottlePath/deep-wine-runner-qemu-system/debian/changelog
bash .github/workflows/run-command-in-chroot.sh .github/workflows/configure-building-enviroment.sh
exit 0