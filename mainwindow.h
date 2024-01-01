#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMap>
#include <QDir>
#include <QCoreApplication>

class MainWindow
{

public:
    MainWindow();
    ~MainWindow();
    void CheckWine();
    QString get_home();

private:
    QString homePath = QDir::homePath();
    QString programPath = QCoreApplication::applicationDirPath();
    QMap<QString, QString> wine;
    QStringList untipsWine = {"使用 Flatpak 安装的 Wine", "基于 exagear 的 deepin-wine6-stable", "基于 UOS box86 的 deepin-wine6-stable", "基于 UOS exagear 的 deepin-wine6-stable", "基于 linglong 的 deepin-wine6-stable（不推荐）"};
    QStringList canUseWine = {};


};
#endif // MAINWINDOW_H
