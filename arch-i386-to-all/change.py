#!/usr/bin/env python3
import os
import sys
import random
import subprocess

# 读取文本文档
def ReadTXT(path):
    with open(path, "r") as file:
        result = file.read()
    return result

# 写入文本文档
def WriteTXT(path, things):
    with open(path, "w") as file:
        file.write(things)


for i in sys.argv[1:]:
    #result = subprocess.getoutput(f"apt info '{i}'")
    tempPath = f"/tmp/unpack-wine-{random.randint(0, 1000)}"
    #os.system(f"mkdir -p '{tempPath}/DEBIAN'")
    #result = ReadTXT(f"{tempPath}/DEBIAN/control")
    result = subprocess.getoutput(f"dpkg --info '{i}'")
    package = "demo"
    version = "1.0.0"
    for k in result.splitlines():
        # 删除前后空格
        k = k.strip()
        # 判断架构
        if k[:8] == "Package:":
            package = k[9:].strip()
        if k[:8] == "Version:":
            version = k[9:].strip()
        
        if k[:13] == "Architecture:":
            arch = k[14:].strip()
            if arch != "all":
                print(f"需要转换架构：{arch}=>all")
                print("开始自动转换")
                os.system(f"mkdir -pv '{tempPath}'")
                os.system(f"dpkg -x '{i}' '{tempPath}'")
                os.system(f"dpkg -e '{i}' '{tempPath}/DEBIAN'")
                control = ReadTXT(f"{tempPath}/DEBIAN/control")
                newControl = ""
                for g in control.splitlines():
                    gNoSpace = g.strip()
                    if gNoSpace[:13] == "Architecture:":
                        newControl += "Architecture: all\n"
                        continue
                    if gNoSpace == "Multi-Arch: same":
                        continue
                    newControl += f"{g}\n"
                WriteTXT(f"{tempPath}/DEBIAN/control", newControl)
                os.system(f"dpkg-deb -Z xz -z 9 -b '{tempPath}' '{package}_{version}_all.deb'")
                os.system(f"rm -rfv '{tempPath}'")
                break

