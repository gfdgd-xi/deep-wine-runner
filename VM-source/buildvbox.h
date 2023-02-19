#ifndef BUILDVBOX_H
#define BUILDVBOX_H
#include <QString>

class buildvbox
{
//    Q_OBJECT
public:
    buildvbox(QString isoPath, int id=0);
    void CleanScreen();
    QString GetNet();
};

#endif // BUILDVBOX_H
