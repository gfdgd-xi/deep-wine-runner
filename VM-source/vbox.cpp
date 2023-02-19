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
    //return os.system(f"\"{self.managerPath}\" modifyvm \"{self.name}\" --boot1 {bootDrive}")
}
int vbox::SetNetBridge(QString netDriver){

}
int vbox::SetCPU(int number){

}
int vbox::SetMemory(int memory){

}
int vbox::SetRemote(bool setting){

}
int vbox::SetRemoteConnectSetting(int port){

}
void vbox::Start(bool unShown){

}
int vbox::Stop(){

}
int vbox::Delete(){

}
int vbox::SetDisplayMemory(int memory){

}
int vbox::InstallGuessAdditions(QString controlName, int port, int device){

}
int vbox::EnabledAudio(){

}
int vbox::EnabledClipboardMode(){

}
int vbox::EnabledDraganddrop(){

}
int vbox::ShareFile(QString name, QString path){

}
int vbox::SetVBoxSVGA(){

}
int vbox::SetMousePS2(){

}
int vbox::SetKeyboardPS2(){

}
int vbox::OpenUSB(){

}
