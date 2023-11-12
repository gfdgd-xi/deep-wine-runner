#!/bin/bash
# 读取程序版本号
cd `dirname $0`
export PROGRAMVERSION=`python3 GetProgramVersion.py`
export SIZE=`du /tmp/spark-deepin-wine-runner-builder/ | tail -n1 | awk '{print  $1}'`
sed -i "s%@@VERSION@@%$PROGRAMVERSION%g" /tmp/spark-deepin-wine-runner-builder/DEBIAN/control
sed -i "s%@@SIZE@@%$SIZE%g" /tmp/spark-deepin-wine-runner-builder/DEBIAN/control