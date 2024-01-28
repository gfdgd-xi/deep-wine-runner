#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "installdeb.h"
#include "messagebox.h"
#include <qtermwidget5/qtermwidget.h>
#include <QMessageBox>
#include <QFile>
#include <DTitlebar>
#include <QDesktopServices>
#include <DApplication>

MainWindow::MainWindow(QWidget *parent)
    : DMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    // 自定义标题栏
    DTitlebar *bar = this->titlebar();
    bar->setTitle("应用安装器");
    bar->setIcon(QIcon(":/Icon/deepin-wine-runner.svg"));
    bar->setBackgroundTransparent(true);
    QMenu *openProgramWebsite = bar->menu()->addMenu("项目地址");
    QAction *openProgramGitee = new QAction(DApplication::style()->standardIcon(QStyle::SP_DirLinkOpenIcon), "Gitee");
    QAction *openProgramGithub = new QAction("Github");
    QAction *openProgramSourceforge = new QAction("Sourceforge");
    openProgramWebsite->addAction(openProgramGitee);
    openProgramWebsite->addAction(openProgramGithub);
    openProgramWebsite->addAction(openProgramSourceforge);
    connect(openProgramGitee, &QAction::triggered, this, [](){
        QDesktopServices::openUrl(QUrl("https://gitee.com/gfdgd-xi/deep-wine-runner"));
    });
    connect(openProgramGithub, &QAction::triggered, this, [](){
        QDesktopServices::openUrl(QUrl("https://github.com/gfdgd-xi/deep-wine-runner"));
    });
    connect(openProgramSourceforge, &QAction::triggered, this, [](){
        QDesktopServices::openUrl(QUrl("https://sourceforge.net/project/deep-wine-runner"));
    });

    terminal = new QTermWidget(0);
    terminal->setColorScheme("DarkPastels");
    terminal->setAutoClose(0);
    ui->gridLayout->addWidget(terminal, 1, 0);
}

MainWindow::~MainWindow()
{
    delete ui;
}


void MainWindow::on_installPath_clicked()
{
    if(ui->debPath->text().replace(" ", "") == ""){
        MessageBox *message = new MessageBox(this);
        message->critical("提示", "您没有输入 deb 包，无法继续");
        return;
    }
    if(!QFile::exists(ui->debPath->text())){
        MessageBox *message = new MessageBox(this);
        message->critical("提示", "您选择的 deb 包不存在");
        return;
    }
    InstallDEB *deb = new InstallDEB(terminal, this);
    deb->AddCommand("aptss update");
    deb->AddCommand("aptss install \"" + ui->debPath->text() + "\" -y");
    deb->RunCommand(1);


}

