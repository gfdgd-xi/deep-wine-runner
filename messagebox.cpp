#include "messagebox.h"
#include <QGridLayout>
#include <DLabel>
#include <DPushButton>
#include <DTitlebar>
#include <QScreen>


MessageBox::MessageBox(DWidget *parent){
    this->parent = parent;
}

void MessageBox::ShowMessageBox(QString iconPath, QString title, QString text){
    DMainWindow *messageBox = new DMainWindow();
    DWidget *widget = new DWidget();
    QGridLayout *layout = new QGridLayout();
    DPushButton *ok = new DPushButton("确定");
    QObject::connect(ok, &DPushButton::clicked, messageBox, [messageBox](){
        messageBox->close();
    });
    DTitlebar *bar = messageBox->titlebar();
    bar->setTitle(title);
    bar->setIcon(QIcon(":/Icon/deepin-wine-runner.svg"));
    bar->setMenuVisible(false);
    bar->setBackgroundTransparent(true);
    layout->addWidget(new DLabel("<img src='" + iconPath + "'>"));
    layout->addWidget(new DLabel(text), 0, 1);
    layout->addWidget(ok, 1, 0, 1, 2);
    widget->setLayout(layout);
    messageBox->setEnableBlurWindow(false);
    messageBox->setEnableSystemResize(false);
    messageBox->setWindowFlags(messageBox->windowFlags() &~ Qt::WindowMaximizeButtonHint &~ Qt::Dialog &~ Qt::WindowMinimizeButtonHint);
    messageBox->setCentralWidget(widget);
    messageBox->setWindowTitle(title);
    // 设置窗口顶置
    messageBox->setWindowFlag(Qt::WindowStaysOnTopHint);
    messageBox->show();
    messageBox->resize(messageBox->frameSize().width(), messageBox->frameSize().height());

    //// 根据窗口信息获取中点
    if(this->parent == NULL){
        /// 如果没有传入窗口
        // 获取主屏幕信息
        int screenWidth = QGuiApplication::primaryScreen()->geometry().width();
        int screenHeight = QGuiApplication::primaryScreen()->geometry().height();
        // 获取对话框信息
        int messageBoxWidth = messageBox->frameSize().width();
        int messageBoxHeight = messageBox->frameSize().height();
        // 计算坐标
        int x = (screenWidth / 2) - (messageBoxWidth / 2);
        int y = (screenHeight / 2) - (messageBoxHeight / 2);
        messageBox->move(x, y);
        qDebug() << screenWidth;
        qDebug() << screenHeight;
        qDebug() << messageBoxWidth;
        qDebug() << messageBoxHeight;
        qDebug() << x << y;
        return;
    }
    // 获取窗口信息
    int parentWindowX = this->parent->frameGeometry().x();
    int parentWindowY = this->parent->frameGeometry().y();
    int parentWindowWidth = this->parent->frameGeometry().width();
    int parentWindowHeight = this->parent->frameGeometry().height();
    int messageBoxWidth = messageBox->frameSize().width();
    int messageBoxHeight = messageBox->frameSize().height();
    // 计算坐标
    int x = parentWindowX + ((parentWindowWidth / 2) - (messageBoxWidth / 2));
    int y = parentWindowY + ((parentWindowHeight / 2) - (messageBoxHeight / 2));
    messageBox->move(x, y);
    qDebug() << parentWindowX;
    qDebug() << parentWindowY;
    qDebug() << parentWindowWidth;
    qDebug() << parentWindowHeight;
    qDebug() << messageBoxWidth;
    qDebug() << messageBoxHeight;
    qDebug() << x << y;
}

void MessageBox::information(QString title, QString text){
    ShowMessageBox(":/Icon/MessageBox/dialog-information.svg", title, text);
}

void MessageBox::critical(QString title, QString text){
    ShowMessageBox(":/Icon/MessageBox/dialog-error.svg", title, text);
}
