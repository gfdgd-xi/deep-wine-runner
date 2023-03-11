#!/usr/bin/env python3
import os
def Remove(path):
    for i in os.listdir(path):
        nowPath = f"{path}/{i}"
        if os.path.isdir(nowPath):
            if i == "__pycache__":
                os.system(f"rm -rfv '{nowPath}'")
            else:
                Remove(nowPath)
programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
debPath = f"{programPath}/"
Remove(debPath)
