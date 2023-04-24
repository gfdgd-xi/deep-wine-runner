/*
 * gfdgd xi
 */
#include "vbox.h"
#include "command.h"
#include <QMessageBox>

vbox::vbox(QString name, QString managerPath) {
    this->name = name;
    this->managerPath = managerPath;
    //Command command = Command();
    this->vboxVersion = Command().GetCommand("'" + managerPath + "' -v");
}

int vbox::Create(QString type){
    system(("\"" + managerPath + "\" createvm --name \""
                   + name + "\" --ostype \"" + type +
                   "\" --register").toLatin1());
    return system(("\"" + managerPath + "\" modifyvm \""
                   + name + "\" --ostype \"" + type +
                   "\" ").toLatin1());
    //vboxmanage modifyvm testvm --ostype
}
int vbox::CreateDisk(QString path, int size){
    return system(("\"" + managerPath + "\" createvdi --filename \"" + path + "\" --size \"" + QString::number(size) + "\"").toLatin1());
}
int vbox::CreateDiskControl(QString controlName){
    return system(("\"" + managerPath + "\" storagectl \"" + name + "\" --name \"" + controlName + "\" --add ide").toLatin1());
}
int vbox::MountDisk(QString diskPath, QString controlName, int port, int device){
    return system(("\"" + managerPath + "\" storageattach \"" + name +
                   "\" --storagectl \"" + controlName + "\" --type hdd --port "
                   + QString::number(port) + " --device " + QString::number(device) + " --medium \"" + diskPath + "\"").toLatin1());
}
int vbox::MountISO(QString isoPath, QString controlName, int port, int device){
    return system(("\"" + managerPath + "\" storageattach \"" + name + "\" --storagectl \"" +
                   controlName + "\" --type dvddrive --port " + QString::number(port) + " --device " + QString::number(device)
                   + " --medium \"" + isoPath + "\"").toLatin1());
}
int vbox::BootFirst(QString bootDrive){
    return system(("\"" + managerPath + "\" modifyvm \"" + name + "\" --boot1 " + bootDrive).toLatin1());
}
int vbox::SetNetBridge(QString netDriver){
    return system(("\"" + managerPath + "\" modifyvm \"" + name +
                   "\" --nic1 bridged --cableconnected1 on --nictype1 82540EM --bridgeadapter1 \"" + netDriver + "\" --intnet1 brigh1 --macaddress1 auto").toLatin1());
}
int vbox::SetCPU(int number){
    return system(("\"" + managerPath + "\" modifyvm \"" + name + "\" --cpus " + QString::number(number)).toLatin1());
}
int vbox::SetMemory(int memory){
    return system(("\"" + managerPath + "\" modifyvm \"" + name + "\" --memory " + QString::number(memory)).toLatin1());
}
int vbox::SetRemote(bool setting){
    if(setting){
        return system(("\"" + managerPath + "\" modifyvm \"" + name + "\" --vrde on").toLatin1());
    }
    return system(("\"" + managerPath + "\" modifyvm \"" + name + "\" --vrde off").toLatin1());
}
int vbox::SetRemoteConnectSetting(int port){
    return system(("\"" + managerPath + "\" modifyvm \"" + name + "\" --vrdeport " + QString::number(port) + " --vrdeaddress """).toLatin1());
}
int vbox::Start(bool unShown){
    if(unShown){
        return system(("\"" + managerPath + "\"").toLatin1());
    }
    return system(("\"" + managerPath + "\" startvm \"" + name + "\"").toLatin1());
}
int vbox::Stop(){
    return system(("\"" + managerPath + "\" controlvm \"" + name + "\" poweroff").toLatin1());
}
int vbox::Delete(){
    return system(("\"" + managerPath + "\" unregistervm --delete \"" + name + "\"").toLatin1());
}
int vbox::SetDisplayMemory(int memory){
    return system(("\"" + managerPath + "\" modifyvm \"" + name + "\" --vram " + QString::number(memory)).toLatin1());
}
int vbox::InstallGuessAdditions(QString controlName, int port, int device){
    return MountISO("/usr/share/virtualbox/VBoxGuestAdditions.iso", controlName, port, device);
}
int vbox::EnabledAudio(){
    return system(("\"" + managerPath + "\" modifyvm \"" + name + "\" --audio-driver pulse --audiocontroller hda --audioin on --audioout on").toLatin1());
}
int vbox::EnabledClipboardMode(){
    return system(("\"" + managerPath + "\" modifyvm \"" + name + "\" --clipboard-mode bidirectional").toLatin1());
}
int vbox::EnabledDraganddrop(){
    return system(("\"" + managerPath + "\" modifyvm \"" + name + "\" --draganddrop bidirectional").toLatin1());
}
int vbox::ShareFile(QString name, QString path){
    return system(("\"" + managerPath + "\" sharedfolder add \"" + this->name + "\" -name \"" + name + "\" -hostpath \"" + path + "\"").toLatin1());
}
int vbox::SetVBoxSVGA(){
    return system(("\"" + managerPath + "\" modifyvm \"" + name + "\" --graphicscontroller vboxsvga").toLatin1());
}
int vbox::SetMousePS2(){
    return system(("\"" + managerPath + "\" modifyvm \"" + name + "\" --mouse usb").toLatin1());
}
int vbox::SetKeyboardPS2(){
    return system(("\"" + managerPath + "\" modifyvm \"" + name + "\" --keyboard usb").toLatin1());
}
int vbox::OpenUSB(){
    return system(("\"" + managerPath + "\" modifyvm \"" + name + "\" --usbohci on").toLatin1());
}
