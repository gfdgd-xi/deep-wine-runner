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
print(requests.get(base64.b64decode("aHR0cDovLzEyMC4yNS4xNTMuMTQ0L3NwYXJrLWRlZXBpbi13aW5lLXJ1bm5lci9JbnN0YWxsLnBocD9WZXJzaW9uPQ==").decode("utf-8") + version).text)