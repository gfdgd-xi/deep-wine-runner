#include "buildvbox.h"
#include <QFile>
#include <QNetworkInterface>
#include <QMessageBox>
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
            if(ip != "127.0.0.1" && ip != "192.168.250.1"){
                // 返回网卡名称
                return net.name();
            }
        }
    }
    return "";
}

buildvbox::buildvbox()
{
    QString net = GetNet();
    qDebug() << "使用网卡：" << net << endl;

}
