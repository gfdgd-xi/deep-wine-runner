#include "qemusetting.h"
#include "ui_qemusetting.h"
#include <QMessageBox>
#include <QDesktopServices>
#include <QUrl>

QemuSetting::QemuSetting(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::QemuSetting)
{
    ui->setupUi(this);
}

QemuSetting::~QemuSetting()
{
    delete ui;
}

void QemuSetting::on_buttonBox_accepted()
{
    QMessageBox::information(NULL, "", "");
    acceptDrops();
}

void QemuSetting::on_save_clicked()
{

}

void QemuSetting::on_cancel_clicked()
{
    accept();
}

void QemuSetting::on_getrunner_clicked()
{
    QDesktopServices::openUrl(QUrl("https://gitee.com/gfdgd-xi/deep-wine-runner/"));
}
