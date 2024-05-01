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
    info = ReadTXT("/tmp/change-old-to-new/DEBIAN/control").replace(": loongarch64", ": loong64").replace("Depends: ", "Depends: liblol, ")
    WriteTXT("/tmp/change-old-to-new/DEBIAN/control", info)
    os.system(f"dpkg-deb -Z xz -z 9 -b /tmp/change-old-to-new '{os.path.basename(i).replace('_loongarch64', '_loong64')}'")
    # 检查是否能正常安装
