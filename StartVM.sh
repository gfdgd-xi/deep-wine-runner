#!/bin/bash
# 使用系统默认的 bash 运行
###########################################################################################
# 作者：gfdgd xi
# 版本：1.7.0
# 更新时间：2022年07月15日
# 感谢：感谢 wine 以及 deepin-wine 团队，提供了 wine 和 deepin-wine 给大家使用，让我能做这个程序
# 基于 Python3 的 tkinter 构建
###########################################################################################
VBoxManage showvminfo Windows
if [[ 0 == $? ]]; then
    # 检测到虚拟机存在，启动虚拟机
    VBoxManage startvm Windows
    exit
fi
# 检查是否有 QEMU
which qemu-system-x86_64
if [[ $? == 0 ]] && [[ -f "$HOME/Qemu/Windows/Windows.qcow2" ]]; then
    if [[ -f "$HOME/.config/deepin-wine-runner/QemuSetting.json" ]]; then
        echo 有设置文件，读设置文件
        cd `dirname $0`
        python3 ./VM/StartQemu.py
        exit
    fi
    # 查看CPU个数
    CpuSocketNum=`cat /proc/cpuinfo | grep "cpu cores" | uniq | wc -l`
    # 查看CPU核心数
    CpuCoreNum=`grep 'core id' /proc/cpuinfo | sort -u | wc -l`
    # 查看逻辑CPU的个数
    CpuCount=`cat /proc/cpuinfo| grep "processor"| wc -l`
 
    # 总内存大小GB
    MemTotal=`awk '($1 == "MemTotal:"){printf "%.2f\n",$2/1024/1024}' /proc/meminfo`
    use=$(echo "scale=4; $MemTotal / 3" | bc)
    if [[ `arch` == "x86_64" ]]; then
        echo X86 架构，使用 kvm 加速
        kvm -cpu host --hda "$HOME/Qemu/Windows/Windows.qcow2" -soundhw all -smp $CpuCount,sockets=$CpuSocketNum,cores=$(($CpuCoreNum / $CpuCount)),threads=$(($CpuSocketNum / $CpuCoreNum / $CpuCount)) -m ${use}G -net user,hostfwd=tcp::3389-:3389 -display vnc=:5 -display gtk -usb -nic model=rtl8139
        exit
    fi
    echo 非 X86 架构，不使用 kvm 加速
    qemu-system-x86_64 --hda "$HOME/Qemu/Windows/Windows.qcow2" -soundhw all -smp $CpuCount,sockets=$CpuSocketNum,cores=$(($CpuCoreNum / $CpuCount)),threads=$(($CpuSocketNum / $CpuCoreNum / $CpuCount)) -m ${use}G -net user,hostfwd=tcp::3389-:3389 -display vnc=:5 -display gtk -usb -nic model=rtl8139
    exit
fi
zenity --question --no-wrap --text="检查到您未创建所指定的虚拟机，是否创建虚拟机并继续？\n如果不创建将无法使用"
if [[ 1 == $? ]]; then
    # 用户不想创建虚拟机，结束
    exit
fi
cd `dirname $0`
./VM/VirtualMachine
