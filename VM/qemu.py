import os
import shutil
import subprocess

class qemu:
    name = ""
    managerPath = ""
    vboxVersion = ""
    commandOption = ""
    isUEFI = False

    def applicationDirPath(self):
        return os.path.split(os.path.realpath(__file__))[0]  # 返回 string

    def homePath(self):
        return os.getenv("HOME")

    def __init__(self, name: str, managerPath = "/usr/bin") -> None:
        if (not os.path.exists(name)):
            self.name = self.homePath() + "/Qemu/" + name
        else:
            self.name = name
        self.managerPath = managerPath
        self.qemuPath = "qemu-system-i386"
        if (os.path.exists("/opt/apps/deepin-wine-runner-qemu-system-extra/files/run.sh")):
            # 如果存在拓展 Qemu，则调用此
            self.qemuPath = "/opt/apps/deepin-wine-runner-qemu-system-extra/files/run.sh qemu-system-i386"
        self.vboxVersion = subprocess.getoutput(self.qemuPath + " --version")

    def Create(self, type = "Windows7"):
        if(not os.path.exists(self.name)):
            os.makedirs(self.name)
        return 0

    def CreateDisk(self, path: str, size: int):
        if(os.path.exists(path)):
            return 0
        return os.system(("qemu-img create -f qcow2 '" + self.path + "' " + str(size) + "M"))

    def CreateDiskControl(self, controlName = "storage_controller_1"):
        return 0

    def MountDisk(self, diskPath: str, controlName = "storage_controller_1", port = 0, device = 0):
        self.commandOption += "-drive 'file=" + diskPath + ",if=ide,index=" + str(device) + "' "
        return 0

    def MountISO(self, isoPath, controlName = "storage_controller_1", port = 1, device = 0):
        self.commandOption += "-drive 'media=cdrom,file=" + isoPath + ",if=ide,index=" + str(device) + "' "
        return 0

    def BootFirst(self, bootDrive: str):
        self.commandOption += "-boot '" + bootDrive + "' "
        return 0

    def SetNetBridge(self, netDriver: str):
        return 0

    def SetCPU(self, number: int, cpuNum: int, coreNum: int):
        # self.commandOption += "-smp " + str(number) + " "
        # 调整调用方法
        #qDebug() << number << " " << cpuNum << " " << coreNum
        print("Socket: ", cpuNum)
        print("Core: ", coreNum)
        print("Threads: ", number)
        self.commandOption += "-smp " + str(number) + ",sockets=" + str(cpuNum) + ",cores=" + str(int(coreNum / cpuNum)) + ",threads=" + str(int(number / cpuNum / coreNum)) + " "
        return 0

    def SetMemory(self, memory: str):
        self.commandOption += "-m " + str(memory) + "M "
        return 0

    def SetRemote(self, setting: bool):
        return 0

    def SetRemoteConnectSetting(self, port = 5540):
        return 0

    def MountMainDisk(self, diskPath: str):
        self.commandOption += " --hda '" + diskPath + "' "
        return 0

    def StartArmhf(self):
        print(self.commandOption)
        qemuPath = "qemu-system-arm"
        if(os.path.exists("/opt/apps/deepin-wine-runner-qemu-system-extra/files/run.sh")):
            # 如果存在拓展 Qemu，则调用此
            qemuPath = "/opt/apps/deepin-wine-runner-qemu-system-extra/files/run.sh qemu-system-arm"
        if(subprocess.getoutput("arch").replace("\n", "").replace(" ", "") == "aarch64" and not os.system((self.applicationDirPath() + "/kvm-ok"))):
            return os.system((qemuPath + " --boot 'splash=" + self.GetBootLogoPath() + ",order=d,menu=on,splash-time=2000' -display gtk --enable-kvm -cpu host -M virt " + self.commandOption + " -device virtio-gpu-pci -device nec-usb-xhci,id=xhci,addr=0x1b -device usb-tablet,id=tablet,bus=xhci.0,port=1 -device usb-kbd,id=keyboard,bus=xhci.0,port=2 > /tmp/windows-virtual-machine-installer-for-wine-runner-install.log 2>&1 &"))
    
        return os.system((qemuPath + " --boot 'splash=" + self.GetBootLogoPath() + ",order=d,menu=on,splash-time=2000' -display gtk -cpu max -M virt " + self.commandOption + " -device virtio-gpu-pci -device nec-usb-xhci,id=xhci,addr=0x1b -device usb-tablet,id=tablet,bus=xhci.0,port=1 -device usb-kbd,id=keyboard,bus=xhci.0,port=2 > /tmp/windows-virtual-machine-installer-for-wine-runner-install.log 2>&1 &"))

    def StartAarch64(self):
        bootScreenLogo = ""
        qemuPath = "qemu-system-aarch64"
        # 判断 boot 文件是否存在
        if (os.path.exists(self.applicationDirPath() + "/boot.jpg")):
            bootScreenLogo = self.applicationDirPath() + "/boot.jpg"
        else:
            # 写入 logo
            shutil.copy(":/boot.jpg", "/tmp/deep-wine-runner-boot.jpg")
            bootScreenLogo = "/tmp/deep-wine-runner-boot.jpg"
    
        if(os.path.exists("/opt/apps/deepin-wine-runner-qemu-system-extra/files/run.sh")):
            # 如果存在拓展 Qemu，则调用此
            qemuPath = "/opt/apps/deepin-wine-runner-qemu-system-extra/files/run.sh qemu-system-aarch64"
    
        print(self.commandOption)
        if(subprocess.getoutput("arch").replace("\n", "").replace(" ", "") == "aarch64" and not os.system((self.applicationDirPath() + "/kvm-ok"))):
            return os.system((qemuPath + " --boot 'splash=" + self.GetBootLogoPath() + ",order=d,menu=on,splash-time=2000' -display gtk --enable-kvm -cpu host -M virt " + self.commandOption + " -device virtio-gpu-pci -device nec-usb-xhci,id=xhci,addr=0x1b -device usb-tablet,id=tablet,bus=xhci.0,port=1 -device usb-kbd,id=keyboard,bus=xhci.0,port=2 > /tmp/windows-virtual-machine-installer-for-wine-runner-install.log 2>&1 &"))
    
        return os.system((qemuPath + " --boot 'splash=" + self.GetBootLogoPath() + ",order=d,menu=on,splash-time=2000' -display gtk -cpu max -M virt " + self.commandOption + " -device virtio-gpu-pci -device nec-usb-xhci,id=xhci,addr=0x1b -device usb-tablet,id=tablet,bus=xhci.0,port=1 -device usb-kbd,id=keyboard,bus=xhci.0,port=2 > /tmp/windows-virtual-machine-installer-for-wine-runner-install.log 2>&1 &"))

    def StartLoong64(self):
        return 1

    def Start(self, unShown = False):
        newCommandOption = self.commandOption
        qemuPath = "qemu-system-x86_64"
        print(self.GetBootLogoPath())
        if (self.isUEFI):
            newCommandOption += " -vga none -device virtio-gpu-pci -device nec-usb-xhci,id=xhci,addr=0x1b -device usb-tablet,id=tablet,bus=xhci.0,port=1 -device usb-kbd,id=keyboard,bus=xhci.0,port=2 "
        else:
            newCommandOption += " -vga virtio -device nec-usb-xhci,id=xhci,addr=0x1b -device usb-tablet,id=tablet,bus=xhci.0,port=1 "
        # UOS 3a4000 使用程序自带的 qemu
        info = self.SystemInfo().lower()
        if("uos" in info or "unio" in info):
            # 判断架构
            arch = self.GetArch()
            if(arch == "mips64" or arch == "mipsel64"):
                qemuPath = "bwrap --dev-bind / / --bind '" + self.applicationDirPath() + "/MipsQemu/usr/lib/mips64el-linux-gnuabi64/qemu/ui-gtk.so' /usr/lib/mips64el-linux-gnuabi64/qemu/ui-gtk.so '" + self.applicationDirPath() + "/MipsQemu/usr/bin/qemu-system-x86_64' "    
        if(os.path.exists("/opt/apps/deepin-wine-runner-qemu-system-extra/files/run.sh")):
            # 如果存在拓展 Qemu，则调用此
            qemuPath = "/opt/apps/deepin-wine-runner-qemu-system-extra/files/run.sh qemu-system-x86_64"
        print(self.commandOption)
        if(subprocess.getoutput("arch").replace("\n", "").replace(" ", "") == "x86_64" and not os.system((self.applicationDirPath() + "/kvm-ok"))):
            return os.system((qemuPath + " --boot 'splash=" + self.GetBootLogoPath() + ",order=d,menu=on,splash-time=2000' -display gtk --enable-kvm -cpu host " + newCommandOption + " > /tmp/windows-virtual-machine-installer-for-wine-runner-install.log 2>&1 &"))
        return os.system((qemuPath + " --boot 'splash=" + self.GetBootLogoPath() + ",order=d,menu=on,splash-time=2000' -display gtk -nic model=rtl8139 " + newCommandOption + " > /tmp/windows-virtual-machine-installer-for-wine-runner-install.log 2>&1 &"))

    def Stop(self):
        os.system("killall qemu-system-x86_64 -9")
        os.system("killall qemu-system-aarch64 -9")
        os.system("killall qemu-system-arm -9")
        os.system("killall kvm -9")
        return 0

    def Delete(self):
        return os.system(("rm -rfv '" + self.name + "'"))

    def SetDisplayMemory(self, memory: int):
        return 0

    def InstallGuessAdditions(self, controlName = "storage_controller_1", port = 1, device = 0):
        return 0

    def EnabledAudio(self):
        self.commandOption += "-device AC97 -device ES1370 -device intel-hda -device hda-duplex "
        return 0

    def EnabledClipboardMode(self):
        return 0

    def EnabledDraganddrop(self):
        return 0

    def ShareFile(self, name: str, path: str):
        return 0

    def SetVBoxSVGA(self):
        return 0

    def SetMousePS2(self):
        return 0

    def SetKeyboardPS2(self):
        return 0

    def OpenUSB(self):
        return 0

    def UseAarch64EFI(self):
        if(os.path.exists("/usr/share/qemu-efi-aarch64/QEMU_EFI.fd")):
            self.commandOption += "--bios /usr/share/qemu-efi-aarch64/QEMU_EFI.fd "
            return 0
        if(os.path.exists(self.applicationDirPath() + "/QEMU_AARCH64_EFI.fd")):
            self.commandOption += "--bios '" + self.applicationDirPath() + "/QEMU_AARCH64_EFI.fd' "
            return 0
        return 1

    def UseArmhfEFI(self):
        if(os.path.exists("/usr/share/AAVMF/AAVMF32_CODE.fd")):
            self.commandOption += "--bios /usr/share/AAVMF/AAVMF32_CODE.fd "
            return 0
        if(os.path.exists(self.applicationDirPath() + "/AAVMF32_CODE.fd")):
            self.commandOption += "--bios '" + self.applicationDirPath() + "/AAVMF32_CODE.fd' "
            return 0
        return 1

    def UseLoongarch64EFI(self):
        return 0

    def UseOtherEFI(self, fdFilePath: str):
        return 0

    def EnabledUEFI(self, status: str):
        isUEFI = status
        if(not status):
            return 0    
        if(os.path.exists("/usr/share/qemu/OVMF.fd")):
            self.commandOption += "--bios /usr/share/qemu/OVMF.fd "
            return 0
        if(os.path.exists(self.applicationDirPath() + "/OVMF.fd")):
            self.commandOption += "--bios '" + self.applicationDirPath() + "/OVMF.fd' "
            return 0
        return 1

    def MountMainISO(self, isoPath: str):
        self.commandOption += "--cdrom '" + isoPath + "' "
        return 0

    def AutoInstall(self, iso: str):
        return 0

    def AddDiskSpace(self, path, data: float):
        return os.system(("qemu-img resize '" + self.path + "' +" + str(data) + "G"))

    def GetBootLogoPath(self) -> str:
        bootScreenLogo = ""
        # 判断 boot 文件是否存在
        if(os.path.exists(self.applicationDirPath() + "/boot.jpg")):
            bootScreenLogo = self.applicationDirPath() + "/boot.jpg"
        else:
            # 写入 logo
            if(os.path.exists("/tmp/deep-wine-runner-boot.jpg")):
                os.remove("/tmp/deep-wine-runner-boot.jpg")            
            shutil.copy(":/boot.jpg", "/tmp/deep-wine-runner-boot.jpg")
            bootScreenLogo = "/tmp/deep-wine-runner-boot.jpg"
        return bootScreenLogo


    def SystemInfo(self) -> str:
        with open("/etc/os-version", "r") as file:
            data = file.read()
        return data

    def GetArch(self) -> str:
        return subprocess.getoutput("uname -m").replace("\n", "").replace(" ", "")
    
