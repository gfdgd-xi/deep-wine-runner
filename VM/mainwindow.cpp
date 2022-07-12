#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QFileDialog>
#include <QDebug>
#include <QNetworkInterface>
#include <QProcess>

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    ui->tabWidget->setTabPosition(QTabWidget::West);  // 标签靠左
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_browser_clicked()
{
    // 浏览镜像文件
    QString filePath = QFileDialog::getOpenFileName(this, "选择 ISO 文件", "~", "ISO 镜像文件(*.iso);;所有文件(*.*)");
    if(filePath != ""){
        ui->isoPath->setText(filePath);
    }
}

void MainWindow::on_install_clicked()
{
    QProcess progress;
    QStringList list;
    list << ui->isoPath->text() << QString::number(ui->systemVersion->currentIndex());
    qDebug() << QCoreApplication::applicationDirPath() + QString("/run.py");
    progress.startDetached(QCoreApplication::applicationDirPath() + QString("/run.py"), list);
    ui->tabWidget->setCurrentIndex(1);
}
