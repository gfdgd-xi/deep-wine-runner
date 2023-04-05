#!/usr/bin/env python3
import sys
import os
import atexit

PIDFILE = '/tmp/deepin-wine-runner.pid'

#程序结束时清理pid
@atexit.register
def remove_pid():
    with open(PIDFILE) as pidfile:
        pidlst = pidfile.readlines()
    pidlst.remove(str(PID)+'\n')
    with open(PIDFILE,'w') as pidfile:
        pidfile.writelines(pidlst)

#更新时结束进程
def main():
    for i in open(PIDFILE):
        try:
            os.kill(int(i),15)
        except ProcessLookupError:
            pass
    os.remove(PIDFILE)

#当该程序被直接执行时，执行结束进程操作。如果是导入的形式，则只是记录pid
if __name__ == '__main__':
    sys.exit(main())
else:
    #获取进程pid，用于更新时结束进程
    PID = os.getpid()
    with open(PIDFILE,'a') as pidfile:
        print(PID,file=pidfile) #使用print可以在行末输出换行符，而且可以省去类型转换
