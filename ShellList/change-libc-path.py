#!/bin/bash
import os
import sys
import binascii
def Replace(fileName: str):
    with open(f"{fileName}", "rb") as file:
        data = file.read()
    if (sys.argv[2] == "x86_64"):
        data = data.replace(bytes("/lib64/ld-linux-x86-64.so.2".encode()), 
             bytes("/data/data/com.termux/gfdgd".encode()))  # 替换与被替换需要保证字符数量相同
    if (sys.argv[2] == "aarch64"):
        data = data.replace(bytes("/lib/ld-linux-aarch64.so.1".encode()), 
             bytes("/data/data/com.termux/gfdg".encode()))  # 替换与被替换需要保证字符数量相同
    with open(f"{fileName}", "wb") as file:
        file.write(data)

longest = 0
def Find(path: str):
    global longest
    for i in os.listdir(path):
        newpath = f"{path}/{i}"
        if (len(newpath) > longest):
            longest = len(newpath)
        print(f"\r{newpath}" + " " * (longest - len(newpath)), end="")
        if (os.path.isfile(newpath)):
            Replace(newpath)
        if (os.path.isdir(newpath)):
            Find(newpath)

Find(sys.argv[1])