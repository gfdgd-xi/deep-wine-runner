#!/usr/bin/env python3
import os
import sys
import json
import base64
import requests
# 读取版本号
programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
with open(f"{programPath}/information.json") as file:
    version = json.loads(file.read())["Version"]
print(requests.get(base64.b64decode("aHR0cHM6Ly9zb3VyY2Vmb3JnZS5uZXQvcHJvamVjdHMvZGVlcC13aW5lLXJ1bm5lci13aW5lLWRvd25sb2FkL2ZpbGVzL2Rvd25sb2FkLXRpbWUv").decode("utf-8") 
                   + version
                   + base64.b64decode("L2Rvd25sb2Fk").decode("utf-8"),
                   timeout=5  # timeout 设置为 5S
                   ).text)