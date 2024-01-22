#include "messagebox.h"
#include <QGridLayout>
#include <DLabel>
#include <DPushButton>

MessageBox::MessageBox(DWidget *parent){
    this->parent = parent;
}

void MessageBox::information(QString title, QString text){
    DMainWindow *messageBox = new DMainWindow(this->parent);
    DWidget *widget = new DWidget();
    QGridLayout *layout = new QGridLayout();
    DPushButton *ok = new DPushButton("确定");
    QObject::connect(ok, &DPushButton::clicked, messageBox, [messageBox](){
        messageBox->close();
    });
    layout->addWidget(new DLabel("<img src=':/Icon/MessageBox/dialog-information.svg'>"));
    layout->addWidget(new DLabel(text), 0, 1);
    layout->addWidget(ok, 1, 0, 1, 2);
    widget->setLayout(layout);
    //messageBox->setEnableSystemResize(true);
    messageBox->setEnableBlurWindow(false);
    messageBox->setEnableSystemResize(false);
    messageBox->setWindowFlags(messageBox->windowFlags() &~ Qt::WindowMaximizeButtonHint &~ Qt::Dialog &~ Qt::WindowMinimizeButtonHint);
    messageBox->setCentralWidget(widget);
    messageBox->setWindowTitle(title);
    messageBox->show();
    messageBox->resize(messageBox->frameSize().width(), messageBox->frameSize().height());
}
