#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "installdeb.h"
#include <qtermwidget5/qtermwidget.h>
#include <QMessageBox>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);

}

MainWindow::~MainWindow()
{
    delete ui;
}


void MainWindow::on_installPath_clicked()
{
    QTermWidget *terminal = new QTermWidget(0);
    terminal->setColorScheme("DarkPastels");
    terminal->setShellProgram("/usr/bin/bash");
    terminal->setArgs(QStringList() << "-c" << "gedit");
    connect(terminal, &QTermWidget::finished, this, [&, this](){QMessageBox::information(NULL, "提示", "系统安装完成"); });
    terminal->startShellProgram();


    ui->gridLayout->addWidget(terminal, 1, 0);
}

