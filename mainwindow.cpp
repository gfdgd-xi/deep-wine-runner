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
    /*MessageBox *message = new MessageBox();
    message->information("A", "B");
    this->close();*/
}

MainWindow::~MainWindow()
{
    delete ui;
}


void MainWindow::on_installPath_clicked()
{
    QTermWidget *terminal = new QTermWidget(0);
    terminal->setColorScheme("DarkPastels");
    terminal->setAutoClose(1);
    InstallDEB *deb = new InstallDEB(terminal, this);
    deb->AddCommand("aptss update");
    deb->AddCommand("aptss install \"" + ui->debPath->text() + "\"");
    deb->RunCommand(1);
    ui->gridLayout->addWidget(terminal, 1, 0);
}

