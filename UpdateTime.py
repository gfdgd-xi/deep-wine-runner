#!/usr/bin/env python3
# 更新构建时间
import os
import sys
import json
import platform
import datetime
programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
with open(sys.argv[1], "r") as file:
    info = json.loads(file.read())
info["Time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + platform.platform()
with open(sys.argv[1], "w") as file:
    file.write(json.dumps(info, ensure_ascii=False, indent=4))
