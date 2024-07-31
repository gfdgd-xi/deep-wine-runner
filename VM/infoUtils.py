PROC_UPTIME = "/proc/uptime"
PROC_CPU =    "/proc/stat"
PROC_MEM =    "/proc/meminfo"
PROC_NET =    "/proc/net/dev"

import enum
from PyQt5.QtCore import *

class infoUtils:
    class RateUnit(enum.Enum):
        RateBit = 0,
        RateByte = 1,
        RateKb = 2,
        RateMb = 3,
        RateGb = 4,
        RateTb = 5,
        RateUnknow = 6

    class Sensitive(enum.Enum):
        Default = 0,  # 大小写混合
        Upper = 1,    # 全部大写
        Lower = 2     # 全部小写
    
    def setRateUnitSensitive(self, unit: RateUnit, sensitive: Sensitive):
        if (sensitive == self.Sensitive.Default):
            if (unit == self.RateUnit.RateBit):
                return str("b/s")
            elif (unit == self.RateUnit.RateByte):
                return str("B/s")
            elif (unit == self.RateUnit.RateKb):
                return str("Kb/s")
            elif (unit == self.RateUnit.RateMb):
                return str("Mb/s")
            elif (unit == self.RateUnit.RateGb):
                return str("Gb/s")
            elif (unit == self.RateUnit.RateTb):
                return str("Tb/s")
            else:
                # print("Sensitive::Default,  RateUnit is RateUnknow.")
                return str("")
        elif (sensitive == self.Sensitive.Upper): 
            if (unit == self.RateUnit.RateBit):
                return str("BIT/S")
            elif (unit == self.RateUnit.RateByte):
                return str("B/S")
            elif (unit == self.RateUnit.RateKb):
                return str("KB/S")
            elif (unit == self.RateUnit.RateMb):
                return str("MB/S")
            elif (unit == self.RateUnit.RateGb):
                return str("GB/S")
            elif (unit == self.RateUnit.RateTb):
                return str("TB/S")
            else:
                #print("Sensitive::Upper,  RateUnit is RateUnknow.")
                return str("")
        elif (sensitive == self.Sensitive.Lower):
            if (unit == self.RateUnit.RateBit):
                return str("bit/s")
            elif (unit == self.RateUnit.RateByte):
                return str("b/s")
            elif (unit == self.RateUnit.RateKb):
                return str("kb/s")
            elif (unit == self.RateUnit.RateMb):
                return str("mb/s")
            elif (unit == self.RateUnit.RateGb):
                return str("gb/s")
            elif (unit == self.RateUnit.RateTb):
                return str("tb/s")
            else:
                #qDebug()<<str("Sensitive::Lower,  RateUnit is RateUnknow.")
                return str("")
        else: 
            # qDebug()<<str("Sensitive is RateUnknow.")
            return str("")
        
    # TODO unit 在原来是指针，这里还没做处理
    def autoRateUnits(self, speed: int, unit: RateUnit) -> float:
        # 自动判断合适的速率单位,默认传进来的是 Byte
        # * bit    0 ~ 7 位 (不到 1 字节)
        # * Byte   1    ~ 2^10  Byte
        # * KB     2^10 ~ 2^20  Byte
        # * MB     2^20 ~ 2^30  Byte
        # * GB     2^30 ~ 2^40  Byte
        # * TB     2^40 ~ 2^50  Byte
        if (unit != self.RateUnit.RateByte):
            #print("请先将单位转为字节(byte)后再传参")
            return -1
        sp = 0
        if (0 <= speed and speed < pow(2, 10)):
            unit = self.RateUnit.RateByte
            sp = speed
        elif (pow(2, 10) <= speed and speed < pow(2, 20)):
            unit = self.RateUnit.RateKb
            sp = float(speed / pow(2, 10) * 1.0)
        elif (pow(2, 20) <= speed and speed < pow(2, 30)):
            unit = self.RateUnit.RateMb
            sp = float(speed / pow(2, 20) * 1.0)
        elif (pow(2, 30) <= speed and speed < pow(2, 40)):
            unit = self.RateUnit.RateGb
            sp = float(speed / pow(2, 30) * 1.0)
        elif (pow(2, 40) <= speed and speed < pow(2, 50)):
            unit = self.RateUnit.RateTb
            sp = float(speed / pow(2, 40) * 1.0)
        else:
            unit = self.RateUnit.RateUnknow
            # qDebug()<<"本设备网络速率单位传输超过 TB, 或者低于 0 Byte."
            sp = -1
        return sp
    
    # TODO run,idle 在原来是指针，这里还没做处理
    def uptime(self):
        file = QFile(PROC_UPTIME) # /proc/uptime
        if(not file.open(QIODevice.ReadOnly or QIODevice.Text)):
            return
        stream = QTextStream(file)
        line = stream.readLine()
        list = line.split(QRegExp("\\s{1,}"))
        if(list.count()):
            run = float(list[0])
            idle = float(list[1])
        file.close()
        return run, idle

    # TODO netDown, netUpload 在原来是指针，这里还没做处理
    def netRate(self, netDown, netUpload):
        file = QFile(PROC_NET) #  /proc/net/dev
        if (not file.open(QIODevice.ReadOnly or QIODevice.Text)):  # 在读取时，把行尾结束符修改为 '\n'； 在写入时，把行尾结束符修改为本地系统换行风格，比如Windows文本换行是 "\r\n"
            return
        down = 0
        upload = 0
        stream = QTextStream(file)
        line = stream.readLine()
        line  = stream.readLine()
        line  = stream.readLine()
        while (not line.isNull()):
            line = line.trimmed()
            list = line.split(QRegExp("\\s{1,}"))   # 匹配任意 大于等于1个的 空白字符
            if (list.count()):
                down = int(list[1])
                upload = int(list[9])
            netDown += down
            netUpload += upload
            line  = stream.readLine()
        file.close()

    '''def cpuRate(self, cpuAll, cpuFree):
        cpuAll = cpuFree = 0
        ok = False
        file = QFile(PROC_CPU) # /proc/stat
        if(not file.open(QIODevice.ReadOnly or QIODevice.Text)):
            return
        stream = QTextStream(file)
        line = stream.readLine()
        if (line != None):
            list = line.split(QRegExp("\\s{1,}"))
            for (auto v = list.begin() + 1 v != list.end() ++v)
                cpuAll += (*v).toLong(&ok)
            cpuFree = list.at(4).toLong(&ok)
        file.close()'''

    def memoryRate(self):
        memory = memoryAll = 0
        swap = swapAll = 0
        ok = False
        file = QFile(PROC_MEM) # /proc/meminfo
        if (not file.open(QIODevice.ReadOnly or QIODevice.Text)):
            return
        stream = QTextStream(file)
        buff = [0]
        for i in range(16):
            line = stream.readLine()
            list = line.split(QRegExp("\\s{1,}"))
            buff[i] = int(list[1])
        memoryAll = buff[0]
        memory = buff[0] - buff[2]
        swapAll = buff[14]
        swap = buff[14] - buff[15]
        file.close()
        return memory, memoryAll, swap, swapAll