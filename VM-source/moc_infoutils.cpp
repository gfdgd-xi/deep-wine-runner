/****************************************************************************
** Meta object code from reading C++ file 'infoutils.h'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.15.6)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include <memory>
#include "infoutils.h"
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'infoutils.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.15.6. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
struct qt_meta_stringdata_infoUtils_t {
    QByteArrayData data[9];
    char stringdata0[75];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_infoUtils_t, stringdata0) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
static const qt_meta_stringdata_infoUtils_t qt_meta_stringdata_infoUtils = {
    {
QT_MOC_LITERAL(0, 0, 9), // "infoUtils"
QT_MOC_LITERAL(1, 10, 8), // "RateUnit"
QT_MOC_LITERAL(2, 19, 7), // "RateBit"
QT_MOC_LITERAL(3, 27, 8), // "RateByte"
QT_MOC_LITERAL(4, 36, 6), // "RateKb"
QT_MOC_LITERAL(5, 43, 6), // "RateMb"
QT_MOC_LITERAL(6, 50, 6), // "RateGb"
QT_MOC_LITERAL(7, 57, 6), // "RateTb"
QT_MOC_LITERAL(8, 64, 10) // "RateUnknow"

    },
    "infoUtils\0RateUnit\0RateBit\0RateByte\0"
    "RateKb\0RateMb\0RateGb\0RateTb\0RateUnknow"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_infoUtils[] = {

 // content:
       8,       // revision
       0,       // classname
       0,    0, // classinfo
       0,    0, // methods
       0,    0, // properties
       1,   14, // enums/sets
       0,    0, // constructors
       0,       // flags
       0,       // signalCount

 // enums: name, alias, flags, count, data
       1,    1, 0x0,    7,   19,

 // enum data: key, value
       2, uint(infoUtils::RateBit),
       3, uint(infoUtils::RateByte),
       4, uint(infoUtils::RateKb),
       5, uint(infoUtils::RateMb),
       6, uint(infoUtils::RateGb),
       7, uint(infoUtils::RateTb),
       8, uint(infoUtils::RateUnknow),

       0        // eod
};

void infoUtils::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    (void)_o;
    (void)_id;
    (void)_c;
    (void)_a;
}

QT_INIT_METAOBJECT const QMetaObject infoUtils::staticMetaObject = { {
    QMetaObject::SuperData::link<QObject::staticMetaObject>(),
    qt_meta_stringdata_infoUtils.data,
    qt_meta_data_infoUtils,
    qt_static_metacall,
    nullptr,
    nullptr
} };


const QMetaObject *infoUtils::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *infoUtils::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_meta_stringdata_infoUtils.stringdata0))
        return static_cast<void*>(this);
    return QObject::qt_metacast(_clname);
}

int infoUtils::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QObject::qt_metacall(_c, _id, _a);
    return _id;
}
QT_WARNING_POP
QT_END_MOC_NAMESPACE
