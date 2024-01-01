#ifndef ABOUT_THIS_PROGRAM_H
#define ABOUT_THIS_PROGRAM_H

#include <QDialog>

namespace Ui {
class about_this_program;
}

class about_this_program : public QDialog
{
    Q_OBJECT

public:
    explicit about_this_program(QWidget *parent = nullptr);
    ~about_this_program();

private slots:
    void on_ok_clicked();

private:
    Ui::about_this_program *ui;
};

#endif // ABOUT_THIS_PROGRAM_H
