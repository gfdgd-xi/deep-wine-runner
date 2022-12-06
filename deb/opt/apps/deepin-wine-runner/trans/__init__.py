#!/usr/bin/env python3
import os
import json
import requests
import traceback

class Trans():
    isTrans = False
    unCloudTrans = True
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
            return self.word[text]
        except:
            if self.unCloudTrans:
                return text
            # 机翻
            data = { 'doctype': 'json', 'type': 'auto','i': text}
            jsonReturn = requests.post("http://fanyi.youdao.com/translate", data=data).json()["translateResult"]
            transText = ""
            for i in jsonReturn:
                print(i[0])
                transText += f'{i[0]["tgt"]}\n'
            if "\n" in text:
                transText = transText.replace("\n\n", "\n")[:-1]
            else:
                transText = transText[:-1]
            self.word[text] = transText
            try:
                with open(self.fileName, "w") as file:
                    file.write(json.dumps(self.word, ensure_ascii=False))
            except:
                traceback.print_exc()
            print(f"{text}=>{transText}")
            return transText