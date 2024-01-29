#include "installdeb.h"
#include "messagebox.h"
#include <QDateTime>
#include <QObject>
#include <QMessageBox>
#include <QMainWindow>

InstallDEB::InstallDEB(QTermWidget *terminal, DMainWindow *mainWindow)
{
    this->terminal = terminal;
    this->mainWindow = mainWindow;
}

void InstallDEB::AddCommand(QString command){
    this->commandList.append(command);
}

void InstallDEB::SetCommandAfterRootRun(QString command){
    commandAfterRootRun = command;
}

void InstallDEB::RunCommand(bool withRoot){
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
    if(withRoot){
        QString bashMainPath = "/tmp/deepin-wine-runner-aptss-installer-root-" + QString::number(QDateTime::currentMSecsSinceEpoch()) + ".sh";
        QString commandCode = "#!/bin/bash\n"\
                              "pkexec env DISPLAY=$DISPLAY bash '" + bashPath + "'\n" +
                              this->commandAfterRootRun +
                              "\nrm -rfv '" + bashMainPath + "'\n"
                              "rm -rfv '" + bashPath + "'";

        QFile file(bashMainPath);
        file.open(QFile::WriteOnly);
        if(!file.isWritable()){
            throw "Can't write the file!";
        }
        file.write(commandCode.toUtf8());
        file.close();
        system(("chmod +x '" + bashMainPath + "'").toUtf8()); // 赋予运行权限
        this->terminal->setShellProgram("/usr/bin/bash");
        this->terminal->setArgs(QStringList() << bashMainPath);
    }
    else{
        this->terminal->setShellProgram("/usr/bin/bash");
        this->terminal->setArgs(QStringList() << bashPath);
    }
    //this->terminal->setAutoClose(1);
    //this->terminal->setAutoFillBackground(1);
    /*QObject::connect(this->terminal, &QTermWidget::finished, this->mainWindow, [this](){
        MessageBox *message = new MessageBox();
        message->information("提示", "应用安装完成");
        this->mainWindow->sendMessage(QIcon(":/Icon/MessageBox/dialog-information.svg"), "应用安装完成");
    });*/
    this->terminal->startShellProgram();

}
