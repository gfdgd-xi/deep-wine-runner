#!/usr/bin/env python3
import os
import sys
import time
import json
import threading
import traceback
import pynput.keyboard as keyboard
keyList = []
'''keyMap = [
    [keyboard.Key.ctrl, keyboard.Key.alt, "j", "ls"]
]'''
keyChangeMap = [
    ["ctrl", keyboard.Key.ctrl],
    ["alt", keyboard.Key.alt],
    ["esc", keyboard.Key.esc],
    ["enter", keyboard.Key.enter],
]
programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
file = open(f"{programPath}/KeyList.json", "r")
keyMap = json.loads(file.read())
for i in range(len(keyMap)):
    for k in range(len(keyMap[i])):
        for j in keyChangeMap:
            if keyMap[i][k] == j[0]:
                keyMap[i][k] = j[1]

def on_press(key):
    try:
        if key.char in keyList:
            # 重复的值就不认了，摊牌了
            return
        keyList.append(key.char)
        print(f'alphanumeric key {key.char} pressed')
    except AttributeError:
        keyList.append(key)
        print(f'special key {key} pressed')

def on_release(key):
    '松开按键时执行。'
    print(f'{key} released')
    try:
        del keyList[keyList.index(key.char)]
    except AttributeError:
        del keyList[keyList.index(key)]
    except:
        traceback.print_exc()

def ReadKey():
    next = False
    command = ""
    for i in keyMap:
        for k in range(0, len(i) - 1):
            k = i[k]
            if not k in keyList:
                next = True
                break
        if not next:
            # 执行命令
            os.system(i[-1])
            # 必须等待按键全部松开才行
            while len(keyList) != 0:
                time.sleep(0.01)


def Read():
    while True:
        ReadKey()
        time.sleep(0.01)

# Lock 锁防止多次调用
if os.path.exists("/tmp/deepin-wine-runner-keyboard-lock"):
    print("不可多次调用")
    print("锁 /tmp/deepin-wine-runner-keyboard-lock 已存在")
    sys.exit(1)
os.mknod("/tmp/deepin-wine-runner-keyboard-lock")
threading.Thread(target=Read).start()
# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
os.remove("/tmp/deepin-wine-runner-keyboard-lock")