#include "qemusetting.h"
#include "ui_qemusetting.h"
#include <QMessageBox>
#include <QDesktopServices>
#include <QUrl>
#include <QJsonObject>
#include <QJsonDocument>
#include <QFile>
#include "infoutils.h"
#include <QDir>
#include <sys/sysinfo.h>

QemuSetting::QemuSetting(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::QemuSetting)
{
    ui->setupUi(this);
    // 设置变量
    if(QFile::exists(QDir::homePath() + "/.config/deepin-wine-runner/QemuSetting.json")){
        // 读取配置文件
        QFile file(QDir::homePath() + "/.config/deepin-wine-runner/QemuSetting.json");
        file.open(QIODevice::ReadOnly);
        QJsonParseError error;
        QJsonDocument document = QJsonDocument::fromJson(file.readAll(), &error);
        file.close();
        if(error.error != QJsonParseError::NoError){
            QMessageBox::critical(this, "错误", error.errorString());
        }
        else {
            QJsonObject object = document.object();
            qDebug() << QJsonDocument(object).toJson();
            ui->enableKvm->setChecked(object.value("EnableKVM").toBool());
            ui->enableRdp->setChecked(object.value("EnableRDP").toBool());
            ui->enableVnc->setChecked(object.value("EnableVNC").toBool());
            ui->enableSound->setChecked(object.value("EnableSound").toBool());
            ui->memoryNumber->setValue(object.value("Memory").toInt());
            ui->vncNumber->setValue(object.value("VNC").toInt());
            ui->cpuNumber->setValue(object.value("CPU").toInt());
        }
    }
    else {
        // 默认
        this->SetDefaultValue();
    }
}

void QemuSetting::SetDefaultValue(){
    long memory = 0;
    long memoryAll = 0;
    long swap = 0;
    long swapAll = 0;
    infoUtils::memoryRate(memory, memoryAll, swap, swapAll);
    ui->memoryNumber->setValue(memoryAll / 3 / 1024);
    ui->vncNumber->setValue(5);
    ui->cpuNumber->setValue(get_nprocs());
    ui->enableKvm->setChecked(true);
    ui->enableRdp->setChecked(true);
    ui->enableVnc->setChecked(true);
    ui->enableSound->setChecked(true);
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
    QJsonParseError error;
    QJsonDocument document = QJsonDocument::fromJson("{}", &error);
    if(error.error != QJsonParseError::NoError){
        QMessageBox::critical(this, "错误", error.errorString());
        return;
    }
    QJsonObject object = document.object();
    //object.insert("1", QJsonValue("aa"));
    object.insert("EnableKVM", ui->enableKvm->isChecked());
    object.insert("EnableRDP", ui->enableRdp->isChecked());
    object.insert("EnableVNC", ui->enableVnc->isChecked());
    object.insert("EnableSound", ui->enableSound->isChecked());
    object.insert("Memory", ui->memoryNumber->value());
    object.insert("VNC", ui->vncNumber->value());
    object.insert("CPU", ui->cpuNumber->value());
    qDebug() << QJsonDocument(object).toJson();
}

void QemuSetting::on_cancel_clicked()
{
    delete this;
}

void QemuSetting::on_getrunner_clicked()
{
    QDesktopServices::openUrl(QUrl("https://gitee.com/gfdgd-xi/deep-wine-runner/"));
}
