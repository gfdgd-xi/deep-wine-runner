/*
 * gfdgd xi
 * 依照 GPLV3 开源
 */
#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "buildvbox.h"
#include <QFileDialog>
#include <QDebug>
#include <QNetworkInterface>
#include <QProcess>
#include <QLoggingCategory>
#include <infoutils.h>
#include <QMessageBox>
#include <QTimer>
#include <QJsonParseError>
#include <QJsonValue>
#include <QJsonObject>
#include <QtMath>
#include <QJsonArray>
#include <QDesktopServices>
#include <QMessageBox>
#include <iostream>
#include "qemusetting.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    ui->tabWidget->setTabPosition(QTabWidget::West);  // 标签靠左
    // 选择最优虚拟机
    if(!system("which qemu-system-x86_64")){
        ui->vmChooser->setCurrentIndex(0);
    }
    if(!system("which vboxmanage")){
        ui->vmChooser->setCurrentIndex(1);
    }
    if(!QFile::exists(QCoreApplication::applicationDirPath() + "/../RunCommandWithTerminal.py")){
        ui->getQemu->setDisabled(true);
    }
    // 允许输出 qDebug 信息
    QLoggingCategory::defaultCategory()->setEnabled(QtDebugMsg, true);
    // 判断是否安装 vbox（无需判断）
    /*if(system("which VBoxManage")){
        if(QMessageBox::question(this, "提示", "检测到您似乎没有安装 VirtualBox，立即安装？") == QMessageBox::Yes){
            system("xdg-open https://www.virtualbox.org/wiki/Linux_Downloads");
        }
    }*/
    // QTimer
    QTimer *cpuGet = new QTimer(this);
    connect(cpuGet, &QTimer::timeout, this, &MainWindow::ShowCPUMessage);
    cpuGet->setInterval(1000);
    cpuGet->start();
    MainWindow::ShowCPUMessage();
    // 读取程序版本号
    // / 版本号文件是否存在
    QFile fileinfo(QCoreApplication::applicationDirPath() + "/../information.json");
    if(!fileinfo.exists()){
        fileinfo.close();
        return;
    }
    fileinfo.open(QIODevice::ReadOnly);
    QJsonParseError error;
    QJsonDocument doc = QJsonDocument::fromJson(fileinfo.readAll(), &error);
    if(error.error != QJsonParseError::NoError){
        QMessageBox::critical(this, "错误", "无法读取版本号！");
        qDebug() << error.errorString();
        fileinfo.close();
        return;
    }
    QJsonObject versionObject = doc.object();
    QJsonValue buildTime = versionObject.value("Time");
    QJsonValue versionValue = versionObject.value("Version");
    QJsonArray thank = versionObject.value("Thank").toArray();
    QString thankText = "";
    for (int i = 0; thank.count() > i; i++) {
        thankText += "<p>" + thank.at(i).toString() + "</p>\n";
        qDebug() << thank.at(i).toString();

    }
    // 设置程序标题
    this->setWindowTitle("Windows 应用适配工具 " + versionValue.toString());
    // 读取谢明列表
    ui->textBrowser_2->setHtml("<p>程序版本号：" + versionValue.toString() + ", " + GetRunCommand("arch") + "</p><p>安装包构建时间：" + buildTime.toString() + "</p><p>该组件构建时间："
                               + __DATE__ + " " + __TIME__ + "</p>" + ui->textBrowser_2->toHtml() +
                               "<hr/><h1>谢明列表</h1>" + thankText);
    connect(ui->textBrowser_2, &QTextBrowser::anchorClicked, this, [=](const QUrl &link){
        QDesktopServices::openUrl(link);
    });
    connect(ui->textBrowser, &QTextBrowser::anchorClicked, this, [=](const QUrl &link){
        QDesktopServices::openUrl(link);
    });
    connect(ui->textBrowser_3, &QTextBrowser::anchorClicked, this, [=](const QUrl &link){
        QDesktopServices::openUrl(link);
    });

}

void MainWindow::ShowCPUMessage(){
    // 获取 CPU 占用率
    long cpuAll = 0;
    long cpuFree = 0;
    infoUtils::cpuRate(cpuAll, cpuFree);
    long cpu = ((cpuAll - m_cpuAll) - (cpuFree - m_cpuFree)) * 100 / (cpuAll - m_cpuAll);
    if(cpu > 100){
        // 处理异常值
        cpu = 100;
    }
    // 获取内存占用率
    long memory = 0;
    long memoryAll = 0;
    long swap = 0;
    long swapAll = 0;

    infoUtils::memoryRate(memory, memoryAll, swap, swapAll);

    // 获取开机时间
    double run,idle;
    infoUtils::uptime(run,idle);
    int time = qFloor(run);
    int ss = time % 60;
    int MM = (time % 3600) / 60;
    int hh = (time % 86400) / 3600;
    int dd = time / 86400;


    QString info = "CPU: " + QString::number(cpu) + "%  内存: " +
            QString::number(memory * 100 / memoryAll) + "% " + QString::number(memory / 1024) + "MB/" + QString::number(memoryAll / 1024) + "MB" +
            " 开机时间: " + QString::number(dd) + "天 " + QString::number(hh) + ":" + QString::number(MM) + ":" + QString::number(ss);
    //qDebug() << cpuAll << "  " << cpuFree;
    ui->CPUValue->showMessage(info, 5000);
    m_cpuAll = cpuAll;
    m_cpuFree = cpuFree;
}

QString MainWindow::GetRunCommand(QString command){
    QProcess process;
    process.start(command);
    process.waitForStarted();
    process.waitForFinished();
    QString re = process.readAllStandardOutput();
    process.close();
    return re;
}


MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_browser_clicked()
{
    // 浏览镜像文件
    QString filePath = QFileDialog::getOpenFileName(this, "选择 ISO 文件", QDir::homePath(), "ISO 镜像文件(*.iso);;所有文件(*.*)");
    if(filePath != ""){
        ui->isoPath->setText(filePath);
    }
}

void MainWindow::on_install_clicked()
{
    switch (ui->vmChooser->currentIndex()) {
    case 0:
        if(system("which qemu-system-x86_64")){
            if(QMessageBox::question(this, "提示", "您似乎没有安装 Qemu，是否继续创建虚拟机？") == QMessageBox::No){
                return;
            }
        }
        break;
    case 1:
        if(system("which vboxmanage")){
            if(QMessageBox::question(this, "提示", "您似乎没有安装 VBox，是否继续创建虚拟机？") == QMessageBox::No){
                return;
            }
        }
        break;
    }
    buildvbox(ui->isoPath->text(), ui->systemVersion->currentIndex(), ui->vmChooser->currentIndex());
    return;
}

void MainWindow::on_getvbox_clicked()
{
    QDesktopServices::openUrl(QUrl("https://www.virtualbox.org/wiki/Linux_Downloads"));
}

void MainWindow::on_getQemu_clicked()
{
    system(("python3 '" + QCoreApplication::applicationDirPath() + "/../RunCommandWithTerminal.py' '" + QCoreApplication::applicationDirPath() + "/../QemuSystemInstall.sh'").toLatin1());
}

void MainWindow::on_vmChooser_currentIndexChanged(int index)
{
    ui->qemuSetting->setDisabled(index);
}

void MainWindow::on_qemuSetting_clicked()
{
    QemuSetting *show = new QemuSetting();
    show->show();

}

void MainWindow::on_addQemuDisk_triggered()
{
    if(QFile::exists(QDir::homePath() + "/Qemu/Windows/Windows.qcow2")){
        if(QMessageBox::question(this, "提示", "磁盘文件已存在，是否覆盖？\n覆盖后将无法恢复！") == QMessageBox::No){
            return;
        }
    }
    QString path = QFileDialog::getOpenFileName(this, "选择 Qemu 镜像", QDir::homePath(), "Qemu镜像(*.qcow2 *.img *.raw *.qcow *.qed *.vdi *.vhdx *.vmdk);;所有文件(*.*)");
    qDebug() << path;
    if(path == ""){
        return;
    }
    QDir dir(QDir::homePath() + "/Qemu/Windows/Windows.qcow2");
    if(!dir.exists()){
        dir.mkpath(QDir::homePath() + "/Qemu/Windows/Windows.qcow2");
    }
    if(!QFile::remove(QDir::homePath() + "/Qemu/Windows/Windows.qcow2") | !QFile::copy(path, QDir::homePath() + "/Qemu/Windows/Windows.qcow2")){
        QMessageBox::critical(this, "提示", "添加错误！");
        return;
    }
    QMessageBox::information(this, "提示", "添加完成！");
}

void MainWindow::on_delQemuDisk_triggered()
{
    if(!QFile::exists(QDir::homePath() + "/Qemu/Windows/Windows.qcow2")){
        QMessageBox::information(this, "提示", "不存在磁盘文件，无法导出");
        return;
    }
    std::system(("xdg-open \"" + QDir::homePath() + "/Qemu/Windows/\"").toUtf8());
}
