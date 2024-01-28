#ifndef INSTALLDEB_H
#define INSTALLDEB_H

#include <QObject>
#include <qtermwidget5/qtermwidget.h>
#include <DMainWindow>
DWIDGET_USE_NAMESPACE

class InstallDEB
{
public:
    InstallDEB(QTermWidget *terminal, DMainWindow *mainWindow = NULL);
    void AddCommand(QString command);
    void RunCommand(bool withRoot=false);
    QStringList commandList;
private:
    QTermWidget *terminal;
    DMainWindow *mainWindow = NULL;
    bool runStatus;
};

#endif // INSTALLDEB_H
