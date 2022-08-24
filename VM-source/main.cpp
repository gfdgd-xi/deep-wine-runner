#include "mainwindow.h"
#include <QApplication>
#include <QTranslator>
#include <QCoreApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    // 语言
    QTranslator *trans = new QTranslator(&a);
    trans->load("virtualmachine-en_US.qm");

    a.installTranslator(trans);
    MainWindow w;

    w.show();

    return a.exec();
}
