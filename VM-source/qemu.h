/*
 * gfdgd xi、为什么您不喜欢熊出没和阿布呢
 * 依照 GPLV3 开源
 */
#ifndef QEMU_H
#define QEMU_H
#include <QString>

class qemu
{
public:
    // 虚拟机信息
    QString name;
    QString managerPath;
    QString vboxVersion;
    qemu(QString name, QString managerPath="/usr/bin");
    int Create(QString type="Windows7");
    int CreateDisk(QString path, int size);
    int CreateDiskControl(QString controlName="storage_controller_1");
    int MountDisk(QString diskPath, QString controlName="storage_controller_1", int port=0, int device=0);
    int MountISO(QString isoPath, QString controlName="storage_controller_1", int port=1, int device=0);
    int BootFirst(QString bootDrive);
    int SetNetBridge(QString netDriver);
    int SetCPU(int number);
    int SetMemory(int memory);
    int SetRemote(bool setting);
    int SetRemoteConnectSetting(int port=5540);
    int Start(bool unShown=false);
    int Stop();
    int Delete();
    int SetDisplayMemory(int memory);
    int InstallGuessAdditions(QString controlName="storage_controller_1", int port=1, int device=0);
    int EnabledAudio();
    int EnabledClipboardMode();
    int EnabledDraganddrop();
    int ShareFile(QString name, QString path);
    int SetVBoxSVGA();
    int SetMousePS2();
    int SetKeyboardPS2();
    int OpenUSB();
private:
    QString commandOption;

};

#endif // QEMU_H
