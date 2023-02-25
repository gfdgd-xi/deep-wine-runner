/*
 * gfdgd xi、为什么您不喜欢熊出没和阿布呢
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

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    ui->tabWidget->setTabPosition(QTabWidget::West);  // 标签靠左
    // 允许输出 qDebug 信息
    QLoggingCategory::defaultCategory()->setEnabled(QtDebugMsg, true);
    // 判断是否安装 vbox
    if(system("which VBoxManage")){
        if(QMessageBox::question(NULL, "提示", "检测到您似乎没有安装 VirtualBox，立即安装？") == QMessageBox::Yes){
            system("xdg-open https://www.virtualbox.org/wiki/Linux_Downloads");
        }
    }
    // QTimer
    QTimer *cpuGet = new QTimer(this);
    connect(cpuGet, &QTimer::timeout, this, &MainWindow::ShowCPUMessage);
    cpuGet->setInterval(600);
    cpuGet->start();
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

    QString info = "CPU: " + QString::number(cpu) + "%  内存: " +
            QString::number(memory * 100 / memoryAll) + "% " + QString::number(memory / 1024) + "MB/" + QString::number(memoryAll / 1024) + "MB";
    qDebug() << cpuAll << "  " << cpuFree;
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
    buildvbox(ui->isoPath->text(), ui->systemVersion->currentIndex());
    return;
}
