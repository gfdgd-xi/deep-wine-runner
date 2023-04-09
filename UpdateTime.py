#!/usr/bin/env python3
# 更新构建时间
import os
import json
import platform
import datetime
programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
with open(f"{programPath}/deb/opt/apps/deepin-wine-runner/information.json", "r") as file:
    info = json.loads(file.read())
info["Time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + platform.platform()
with open(f"{programPath}/deb/opt/apps/deepin-wine-runner/information.json", "w") as file:
    file.write(json.dumps(info, ensure_ascii=False, indent=4))
