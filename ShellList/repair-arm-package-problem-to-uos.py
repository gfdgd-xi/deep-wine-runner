#!/usr/bin/env python3
import os
import sys

def Replace(path):
    "spark-dwine-helper | store.spark-app.spark-dwine-helper"
    "deepin-wine-helper (>= 5.1.30-1)"
    "com.wine-helper.deepin"
    with open(f"{path}/DEBIAN/control", "r") as file:
        data = file.read()
    
    isReplace = False
    isSparkHelper = False
    # 替换 Wine 包名
    data = data.replace("deepin-wine6-stable,", "deepin-wine6-stable | com.deepin-wine6-stable.deepin,")
    data = data.replace("deepin-wine6-stable | deepin-wine6-stable-bcm | deepin-wine6-stable-dcm,", "deepin-wine6-stable | deepin-wine6-stable-bcm | deepin-wine6-stable-dcm | com.deepin-wine6-stable.deepin,")
    if "spark-dwine-helper | store.spark-app.spark-dwine-helper" in data and not isReplace:
        isReplace = True
        isSparkHelper = True
        data = data.replace("spark-dwine-helper | store.spark-app.spark-dwine-helper", "deepin-wine-helper | com.wine-helper.deepin")
        
    if "deepin-wine-helper (>= 5.1.30-1)" in data and not isReplace:
        isReplace = True
        data = data.replace("deepin-wine-helper (>= 5.1.30-1)", "deepin-wine-helper | com.wine-helper.deepin")
    with open(f"{path}/DEBIAN/control", "w") as file:
        file.write(data)
    if isSparkHelper:
        ReplaceSparkHelper(path)

def ReplaceSparkHelper(path):
    name = os.listdir(f"{path}/opt/apps/")[0]
    with open(f"{path}/opt/apps/{name}/files/run.sh", "r") as file:
        data = file.read().replace("/opt/deepinwine/tools/spark_run_v4.sh", "/opt/deepinwine/tools/run_v4.sh")
    with open(f"{path}/opt/apps/{name}/files/run.sh", "w") as file:
        file.write(data)

if len(sys.argv) <= 1:
    print(f"请加参数，命令示例： {sys.argv[0]} xxx.deb")
    exit(1)

tempPath = "/tmp/turn-deb"
for i in sys.argv[1:]:
    os.system(f"rm -rf '{tempPath}'")
    os.system(f"dpkg -x '{i}' '{tempPath}'")
    os.system(f"dpkg -e '{i}' '{tempPath}/DEBIAN'")
    fileName = os.path.splitext(i)[0]
    # 修改 control 文件
    Replace(tempPath)
    
    os.system(f"dpkg-deb -Z xz -z 0 -b '{tempPath}' '{fileName}-new.deb'")