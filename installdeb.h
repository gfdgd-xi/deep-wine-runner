#ifndef INSTALLDEB_H
#define INSTALLDEB_H

#include <QObject>
#include <qtermwidget5/qtermwidget.h>
#include <QMainWindow>

class InstallDEB
{
public:
    InstallDEB(QTermWidget *terminal, QMainWindow *mainWindow = NULL);
    void AddCommand(QString command);
    void RunCommand();
    QStringList commandList;
private:
    QTermWidget *terminal;
    QMainWindow *mainWindow = NULL;
    bool runStatus;
};

#endif // INSTALLDEB_H
