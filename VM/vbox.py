import os
import subprocess

class vbox:
    name = ""
    managerPath = ""
    vboxVersion = ""

    def __init__(self, name: str, managerPath = "VBoxManage") -> None:
        self.name = name
        self.managerPath = managerPath
        self.vboxVersion = subprocess.getoutput("'" + managerPath + "' -v")
    
    def Create(self, type = "Windows7"):
        os.system(("\"" + self.managerPath + "\" createvm --name \""
                   + self.name + "\" --ostype \"" + type +
                   "\" --register"))
        return os.system(("\"" + self.managerPath + "\" modifyvm \""
                   + self.name + "\" --ostype \"" + type +
                   "\" "))
        # vboxmanage modifyvm testvm --ostype

    def CreateDisk(self, path: str, size: int):
        return os.system(("\"" + self.managerPath + "\" createvdi --filename \"" + path + "\" --size \"" + str(size) + "\""))

    def CreateDiskControl(self, controlName = "storage_controller_1"):
        return os.system(("\"" + self.managerPath + "\" storagectl \"" + self.name + "\" --name \"" + controlName + "\" --add ide"))

    def MountDisk(self, diskPath: str, controlName = "storage_controller_1", port = 0, device = 0):
        return os.system(("\"" + self.managerPath + "\" storageattach \"" + self.name +
                   "\" --storagectl \"" + controlName + "\" --type hdd --port "
                   + str(port) + " --device " + str(device) + " --medium \"" + diskPath + "\""))

    def MountISO(self, isoPath: str, controlName = "storage_controller_1", port = 1, device = 0):
        return os.system(("\"" + self.managerPath + "\" storageattach \"" + self.name + "\" --storagectl \"" +
                   controlName + "\" --type dvddrive --port " + str(port) + " --device " + str(device)
                   + " --medium \"" + isoPath + "\""))

    def BootFirst(self, bootDrive: str):
        return os.system(("\"" + self.managerPath + "\" modifyvm \"" + self.name + "\" --boot1 " + bootDrive))

    def SetNetBridge(self, netDriver: str):
        return os.system(("\"" + self.managerPath + "\" modifyvm \"" + self.name +
                   "\" --nic1 bridged --cableconnected1 on --nictype1 82540EM --bridgeadapter1 \"" + netDriver + "\" --intnet1 brigh1 --macaddress1 auto"))

    def SetCPU(self, number: int, cpuNum: int, coreNum: int):
        return os.system(("\"" + self.managerPath + "\" modifyvm \"" + self.name + "\" --cpus " + str(number)))

    def SetMemory(self, memory: int):
        return os.system(("\"" + self.managerPath + "\" modifyvm \"" + self.name + "\" --memory " + str(memory)))

    def SetRemote(self, setting: bool):
        if (setting):
            return os.system(("\"" + self.managerPath + "\" modifyvm \"" + self.name + "\" --vrde on"))
        return os.system(("\"" + self.managerPath + "\" modifyvm \"" + self.name + "\" --vrde off"))

    def SetRemoteConnectSetting(self, port = 5540):
        return os.system(("\"" + self.managerPath + "\" modifyvm \"" + self.name + "\" --vrdeport " + str(port) + " --vrdeaddress """))

    def Start(self, unShown = False):
        if (unShown):
            return os.system(("\"" + self.managerPath + "\" > /tmp/windows-virtual-machine-installer-for-wine-runner-install.log 2>&1"))
        return os.system(("\"" + self.managerPath + "\" startvm \"" + self.name + "\"  > /tmp/windows-virtual-machine-installer-for-wine-runner-install.log 2>&1"))

    def Stop(self):
        return os.system(("\"" + self.managerPath + "\" controlvm \"" + self.name + "\" poweroff"))

    def Delete(self):
        return os.system(("\"" + self.managerPath + "\" unregistervm --delete \"" + self.name + "\""))

    def SetDisplayMemory(self, memory: int):
        return os.system(("\"" + self.managerPath + "\" modifyvm \"" + self.name + "\" --vram " + str(memory)))

    def InstallGuessAdditions(self, controlName = "storage_controller_1", port = 1, device = 0):
        return self.MountISO("/usr/share/virtualbox/VBoxGuestAdditions.iso", controlName, port, device);
    
    def EnabledAudio(self):
        return os.system(("\"" + self.managerPath + "\" modifyvm \"" + self.name + "\" --audio-driver pulse --audiocontroller hda --audioin on --audioout on"))

    def EnabledClipboardMode(self):
        return os.system(("\"" + self.managerPath + "\" modifyvm \"" + self.name + "\" --clipboard-mode bidirectional"))

    def EnabledDraganddrop(self):
        return os.system(("\"" + self.managerPath + "\" modifyvm \"" + self.name + "\" --draganddrop bidirectional"))
    
    def ShareFile(self, name: str, path: str):
        return os.system(("\"" + self.managerPath + "\" sharedfolder add \"" + self.name + "\" -name \"" + self.name + "\" -hostpath \"" + path + "\""))

    def SetVBoxSVGA(self):
        return os.system(("\"" + self.managerPath + "\" modifyvm \"" + self.name + "\" --graphicscontroller vboxsvga"))

    def SetMousePS2(self):
        return os.system(("\"" + self.managerPath + "\" modifyvm \"" + self.name + "\" --mouse usb"))

    def SetKeyboardPS2(self):
        return os.system(("\"" + self.managerPath + "\" modifyvm \"" + self.name + "\" --keyboard usb"))
    
    def OpenUSB(self):
        return os.system(("\"" + self.managerPath + "\" modifyvm \"" + self.name + "\" --usbohci on"))

    def EnabledUEFI(self, status: bool):
        if (status):
            return os.system(("\"" + self.managerPath + "\" modifyvm \"" + self.name + "\" --firmware=efi"))
        return os.system(("\"" + self.managerPath + "\" modifyvm \"" + self.name + "\" --firmware=bios"))

    def AutoInstall(self, iso: str):
        return os.system(("vboxmanage unattended install '" + self.name + "' '--iso=" + iso + "'"))
