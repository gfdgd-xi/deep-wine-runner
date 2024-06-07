/*
 * gfdgd xi
 */
#include "qemu.h"
#include <QDir>
#include <QFile>
#include <QCoreApplication>
#include "command.h"
#include <QMessageBox>
#include <QProcess>
#include <QDebug>
#include <iostream>
using namespace std;

qemu::qemu(QString name, QString managerPath)
{
    if(!QFile::exists(name)){
        this->name = QDir::homePath() + "/Qemu/" + name;
    }
    else{
        this->name = name;
    }
    this->managerPath = managerPath;
    //Command command = Command();

    this->vboxVersion = Command().GetCommand("'" + managerPath + "qemu-system-i386' --version");
}

int qemu::Create(QString type)
{
    if(!QFile::exists(this->name)){
        QDir dir(this->name);
        dir.mkpath(this->name);
    }
    return 0;
}

int qemu::CreateDisk(QString path, int size)
{
    if(QFile::exists(path)){
        return 0;
    }
    return system(("qemu-img create -f qcow2 '" + path + "' " + QString::number(size) + "M").toLatin1());
}

int qemu::CreateDiskControl(QString controlName)
{
    return 0;
}

int qemu::MountDisk(QString diskPath, QString controlName, int port, int device)
{
    commandOption += "-drive 'file=" + diskPath + ",if=ide,index=" + QString::number(device) + "' ";
    return 0;
}

int qemu::MountISO(QString isoPath, QString controlName, int port, int device)
{
    commandOption += "-drive 'media=cdrom,file=" + isoPath + ",if=ide,index=" + QString::number(device) + "' ";
    return 0;
}

int qemu::BootFirst(QString bootDrive)
{
    commandOption += "-boot '" + bootDrive + "' ";
    return 0;
}

int qemu::SetNetBridge(QString netDriver)
{
    return 0;
}

int qemu::SetCPU(int number, int cpuNum, int coreNum)
{
    // commandOption += "-smp " + QString::number(number) + " ";
    // 调整调用方法
    //qDebug() << number << " " << cpuNum << " " << coreNum;
    qDebug() << "Socket: " << cpuNum;
    qDebug() << "Core: " << coreNum;
    qDebug() << "Threads: " << number;
    commandOption += "-smp " + QString::number(number) + ",sockets=" + QString::number(cpuNum) + ",cores=" + QString::number(coreNum / cpuNum) + ",threads=" + QString::number(number / cpuNum / coreNum) + " ";
    return 0;
}

int qemu::SetMemory(int memory)
{
    commandOption += "-m " + QString::number(memory) + "M ";
    return 0;
}

int qemu::SetRemote(bool setting)
{
    return 0;
}

int qemu::SetRemoteConnectSetting(int port)
{
    return 0;
}

int qemu::MountMainDisk(QString diskPath)
{
    commandOption += " --hda '" + diskPath + "' ";
    return 0;
}

int qemu::StartArmhf()
{
    qDebug() << commandOption;
    if(Command().GetCommand("arch").replace("\n", "").replace(" ", "") == "aarch64" && !system((QCoreApplication::applicationDirPath() + "/kvm-ok").toUtf8())){
        return system(("qemu-system-arm --boot 'splash=" + GetBootLogoPath() + ",order=d,menu=on,splash-time=2000' -display vnc=:5 -display gtk --enable-kvm -cpu host -M virt " + commandOption + " -device virtio-gpu-pci -device nec-usb-xhci,id=xhci,addr=0x1b -device usb-tablet,id=tablet,bus=xhci.0,port=1 -device usb-kbd,id=keyboard,bus=xhci.0,port=2 > /tmp/windows-virtual-machine-installer-for-wine-runner-install.log 2>&1 &").toLatin1());
    }
    return system(("qemu-system-arm --boot 'splash=" + GetBootLogoPath() + ",order=d,menu=on,splash-time=2000'  -display vnc=:5 -display gtk -cpu max -M virt " + commandOption + " -device virtio-gpu-pci -device nec-usb-xhci,id=xhci,addr=0x1b -device usb-tablet,id=tablet,bus=xhci.0,port=1 -device usb-kbd,id=keyboard,bus=xhci.0,port=2 > /tmp/windows-virtual-machine-installer-for-wine-runner-install.log 2>&1 &").toLatin1());
}

int qemu::StartAarch64()
{
    QString bootScreenLogo = "";
    // 判断 boot 文件是否存在
    if(QFile::exists(QCoreApplication::applicationDirPath() + "/boot.jpg")) {
        bootScreenLogo = QCoreApplication::applicationDirPath() + "/boot.jpg";
    }
    else {
        // 写入 logo
        QFile::copy(":/boot.jpg", "/tmp/deep-wine-runner-boot.jpg");
        bootScreenLogo = "/tmp/deep-wine-runner-boot.jpg";
    }
    qDebug() << commandOption;
    if(Command().GetCommand("arch").replace("\n", "").replace(" ", "") == "aarch64" && !system((QCoreApplication::applicationDirPath() + "/kvm-ok").toUtf8())){
        return system(("qemu-system-aarch64 --boot 'splash=" + GetBootLogoPath() + ",order=d,menu=on,splash-time=2000' -display vnc=:5 -display gtk --enable-kvm -cpu host -M virt " + commandOption + " -device virtio-gpu-pci -device nec-usb-xhci,id=xhci,addr=0x1b -device usb-tablet,id=tablet,bus=xhci.0,port=1 -device usb-kbd,id=keyboard,bus=xhci.0,port=2 > /tmp/windows-virtual-machine-installer-for-wine-runner-install.log 2>&1 &").toLatin1());
    }
    return system(("qemu-system-aarch64 --boot 'splash=" + GetBootLogoPath() + ",order=d,menu=on,splash-time=2000'  -display vnc=:5 -display gtk -cpu max -M virt " + commandOption + " -device virtio-gpu-pci -device nec-usb-xhci,id=xhci,addr=0x1b -device usb-tablet,id=tablet,bus=xhci.0,port=1 -device usb-kbd,id=keyboard,bus=xhci.0,port=2 > /tmp/windows-virtual-machine-installer-for-wine-runner-install.log 2>&1 &").toLatin1());
}

int qemu::StartLoong64()
{
    return 1;
}

int qemu::Start(bool unShown)
{
    QString newCommandOption = commandOption;
    QString qemuPath = "qemu-system-x86_64";
    qDebug() << GetBootLogoPath();
    if(isUEFI) {
        newCommandOption += " -vga none -device virtio-gpu-pci -device nec-usb-xhci,id=xhci,addr=0x1b -device usb-tablet,id=tablet,bus=xhci.0,port=1 -device usb-kbd,id=keyboard,bus=xhci.0,port=2 ";
    }
    else {
        newCommandOption += " -vga virtio -device nec-usb-xhci,id=xhci,addr=0x1b -device usb-tablet,id=tablet,bus=xhci.0,port=1 ";
    }
    // UOS 3a4000 使用程序自带的 qemu
    QString info = SystemInfo().toLower();
    if(info.contains("uos") || info.contains("unio")) {
        // 判断架构
        QString arch = GetArch();
        if(arch == "mips64" || arch == "mipsel64") {
            qemuPath = "bwrap --dev-bind / / --bind '" + QCoreApplication::applicationDirPath() + "/MipsQemu/usr/lib/mips64el-linux-gnuabi64/qemu/ui-gtk.so' /usr/lib/mips64el-linux-gnuabi64/qemu/ui-gtk.so '" + QCoreApplication::applicationDirPath() + "/MipsQemu/usr/bin/qemu-system-x86_64' ";
        }
    }
    qDebug() << commandOption;
    if(Command().GetCommand("arch").replace("\n", "").replace(" ", "") == "x86_64" && !system((QCoreApplication::applicationDirPath() + "/kvm-ok").toUtf8())){
        return system((qemuPath + " --boot 'splash=" + GetBootLogoPath() + ",order=d,menu=on,splash-time=2000' -display vnc=:5 -display gtk --enable-kvm -cpu host " + newCommandOption + " > /tmp/windows-virtual-machine-installer-for-wine-runner-install.log 2>&1 &").toLatin1());
    }
    return system((qemuPath + " --boot 'splash=" + GetBootLogoPath() + ",order=d,menu=on,splash-time=2000' -display vnc=:5 -display gtk -nic model=rtl8139 " + newCommandOption + " > /tmp/windows-virtual-machine-installer-for-wine-runner-install.log 2>&1 &").toLatin1());
}
int qemu::Stop()
{
    system("killall qemu-system-x86_64 -9");
    system("killall qemu-system-aarch64 -9");
    system("killall qemu-system-arm -9");
    system("killall kvm -9");
    return 0;
}

int qemu::Delete()
{
    return system(("rm -rfv '" + name + "'").toLatin1());
}

int qemu::SetDisplayMemory(int memory)
{
    return 0;
}

int qemu::InstallGuessAdditions(QString controlName, int port, int device)
{
    return 0;
}

int qemu::EnabledAudio()
{
    commandOption += "-device AC97 -device ES1370 -device intel-hda -device hda-duplex ";
    return 0;
}

int qemu::EnabledClipboardMode()
{
    return 0;
}

int qemu::EnabledDraganddrop()
{
    return 0;
}

int qemu::ShareFile(QString name, QString path)
{
    return 0;
}

int qemu::SetVBoxSVGA()
{
    return 0;
}

int qemu::SetMousePS2()
{
    return 0;
}

int qemu::SetKeyboardPS2()
{
    return 0;
}

int qemu::OpenUSB()
{
    return 0;
}

int qemu::UseAarch64EFI()
{
    if(QFile::exists("/usr/share/qemu-efi-aarch64/QEMU_EFI.fd")){
        commandOption += "--bios /usr/share/qemu-efi-aarch64/QEMU_EFI.fd ";
        return 0;
    }
    if(QFile::exists(QCoreApplication::applicationDirPath() + "/QEMU_AARCH64_EFI.fd")){
            commandOption += "--bios '" + QCoreApplication::applicationDirPath() + "/QEMU_AARCH64_EFI.fd' ";
            return 0;
    }
    return 1;
}

int qemu::UseArmhfEFI()
{
    if(QFile::exists("/usr/share/AAVMF/AAVMF32_CODE.fd")){
        commandOption += "--bios /usr/share/AAVMF/AAVMF32_CODE.fd ";
        return 0;
    }
    if(QFile::exists(QCoreApplication::applicationDirPath() + "/AAVMF32_CODE.fd")){
            commandOption += "--bios '" + QCoreApplication::applicationDirPath() + "/AAVMF32_CODE.fd' ";
            return 0;
    }
    return 1;
}

int qemu::UseLoongarch64EFI()
{

}

int qemu::UseOtherEFI(QString fdFilePath)
{

}

int qemu::EnabledUEFI(bool status)
{
    isUEFI = status;
    if(!status){
        return 0;
    }
    if(QFile::exists("/usr/share/qemu/OVMF.fd")){
        commandOption += "--bios /usr/share/qemu/OVMF.fd ";
        return 0;
    }
    if(QFile::exists(QCoreApplication::applicationDirPath() + "/OVMF.fd")){
        commandOption += "--bios '" + QCoreApplication::applicationDirPath() + "/OVMF.fd' ";
        return 0;
    }
    return 1;
}

int qemu::MountMainISO(QString isoPath)
{
    commandOption += "--cdrom '" + isoPath + "' ";
    return 0;
}

int qemu::AutoInstall(QString iso)
{
    return 0;
}

int qemu::AddDiskSpace(QString path, double data)
{
    return system(("qemu-img resize '" + path + "' +" + QString::number(data) + "G").toUtf8());
}

QString qemu::GetBootLogoPath()
{
    QString bootScreenLogo = "";
    // 判断 boot 文件是否存在
    if(QFile::exists(QCoreApplication::applicationDirPath() + "/boot.jpg")) {
        bootScreenLogo = QCoreApplication::applicationDirPath() + "/boot.jpg";
    }
    else {
        // 写入 logo
        if(QFile::exists("/tmp/deep-wine-runner-boot.jpg")) {
            QFile::remove("/tmp/deep-wine-runner-boot.jpg");
        }
        QFile::copy(":/boot.jpg", "/tmp/deep-wine-runner-boot.jpg");
        bootScreenLogo = "/tmp/deep-wine-runner-boot.jpg";
    }
    return bootScreenLogo;
}

QString qemu::SystemInfo()
{
    QFile file("/etc/os-version");
    file.open(QFile::ReadOnly);
    QString data = file.readAll();
    file.close();
    return data;
}

QString qemu::GetArch()
{
    QProcess process;
    process.start("uname", QStringList() << "-m");
    process.waitForStarted();
    process.waitForFinished();
    QString data = process.readAllStandardOutput();
    process.close();
    return data.replace("\n", "").replace(" ", "");
}
