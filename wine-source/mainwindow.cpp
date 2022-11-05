#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QProcess>
#include <QFile>
#include <QJsonDocument>
#include <QJsonArray>
#include <QMessageBox>
#include <QStandardItemModel>
#include <QLoggingCategory>
#include <QNetworkReply>
#include <QMessageBox>
#include <QNetworkAccessManager>
#include <QNetworkRequest>
#include <QProgressDialog>
#include <QDir>
#include "downloadthread.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    // 设置列表双击不会编辑
    ui->localWineList->setEditTriggers(QAbstractItemView::NoEditTriggers);
    ui->internetWineList->setEditTriggers(QAbstractItemView::NoEditTriggers);
    // 读取信息
    ReadLocalInformation();
    ReadInternetInformation();
    // 图标
    this->setWindowIcon(QIcon(QCoreApplication::applicationDirPath() + "/../deepin-wine-runner.svg"));
    // 允许 qDebug() 输出
    QLoggingCategory::defaultCategory()->setEnabled(QtDebugMsg, true);
}

MainWindow::~MainWindow()
{
    delete ui;
}
void MainWindow::MessageBoxInfo(QString info){
    QMessageBox::information(this, "提示", info);
}
void MainWindow::MessageBoxError(QString info){
    QMessageBox::critical(this, "错误", info);
}
void MainWindow::ChangeDialog(QProgressDialog *dialog, int value, int downloadBytes, int totalBytes){
    dialog->setValue(value);
    dialog->setLabelText(QString::number(downloadBytes) + "MB/" + QString::number(totalBytes) + "MB");
}
void MainWindow::DownloadFinish(){
    ui->centralWidget->setEnabled(true);
}
void MainWindow::on_addButton_clicked()
{
    // 获取下载链接
    int choose = ui->internetWineList->currentIndex().row();
    if (choose < 0){
        QMessageBox::information(this, "提示", "您未选中任何项，无法继续");
        return;
    }
    QString downloadName = internetJsonList.at(choose).toArray().at(1).toString();
    // 判断值是否在列表内
    ReadLocalInformation();
    for (int i = 0; i < localJsonList.size(); ++i) {
        if(localJsonList.at(i).toString() == internetJsonList.at(choose).toArray().at(0).toString()){
            qDebug() << localJsonList.at(i).toString();
            QMessageBox::information(this, "提示", "您已经安装了这个Wine了！无需重复安装！");
            return;
        }
    }
    // 设置选项
    if(ui->deleteZip->isChecked() + ui->unzip->isChecked() == 2){
        ui->deleteZip->setChecked(false);
        ui->unzip->setChecked(false);
    }
    QString downloadUrl = internetWineSource + downloadName;
    QProgressDialog *dialog = new QProgressDialog();
    QPushButton *cancel = new QPushButton("取消");
    cancel->setDisabled(true);
    dialog->setWindowIcon(QIcon(QCoreApplication::applicationDirPath() + "/../deepin-wine-runner.svg"));
    dialog->setCancelButton(cancel);
    dialog->setWindowTitle("正在下载“" + internetJsonList.at(choose).toArray().at(0).toString() + "”");
    DownloadThread *thread = new DownloadThread(
                dialog,
                downloadUrl,
                "",
                internetJsonList.at(choose).toArray().at(1).toString(),
                ui->localWineList, ui->deleteZip->isChecked(),
                !ui->unzip->isChecked(),
                &localJsonList
                );
    connect(thread, &DownloadThread::MessageBoxInfo, this, &MainWindow::MessageBoxInfo);
    connect(thread, &DownloadThread::MessageBoxError, this, &MainWindow::MessageBoxError);
    connect(thread, &DownloadThread::ChangeDialog, this, &MainWindow::ChangeDialog);
    connect(thread, &DownloadThread::Finish, this, &MainWindow::DownloadFinish);
    ui->centralWidget->setDisabled(true);
    thread->start();
}
void MainWindow::ReadInternetInformation(){
    // 我们采用最简单的 curl 来获取信息
    QProcess internet;
    QStringList command = {internetWineSource + "/information.json"};
    internet.start("curl", command);
    internet.waitForFinished();
    // 读取显示
    QJsonDocument internetList = QJsonDocument::fromJson(internet.readAllStandardOutput());
    QStandardItemModel *nmodel = new QStandardItemModel(this);
    internetJsonList = internetList.array();
    for (int i = 0; i < internetJsonList.size(); ++i) {
        QJsonArray list = internetJsonList.at(i).toArray();
        QStandardItem *item = new QStandardItem(list.at(0).toString());
        nmodel->appendRow(item);
    }
    ui->internetWineList->setModel(nmodel);
    internet.close();
}

void MainWindow::ReadLocalInformation(){
    QFile file(QCoreApplication::applicationDirPath() + "/winelist.json");
    file.open(QFileDevice::ReadOnly);
    QJsonDocument list = QJsonDocument::fromJson(file.readAll());
    QStandardItemModel *nmodel = new QStandardItemModel(this);
    localJsonList = list.array();
    for (int i = 0; i < localJsonList.size(); ++i) {
        QStandardItem *item = new QStandardItem(localJsonList.at(i).toString());
        nmodel->appendRow(item);
    }
    ui->localWineList->setModel(nmodel);
    file.close();
}

void MainWindow::on_delButton_clicked()
{
    if(QMessageBox::question(this, "提示", "你确定要删除吗？") == QMessageBox::No){
        return;
    }
    if(ui->localWineList->currentIndex().row() < 0){
        QMessageBox::information(this, "提示", "您未选择任何项");
        return;
    }
    QString name = QCoreApplication::applicationDirPath() + "/" + localJsonList.at(ui->localWineList->currentIndex().row()).toString();
    QDir dir(name);
    dir.removeRecursively();
    QFile::remove(name + ".7z");
    localJsonList.removeAt(ui->localWineList->currentIndex().row());
    QFile file(QCoreApplication::applicationDirPath() + "/winelist.json");
    file.open(QFileDevice::WriteOnly);
    QJsonDocument list;
    list.setArray(localJsonList);
    file.write(list.toJson());
    file.close();
    ReadLocalInformation();
    QMessageBox::information(this, "提示", "删除成功！");
}
