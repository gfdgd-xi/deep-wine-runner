#include "qr.h"
#include "ui_qr.h"

QR::QR(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::QR)
{
    ui->setupUi(this);
}

QR::~QR()
{
    delete ui;
}
