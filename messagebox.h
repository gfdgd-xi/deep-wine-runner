#ifndef MESSAGEBOX_H
#define MESSAGEBOX_H

#include <DMainWindow>
#include <QObject>
#include <DWidget>
using namespace Dtk::Widget;
class MessageBox
{
    //Q_OBJECT
public:
    explicit MessageBox(DWidget *parent = nullptr);
    void information(QString title, QString text);
private:
    DWidget *parent;
signals:

};

#endif // MESSAGEBOX_H
