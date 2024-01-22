#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "installdeb.h"
#include "messagebox.h"
#include <qtermwidget5/qtermwidget.h>
#include <QMessageBox>

MainWindow::MainWindow(QWidget *parent)
    : DMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    MessageBox *message = new MessageBox();
    message->information("A", "B");
    this->close();
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
    connect(terminal, &QTermWidget::finished, this, [&, this](){
        //QMessageBox::information(NULL, "提示", "系统安装完成");
        MessageBox *message = new MessageBox();
        message->information("A", "B");
    });
    terminal->startShellProgram();


    ui->gridLayout->addWidget(terminal, 1, 0);
}

