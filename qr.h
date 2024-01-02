#ifndef QR_H
#define QR_H

#include <QDialog>

namespace Ui {
class QR;
}

class QR : public QDialog
{
    Q_OBJECT

public:
    explicit QR(QWidget *parent = nullptr);
    ~QR();

private:
    Ui::QR *ui;
};

#endif // QR_H
