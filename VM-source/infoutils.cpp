#include "infoutils.h"

#include <QFile>
#include <QTextStream>
#include <QtMath>

infoUtils::infoUtils(QObject *parent) : QObject(parent)
{

}

QString infoUtils::setRateUnitSensitive(infoUtils::RateUnit unit, infoUtils::Sensitive sensitive)
{
    switch (sensitive) {
    case Sensitive::Default: {
        switch (unit) {
        case RateUnit::RateBit:
            return QString("b/s");
        case RateUnit::RateByte:
            return QString("B/s");
        case RateUnit::RateKb:
            return QString("Kb/s");
        case RateUnit::RateMb:
            return QString("Mb/s");
        case RateUnit::RateGb:
            return QString("Gb/s");
        case RateUnit::RateTb:
            return QString("Tb/s");
        default:
//            qDebug()<<QString("Sensitive::Default,  RateUnit is RateUnknow.");
            return QString("");
        }
    }
    case Sensitive::Upper: {
        switch (unit) {
        case RateUnit::RateBit:
            return QString("BIT/S");
        case RateUnit::RateByte:
            return QString("B/S");
        case RateUnit::RateKb:
            return QString("KB/S");
        case RateUnit::RateMb:
            return QString("MB/S");
        case RateUnit::RateGb:
            return QString("GB/S");
        case RateUnit::RateTb:
            return QString("TB/S");
        default:
//            qDebug()<<QString("Sensitive::Upper,  RateUnit is RateUnknow.");
            return QString("");
        }
    }
    case Sensitive::Lower: {
        switch (unit) {
        case RateUnit::RateBit:
            return QString("bit/s");
        case RateUnit::RateByte:
            return QString("b/s");
        case RateUnit::RateKb:
            return QString("kb/s");
        case RateUnit::RateMb:
            return QString("mb/s");
        case RateUnit::RateGb:
            return QString("gb/s");
        case RateUnit::RateTb:
            return QString("tb/s");
        default:
//            qDebug()<<QString("Sensitive::Lower,  RateUnit is RateUnknow.");
            return QString("");
        }
    }
    default: {
//        qDebug()<<QString("Sensitive is RateUnknow.");
        return QString("");
    }
    }
}

double infoUtils::autoRateUnits(long speed, infoUtils::RateUnit &unit)
{
    /* 自动判断合适的速率单位,默认传进来的是 Byte
     * bit    0 ~ 7 位 (不到 1 字节)
     * Byte   1    ~ 2^10  Byte
     * KB     2^10 ~ 2^20  Byte
     * MB     2^20 ~ 2^30  Byte
     * GB     2^30 ~ 2^40  Byte
     * TB     2^40 ~ 2^50  Byte
     */

    if (unit != infoUtils::RateByte) {
//        qDebug()<<"请先将单位转为字节(byte)后再传参";
        return -1;
    }

    double sp = 0;
    if (0 <= speed && speed < qPow(2, 10)) {
        unit = infoUtils::RateByte;
        sp = speed;
    } else if (qPow(2, 10) <= speed && speed < qPow(2, 20)) {
        unit = infoUtils::RateKb;
        sp = static_cast<double>(speed / qPow(2, 10) * 1.0);
    } else if (qPow(2, 20) <= speed && speed < qPow(2, 30)) {
        unit = infoUtils::RateMb;
        sp = static_cast<double>(speed / qPow(2, 20) * 1.0);
    } else if (qPow(2, 30) <= speed && speed < qPow(2, 40)) {
        unit = infoUtils::RateGb;
        sp = static_cast<double>(speed / qPow(2, 30) * 1.0);
    } else if (qPow(2, 40) <= speed && speed < qPow(2, 50)) {
        unit = infoUtils::RateTb;
        sp = static_cast<double>(speed / qPow(2, 40) * 1.0);
    } else {
        unit = infoUtils::RateUnknow;
//        qDebug()<<"本设备网络速率单位传输超过 TB, 或者低于 0 Byte.";
        sp = -1;
    }

    return sp;
}

void infoUtils::uptime(double &run, double &idle)
{
    QFile file(PROC_UPTIME); // /proc/uptime
    if(!file.open(QIODevice::ReadOnly | QIODevice::Text)) {
        return;
    }

    QTextStream stream(&file);
    QString line = stream.readLine();
    QStringList list = line.split(QRegExp("\\s{1,}"));
    if(!list.isEmpty()) {
        run = list.at(0).toDouble();
        idle = list.at(1).toDouble();
    }
    file.close();
}

void infoUtils::netRate(long &netDown, long &netUpload)
{
    QFile file(PROC_NET); //  /proc/net/dev
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text)) {  // 在读取时，把行尾结束符修改为 '\n'； 在写入时，把行尾结束符修改为本地系统换行风格，比如Windows文本换行是 "\r\n"
        return;
    }

    long down = 0;
    long upload = 0;
    QTextStream stream(&file);
    QString line = stream.readLine();
    line  = stream.readLine();
    line  = stream.readLine();
    while (!line.isNull()) {
        line = line.trimmed();
        QStringList list = line.split(QRegExp("\\s{1,}"));   // 匹配任意 大于等于1个的 空白字符

        if (!list.isEmpty()) {
            down = list.at(1).toLong();
            upload = list.at(9).toLong();
        }

        netDown += down;
        netUpload += upload;
        line  = stream.readLine();
    }

    file.close();
}

void infoUtils::cpuRate(long &cpuAll, long &cpuFree)
{
    cpuAll = cpuFree = 0;
    bool ok = false;

    QFile file(PROC_CPU); // /proc/stat
    if(!file.open(QIODevice::ReadOnly | QIODevice::Text)) {
        return;
    }

    QTextStream stream(&file);
    QString line = stream.readLine();
    if (!line.isNull()) {
        QStringList list = line.split(QRegExp("\\s{1,}"));
        for (auto v = list.begin() + 1; v != list.end(); ++v)
            cpuAll += (*v).toLong(&ok);

        cpuFree = list.at(4).toLong(&ok);
    }

    file.close();
}

void infoUtils::memoryRate(long &memory, long &memoryAll, long &swap, long &swapAll)
{
    memory = memoryAll = 0;
    swap = swapAll = 0;
    bool ok = false;

    QFile file(PROC_MEM); // /proc/meminfo
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
        return;

    QTextStream stream(&file);
    long buff[16] = {0};
    for (int i = 0; i <= 15; ++i) {
        QString line = stream.readLine();
        QStringList list = line.split(QRegExp("\\s{1,}"));
        buff[i] = list.at(1).toLong(&ok);
    }

    memoryAll = buff[0];
    memory = buff[0] - buff[2];
    swapAll = buff[14];
    swap = buff[14] - buff[15];

    file.close();
}
