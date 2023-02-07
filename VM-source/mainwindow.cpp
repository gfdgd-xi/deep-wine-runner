/*
 * 归属 RacoonGX 团队，开发者：gfdgd xi、为什么您不喜欢熊出没和阿布呢
*/
#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "buildvbox.h"
#include <QFileDialog>
#include <QDebug>
#include <QNetworkInterface>
#include <QProcess>
#include <QLoggingCategory>

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    ui->tabWidget->setTabPosition(QTabWidget::West);  // 标签靠左
    // 允许输出 qDebug 信息
    QLoggingCategory::defaultCategory()->setEnabled(QtDebugMsg, true);
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
    buildvbox();
    return;
    //
    QProcess progress;
    QStringList list;
    list << ui->isoPath->text() << QString::number(ui->systemVersion->currentIndex());
    qDebug() << QCoreApplication::applicationDirPath() + QString("/run.py");
    progress.startDetached(QCoreApplication::applicationDirPath() + QString("/run.py"), list);
    ui->tabWidget->setCurrentIndex(1);
}
