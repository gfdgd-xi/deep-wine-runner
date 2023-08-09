/*
 * gfdgd xi
 * 依照 GPLV3 开源
 */
#ifndef BUILDVBOX_H
#define BUILDVBOX_H
#include <QString>

class buildvbox
{
//    Q_OBJECT
public:
    buildvbox(QString isoPath, int id=0, int vm=0);
    void CleanScreen();
    QString GetNet();
    int Download(QString url, QString path, QString fileName);
    int GetCPUSocket();
    int GetCPUCore();
};

#endif // BUILDVBOX_H
