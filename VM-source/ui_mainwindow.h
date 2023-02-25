/********************************************************************************
** Form generated from reading UI file 'mainwindow.ui'
**
** Created by: Qt User Interface Compiler version 5.15.6
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

#include <QtCore/QVariant>
#include <QtGui/QIcon>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QComboBox>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QLabel>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QSpacerItem>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QTabWidget>
#include <QtWidgets/QTextBrowser>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QAction *action;
    QAction *action_2;
    QWidget *centralWidget;
    QHBoxLayout *horizontalLayout;
    QTabWidget *tabWidget;
    QWidget *tab;
    QVBoxLayout *verticalLayout;
    QHBoxLayout *horizontalLayout_2;
    QLabel *label;
    QLineEdit *isoPath;
    QPushButton *browser;
    QHBoxLayout *horizontalLayout_3;
    QLabel *label_2;
    QComboBox *systemVersion;
    QHBoxLayout *horizontalLayout_4;
    QSpacerItem *horizontalSpacer;
    QPushButton *install;
    QTextBrowser *textBrowser_3;
    QWidget *tab_3;
    QHBoxLayout *horizontalLayout_5;
    QTextBrowser *textBrowser;
    QWidget *tab_2;
    QHBoxLayout *horizontalLayout_6;
    QVBoxLayout *verticalLayout_3;
    QLabel *label_3;
    QSpacerItem *verticalSpacer_2;
    QTextBrowser *textBrowser_2;
    QStatusBar *CPUValue;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QString::fromUtf8("MainWindow"));
        MainWindow->resize(807, 429);
        QIcon icon;
        icon.addFile(QString::fromUtf8(":/icon.png"), QSize(), QIcon::Normal, QIcon::Off);
        MainWindow->setWindowIcon(icon);
        action = new QAction(MainWindow);
        action->setObjectName(QString::fromUtf8("action"));
        action_2 = new QAction(MainWindow);
        action_2->setObjectName(QString::fromUtf8("action_2"));
        centralWidget = new QWidget(MainWindow);
        centralWidget->setObjectName(QString::fromUtf8("centralWidget"));
        horizontalLayout = new QHBoxLayout(centralWidget);
        horizontalLayout->setSpacing(6);
        horizontalLayout->setContentsMargins(11, 11, 11, 11);
        horizontalLayout->setObjectName(QString::fromUtf8("horizontalLayout"));
        tabWidget = new QTabWidget(centralWidget);
        tabWidget->setObjectName(QString::fromUtf8("tabWidget"));
        tabWidget->setTabShape(QTabWidget::Rounded);
        tab = new QWidget();
        tab->setObjectName(QString::fromUtf8("tab"));
        verticalLayout = new QVBoxLayout(tab);
        verticalLayout->setSpacing(6);
        verticalLayout->setContentsMargins(11, 11, 11, 11);
        verticalLayout->setObjectName(QString::fromUtf8("verticalLayout"));
        horizontalLayout_2 = new QHBoxLayout();
        horizontalLayout_2->setSpacing(6);
        horizontalLayout_2->setObjectName(QString::fromUtf8("horizontalLayout_2"));
        label = new QLabel(tab);
        label->setObjectName(QString::fromUtf8("label"));

        horizontalLayout_2->addWidget(label);

        isoPath = new QLineEdit(tab);
        isoPath->setObjectName(QString::fromUtf8("isoPath"));

        horizontalLayout_2->addWidget(isoPath);

        browser = new QPushButton(tab);
        browser->setObjectName(QString::fromUtf8("browser"));

        horizontalLayout_2->addWidget(browser);


        verticalLayout->addLayout(horizontalLayout_2);

        horizontalLayout_3 = new QHBoxLayout();
        horizontalLayout_3->setSpacing(6);
        horizontalLayout_3->setObjectName(QString::fromUtf8("horizontalLayout_3"));
        label_2 = new QLabel(tab);
        label_2->setObjectName(QString::fromUtf8("label_2"));

        horizontalLayout_3->addWidget(label_2);

        systemVersion = new QComboBox(tab);
        systemVersion->addItem(QString());
        systemVersion->addItem(QString());
        systemVersion->addItem(QString());
        systemVersion->setObjectName(QString::fromUtf8("systemVersion"));

        horizontalLayout_3->addWidget(systemVersion);

        horizontalLayout_3->setStretch(1, 1);

        verticalLayout->addLayout(horizontalLayout_3);

        horizontalLayout_4 = new QHBoxLayout();
        horizontalLayout_4->setSpacing(6);
        horizontalLayout_4->setObjectName(QString::fromUtf8("horizontalLayout_4"));
        horizontalSpacer = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_4->addItem(horizontalSpacer);

        install = new QPushButton(tab);
        install->setObjectName(QString::fromUtf8("install"));

        horizontalLayout_4->addWidget(install);


        verticalLayout->addLayout(horizontalLayout_4);

        textBrowser_3 = new QTextBrowser(tab);
        textBrowser_3->setObjectName(QString::fromUtf8("textBrowser_3"));

        verticalLayout->addWidget(textBrowser_3);

        tabWidget->addTab(tab, QString());
        tab_3 = new QWidget();
        tab_3->setObjectName(QString::fromUtf8("tab_3"));
        horizontalLayout_5 = new QHBoxLayout(tab_3);
        horizontalLayout_5->setSpacing(6);
        horizontalLayout_5->setContentsMargins(11, 11, 11, 11);
        horizontalLayout_5->setObjectName(QString::fromUtf8("horizontalLayout_5"));
        textBrowser = new QTextBrowser(tab_3);
        textBrowser->setObjectName(QString::fromUtf8("textBrowser"));
        textBrowser->setUndoRedoEnabled(false);

        horizontalLayout_5->addWidget(textBrowser);

        tabWidget->addTab(tab_3, QString());
        tab_2 = new QWidget();
        tab_2->setObjectName(QString::fromUtf8("tab_2"));
        QSizePolicy sizePolicy(QSizePolicy::Minimum, QSizePolicy::Preferred);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(tab_2->sizePolicy().hasHeightForWidth());
        tab_2->setSizePolicy(sizePolicy);
        horizontalLayout_6 = new QHBoxLayout(tab_2);
        horizontalLayout_6->setSpacing(6);
        horizontalLayout_6->setContentsMargins(11, 11, 11, 11);
        horizontalLayout_6->setObjectName(QString::fromUtf8("horizontalLayout_6"));
        verticalLayout_3 = new QVBoxLayout();
        verticalLayout_3->setSpacing(6);
        verticalLayout_3->setObjectName(QString::fromUtf8("verticalLayout_3"));
        label_3 = new QLabel(tab_2);
        label_3->setObjectName(QString::fromUtf8("label_3"));
        QSizePolicy sizePolicy1(QSizePolicy::Maximum, QSizePolicy::Maximum);
        sizePolicy1.setHorizontalStretch(0);
        sizePolicy1.setVerticalStretch(0);
        sizePolicy1.setHeightForWidth(label_3->sizePolicy().hasHeightForWidth());
        label_3->setSizePolicy(sizePolicy1);
        label_3->setMinimumSize(QSize(200, 200));
        label_3->setMaximumSize(QSize(200, 200));
        label_3->setStyleSheet(QString::fromUtf8("border-image: url(:/deepin-wine-runner.png);"));

        verticalLayout_3->addWidget(label_3);

        verticalSpacer_2 = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);

        verticalLayout_3->addItem(verticalSpacer_2);


        horizontalLayout_6->addLayout(verticalLayout_3);

        textBrowser_2 = new QTextBrowser(tab_2);
        textBrowser_2->setObjectName(QString::fromUtf8("textBrowser_2"));
        QSizePolicy sizePolicy2(QSizePolicy::Minimum, QSizePolicy::Expanding);
        sizePolicy2.setHorizontalStretch(0);
        sizePolicy2.setVerticalStretch(0);
        sizePolicy2.setHeightForWidth(textBrowser_2->sizePolicy().hasHeightForWidth());
        textBrowser_2->setSizePolicy(sizePolicy2);

        horizontalLayout_6->addWidget(textBrowser_2);

        tabWidget->addTab(tab_2, QString());

        horizontalLayout->addWidget(tabWidget);

        MainWindow->setCentralWidget(centralWidget);
        CPUValue = new QStatusBar(MainWindow);
        CPUValue->setObjectName(QString::fromUtf8("CPUValue"));
        MainWindow->setStatusBar(CPUValue);

        retranslateUi(MainWindow);

        tabWidget->setCurrentIndex(1);


        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QCoreApplication::translate("MainWindow", "Windows \345\272\224\347\224\250\351\200\202\351\205\215\345\267\245\345\205\267", nullptr));
        action->setText(QCoreApplication::translate("MainWindow", "\351\200\200\345\207\272", nullptr));
        action_2->setText(QCoreApplication::translate("MainWindow", "\345\205\263\344\272\216", nullptr));
        label->setText(QCoreApplication::translate("MainWindow", "\351\225\234\345\203\217\350\267\257\345\276\204\357\274\232", nullptr));
        isoPath->setPlaceholderText(QCoreApplication::translate("MainWindow", "\350\257\267\351\200\211\346\213\251\347\263\273\347\273\237\351\225\234\345\203\217", nullptr));
        browser->setText(QCoreApplication::translate("MainWindow", "\346\265\217\350\247\210\342\200\246\342\200\246", nullptr));
        label_2->setText(QCoreApplication::translate("MainWindow", "\347\263\273\347\273\237\347\211\210\346\234\254\357\274\232", nullptr));
        systemVersion->setItemText(0, QCoreApplication::translate("MainWindow", "Windows 7 32 \344\275\215\357\274\210\346\224\257\346\214\201\350\207\252\345\212\250\345\256\211\350\243\205\357\274\211", nullptr));
        systemVersion->setItemText(1, QCoreApplication::translate("MainWindow", "Windows 7 64 \344\275\215\357\274\210\346\224\257\346\214\201\350\207\252\345\212\250\345\256\211\350\243\205\357\274\211", nullptr));
        systemVersion->setItemText(2, QCoreApplication::translate("MainWindow", "\345\205\266\345\256\203 Windows \347\263\273\347\273\237\357\274\210\344\270\215\346\224\257\346\214\201\350\207\252\345\212\250\345\256\211\350\243\205\357\274\211", nullptr));

        systemVersion->setCurrentText(QString());
        systemVersion->setPlaceholderText(QCoreApplication::translate("MainWindow", "\350\257\267\351\200\211\346\213\251\347\263\273\347\273\237\347\261\273\345\236\213\357\274\210\345\246\202\346\236\234\350\257\206\345\210\253\344\270\215\344\272\206\350\257\267\350\207\252\350\241\214\351\200\211\346\213\251\357\274\214\345\246\202\346\236\234\351\200\211\346\213\251\351\224\231\350\257\257\346\210\226\344\270\215\346\224\257\346\214\201\345\260\206\346\227\240\346\263\225\350\277\233\350\241\214\350\207\252\345\212\250\345\256\211\350\243\205\357\274\211", nullptr));
        install->setText(QCoreApplication::translate("MainWindow", "\345\256\211\350\243\205", nullptr));
        textBrowser_3->setHtml(QCoreApplication::translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Noto Sans CJK SC'; font-size:10.5pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">\344\275\277\347\224\250\350\277\205\351\233\267\346\210\226\350\200\205\347\275\221\347\233\230\344\270\213\350\275\275\344\273\245\344\270\213\344\273\273\346\204\217\344\270\200\344\270\252\351\223\276\346\216\245\347\204\266\345\220\216\345\234\250\344\270\212\351\235\242\351\200\211\346\213\251\345\215\263\345\217\257\357\274\232</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">123 \347\275\221"
                        "\347\233\230\351\223\276\346\216\245\357\274\232https://www.123pan.com/s/pDSKVv-oypWv</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">\350\277\205\351\233\267\347\275\221\347\233\230\357\274\232https://pan.xunlei.com/s/VNKMz3wgbYHg6JIh50ZKIc7pA1?pwd=35e5  \346\217\220\345\217\226\347\240\201\357\274\23235e5</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">\347\231\276\345\272\246\347\275\221\347\233\230\357\274\232https://pan.baidu.com/s/19WbvinITCQJFZpAdZutrjg?pwd=me4y \346\217\220\345\217\226\347\240\201: me4y</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">\357\274\210\345\246\202\346\236\234\344\270\213\350\275\275\350\277\231\344\270\252\357\274"
                        "\214\347\263\273\347\273\237\347\211\210\346\234\254\351\200\211\347\254\254\344\270\200\351\241\271\357\274\214\344\270\200\350\210\254\346\216\250\350\215\220\350\277\231\344\270\252\357\274\211ed2k://|file|cn_windows_7_ultimate_with_sp1_x86_dvd_u_677486.iso|2653276160|7503E4B9B8738DFCB95872445C72AEFB|/</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">\357\274\210\345\246\202\346\236\234\344\270\213\350\275\275\350\277\231\344\270\252\357\274\214\347\263\273\347\273\237\347\211\210\346\234\254\351\200\211\347\254\254\344\272\214\351\241\271\357\274\211ed2k://|file|cn_windows_7_ultimate_with_sp1_x64_dvd_u_677408.iso|3420557312|B58548681854236C7939003B583A8078|/</span></p>\n"
"<hr /></body></html>", nullptr));
        tabWidget->setTabText(tabWidget->indexOf(tab), QCoreApplication::translate("MainWindow", "\350\256\276\347\275\256", nullptr));
#if QT_CONFIG(tooltip)
        tabWidget->setTabToolTip(tabWidget->indexOf(tab), QCoreApplication::translate("MainWindow", "\350\256\276\347\275\256", nullptr));
#endif // QT_CONFIG(tooltip)
        textBrowser->setHtml(QCoreApplication::translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Noto Sans CJK SC'; font-size:10.5pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:26pt; font-weight:600;\">\347\273\231\345\260\217\347\231\275\347\232\204\344\270\200\346\256\265\350\257\235</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\345\205\266\345\256\236\346\234\254\350\264\250\344\270\212\350\267\221\345\256\214\345\256\211\350\243\205\347\250\213\345\272\217\345\260\261\346\262\241\346\234\211\347\204\266\345\220\216\344\272\206\357\274\214\351\241\266\345\244\232\345\246\202\346\236\234\346\203\263\350\246\201"
                        "\350\277\220\350\241\214\350\210\222\346\234\215\344\270\200\347\202\271\347\202\271\357\274\214\345\217\257\344\273\245\345\256\211\350\243\205\345\212\240\345\274\272\345\212\237\350\203\275\357\274\214\347\233\264\346\216\245\346\213\211\345\210\260\346\234\200\345\272\225\344\270\213\347\234\213\345\260\261\345\217\257\344\273\245\344\272\206</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\345\246\202\346\236\234\347\210\261\346\212\230\350\205\276\347\232\204\350\257\235\357\274\214\344\270\213\351\235\242\347\232\204\351\203\275\347\234\213\347\234\213\344\271\237\346\227\240\346\211\200\350\260\223\347\232\204\357\274\214\346\203\263\347\234\213\345\276\200\344\270\213\347\277\273\345\260\261\345\217\257\344\273\245\344\272\206</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\357\274\210\345\246\202\346\236\234\351\274\240\346\240\207\350\242\253"
                        "\351\224\201\345\256\232\345\210\260\351\207\214\351\235\242\344\272\206\346\214\211\344\270\213\351\224\256\347\233\230\345\217\263\350\276\271\347\232\204\342\200\234Ctrl\342\200\235\351\224\256\345\260\261\345\217\257\344\273\245\344\272\206\357\274\211</p>\n"
"<hr />\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:26pt; font-weight:600;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:26pt; font-weight:600;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:26pt; font-weight:600;\"><br /></p>\n"
"<p sty"
                        "le=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:26pt; font-weight:600;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:26pt; font-weight:600;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:26pt; font-weight:600;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:26pt; font-weight:600;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:26pt; font-weight:600;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-b"
                        "ottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:26pt; font-weight:600;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:26pt; font-weight:600;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:26pt; font-weight:600;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:26pt; font-weight:600;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:26pt; font-weight:600;\">\345\256\211\350\243\205\346\230\257\345\220\246\351\234\200\350\246\201\344\272\272\345\267\245\350\277\233\350\241\214\346\223\215\344\275"
                        "\234\357\274\237</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\345\246\202\346\236\234\346\202\250\344\270\213\350\275\275\347\232\204\351\225\234\345\203\217\346\234\254\347\250\213\345\272\217\346\224\257\346\214\201\357\274\214\345\210\231\345\244\247\351\203\250\345\210\206\344\270\215\347\224\250\357\274\214\345\267\262\347\273\217\345\260\275\351\207\217\347\234\201\345\216\273\344\272\206\350\256\251\346\226\260\346\211\213\345\244\264\347\226\274\347\232\204\350\231\232\346\213\237\346\234\272\347\250\213\345\272\217\345\256\211\350\243\205\357\274\214\345\210\233\345\273\272\343\200\201\350\256\276\347\275\256\350\231\232\346\213\237\346\234\272\357\274\214\350\231\232\346\213\237\347\243\201\347\233\230\345\210\206\345\214\272\357\274\214\345\257\273\346\211\276\345\216\237\347\211\210\351\225\234\345\203\217\346\226\207\344\273\266\347\255\211\345\206\205\345\256\271</p>\n"
"<p style=\" margin-top:0px; margin-"
                        "bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\":/picture/\346\210\252\345\233\276/\346\210\252\345\233\276_VirtualBox Machine_20220712191756.png\" /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\344\275\206\346\234\211\344\272\233\350\256\276\347\275\256\344\276\235\346\227\247\351\234\200\350\246\201\344\272\272\345\267\245\350\207\252\350\241\214\350\256\276\347\275\256\357\274\214\344\276\213\345\246\202\345\256\211\350\243\205\347\225\214\351\235\242\345\257\206\351\222\245\347\232\204\350\276\223\345\205\245\343\200\201\347\263\273\347\273\237\347\232\204\346\277\200\346\264\273\357\274\210\346\266\211\345\217\212\347\211\210\346\235\203\351\227\256\351\242\230\357\274\214\344\270\215\344\274\232\350\200\203\350\231\221\347\234\201\347\225\245\357\274\211\343\200\201\345\242\236\345\274\272\345\212\237\350\203\275\347\232\204\345\256\211\350\243\205\343\200\201\351\234\200"
                        "\350\246\201\344\275\277\347\224\250\347\232\204\350\275\257\344\273\266\347\255\211\347\255\211</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\":/picture/\346\210\252\345\233\276/\346\210\252\345\233\276_VirtualBox Machine_20220712192850.png\" /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\":/picture/\346\210\252\345\233\276/\346\210\252\345\233\276_VirtualBox Machine_20220712193527.png\" /></p>\n"
"<hr />\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:26pt; font-weight:600;\">\344\273\200\344\271\210\346\240\267\347\232\204\351\225\234\345\203\217\346\234\254\347\250\213\345\272\217\357\274\210\345\217\257\350\203\275\357\274\211\344\270\215\346\224\257\346\214\201\350\207\252\345\212\250\345\256\211\350\243\205\357\274\237"
                        "</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\351\235\236 Windows 7 \351\225\234\345\203\217\345\217\257\350\203\275\344\270\215\346\224\257\346\214\201\350\207\252\345\212\250\345\256\211\350\243\205\357\274\210\347\272\257\347\232\204 Windows 7 \344\274\201\344\270\232\347\211\210\351\225\234\345\203\217\345\217\257\350\203\275\344\270\215\346\224\257\346\214\201\350\207\252\345\212\250\345\256\211\350\243\205\357\274\211\357\274\214\344\270\215\344\277\235\350\257\201\347\263\273\347\273\237\350\203\275\350\207\252\345\212\250\345\256\211\350\243\205\346\210\220\345\212\237\357\274\214\344\276\213\345\246\202 Windows XP\343\200\201Windows 10\343\200\201Deepin\343\200\201Ubuntu \347\255\211\347\255\211</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<hr />\n"
"<p style=\" margin-top:0px; margin-bott"
                        "om:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:26pt; font-weight:600;\">\351\273\230\350\256\244\347\232\204\350\231\232\346\213\237\346\234\272\350\256\276\347\275\256\344\270\215\344\271\240\346\203\257\346\200\216\344\271\210\346\224\271\357\274\237</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">1\343\200\201\346\211\223\345\274\200\345\220\257\345\212\250\345\231\250\357\274\214\346\211\223\345\274\200 Oracle VM VirtualBox \347\250\213\345\272\217</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">2\343\200\201\351\200\211\346\213\251\345\220\215\345\255\227\344\270\272\342\200\234Windows\342\200\235\347\232\204\350\231\232\346\213\237\346\234\272\357\274\214\347\204\266\345\220\216\345\234\250\345\217\263\350\276"
                        "\271\347\202\271\345\207\273\350\256\276\347\275\256</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\":/picture/\346\210\252\345\233\276/\346\210\252\345\233\276_VirtualBox Manager_20220712223602.png\" /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">3\343\200\201\345\234\250\350\277\231\351\207\214\344\277\256\346\224\271\345\215\263\345\217\257</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\":/picture/\346\210\252\345\233\276/\346\210\252\345\233\276_VirtualBox_20220712223705.png\" /></p>\n"
"<hr />\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:26pt; font-weight:600;\">\345\256\211\350\243\205\345\212"
                        "\240\345\274\272\345\212\237\350\203\275\346\234\211\344\273\200\344\271\210\345\245\275\345\244\204\357\274\237</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">1\343\200\201\346\224\257\346\214\201\351\274\240\346\240\207\350\207\252\347\224\261\344\273\216\350\231\232\346\213\237\346\234\272\345\222\214\345\256\236\344\275\223\346\234\272\345\210\207\346\215\242</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">2\343\200\201\346\224\257\346\214\201\350\231\232\346\213\237\346\234\272\346\240\271\346\215\256\347\252\227\345\217\243\345\244\247\345\260\217\350\207\252\345\212\250\350\256\276\347\275\256\345\210\206\350\276\250\347\216\207</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">3\343\200\201\346\224\257\346\214\201\346\226\207\344\273\266\345\205\261\344\272\253"
                        "\343\200\201\345\211\252\345\210\207\346\235\277\345\205\261\344\272\253\343\200\201\346\226\207\344\273\266\346\213\226\346\224\276</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">4\343\200\201\346\224\257\346\214\201\346\227\240\347\274\235\346\250\241\345\274\217</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\":/picture/\346\210\252\345\233\276/\346\210\252\345\233\276_\351\200\211\346\213\251\345\214\272\345\237\237_20220712224639.png\" /></p>\n"
"<hr />\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:26pt; font-weight:600;\">\345\246\202\344\275\225\345\256\211\350\243\205\345\212\240\345\274\272\345\212\237\350\203\275\357\274\237</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-bloc"
                        "k-indent:0; text-indent:0px;\">1\343\200\201\347\202\271\345\207\273\342\200\234\350\256\276\345\244\207\342\200\235=\343\200\213\342\200\234\345\212\240\345\274\272\345\212\237\350\203\275\342\200\235</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\":/picture/\346\210\252\345\233\276_VirtualBox Machine_20220712142929.png\" /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">2\343\200\201\346\211\223\345\274\200\342\200\234\350\256\241\347\256\227\346\234\272\342\200\235\357\274\214\346\211\276\345\210\260\345\220\215\344\270\272\342\200\234VirtualBox Guest Additions\342\200\235\347\232\204\345\205\211\347\233\230\357\274\214\345\217\214\345\207\273\350\277\233\345\205\245\357\274\214\347\204\266\345\220\216\345\217\214\345\207\273\346\211\223\345\274\200\345\220\215\344\270\272\342\200\234VBoxWindowsAdditions\342\200\235\347\232\204\347\250\213"
                        "\345\272\217</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\":/picture/\346\210\252\345\233\276/\346\210\252\345\233\276_VirtualBox Machine_20220712143006.png\" /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">3\343\200\201\345\234\250\345\274\271\345\207\272\347\232\204\347\225\214\351\235\242\347\202\271\345\207\273\342\200\234\346\230\257\342\200\235</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\":/picture/\346\210\252\345\233\276/\346\210\252\345\233\276_VirtualBox Machine_20220712143018.png\" /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">4\343\200\201\344\270\200\347\233\264\347\202\271\342\200\234Next\342\200\235</p>\n"
"<p style=\" margin-top:0px; margin-b"
                        "ottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\":/picture/\346\210\252\345\233\276/\346\210\252\345\233\276_VirtualBox Machine_20220712143029.png\" /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\":/picture/\346\210\252\345\233\276/\346\210\252\345\233\276_VirtualBox Machine_20220712143037.png\" /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">5\343\200\201\345\205\250\351\203\250\351\200\211\346\213\251\357\274\214\347\204\266\345\220\216\347\202\271\345\207\273\342\200\234Install\342\200\235\350\277\233\350\241\214\345\256\211\350\243\205</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\":/picture/\346\210\252\345\233\276/\346\210\252\345\233\276_VirtualBox Ma"
                        "chine_20220712143044.png\" /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">6\343\200\201\347\255\211\345\276\205\345\256\211\350\243\205\345\256\214\346\257\225\345\220\216\357\274\214\351\200\211\346\213\251\342\200\234Reboot now\342\200\235\347\204\266\345\220\216\347\202\271\345\207\273\342\200\234Finish\342\200\235\351\207\215\345\220\257\346\255\244\350\231\232\346\213\237\346\234\272\345\215\263\345\217\257\345\256\211\350\243\205\346\210\220\345\212\237\357\274\210\351\200\211\346\213\251\342\200\234Reboot now\342\200\235\345\271\266\347\202\271\342\200\234Finish\342\200\235\344\274\232\350\207\252\345\212\250\351\207\215\346\226\260\345\220\257\345\212\250\357\274\211</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\":/picture/\346\210\252\345\233\276/\346\210\252\345\233\276_VirtualBox Machi"
                        "ne_20220712143103.png\" /></p></body></html>", nullptr));
        tabWidget->setTabText(tabWidget->indexOf(tab_3), QCoreApplication::translate("MainWindow", "\345\256\211\350\243\205/\344\275\277\347\224\250\345\270\256\345\212\251", nullptr));
        label_3->setText(QString());
        textBrowser_2->setHtml(QCoreApplication::translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Noto Sans CJK SC'; font-size:10.5pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\346\255\244\344\270\272 wine \350\277\220\350\241\214\345\231\250\351\231\204\345\261\236\347\273\204\344\273\266\357\274\210\350\231\275\347\204\266\350\277\235\350\203\214\344\272\206\342\200\234Wine Is Not An Emulator\342\200\235&lt;Wine \344\270\215\346\230\257\344\270\200\344\270\252\346\250\241\346\213\237\345\231\250&gt;\347\232\204\345\216\237\346\204\217\357\274\211\357\274\214\346\227\250\345\234\250\350\203\275\346\233\264\345\212\240\345\256\214\347\276\216\343\200\201\347\256\200\345\215\225\347\232\204\350\277\220\350\241\214 Windows \345"
                        "\272\224\347\224\250</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\346\234\254\347\250\213\345\272\217\345\237\272\344\272\216 C++ Qt\343\200\201Python \345\222\214 Virtualbox \345\210\266\344\275\234\357\274\214\351\200\232\350\277\207\350\277\220\350\241\214\345\256\211\350\243\205 Windows \346\223\215\344\275\234\347\263\273\347\273\237\347\232\204\350\231\232\346\213\237\346\234\272\345\256\236\347\216\260\345\234\250 Linux \350\277\220\350\241\214 Windows exe \347\250\213\345\272\217\347\232\204\345\212\237\350\203\275\343\200\202</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\345\237\272\344\272\216 GPL V3 \345\215\217\350\256\256\345\274\200\346\272\220</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\351\241\271\347\233\256\345\234\260\345\235\200\357\274\232"
                        "</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">    Gitee\357\274\232<a href=\"https://gitee.com/gfdgd-xi/deep-wine-runner\"><span style=\" font-size:11pt; text-decoration: underline; color:#0082fa;\">https://gitee.com/gfdgd-xi/deep-wine-runner</span></a></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">    Github\357\274\232<a href=\"https://github.com/gfdgd-xi/deep-wine-runner\"><span style=\" font-size:11pt; text-decoration: underline; color:#0082fa;\">https://github.com/gfdgd-xi/deep-wine-runner</span></a></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">    Gitlink\357\274\232<a href=\"https://gitlink.org.cn/gfdgd_xi/deep-wine-runner\"><span style=\" font-size:11pt; text-decoration: underline; color:#0082fa;\">https://gitlink.org.cn/gfdgd_xi/deep-wine-runner</span></a"
                        "></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\346\255\244\347\273\204\344\273\266\344\271\237\346\234\211\351\235\236\345\270\270\345\244\247\347\232\204\347\274\272\347\202\271\357\274\214\345\260\261\346\230\257\347\233\270\346\257\224\344\272\216 Wine\357\274\214\344\274\232\351\234\200\350\246\201\345\215\240\347\224\250\345\244\247\351\207\217\347\232\204\347\251\272\351\227\264\343\200\201\345\256\211\350\243\205\351\234\200\350\246\201\345\244\247\351\207\217\347\232\204\346\227\266\351\227\264\343\200\201\346\237\220\344\272\233\346\203\205\345\206\265\344\270\213\351\234\200\350\246\201\347\233\270\346\257\224\344\272\216 Wine \351\234\200\350\246\201\346\266\210\350\200\227\346\233\264\345\244\232\347\232\204\347\263\273\347\273\237\350\265\204\346\272\220\357\274\214\344\275\206\345\217\257\344\273\245\346\233\264\345\212\240\345\256\214\347\276\216\343\200\201\346\265\201\347\225\205\347\232\204\350\277\220\350\241"
                        "\214 Windows \345\272\224\347\224\250\357\274\214\344\274\232\345\260\275\351\207\217\345\207\217\345\260\221\345\233\240\344\270\272\347\274\272\345\260\221\346\210\226\346\234\252\345\256\236\347\216\260\345\257\274\350\207\264\347\232\204 Windows exe \347\250\213\345\272\217\350\277\220\350\241\214\345\274\202\345\270\270</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\350\257\245\347\273\204\344\273\266\345\210\266\344\275\234\350\200\205\357\274\232RacoonGX \345\233\242\351\230\237\357\274\214By gfdgd xi\343\200\201\344\270\272\344\273\200\344\271\210\346\202\250\344\270\215\345\226\234\346\254\242\347\206\212\345\207\272\346\262\241\345\222\214\351\230\277\345\270\203\345\221\242</p>\n"
"<hr />\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\345\217\202\350\200\203\346\226\207\347\214\256\357\274\232</p>\n"
"<p style=\" margin-top:0px; margin-bott"
                        "om:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Droid Sans Mono','monospace','monospace'; font-size:11pt; color:#6a9955;\">https://juejin.cn/post/7080484519328874510</span></p></body></html>", nullptr));
        tabWidget->setTabText(tabWidget->indexOf(tab_2), QCoreApplication::translate("MainWindow", "\345\205\263\344\272\216", nullptr));
#if QT_CONFIG(statustip)
        CPUValue->setStatusTip(QString());
#endif // QT_CONFIG(statustip)
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
