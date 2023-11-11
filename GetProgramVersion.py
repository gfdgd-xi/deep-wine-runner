#!/usr/bin/env python3
# 读取程序版本号
import os
import json
programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
try:
    with open(f"{programPath}/information.json") as file:
        print(json.loads(file.read())["Version"])
except:
    print("1.0.0")