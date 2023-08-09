/*
 * gfdgd xi
 * 依照 GPLV3 开源
 */
#include <sys/sysinfo.h>
#include "buildvbox.h"
#include "vbox.h"
#include <QFile>
#include <QDir>
#include <QNetworkInterface>
#include <QMessageBox>
#include <QCoreApplication>
#include <infoutils.h>
#include "qemu.h"
#include <QProcess>
// 懒得用 QThread 了（要继承）
#include <thread>
using namespace std;

// 清屏
void buildvbox::CleanScreen(){
    if(QFile::exists("/etc/os-version")){
        // Unix
        system("clear");
        return;
    }
    // Windows
    system("cls");
}

// 获取 CPU 个数
int buildvbox::GetCPUSocket(){
    // 获取命令返回值
    QProcess process;
    process.start("bash", QStringList() << "-c" << "cat /proc/cpuinfo | grep \"cpu cores\" | uniq | wc -l");
    process.waitForStarted();
    process.waitForFinished();
    int value = process.readAllStandardOutput().toInt();
    process.close();
    // 判断异常值，例如没挂载 /proc
    if(value <= 0){
        value = 1;
    }
    return value;
}

// 获取 CPU 核心数
int buildvbox::GetCPUCore(){
    QProcess process;
    process.start("bash", QStringList() << "-c" << "grep 'core id' /proc/cpuinfo | sort -u | wc -l");
    process.waitForStarted();
    process.waitForFinished();
    int value = process.readAllStandardOutput().toInt();
    process.close();
    // 判断异常值，例如没挂载 /proc
    if(value <= 0){
        value = 1;
    }
    return value;
}

QString buildvbox::GetNet(){
    QList<QNetworkInterface> netList = QNetworkInterface::allInterfaces();
    foreach(QNetworkInterface net, netList){
        qDebug() << "Device:" << net.name();
        QList<QNetworkAddressEntry> entryList = net.addressEntries();
        foreach(QNetworkAddressEntry entry, entryList){
            QString ip = entry.ip().toString();
            qDebug() << "IP Address: " << ip;
            if(ip != "127.0.0.1" && ip != "192.168.250.1" && ip != "::1" && net.name() != "lo"){
                // 返回网卡名称
                return net.name();
            }
        }
    }
    return "";
}

int buildvbox::Download(QString url, QString path, QString fileName){
    return system(("aria2c -x 16 -s 16 -c " + url + " -d " + path + " -o " + fileName).toUtf8());
}

buildvbox::buildvbox(QString isoPath, int id, int vm){
    /*if(vm == 1){
        QDir vboxPath(QDir::homePath() + "/VirtualBox VMs/Windows");
        if(vboxPath.exists()){
            qDebug("虚拟机存在，直接启动！");
            vbox vm("Windows");
            vm.Start();
            return;
         }
    }*/
    QString programPath = QCoreApplication::applicationDirPath();

    /*if(!QFile::exists(programPath + "/a.iso")){
        std::thread([=](){
            while(1){
                qDebug() << "a";
            }
        }).detach();
    }*/

    QString net = GetNet();
    qDebug() << "使用网卡：" << net << endl;
    if(vm == 0){
        //vbox *box = new vbox("Window");
        //vbox vm("Windows");
        qemu vm("Windows");

        switch (id) {
            case 0:
                vm.Create("Windows7");
                break;
            case 1:
                vm.Create("Windows7_64");
                break;
            case 2:
                vm.Create("WindowsNT_64");
                break;
            case 3:
                vm.Create("WindowsNT_64");
                vm.EnabledUEFI(true);
                break;
        }
        vm.CreateDiskControl();
        //vm.CreateDiskControl("storage_controller_2");
        vm.CreateDisk(QDir::homePath() + "/Qemu/Windows/Windows.qcow2", 131072);
        vm.MountDisk(QDir::homePath() + "/Qemu/Windows/Windows.qcow2");
        vm.MountISO(isoPath, "storage_controller_1", 0, 1);
        switch (id) {
            case 0:
                vm.MountISO(programPath + "/Windows7X86Auto.iso", "storage_controller_1", 1, 2);
                break;
            case 1:
                vm.MountISO(programPath + "/Windows7X64Auto.iso", "storage_controller_1", 1, 2);
                break;
        }
        /*vm.MountISO(isoPath, "storage_controller_1", 0, 1);
        switch (id) {
            case 0:
                vm.MountISO(programPath + "/Windows7X86Auto.iso", "storage_controller_1", 1, 0);
                break;
            case 1:
                vm.MountISO(programPath + "/Windows7X64Auto.iso", "storage_controller_1", 1, 0);
                break;
        }*/
        // 判断 VirtualBox Guest ISO 是否存在
        // 在的话直接挂载
        /*if(QFile::exists("/usr/share/virtualbox/VBoxGuestAdditions.iso")){
            vm.MountISO("/usr/share/virtualbox/VBoxGuestAdditions.iso", "storage_controller_1", 1, 1);
        }*/

        vm.SetCPU(get_nprocs(), GetCPUSocket(), GetCPUCore());
        long memory = 0;
        long memoryAll = 0;
        long swap = 0;
        long swapAll = 0;
        infoUtils::memoryRate(memory, memoryAll, swap, swapAll);
        //memoryRate(memory, memoryAll, swap, swapAll);
        vm.SetMemory(memoryAll / 3 / 1024);
        vm.SetDisplayMemory(32);
        vm.SetNetBridge(net);
        vm.EnabledAudio();
        vm.EnabledClipboardMode();
        vm.EnabledDraganddrop();
        vm.SetVBoxSVGA();
        vm.SetMousePS2();
        vm.SetKeyboardPS2();
        vm.OpenUSB();
        vm.ShareFile("ROOT", "/");
        vm.ShareFile("HOME", QDir::homePath());
        vm.Start();
    }
    else if(vm == 1){
        // ?
        //vbox *box = new vbox("Window");
        vbox vm("Windows");
        //qemu vm("Windows");

        switch (id) {
            case 0:
                vm.Create("Windows7");
                break;
            case 1:
                vm.Create("Windows7_64");
                break;
            case 2:
                vm.Create("WindowsNT_64");
                break;
            case 3:
                vm.Create("WindowsNT_64");
                vm.EnabledUEFI(true);
                break;
        }
        QDir dir("/home/gfdgd_xi/Qemu/Windows/");
        dir.mkpath("/home/gfdgd_xi/Qemu/Windows/");
        vm.CreateDiskControl();
        //vm.CreateDiskControl("storage_controller_2");
        vm.CreateDisk(QDir::homePath() + "/VirtualBox VMs/Windows/Windows.vdi", 131072);
        vm.MountDisk(QDir::homePath() + "/VirtualBox VMs/Windows/Windows.vdi");
        vm.MountISO(isoPath, "storage_controller_1", 0, 1);
        switch (id) {
            case 0:
                vm.MountISO(programPath + "/Windows7X86Auto.iso", "storage_controller_1", 1, 0);
                break;
            case 1:
                vm.MountISO(programPath + "/Windows7X64Auto.iso", "storage_controller_1", 1, 0);
                break;
        }

        // 判断 VirtualBox Guest ISO 是否存在
        // 在的话直接挂载
        if(QFile::exists("/usr/share/virtualbox/VBoxGuestAdditions.iso")){
            vm.MountISO("/usr/share/virtualbox/VBoxGuestAdditions.iso", "storage_controller_1", 1, 1);
        }

        vm.SetCPU(get_nprocs(), GetCPUSocket(), GetCPUCore());
        long memory = 0;
        long memoryAll = 0;
        long swap = 0;
        long swapAll = 0;
        infoUtils::memoryRate(memory, memoryAll, swap, swapAll);
        //memoryRate(memory, memoryAll, swap, swapAll);
        vm.SetMemory(memoryAll / 3 / 1024);
        vm.SetDisplayMemory(32);
        vm.SetNetBridge(net);
        vm.EnabledAudio();
        vm.EnabledClipboardMode();
        vm.EnabledDraganddrop();
        vm.SetVBoxSVGA();
        vm.SetMousePS2();
        vm.SetKeyboardPS2();
        vm.OpenUSB();
        vm.ShareFile("ROOT", "/");
        vm.ShareFile("HOME", QDir::homePath());
        vm.Start();
    }

}
