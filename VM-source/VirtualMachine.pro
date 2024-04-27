#-------------------------------------------------
#
# Project created by QtCreator 2022-07-12T13:39:19
#
#-------------------------------------------------

QT       += core gui
TRANSLATIONS += zh_CN.ts\
                en_US.ts

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = VirtualMachine
TEMPLATE = app
QT += network

# The following define makes your compiler emit warnings if you use
# any feature of Qt which has been marked as deprecated (the exact warnings
# depend on your compiler). Please consult the documentation of the
# deprecated API in order to know how to port your code away from it.
DEFINES += QT_DEPRECATED_WARNINGS

# You can also make your code fail to compile if you use deprecated APIs.
# In order to do so, uncomment the following line.
# You can also select to disable deprecated APIs only up to a certain version of Qt.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

CONFIG += c++11

SOURCES += \
        main.cpp \
        mainwindow.cpp \
    buildvbox.cpp \
    vbox.cpp \
    command.cpp \
    infoutils.cpp \
    qemu.cpp \
    qemusetting.cpp

HEADERS += \
        mainwindow.h \
    buildvbox.h \
    vbox.h \
    command.h \
    infoutils.h \
    qemu.h \
    qemusetting.h

FORMS += \
        mainwindow.ui \
    qemusetting.ui

# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target

RESOURCES += \
    trans.qrc \
    图标.qrc

DISTFILES += \
    en_US.qm \
    en_US.ts

# 编译时拷贝所需文件
file_need.files += Windows7X64Auto.iso \
    Windows7X86Auto.iso \
    kvm-ok \
    AAVMF32_CODE.fd \
    deepin-wine-runner.svg \
    OVMF.fd \
    QEMU_AARCH64_EFI.fd \
    QEMU_EFI_LOONG64_7.1.fd \
    test.qcow2
file_need.path += $$OUT_PWD
COPIES += file_need
system(chmod 777 $$OUT_PWD/kvm-ok)
