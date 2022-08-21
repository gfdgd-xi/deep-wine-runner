/****************************************************************************
** Meta object code from reading C++ file 'downloadthread.h'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.15.3)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include <memory>
#include "../wine-source/downloadthread.h"
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'downloadthread.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.15.3. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
struct qt_meta_stringdata_DownloadThread_t {
    QByteArrayData data[12];
    char stringdata0[127];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_DownloadThread_t, stringdata0) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
static const qt_meta_stringdata_DownloadThread_t qt_meta_stringdata_DownloadThread = {
    {
QT_MOC_LITERAL(0, 0, 14), // "DownloadThread"
QT_MOC_LITERAL(1, 15, 14), // "MessageBoxInfo"
QT_MOC_LITERAL(2, 30, 0), // ""
QT_MOC_LITERAL(3, 31, 4), // "info"
QT_MOC_LITERAL(4, 36, 15), // "MessageBoxError"
QT_MOC_LITERAL(5, 52, 12), // "ChangeDialog"
QT_MOC_LITERAL(6, 65, 16), // "QProgressDialog*"
QT_MOC_LITERAL(7, 82, 6), // "dialog"
QT_MOC_LITERAL(8, 89, 5), // "value"
QT_MOC_LITERAL(9, 95, 13), // "downloadBytes"
QT_MOC_LITERAL(10, 109, 10), // "totalBytes"
QT_MOC_LITERAL(11, 120, 6) // "Finish"

    },
    "DownloadThread\0MessageBoxInfo\0\0info\0"
    "MessageBoxError\0ChangeDialog\0"
    "QProgressDialog*\0dialog\0value\0"
    "downloadBytes\0totalBytes\0Finish"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_DownloadThread[] = {

 // content:
       8,       // revision
       0,       // classname
       0,    0, // classinfo
       4,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       4,       // signalCount

 // signals: name, argc, parameters, tag, flags
       1,    1,   34,    2, 0x06 /* Public */,
       4,    1,   37,    2, 0x06 /* Public */,
       5,    4,   40,    2, 0x06 /* Public */,
      11,    0,   49,    2, 0x06 /* Public */,

 // signals: parameters
    QMetaType::Void, QMetaType::QString,    3,
    QMetaType::Void, QMetaType::QString,    3,
    QMetaType::Void, 0x80000000 | 6, QMetaType::Int, QMetaType::Int, QMetaType::Int,    7,    8,    9,   10,
    QMetaType::Void,

       0        // eod
};

void DownloadThread::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        auto *_t = static_cast<DownloadThread *>(_o);
        (void)_t;
        switch (_id) {
        case 0: _t->MessageBoxInfo((*reinterpret_cast< QString(*)>(_a[1]))); break;
        case 1: _t->MessageBoxError((*reinterpret_cast< QString(*)>(_a[1]))); break;
        case 2: _t->ChangeDialog((*reinterpret_cast< QProgressDialog*(*)>(_a[1])),(*reinterpret_cast< int(*)>(_a[2])),(*reinterpret_cast< int(*)>(_a[3])),(*reinterpret_cast< int(*)>(_a[4]))); break;
        case 3: _t->Finish(); break;
        default: ;
        }
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        switch (_id) {
        default: *reinterpret_cast<int*>(_a[0]) = -1; break;
        case 2:
            switch (*reinterpret_cast<int*>(_a[1])) {
            default: *reinterpret_cast<int*>(_a[0]) = -1; break;
            case 0:
                *reinterpret_cast<int*>(_a[0]) = qRegisterMetaType< QProgressDialog* >(); break;
            }
            break;
        }
    } else if (_c == QMetaObject::IndexOfMethod) {
        int *result = reinterpret_cast<int *>(_a[0]);
        {
            using _t = void (DownloadThread::*)(QString );
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&DownloadThread::MessageBoxInfo)) {
                *result = 0;
                return;
            }
        }
        {
            using _t = void (DownloadThread::*)(QString );
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&DownloadThread::MessageBoxError)) {
                *result = 1;
                return;
            }
        }
        {
            using _t = void (DownloadThread::*)(QProgressDialog * , int , int , int );
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&DownloadThread::ChangeDialog)) {
                *result = 2;
                return;
            }
        }
        {
            using _t = void (DownloadThread::*)();
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&DownloadThread::Finish)) {
                *result = 3;
                return;
            }
        }
    }
}

QT_INIT_METAOBJECT const QMetaObject DownloadThread::staticMetaObject = { {
    QMetaObject::SuperData::link<QThread::staticMetaObject>(),
    qt_meta_stringdata_DownloadThread.data,
    qt_meta_data_DownloadThread,
    qt_static_metacall,
    nullptr,
    nullptr
} };


const QMetaObject *DownloadThread::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *DownloadThread::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_meta_stringdata_DownloadThread.stringdata0))
        return static_cast<void*>(this);
    return QThread::qt_metacast(_clname);
}

int DownloadThread::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QThread::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 4)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 4;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 4)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 4;
    }
    return _id;
}

// SIGNAL 0
void DownloadThread::MessageBoxInfo(QString _t1)
{
    void *_a[] = { nullptr, const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t1))) };
    QMetaObject::activate(this, &staticMetaObject, 0, _a);
}

// SIGNAL 1
void DownloadThread::MessageBoxError(QString _t1)
{
    void *_a[] = { nullptr, const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t1))) };
    QMetaObject::activate(this, &staticMetaObject, 1, _a);
}

// SIGNAL 2
void DownloadThread::ChangeDialog(QProgressDialog * _t1, int _t2, int _t3, int _t4)
{
    void *_a[] = { nullptr, const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t1))), const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t2))), const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t3))), const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t4))) };
    QMetaObject::activate(this, &staticMetaObject, 2, _a);
}

// SIGNAL 3
void DownloadThread::Finish()
{
    QMetaObject::activate(this, &staticMetaObject, 3, nullptr);
}
QT_WARNING_POP
QT_END_MOC_NAMESPACE
