#include "mainwindow.h"
#include <QApplication>
#include <QTranslator>
#include <QCoreApplication>
#include <QProcess>
#include <QMessageBox>

QString GetRunCommand(QString command){
    QProcess process;
    process.start(command);
    process.waitForStarted();
    process.waitForFinished();
    QString re = process.readAllStandardOutput();
    process.close();
    return re;
}

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    // 语言
    QTranslator *trans = new QTranslator(&a);
    trans->load("virtualmachine-en_US.qm");

    a.installTranslator(trans);
    // 判断是否为 !amd64
    if(GetRunCommand("arch").replace(" ", "").replace("\n", "") == QString("x86_64")){
        QMessageBox::critical(NULL, "错误", "此程序不支持非 X86 架构，立即退出");
        return 0;
    }
    MainWindow w;

    w.show();

    return a.exec();
}
