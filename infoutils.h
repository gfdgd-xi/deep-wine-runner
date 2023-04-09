#ifndef INFOUTILS_H
#define INFOUTILS_H

#include <QObject>

#define PROC_UPTIME  "/proc/uptime"
#define PROC_CPU     "/proc/stat"
#define PROC_MEM     "/proc/meminfo"
#define PROC_NET     "/proc/net/dev"

class infoUtils : public QObject
{
    Q_OBJECT

public:
    enum RateUnit {
        RateBit,
        RateByte,
        RateKb,
        RateMb,
        RateGb,
        RateTb,
        RateUnknow
    };
    Q_ENUM(RateUnit)

    enum Sensitive {
        Default,  // 大小写混合
        Upper,    // 全部大写
        Lower     // 全部小写
    };
public:
    explicit infoUtils(QObject *parent = nullptr);

    static QString setRateUnitSensitive(RateUnit unit, Sensitive sensitive);
    static double autoRateUnits(long speed, RateUnit &unit);

    static void uptime(double &run, double &idle);
    static void netRate(long &netDown, long &netUpload);
    static void cpuRate(long &cpuAll, long &cpuFree);
    static void memoryRate(long &memory, long &memoryAll, long &swap, long &swapAll);

signals:

public slots:
};

#endif // INFOUTILS_H
