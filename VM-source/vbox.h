#ifndef VBOX_H
#define VBOX_H
#include <QString>

class vbox
{
public:
    vbox(QString name, QString managerPath="VBoxManage");
private:
    // 虚拟机信息
    QString name;
    QString managerPath;
    QString vboxVersion;
};

#endif // VBOX_H
