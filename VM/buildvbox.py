# *
# * gfdgd xi
# * 依照 GPLV3 开源
# *

import os
import psutil
import subprocess
from vbox import *
from qemu import *
from infoUtils import *
from PyQt5.QtNetwork import *

class buildvbox:
    def homePath(self):
        return os.getenv("HOME")

    def applicationDirPath(self):
        return os.path.split(os.path.realpath(__file__))[0]  # 返回 string
    
    # 清屏
    def CleanScreen(self):
        if(os.system("/etc/os-version")):
            # Unix
            os.system("clear")
            return
        # Windows
        os.system("cls")

    # 获取 CPU 个数
    def GetCPUSocket(self) -> int:
        # 获取命令返回值
        value = int(subprocess.getoutput("bash -c 'cat /proc/cpuinfo | grep \"cpu cores\" | uniq | wc -l'"))
        # 判断异常值，例如没挂载 /proc
        if (value <= 0):
            value = 1
        return value

    # 获取 CPU 核心数
    def GetCPUCore(self) -> int:
        value = int(subprocess.getoutput("bash -c \"grep 'core id' /proc/cpuinfo | sort -u | wc -l\""))
        # 判断异常值，例如没挂载 /proc
        if(value <= 0):
            value = 1
        return value

    def GetNet(self) -> str:
        netList = QNetworkInterface.allInterfaces()
        for net in netList:
            print("Device:", net.name())
            entryList = net.addressEntries()
            for entry in entryList:
                ip = entry.ip().toString()
                print("IP Address: ", ip)
                if(ip != "127.0.0.1" and ip != "192.168.250.1" and ip != "::1" and net.name() != "lo"):
                    # 返回网卡名称
                    return net.name()
        return ""

    def Download(self, url: str, path: str, fileName: str) -> int:
        return os.system(("aria2c -x 16 -s 16 -c " + url + " -d " + path + " -o " + fileName))

    def __init__(self, isoPath: str, id = 0, vm = 0):
        programPath = self.applicationDirPath()

        net = self.GetNet()
        print("使用网卡：", net)
        if(vm == 0):
            # Qemu
            vm = qemu("Windows")
            setISOAlready = 0
            if (id == 0):
                vm.Create("Windows7")
                vm.SetDisplayMemory(32)
            elif (id == 1):
                vm.Create("Windows7_64")
                vm.SetDisplayMemory(32)
            elif (id == 2):
                vm.Create("WindowsNT_64")
                vm.SetDisplayMemory(32)
            elif (id == 3):
                vm.Create("WindowsNT_64")
                vm.SetDisplayMemory(32)
                vm.EnabledUEFI(True)
            elif (id == 4):
                vm.Create("Windows11_64")
                vm.SetDisplayMemory(128)
                vm.EnabledUEFI(True)
                setISOAlready = 1
            elif (id == 5):
                vm.Create("WindowsXP_32")
                vm.SetDisplayMemory(32)
                setISOAlready = 1
            elif (id == 6):
                vm.Create("WindowsNT_64")
                vm.SetDisplayMemory(32)
                setISOAlready = 1
            elif (id == 7):
                vm.Create("WindowsNT_64")
                vm.SetDisplayMemory(32)
                vm.EnabledUEFI(True)
                setISOAlready = 1
            elif (id == 8):
                vm.Create("WindowsNT_64")
                vm.SetDisplayMemory(32)
                vm.UseArmhfEFI()
                setISOAlready = 1
            elif (id == 9):
                vm.Create("WindowsNT_64")
                vm.SetDisplayMemory(32)
                vm.UseAarch64EFI()
                setISOAlready = 1
            vm.CreateDiskControl()
            #vm.CreateDiskControl("storage_controller_2")
            if(id == 0 or id == 1):
                vm.CreateDisk(self.homePath() + "/Qemu/Windows/Windows.qcow2", 131072)
            else:
                vm.CreateDisk(self.homePath() + "/Qemu/Windows/Windows.qcow2", 131072 * 5)

            #vm.MountDisk(self.homePath() + "/Qemu/Windows/Windows.qcow2")
            vm.MountMainDisk(self.homePath() + "/Qemu/Windows/Windows.qcow2")
            if(os.path.exists("/opt/apps/deepin-wine-runner-qemu-system-extra/files/resources/virtio-win.iso")):
                vm.MountISO("/opt/apps/deepin-wine-runner-qemu-system-extra/files/resources/virtio-win.iso", "storage_controller_2", 1, 3)
            if(not setISOAlready):
                vm.MountISO(isoPath, "storage_controller_1", 0, 1)
                if (id == 0):
                    if(os.system(programPath + "/Windows7X86Auto.iso")):
                        vm.MountISO(programPath + "/Windows7X86Auto.iso", "storage_controller_1", 1, 2)
                elif (id == 1):
                    if(os.system(programPath + "/Windows7X64Auto.iso")):
                        vm.MountISO(programPath + "/Windows7X64Auto.iso", "storage_controller_1", 1, 2)
            else:
                #vm.AutoInstall(isoPath)
                if(isoPath != ""):
                    vm.MountMainISO(isoPath)
            vm.SetCPU(psutil.cpu_count(), self.GetCPUSocket(), self.GetCPUCore())
            memory = 0
            memoryAll = 0
            swap = 0
            swapAll = 0
            # TODO
            memory, memoryAll, swap, swapAll = infoUtils().memoryRate()
            vm.SetMemory(int(memoryAll / 3 / 1024))
            vm.SetNetBridge(net)
            vm.EnabledAudio()
            vm.EnabledClipboardMode()
            vm.EnabledDraganddrop()
            vm.SetVBoxSVGA()
            vm.SetMousePS2()
            vm.SetKeyboardPS2()
            vm.OpenUSB()
            vm.ShareFile("ROOT", "/")
            vm.ShareFile("HOME", self.homePath())
            # TODO
            if (id == 8):
                vm.StartArmhf()
            elif (id == 9):
                vm.StartAarch64()
            else:
                vm.Start()
        elif(vm == 1):
            # VirtualBox
            vm = vbox("Windows")
            setISOAlready = 1
            if (id == 0):
                vm.Create("Windows7")
                vm.SetDisplayMemory(32)
            elif (id == 1):
                vm.Create("Windows7_64")
                vm.SetDisplayMemory(32)
            elif (id == 2):
                vm.Create("WindowsNT_64")
                vm.SetDisplayMemory(32)
            elif (id == 3):
                vm.Create("WindowsNT_64")
                vm.EnabledUEFI(True)
                vm.SetDisplayMemory(32)
            elif (id == 4):
                vm.Create("Windows11_64")
                vm.SetDisplayMemory(128)
                vm.EnabledUEFI(True)
                setISOAlready = 1
            elif (id == 5):
                vm.Create("WindowsXP_32")
                vm.SetDisplayMemory(32)
                setISOAlready = 1
            elif (id == 6):
                vm.Create("WindowsNT_64")
                vm.SetDisplayMemory(32)
                setISOAlready = 1
            elif (id == 7):
                vm.Create("WindowsNT_64")
                vm.SetDisplayMemory(32)
                vm.EnabledUEFI(True)
                setISOAlready = 1
            if (not os.path.exists):
                os.makedirs("/home/gfdgd_xi/Qemu/Windows/")
            vm.CreateDiskControl()
            #vm.CreateDiskControl("storage_controller_2")
            if(id == 0 or id == 1):
                vm.CreateDisk(self.homePath() + "/VirtualBox VMs/Windows/Windows.vdi", 131072)
            else:
                vm.CreateDisk(self.homePath() + "/VirtualBox VMs/Windows/Windows.vdi", 131072 * 5)
            vm.MountDisk(self.homePath() + "/VirtualBox VMs/Windows/Windows.vdi")
            if(not setISOAlready):
                vm.MountISO(isoPath, "storage_controller_1", 0, 1)
                if (id == 0):
                    if(os.system(programPath + "/Windows7X86Auto.iso")):
                        vm.MountISO(programPath + "/Windows7X86Auto.iso", "storage_controller_1", 1, 0)
                elif (id == 1):
                    if(os.system(programPath + "/Windows7X64Auto.iso")):
                        vm.MountISO(programPath + "/Windows7X64Auto.iso", "storage_controller_1", 1, 0)
            else:
                vm.AutoInstall(isoPath)
            # 判断 VirtualBox Guest ISO 是否存在
            # 在的话直接挂载
            if(os.system("/usr/share/virtualbox/VBoxGuestAdditions.iso")):
                vm.MountISO("/usr/share/virtualbox/VBoxGuestAdditions.iso", "storage_controller_1", 1, 1)
            # VirtualBox 的 CPU 数量设置方法和 Qemu 不一样
            vm.SetCPU(self.GetCPUCore(), self.GetCPUSocket(), self.GetCPUCore())
            memory = 0
            memoryAll = 0
            swap = 0
            swapAll = 0
            # TODO
            memory, memoryAll, swap, swapAll = infoUtils().memoryRate()
            #memoryRate(memory, memoryAll, swap, swapAll)
            vm.SetMemory(int(memoryAll / 3 / 1024))
            print(memoryAll)
            vm.SetNetBridge(net)
            vm.EnabledAudio()
            vm.EnabledClipboardMode()
            vm.EnabledDraganddrop()
            vm.SetVBoxSVGA()
            vm.SetMousePS2()
            vm.SetKeyboardPS2()
            vm.OpenUSB()
            vm.ShareFile("ROOT", "/")
            vm.ShareFile("HOME", self.homePath())
            vm.Start()
    