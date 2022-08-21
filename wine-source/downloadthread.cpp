#define SETTINGSTEP 6
#include "downloadthread.h"
#include <QProgressDialog>
#include <QFile>
#include <QNetworkAccessManager>
#include <QNetworkRequest>
#include <QEventLoop>
#include <QTimer>
#include <QNetworkReply>
#include <QMessageBox>
#include <QCoreApplication>
#include <QJsonDocument>
#include <QStandardItemModel>
#include <QJsonArray>
#include <QProcess>
// 文件操作
#include <QDir>

DownloadThread::DownloadThread(QProgressDialog *progressDialog, QString url, QString savePath, QString fileName, QListView *view, bool deleteZip, bool unzip, QJsonArray *localList){
    dialog = progressDialog;
    fileUrl = url;
    fileSavePath = savePath;
    fileSaveName = fileName;
    localView = view;
    downloadDeleteZip = deleteZip;
    downloadUnzip = unzip;
    localJsonList = localList;
}
void DownloadThread::ReadLocalInformation(){
    QFile file(QCoreApplication::applicationDirPath() + "/winelist.json");
    file.open(QFileDevice::ReadOnly);
    QJsonDocument list = QJsonDocument::fromJson(file.readAll());
    QStandardItemModel *nmodel = new QStandardItemModel(this);
    QJsonArray localJsonList = list.array();
    for (int i = 0; i < localJsonList.size(); ++i) {
        QStandardItem *item = new QStandardItem(localJsonList.at(i).toString());
        nmodel->appendRow(item);
    }
    localView->setModel(nmodel);
    file.close();
}

// 文件下载
void DownloadThread::run(){
    // 创建文件夹
    QDir dir;
    QString configDir = QCoreApplication::applicationDirPath();
    QString savePath = configDir + "/" + fileSaveName;
    // 文件下载
    int timeout = 0;
    QFile f(savePath);
    if(!f.open(QIODevice::WriteOnly)){
        emit MessageBoxError("文件无法写入");
        f.close();
        delete dialog;
        dialog->close();
        return;
    }
    QNetworkAccessManager m;
    QNetworkRequest req;
    // 响应 https（就是不行）
    QSslConfiguration conf = req.sslConfiguration();
    conf.setPeerVerifyMode(QSslSocket::VerifyNone);
    conf.setProtocol(QSsl::TlsV1_1);
    req.setSslConfiguration(conf);
    req.setUrl(QUrl(fileUrl));
    // 下载文件
    QNetworkReply *reply = m.get(req);
    QEventLoop loop;
    QTimer t;
    qDebug() << reply->rawHeader(QString("Content-Length").toUtf8());
    connect(reply, &QNetworkReply::finished, &loop, &QEventLoop::quit);
    connect(reply, &QNetworkReply::downloadProgress, [=, &f, &t](qint64 bytesRead, qint64 totalBytes){
        f.write(reply->readAll());
        emit ChangeDialog(dialog, (float)bytesRead / totalBytes * 100, bytesRead / 1024 / 1024, totalBytes / 1024 / 1024);
        //dialog->setValue();
        //dialog->setLabelText(QString::number(bytesRead / 1024 / 1024) + "MB/" + QString::number(totalBytes / 1024 / 1024) + "MB（在下载/安装时不要乱点程序、拖动程序，否则容易闪退）");
        if(t.isActive()){
            t.start(timeout);
        }
    });
    if(timeout > 0){
        connect(&t, &QTimer::timeout, &loop, &QEventLoop::quit);
        t.start(timeout);
    }
    loop.exec();
    if(reply->error() != QNetworkReply::NoError){
        qDebug() << "b";
        emit MessageBoxError("下载失败");
        f.close();
        delete reply;
        delete dialog;
        dialog->close();
        return;
    }
    // 写入配置文件
    QFile rfile(QCoreApplication::applicationDirPath() + "/winelist.json");
    rfile.open(QFileDevice::ReadOnly);
    QJsonDocument list = QJsonDocument::fromJson(rfile.readAll());
    rfile.close();
    // 不直接用 readwrite 是因为不能覆盖写入
    QFile file(QCoreApplication::applicationDirPath() + "/winelist.json");
    file.open(QFileDevice::WriteOnly);
    QJsonArray allList = list.array();
    allList.append(QJsonValue::fromVariant(fileSaveName.replace(".7z", "")));
    list.setArray(allList);
    file.write(list.toJson());
    file.close();
    // 读取配置文件
    ReadLocalInformation();
    localJsonList = &allList;
    f.close();
    QString shellCommand;
    // 解压文件
    if (downloadUnzip){
        QString path = QCoreApplication::applicationDirPath() + "/" + fileSaveName.replace(".7z", "");
        shellCommand += "mkdir -p \"" + path + "\"\n"
                "7z x \"" + savePath + "\" -o\"" + path + "\" \n";
    }
    // 删除文件
    if (downloadDeleteZip){
        shellCommand += "rm -rf \"" + savePath + "\"\n";
    }
    // 写入脚本文件
    QFile shellFile("/tmp/depein-wine-runner-wine-install.sh");
    shellFile.open(QIODevice::WriteOnly);
    shellFile.write(shellCommand.toUtf8());
    shellFile.close();
    QProcess process;
    QStringList command = {"deepin-terminal", "-e", "bash", "/tmp/depein-wine-runner-wine-install.sh"};
    process.start(QCoreApplication::applicationDirPath() + "/../launch.sh", command);
    process.waitForFinished();
    delete reply;
    emit Finish();
}
