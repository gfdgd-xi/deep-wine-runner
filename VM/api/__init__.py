################################################
# 作者：gfdgd xi、为什么您不喜欢熊出没和阿布呢
# 版本：1.0
# 依照 GPL V3 协议开源
################################################
# 参考文献：
#     https://juejin.cn/post/7080484519328874510
################################################
import os
import subprocess

homePath = os.path.expanduser('~')
programPath = os.path.split(os.path.realpath(__file__))[0]

class File:
    def __init__(self, path) -> None:
        self.path = path

    def getFileFolderSize(self):
        """get size for file or folder"""
        totalSize = 0
        if not os.path.exists(self.path):
            return totalSize
        if os.path.isfile(self.path):
            totalSize = os.path.getsize(self.path)  # 5041481
            return totalSize
        if os.path.isdir(self.path):
            with os.scandir(self.path) as dirEntryList:
                for curSubEntry in dirEntryList:
                    curSubEntryFullPath = os.path.join(self.path, curSubEntry.name)
                    if curSubEntry.is_dir():
                        curSubFolderSize = self.path(curSubEntryFullPath)  # 5800007
                        totalSize += curSubFolderSize
                    elif curSubEntry.is_file():
                        curSubFileSize = os.path.getsize(curSubEntryFullPath)  # 1891
                        totalSize += curSubFileSize
                return totalSize

class Manager:
    def __init__(self, name: str, managerPath: str="VBoxManage") -> None:
        self.name = name
        self.managerPath = managerPath
        self.vboxVersion = subprocess.getoutput(f"\"{self.managerPath}\" -v")

    def Create(self, type: str="Windows7") -> None:
        os.system(f"\"{self.managerPath}\" createvm --name \"{self.name}\" --ostype \"{type}\" --register")

    def CreateDisk(self, path: str, size: int) -> None:
        os.system(f"\"{self.managerPath}\" createvdi --filename \"{path}\" --size \"{size}\"")

    def CreateDiskControl(self, controlName: str="storage_controller_1") -> None:
        os.system(f"\"{self.managerPath}\" storagectl \"{self.name}\" --name \"{controlName}\" --add ide")

    def MountDisk(self, diskPath: str, controlName: str="storage_controller_1", port: int=0, device: int=0) -> None:
        os.system(f"\"{self.managerPath}\" storageattach \"{self.name}\" --storagectl \"{controlName}\" --type hdd --port {port} --device {device} --medium \"{diskPath}\"")

    def MountISO(self, isoPath: str, controlName: str="storage_controller_1", port: int=1, device: int=0) -> None:
        os.system(f"\"{self.managerPath}\" storageattach \"{self.name}\" --storagectl \"{controlName}\" --type dvddrive --port {port} --device {device} --medium \"{isoPath}\"")

    def BootFirst(self, bootDrive: str) -> None:
        os.system(f"\"{self.managerPath}\" modifyvm \"{self.name}\" --boot1 {bootDrive}")

    def SetNetBridge(self, netDriver: str) -> None:
        os.system(f"\"{self.managerPath}\" modifyvm \"{self.name}\" --nic1 bridged --cableconnected1 on --nictype1 82540EM --bridgeadapter1 \"{netDriver}\" --intnet1 brigh1 --macaddress1 auto")
        #os.system(f"\"{self.managerPath}\" modifyvm \"{self.name}\" --nic1 hostif")
        pass

    def SetCPU(self, number: int) -> None:
        os.system(f"\"{self.managerPath}\" modifyvm \"{self.name}\" --cpus {number}")

    def SetMemory(self, memory: int) -> None:
        os.system(f"\"{self.managerPath}\" modifyvm \"{self.name}\" --memory {memory}")

    def SetRemote(self, setting: bool) -> None:
        if setting:
            os.system(f"\"{self.managerPath}\" modifyvm \"{self.name}\" --vrde on")
            return
        os.system(f"\"{self.managerPath}\" modifyvm \"{self.name}\" --vrde off")

    def SetRemoteConnectSetting(self, port: int=5540) -> None:
        os.system(f"\"{self.managerPath}\" modifyvm \"{self.name}\" --vrdeport {port} --vrdeaddress """)

    def Start(self, unShown: bool = False) -> None:
        if unShown:
            os.system(f"\"{self.managerPath}\" startvm \"{self.name}\" -type headless")
            return
        os.system(f"\"{self.managerPath}\" startvm \"{self.name}\"")

    def Stop(self) -> None:
        os.system(f"\"{self.managerPath}\" controlvm \"{self.name}\" poweroff")

    def Delete(self) -> None:
        os.system(f"\"{self.managerPath}\" unregistervm --delete \"{self.name}\"")
    
    def SetDisplayMemory(self, memory: int) -> None:
        os.system(f"\"{self.managerPath}\" modifyvm \"{self.name}\" --vram {memory}")

    def InstallGuessAdditions(self, controlName: str="storage_controller_1", port: int=1, device: int=0) -> None:
        self.MountISO("/usr/share/virtualbox/VBoxGuestAdditions.iso", controlName, port, device)

    def EnabledAudio(self) -> None:
        os.system(f"\"{self.managerPath}\" modifyvm \"{self.name}\" --audio pulse --audiocontroller hda --audioin on --audioout on")
        #os.system("")

    def EnabledClipboardMode(self):
        os.system(f"\"{self.managerPath}\" modifyvm \"{self.name}\" --clipboard-mode bidirectional")

    def EnabledDraganddrop(self):
        os.system(f"\"{self.managerPath}\" modifyvm \"{self.name}\" --draganddrop bidirectional")

    def ShareFile(self, name, path):
        os.system(f"\"{self.managerPath}\" sharedfolder add \"{self.name}\" -name \"{name}\" -hostpath \"{path}\"")