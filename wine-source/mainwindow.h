#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QJsonArray>
#include <QProgressDialog>

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow();
    QString internetWineSource = "https://code.gitlink.org.cn/gfdgd_xi/wine-mirrors/raw/branch/master/";
    QJsonArray internetJsonList;
    QJsonArray localJsonList;

private slots:
    void on_addButton_clicked();
    void ReadLocalInformation();
    void ReadInternetInformation();

    void on_delButton_clicked();

public slots:
    void MessageBoxInfo(QString info);
    void MessageBoxError(QString info);
    void ChangeDialog(QProgressDialog *dialog, int value, int downloadBytes, int totalBytes);
    void DownloadFinish();

private:
    Ui::MainWindow *ui;
};

#endif // MAINWINDOW_H
