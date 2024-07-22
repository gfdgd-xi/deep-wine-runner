#!/usr/bin/env python3
import os
import json
import requests
import traceback

typeList = [
    "Auto",
    "ZH_CN2JA",
    "ZH_CN2KR",
    "ZH_CN2EN"
]

class Trans():
    isTrans = False
    unCloudTrans = False
    word = {}
    fileName = ""

    def __init__(self, lang="zh_CN", fileName=f"trans.json") -> None:
        self.fileName = fileName
        self.isTrans = (lang != "zh_CN")
        if self.isTrans:
            try:
                if not os.path.exists(fileName):
                    with open(fileName, "w") as file:
                        file.write("{}")
                with open(fileName, "r") as file:
                    self.word = json.loads(file.read())
            except:
                traceback.print_exc()
                self.isTrans = False

    def transe(self, temp, text) -> str:
        if not self.isTrans:
            return text
        try:
            return self.word[text].replace("（", "(").replace("）", ")")
        except:
            # 网络翻译接口已废弃
            return text
