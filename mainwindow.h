#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <DMainWindow>
#include <qtermwidget5/qtermwidget.h>
DWIDGET_USE_NAMESPACE
QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public DMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void on_installPath_clicked();

    void on_browserButton_clicked();

private:
    QTermWidget *terminal = new QTermWidget(0);
    Ui::MainWindow *ui;
};
#endif // MAINWINDOW_H
