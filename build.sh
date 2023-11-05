#!/bin/bash
#cd `dirname $0`
bin=$1
nasm -f bin $1 -o `basename $1`.bin
if [[ $? != 0 ]];then
	exit
fi
sudo modprobe nbd 8
sudo qemu-nbd `dirname $0`/test.qcow2 --connect /dev/nbd0
sudo dd if=`basename $1`.bin of=/dev/nbd0
sudo qemu-nbd -d /dev/nbd0
kvm --hda `dirname $0`/test.qcow2 -rtc base=localtime
