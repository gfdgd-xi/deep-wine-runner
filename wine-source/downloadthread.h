/*
 * 重写 QThread 以实现多线程下载功能
 */
#ifndef DOWNLOADTHREAD_H
#define DOWNLOADTHREAD_H

#include <QObject>
#include <QThread>
#include <QProgressDialog>
#include <QListView>
#include <QJsonArray>

class DownloadThread : public QThread  // 继承 QThread
{
    Q_OBJECT
public:
    DownloadThread(QProgressDialog *dialog, QString url, QString save, QString fileName, QListView *view, bool deleteZip, bool unzip, QJsonArray *localList);
    void SettingVirtualMachine(QString savePath);
    QProgressDialog *dialog;
    QString fileUrl;
    QString fileSaveName;
    QString fileSavePath;
    QListView *localView;
    QJsonArray *localJsonList;
    bool downloadDeleteZip;
    bool downloadUnzip;

protected:
    void run(); // 核心
    void ReadLocalInformation();

signals:
    // 防止非主线程刷新控件导致程序退出
    void MessageBoxInfo(QString info);
    void MessageBoxError(QString info);
    void ChangeDialog(QProgressDialog *dialog, int value, int downloadBytes, int totalBytes);
    void Finish();
};

#endif // DOWNLOADTHREAD_H
