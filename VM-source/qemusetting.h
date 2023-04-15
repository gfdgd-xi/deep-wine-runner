#ifndef QEMUSETTING_H
#define QEMUSETTING_H

#include <QDialog>

namespace Ui {
class QemuSetting;
}

class QemuSetting : public QDialog
{
    Q_OBJECT

public:
    explicit QemuSetting(QWidget *parent = nullptr);
    ~QemuSetting();

private slots:
    void on_buttonBox_accepted();

    void on_save_clicked();

    void on_cancel_clicked();

    void on_getrunner_clicked();

private:
    Ui::QemuSetting *ui;
};

#endif // QEMUSETTING_H
