#include "vbox.h"
#include "command.h"

vbox::vbox(QString name, QString managerPath) {
    this->name = name;
    this->managerPath = managerPath;
    Command command = Command();
    this->vboxVersion = Command().GetCommand("'" + managerPath + "' -v");
}

int vbox::Create(QString type){
    return system(("\"" + managerPath + "\" createvm --name \""
                   + name + "\" --ostype \"" + type +
                   "\" --register").toUtf8());
}
int vbox::CreateDisk(QString path, int size){
    return system(("\"" + managerPath + "\" createvdi --filename \"" + path + "\" --size \"" + size + "\"").toUtf8());
}
int vbox::CreateDiskControl(QString controlName){
    return system(("\"" + managerPath + "\" storagectl \"" + name + "\" --name \"" + controlName + "\" --add ide").toUtf8());
}
int vbox::MountDisk(QString diskPath, QString controlName, int port, int device){
    return system(("\"" + managerPath + "\" storageattach \"" + name +
                   "\" --storagectl \"" + controlName + "\" --type hdd --port "
                   + port + " --device " + device + " --medium \"" + diskPath + "\"").toUtf8());
}
int vbox::MountISO(QString isoPath, QString controlName, int port, int device){
    return system(("\"" + managerPath + "\" storageattach \"" + name + "\" --storagectl \"" +
                   controlName + "\" --type dvddrive --port " + port + " --device " + device
                   + " --medium \"{isoPath}\"").toUtf8());
}
int vbox::BootFirst(QString bootDrive){
    return system(("\"" + managerPath + "\" modifyvm \"" + name + "\" --boot1 " + bootDrive).toUtf8());
}
int vbox::SetNetBridge(QString netDriver){
    return system(("\"" + managerPath + "\" modifyvm \"" + name +
                   "\" --nic1 bridged --cableconnected1 on --nictype1 82540EM --bridgeadapter1 \"" + netDriver + "\" --intnet1 brigh1 --macaddress1 auto").toUtf8());
}
int vbox::SetCPU(int number){
    return system(("\"" + managerPath + "\" modifyvm \"" + name + "\" --cpus " + number).toUtf8());
}
int vbox::SetMemory(int memory){
    return system(("\"" + managerPath + "\" modifyvm \"" + name + "\" --memory " + memory).toUtf8());
}
int vbox::SetRemote(bool setting){
    if(setting){
        return system(("\"" + managerPath + "\" modifyvm \"" + name + "\" --vrde on").toUtf8());
    }
    return system(("\"" + managerPath + "\" modifyvm \"" + name + "\" --vrde off").toUtf8());
}
int vbox::SetRemoteConnectSetting(int port){
    return system(("\"" + managerPath + "\" modifyvm \"" + name + "\" --vrdeport " + port + " --vrdeaddress """).toUtf8());
}
int vbox::Start(bool unShown){
    if(unShown){
        return system(("\"" + managerPath + "\"").toUtf8());
    }
    return system(("\"" + managerPath + "\" startvm \"" + name + "\"").toUtf8());
}
int vbox::Stop(){
    return system(("\"" + managerPath + "\" controlvm \"" + name + "\" poweroff").toUtf8());
}
int vbox::Delete(){
    return system(("\"" + managerPath + "\" unregistervm --delete \"" + name + "\"").toUtf8());
}
int vbox::SetDisplayMemory(int memory){
    return system(("\"" + managerPath + "\" modifyvm \"" + name + "\" --vram " + memory).toUtf8());
}
int vbox::InstallGuessAdditions(QString controlName, int port, int device){
    return MountISO("/usr/share/virtualbox/VBoxGuestAdditions.iso", controlName, port, device);
}
int vbox::EnabledAudio(){
    return system(("\"" + managerPath + "\" modifyvm \"" + name + "\" --audio pulse --audiocontroller hda --audioin on --audioout on").toUtf8());
}
int vbox::EnabledClipboardMode(){
    return system(("\"" + managerPath + "\" modifyvm \"" + name + "\" --clipboard-mode bidirectional").toUtf8());
}
int vbox::EnabledDraganddrop(){
    return system(("\"" + managerPath + "\" modifyvm \"" + name + "\" --draganddrop bidirectional").toUtf8());
}
int vbox::ShareFile(QString name, QString path){
    return system(("\"" + managerPath + "\" sharedfolder add \"" + this->name + "\" -name \"" + name + "\" -hostpath \"" + path + "\"").toUtf8());
}
int vbox::SetVBoxSVGA(){
    return system(("\"" + managerPath + "\" modifyvm \"" + name + "\" --graphicscontroller vboxsvga").toUtf8());
}
int vbox::SetMousePS2(){
    return system(("\"" + managerPath + "\" modifyvm \"" + name + "\" --mouse usb").toUtf8());
}
int vbox::SetKeyboardPS2(){
    return system(("\"" + managerPath + "\" modifyvm \"" + name + "\" --keyboard usb").toUtf8());
}
int vbox::OpenUSB(){
    return system(("\"" + managerPath + "\" modifyvm \"" + name + "\" --usbohci on").toUtf8());
}
