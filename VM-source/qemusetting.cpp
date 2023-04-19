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
    // 判断是否安装了 Wine 运行器
    ui->getrunner->setHidden(QFile::exists(QCoreApplication::applicationDirPath() + "/../mainwindow.py"));
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
    // 读取配置文件
    QDir dir(QDir::homePath() + "/.config/deepin-wine-runner/");
    if(!dir.exists()){
        dir.mkpath(QDir::homePath() + "/.config/deepin-wine-runner/");
    }
    QFile file(QDir::homePath() + "/.config/deepin-wine-runner/QemuSetting.json");
    file.open(QIODevice::WriteOnly);
    file.write(QJsonDocument(object).toJson());
    file.close();
    QMessageBox::information(this, "提示", "保存完成！");
}

void QemuSetting::on_cancel_clicked()
{
    delete this;
}

void QemuSetting::on_getrunner_clicked()
{
    QDesktopServices::openUrl(QUrl("https://gitee.com/gfdgd-xi/deep-wine-runner/"));
}

void QemuSetting::on_enableVnc_stateChanged(int arg1)
{
    // 控件的开启/关闭
    ui->vncNumber->setEnabled(ui->enableVnc->isChecked());
}

void QemuSetting::on_setDefault_clicked()
{
    if(QMessageBox::question(this, "提示", "你确定要重置为默认？重置后将无法恢复") == QMessageBox::No){
        return;
    }
    QFile::remove(QDir::homePath() + "/.config/deepin-wine-runner/QemuSetting.json");
    this->SetDefaultValue();
    QMessageBox::information(this, "提示", "设置完成！");
}
