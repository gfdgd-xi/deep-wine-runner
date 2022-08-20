/********************************************************************************
** Form generated from reading UI file 'mainwindow.ui'
**
** Created by: Qt User Interface Compiler version 5.15.3
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QCheckBox>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QListView>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QSpacerItem>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QWidget *centralWidget;
    QVBoxLayout *verticalLayout_2;
    QHBoxLayout *horizontalLayout_2;
    QListView *localWineList;
    QVBoxLayout *verticalLayout;
    QSpacerItem *verticalSpacer;
    QPushButton *addButton;
    QPushButton *delButton;
    QSpacerItem *verticalSpacer_2;
    QListView *internetWineList;
    QHBoxLayout *horizontalLayout;
    QCheckBox *unzip;
    QCheckBox *deleteZip;
    QSpacerItem *horizontalSpacer;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QString::fromUtf8("MainWindow"));
        MainWindow->resize(693, 404);
        centralWidget = new QWidget(MainWindow);
        centralWidget->setObjectName(QString::fromUtf8("centralWidget"));
        verticalLayout_2 = new QVBoxLayout(centralWidget);
        verticalLayout_2->setSpacing(6);
        verticalLayout_2->setContentsMargins(11, 11, 11, 11);
        verticalLayout_2->setObjectName(QString::fromUtf8("verticalLayout_2"));
        horizontalLayout_2 = new QHBoxLayout();
        horizontalLayout_2->setSpacing(6);
        horizontalLayout_2->setObjectName(QString::fromUtf8("horizontalLayout_2"));
        localWineList = new QListView(centralWidget);
        localWineList->setObjectName(QString::fromUtf8("localWineList"));

        horizontalLayout_2->addWidget(localWineList);

        verticalLayout = new QVBoxLayout();
        verticalLayout->setSpacing(6);
        verticalLayout->setObjectName(QString::fromUtf8("verticalLayout"));
        verticalSpacer = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);

        verticalLayout->addItem(verticalSpacer);

        addButton = new QPushButton(centralWidget);
        addButton->setObjectName(QString::fromUtf8("addButton"));

        verticalLayout->addWidget(addButton);

        delButton = new QPushButton(centralWidget);
        delButton->setObjectName(QString::fromUtf8("delButton"));

        verticalLayout->addWidget(delButton);

        verticalSpacer_2 = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);

        verticalLayout->addItem(verticalSpacer_2);


        horizontalLayout_2->addLayout(verticalLayout);

        internetWineList = new QListView(centralWidget);
        internetWineList->setObjectName(QString::fromUtf8("internetWineList"));

        horizontalLayout_2->addWidget(internetWineList);


        verticalLayout_2->addLayout(horizontalLayout_2);

        horizontalLayout = new QHBoxLayout();
        horizontalLayout->setSpacing(6);
        horizontalLayout->setObjectName(QString::fromUtf8("horizontalLayout"));
        unzip = new QCheckBox(centralWidget);
        unzip->setObjectName(QString::fromUtf8("unzip"));

        horizontalLayout->addWidget(unzip);

        deleteZip = new QCheckBox(centralWidget);
        deleteZip->setObjectName(QString::fromUtf8("deleteZip"));
        deleteZip->setChecked(true);
        deleteZip->setTristate(false);

        horizontalLayout->addWidget(deleteZip);

        horizontalSpacer = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout->addItem(horizontalSpacer);


        verticalLayout_2->addLayout(horizontalLayout);

        MainWindow->setCentralWidget(centralWidget);

        retranslateUi(MainWindow);

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QCoreApplication::translate("MainWindow", "\344\270\213\350\275\275 Wine", nullptr));
        addButton->setText(QCoreApplication::translate("MainWindow", "<<", nullptr));
        delButton->setText(QCoreApplication::translate("MainWindow", ">>", nullptr));
        unzip->setText(QCoreApplication::translate("MainWindow", "\344\270\215\350\247\243\345\216\213Wine\350\265\204\346\272\220\346\226\207\344\273\266", nullptr));
        deleteZip->setText(QCoreApplication::translate("MainWindow", "\345\210\240\351\231\244\344\270\213\350\275\275\347\232\204\350\265\204\346\272\220\345\214\205\357\274\214\345\217\252\350\247\243\345\216\213\344\277\235\347\225\231\357\274\210\344\270\244\344\270\252\351\200\211\351\241\271\351\203\275\351\200\211\347\233\270\344\272\222\346\212\265\346\266\210\357\274\211", nullptr));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
