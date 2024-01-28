#include "mainwindow.h"

#include <QLocale>
#include <QTranslator>
#include <DApplication>
#include <DMessageBox>
#include <iostream>
#include <DApplicationSettings>
DWIDGET_USE_NAMESPACE
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
    a.setApplicationLicense("GPLV3");
    a.setOrganizationName("gfdgd_xi");
    a.setApplicationName("deepin-wine-runner-aptss-installer");
    a.setWindowIcon(QIcon(":/Icon/deepin-wine-runner.svg"));
    a.setApplicationDescription("Wine运行器是一个能让Linux用户更加方便地运行Windows应用的程序。原版的 Wine 只能使用命令操作，且安装过程较为繁琐，对小白不友好。于是该运行器为了解决该痛点，内置了对Wine图形化的支持、Wine 安装器、微型应用商店、各种Wine工具、自制的Wine程序打包器、运行库安装工具等。");
    a.setApplicationVersion("3.6.1");
    a.setProductIcon(QIcon(":/Icon/deepin-wine-runner.svg"));
    a.setProductName("aptss 安装器");
    a.setApplicationHomePage("https://gitee.com/gfdgd-xi/deep-wine-runner");
    //DApplication::setApplicationHomePage("https://gitee.com/gfdgd-xi/deep-wine-runner");
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
    DApplicationSettings settings; // 定义 DApplicationSettings，自动保存主题设置
    MainWindow w;
    w.show();
    return a.exec();
}
