#include "mainwindow.h"

#include <QLocale>
#include <QTranslator>
#include <DApplication>
#include <DMessageBox>
#include <iostream>
using namespace Dtk::Widget;
using namespace std;

int main(int argc, char *argv[])
{
    // 强制使用 DTK 平台插件
    QVector<char *> fakeArgs(argc + 2);
    fakeArgs[0] = argv[0];
    fakeArgs[1] = const_cast<char *>("-platformtheme");
    fakeArgs[2] = const_cast<char *>("deepin");
    for(int i = 1; i < argc; i++){
        fakeArgs[i + 2] = argv[i];
    }
    int fakeArgc = argc + 2;
    DApplication a(fakeArgc, fakeArgs.data());
    DApplication::setOrganizationName("gfdgd_xi");
    DApplication::setApplicationName("deepin-wine-runner-aptss-installer");

    if(system("which aptss")){
        DMessageBox::information(NULL, "错误", "无法检测到 aptss\n请确保您已安装星火应用商店并更新至最新版本");
        return 1;
    }

    QTranslator translator;
    const QStringList uiLanguages = QLocale::system().uiLanguages();
    for (const QString &locale : uiLanguages) {
        const QString baseName = "aptss-installer_" + QLocale(locale).name();
        if (translator.load(":/i18n/" + baseName)) {
            a.installTranslator(&translator);
            break;
        }
    }
    MainWindow w;
    w.show();
    return a.exec();
}
