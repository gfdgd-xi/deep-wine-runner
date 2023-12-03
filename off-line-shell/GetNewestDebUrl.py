#!/usr/bin/env python3
import json
import requests
print(requests.get("http://update.gfdgdxi.top/update.json").json()["Url"][0])