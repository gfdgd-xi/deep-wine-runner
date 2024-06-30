#!/bin/bash
# 使用系统默认的 bash 运行
###########################################################################################
# 作者：gfdgd xi
# 版本：1.7.0
# 更新时间：2022年07月15日
# 感谢：感谢 wine 以及 deepin-wine 团队，提供了 wine 和 deepin-wine 给大家使用，让我能做这个程序
# 基于 Python3 的 tkinter 构建
###########################################################################################
cd `dirname $0`
CURRENT_DIR=$(cd $(dirname $0); pwd)
VBoxManage showvminfo Windows
if [[ 0 == $? ]]; then
    # 检测到虚拟机存在，启动虚拟机
    VBoxManage startvm Windows > /tmp/windows-virtual-machine-installer-for-wine-runner-run.log 2>&1
    exit
fi
# 检查是否有 QEMU
export PATH=/opt/apps/deepin-wine-runner-qemu-system-extra/files/usr/local/bin:$PATH
which qemu-system-x86_64
if [[ $? == 0 ]] && [[ -f "$HOME/Qemu/Windows/Windows.qcow2" ]]; then
    if [[ -f "$HOME/.config/deepin-wine-runner/QemuSetting.json" ]]; then
        echo 有设置文件，读设置文件
        cd `dirname $0`
        python3 ./VM/StartQemu.py
        exit
    fi
    # 判断是否有安装增强 Qemu
    if [[ -f /opt/apps/deepin-wine-runner-qemu-system-extra/files/run.sh ]]; then
        qemuMore=/opt/apps/deepin-wine-runner-qemu-system-extra/files/run.sh
    fi
    # 查看CPU个数
    CpuSocketNum=`cat /proc/cpuinfo | grep "cpu cores" | uniq | wc -l`
    # 查看CPU核心数
    CpuCoreNum=`grep 'core id' /proc/cpuinfo | sort -u | wc -l`
    # 查看逻辑CPU的个数
    CpuCount=`cat /proc/cpuinfo| grep "processor"| wc -l`
    # 判断是否检测异常，如果异常则使用默认值
    if [[ $CpuSocketNum == 0 ]]; then
        CpuSocketNum=1
    fi
    if [[ $CpuCoreNum == 0 ]]; then
        CpuCoreNum=1
    fi
    if [[ $CpuCount == 0 ]]; then
        CpuCount=2
    fi
    # 总内存大小GB
    MemTotal=`awk '($1 == "MemTotal:"){printf "%.2f\n",$2/1024/1024}' /proc/meminfo`
    use=$(echo "scale=4; $MemTotal / 3" | bc)

    cat ~/.config/deepin-wine-runner/QEMU-ARCH | grep amd64
    if [[ $? == 0 ]] || [[ ! -e ~/.config/deepin-wine-runner/QEMU-ARCH ]]; then
        # amd64 架构
        if [[ -f $HOME/.config/deepin-wine-runner/QEMU-EFI ]]; then
            echo 使用 UEFI 启动
            if [[ -f /usr/share/qemu/OVMF.fd ]]; then
                qemuUEFI="--bios /usr/share/qemu/OVMF.fd -vga none -device virtio-gpu-pci -device nec-usb-xhci,id=xhci,addr=0x1b -device usb-tablet,id=tablet,bus=xhci.0,port=1 -device usb-kbd,id=keyboard,bus=xhci.0,port=2 "
            else
                if [[ -f `dirname $0`/VM/OVMF.fd ]]; then   
                    qemuUEFI="--bios `dirname $0`/VM/OVMF.fd -vga none -device virtio-gpu-pci -device nec-usb-xhci,id=xhci,addr=0x1b -device usb-tablet,id=tablet,bus=xhci.0,port=1 -device usb-kbd,id=keyboard,bus=xhci.0,port=2 "
                fi
            fi
        else
            qemuUEFI="-vga virtio -device nec-usb-xhci,id=xhci,addr=0x1b -device usb-tablet,id=tablet,bus=xhci.0,port=1 "
        fi
        echo $qemuUEFI
        ./VM/kvm-ok
        if [[ $? == 0 ]] && [[ `arch` == "x86_64" ]]; then
            echo X86 架构，使用 kvm 加速
            $qemuMore qemu-system-x86_64 --enable-kvm -cpu host --hda "$HOME/Qemu/Windows/Windows.qcow2" \
                -smp $CpuCount,sockets=$CpuSocketNum,cores=$(($CpuCoreNum / $CpuSocketNum)),threads=$(($CpuCount / $CpuCoreNum / $CpuSocketNum)) \
                -m ${use}G  -display vnc=:5 -display gtk -usb -nic model=rtl8139 $qemuUEFI \
                -device AC97 -device ES1370 -device intel-hda -device hda-duplex  \
                --boot 'splash=VM/boot.jpg,menu=on,splash-time=2000' \
                > /tmp/windows-virtual-machine-installer-for-wine-runner-run.log 2>&1 # 最新的 qemu 已经移除参数 -soundhw all 
            exit
        fi
        # 判断系统版本以选择 Qemu
        isUOS=0
        qemuPath=qemu-system-x86_64
        cat /etc/os-version | grep -i uos
        if [[ $? == 0 ]]; then
            isUOS=1
        fi
        cat /etc/os-version | grep -i unio
        if [[ $? == 0 ]]; then
            isUOS=1
        fi
        if [[ $isUOS == 1 ]]; then
            arch=`uname -m`
            if [[ $arch == "mips64" ]] || [[ $arch == "mips64el" ]]; then
                qemuPath="bwrap --dev-bind / / --bind ./VM/MipsQemu/usr/lib/mips64el-linux-gnuabi64/qemu/ui-gtk.so /usr/lib/mips64el-linux-gnuabi64/qemu/ui-gtk.so ./VM/MipsQemu/usr/bin/qemu-system-x86_64"
            fi
        fi
        if [[ $qemuMore != "" ]]; then
            qemuPath=$qemuMore 
        fi
        echo 不使用 kvm 加速
        $qemuPath --hda "$HOME/Qemu/Windows/Windows.qcow2" \
            -smp $CpuCount,sockets=$CpuSocketNum,cores=$(($CpuCoreNum / $CpuSocketNum)),threads=$(($CpuCount / $CpuCoreNum / $CpuSocketNum)) \
            -m ${use}G  -display vnc=:5 -display gtk -usb -nic model=rtl8139 $qemuUEFI \
            -device AC97 -device ES1370 -device intel-hda -device hda-duplex  \
            --boot 'splash=VM/boot.jpg,menu=on,splash-time=2000' \
            > /tmp/windows-virtual-machine-installer-for-wine-runner-run.log 2>&1 # 最新的 qemu 已经移除参数 -soundhw all 
        exit
    fi
    cat ~/.config/deepin-wine-runner/QEMU-ARCH | grep armhf
    if [[ $? == 0 ]]; then
        # armhf 架构
        # 寻找 UEFI 固件
        if [[ -f /usr/share/AAVMF/AAVMF32_CODE.fd ]]; then
            qemuUEFI="--bios /usr/share/AAVMF/AAVMF32_CODE.fd"
        else
            if [[ -f ./VM/AAVMF32_CODE.fd ]]; then
                qemuUEFI="--bios ./VM/AAVMF32_CODE.fd"
            fi
        fi
        echo $qemuUEFI
        ./VM/kvm-ok
        if [[ $? == 0 ]] && [[ `arch` == "aarch64" ]]; then
            $qemuMore qemu-system-arm --enable-kvm --hda "$HOME/Qemu/Windows/Windows.qcow2" \
                -smp $CpuCount,sockets=$CpuSocketNum,cores=$(($CpuCoreNum / $CpuSocketNum)),threads=$(($CpuCount / $CpuCoreNum / $CpuSocketNum)) \
                -m ${use}G  -display vnc=:5 -display gtk -usb -nic model=rtl8139 $qemuUEFI \
                -cpu max -M virt -device virtio-gpu-pci \
                -device nec-usb-xhci,id=xhci,addr=0x1b \
                -device usb-tablet,id=tablet,bus=xhci.0,port=1 \
                -device usb-kbd,id=keyboard,bus=xhci.0,port=2 \
                -device AC97 -device ES1370 -device intel-hda -device hda-duplex \
                --boot 'splash=VM/boot.jpg,menu=on,splash-time=2000' \
                > /tmp/windows-virtual-machine-installer-for-wine-runner-install.log 2>&1 # 最新的 qemu 已经移除参数 -soundhw all 
            exit
        fi
        $qemuMore qemu-system-arm --hda "$HOME/Qemu/Windows/Windows.qcow2" \
            -smp $CpuCount,sockets=$CpuSocketNum,cores=$(($CpuCoreNum / $CpuSocketNum)),threads=$(($CpuCount / $CpuCoreNum / $CpuSocketNum)) \
            -m ${use}G  -display vnc=:5 -display gtk -usb -nic model=rtl8139 $qemuUEFI \
            -cpu max -M virt -device virtio-gpu-pci \
            -device nec-usb-xhci,id=xhci,addr=0x1b \
            -device usb-tablet,id=tablet,bus=xhci.0,port=1 \
            -device usb-kbd,id=keyboard,bus=xhci.0,port=2 \
            -device AC97 -device ES1370 -device intel-hda -device hda-duplex \
            --boot 'splash=VM/boot.jpg,menu=on,splash-time=2000' \
            > /tmp/windows-virtual-machine-installer-for-wine-runner-install.log 2>&1 # 最新的 qemu 已经移除参数 -soundhw all 
        exit
    fi
    cat ~/.config/deepin-wine-runner/QEMU-ARCH | grep aarch64
    if [[ $? == 0 ]]; then
        # aarch64 架构
        # 寻找 UEFI 固件
        if [[ -f /usr/share/qemu-efi-aarch64/QEMU_EFI.fd ]]; then
            qemuUEFI="--bios /usr/share/qemu-efi-aarch64/QEMU_EFI.fd"
        else
            if [[ -f ./VM/QEMU_AARCH64_EFI.fd ]]; then
                qemuUEFI="--bios ./VM/QEMU_AARCH64_EFI.fd"
            fi
        fi
        echo $qemuUEFI
        ./VM/kvm-ok
        if [[ $? == 0 ]] && [[ `arch` == "aarch64" ]]; then
            $qemuMore qemu-system-aarch64 --enable-kvm --hda "$HOME/Qemu/Windows/Windows.qcow2" \
                -smp $CpuCount,sockets=$CpuSocketNum,cores=$(($CpuCoreNum / $CpuSocketNum)),threads=$(($CpuCount / $CpuCoreNum / $CpuSocketNum)) \
                -m ${use}G  -display vnc=:5 -display gtk -usb -nic model=rtl8139 $qemuUEFI \
                -cpu max -M virt \
                -device virtio-gpu-pci \
                -device nec-usb-xhci,id=xhci,addr=0x1b \
                -device usb-tablet,id=tablet,bus=xhci.0,port=1 \
                -device usb-kbd,id=keyboard,bus=xhci.0,port=2 \
                -device AC97 -device ES1370 -device intel-hda -device hda-duplex \
                --boot 'splash=VM/boot.jpg,menu=on,splash-time=2000' \
                > /tmp/windows-virtual-machine-installer-for-wine-runner-install.log 2>&1 # 最新的 qemu 已经移除参数 -soundhw all 
            exit
        fi
        $qemuMore qemu-system-aarch64 --hda "$HOME/Qemu/Windows/Windows.qcow2" \
            -smp $CpuCount,sockets=$CpuSocketNum,cores=$(($CpuCoreNum / $CpuSocketNum)),threads=$(($CpuCount / $CpuCoreNum / $CpuSocketNum)) \
            -m ${use}G  -display vnc=:5 -display gtk -usb -nic model=rtl8139 $qemuUEFI \
            -cpu max -M virt \
            -device virtio-gpu-pci \
            -device nec-usb-xhci,id=xhci,addr=0x1b \
            -device usb-tablet,id=tablet,bus=xhci.0,port=1 \
            -device usb-kbd,id=keyboard,bus=xhci.0,port=2 \
            -device AC97 -device ES1370 -device intel-hda -device hda-duplex \
            --boot 'splash=VM/boot.jpg,menu=on,splash-time=2000' \
            > /tmp/windows-virtual-machine-installer-for-wine-runner-install.log 2>&1 # 最新的 qemu 已经移除参数 -soundhw all 
        exit
    fi
    
fi
zenity --question --no-wrap --text="检查到您未创建所指定的虚拟机，是否创建虚拟机并继续？\n如果不创建将无法使用"
if [[ 1 == $? ]]; then
    # 用户不想创建虚拟机，结束
    exit
fi

./VM/VirtualMachine
