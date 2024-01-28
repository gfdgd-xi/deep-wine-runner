#ifndef MESSAGEBOX_H
#define MESSAGEBOX_H

#include <DMainWindow>
#include <QObject>
#include <DWidget>
DWIDGET_USE_NAMESPACE
class MessageBox
{
    //Q_OBJECT
public:
    explicit MessageBox(DWidget *parent = nullptr);
    void information(QString title, QString text);
    void critical(QString title, QString text);
private:
    void ShowMessageBox(QString iconPath, QString title, QString text);
    DWidget *parent;
signals:

};

#endif // MESSAGEBOX_H
