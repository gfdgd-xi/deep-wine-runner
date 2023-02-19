#include "buildvbox.h"
#include "vbox.h"
#include <QFile>
#include <QDir>
#include <QNetworkInterface>
#include <QMessageBox>
#include <QCoreApplication>
#include <infoutils.h>
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

buildvbox::buildvbox(QString isoPath, int id){
    /*QDir vboxPath(QDir::homePath() + "/VirtualBox VMs/Windows");
    if(vboxPath.exists()){
        qDebug("虚拟机存在，直接启动！");
        vbox vm("Windows");
        vm.Start();
        return;
    }*/
    QString programPath = QCoreApplication::applicationDirPath();
    QString net = GetNet();
    qDebug() << "使用网卡：" << net << endl;
    //vbox *box = new vbox("Window");
    vbox vm("Windows");
    switch (id) {
        case 0:
            vm.Create("Windows7");
            break;
        case 1:
            vm.Create("Windows7_64");
            break;
        vm.Create("WindowsNT_64");
    }
    vm.CreateDiskControl();
    vm.CreateDisk(QDir::homePath() + "/VirtualBox VMs/Windows/Windows.vdi", 131072);
    vm.MountDisk(QDir::homePath() + "/VirtualBox VMs/Windows/Windows.vdi");
    vm.MountISO(isoPath);
    switch (id) {
        case 0:
            vm.MountISO(programPath + "/Windows7X86Auto.iso", "storage_controller_1", 1);
            break;
        case 1:
            vm.MountISO(programPath + "/Windows7X64Auto.iso", "storage_controller_1", 1);
            break;
    }
    vm.SetCPU(1);
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
