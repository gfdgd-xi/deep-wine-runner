#!/usr/bin/env python3
import os
import sys

def ReadTXT(path):
    with open(path, "r") as file:
        thing = file.read()
    return thing

def WriteTXT(path, data):
    with open(path, "w") as file:
        file.write(data)

debList = sys.argv[1:]
for i in debList:
    # 解包
    os.system("rm -rf /tmp/change-old-to-new")
    os.system(f"dpkg -x '{i}' /tmp/change-old-to-new")
    os.system(f"dpkg -e '{i}' /tmp/change-old-to-new/DEBIAN")
    info = ReadTXT("/tmp/change-old-to-new/DEBIAN/control").replace("spark-dwine-helper | store.spark-app.spark-dwine-helper", "deepin-wine-helper (>= 5.1.30-1)")
    WriteTXT("/tmp/change-old-to-new/DEBIAN/control", info)
    path = os.listdir("/tmp/change-old-to-new/opt/apps")[0]
    info = ReadTXT(f"/tmp/change-old-to-new/opt/apps/{path}/files/run.sh").replace("/opt/deepinwine/tools/spark_run_v4.sh", "/opt/deepinwine/tools/run_v4.sh")
    WriteTXT(f"/tmp/change-old-to-new/opt/apps/{path}/files/run.sh", info)
    os.system(f"dpkg-deb -Z xz -z 0 -b /tmp/change-old-to-new '{os.path.basename(i)}'")
    # 检查是否能正常安装
