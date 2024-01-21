#include "installdeb.h"
#include <QDateTime>
#include <QObject>
#include <QMessageBox>
#include <QMainWindow>

InstallDEB::InstallDEB(QTermWidget *terminal, QMainWindow *mainWindow)
{
    this->terminal = terminal;
    this->mainWindow = mainWindow;
}

void InstallDEB::AddCommand(QString command){
    this->commandList.append(command);
}

void InstallDEB::RunCommand(){
    this->terminal->setEnabled(true);
    this->runStatus = true;
    // 写入为 Bash 文件，方便执行
    QString commandCode = "#!/bin/bash\n";
    QString bashPath = "/tmp/deepin-wine-runner-aptss-installer-" + QString::number(QDateTime::currentMSecsSinceEpoch()) + ".sh";
    for(int i = 0; i < this->commandList.size(); i++){
        commandCode += this->commandList.at(i) + "\n";
    }
    commandCode += "rm -rfv '" + bashPath + "'";
    QFile file(bashPath);
    file.open(QFile::WriteOnly);
    if(!file.isWritable()){
        throw "Can't write the file!";
    }
    file.write(commandCode.toUtf8());
    file.close();
    system(("chmod +x '" + bashPath + "'").toUtf8()); // 赋予运行权限
    this->terminal->setColorScheme("DarkPastels");
    this->terminal->setShellProgram("/usr/bin/bash");
    this->terminal->setArgs(QStringList() << bashPath);
    //this->terminal->setAutoClose(1);
    this->terminal->setAutoFillBackground(1);
    this->terminal->startShellProgram();
    QObject::connect(this->terminal, &QTermWidget::finished, this->mainWindow, [this](){
        QMessageBox::information(this->mainWindow, "A", "B");
    });
}
