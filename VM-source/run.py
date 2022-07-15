#!/usr/bin/env python3
import os
import api
import sys
import psutil

if __name__ == "__main__":
    os.system("clear")
    programPath = os.path.split(os.path.realpath(__file__))[0]
    if len(sys.argv) < 3 :
        print("参数不齐！")
        exit()
    net = ""
    for k, v in psutil.net_if_addrs().items():
        for item in v:
            if item[0] == 2 and not item[1] == "127.0.0.1" and not item[1] == "192.168.250.1":
                net = k
                break
    if net == "":
        exit()
    # 创建一个叫Windows的虚拟机
    vm = api.Manager("Windows")
    if sys.argv[2] == "0":
        vm.Create("Windows7")
    elif sys.argv[2] == "1":
        vm.Create("Windows7_64")
    else:
        vm.Create("WindowsNT_64")
    vm.CreateDisk(f"{api.homePath}/VirtualBox VMs/Windows/Windows.vdi", 131072)
    vm.CreateDiskControl()
    vm.MountDisk(f"{api.homePath}/VirtualBox VMs/Windows/Windows.vdi")
    vm.MountISO(sys.argv[1])
    if sys.argv[2] == "0":
        vm.MountISO(f"{programPath}/Windows7X86Auto.iso", device=1)
    elif sys.argv[2] == "1":
        vm.MountISO(f"{programPath}/Windows7X64Auto.iso", device=1)
    vm.SetCPU(1)
    vm.SetMemory(psutil.virtual_memory().total // 1024 // 1024 // 3)
    vm.SetDisplayMemory(32)
    vm.SetNetBridge(net)
    vm.EnabledAudio()
    vm.EnabledClipboardMode()
    vm.EnabledDraganddrop()
    vm.SetVBoxSVGA()
    vm.SetMousePS2()
    vm.SetKeyboardPS2()
    vm.OpenUSB()
    vm.ShareFile("ROOT", "/")
    vm.ShareFile("HOME", api.homePath)
    vm.Start()