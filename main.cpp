#include "mainwindow.h"

#include <QLocale>
#include <QTranslator>
#include <DApplication>
using namespace Dtk::Widget;

int main(int argc, char *argv[])
{
    DApplication a(argc, argv);

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
