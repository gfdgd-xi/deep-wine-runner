#!/usr/bin/env python3
# 使用系统默认的 python3 运行
###########################################################################################
# 作者：gfdgd xi、为什么您不喜欢熊出没和阿布呢
# 版本：1.8.0
# 更新时间：2022年08月01日
# 感谢：感谢 wine 以及 deepin-wine 团队，提供了 wine 和 deepin-wine 给大家使用，让我能做这个程序
# 基于 Python3 构建
###########################################################################################
#################
# 引入所需的库
#################
import os
import sys
import json
import pyquery
import requests
import urllib.parse as parse

def CleanTerminal():
    os.system("clear")
    print("本软件源来自腾讯软件管家，只会下载文件后缀为“.exe”的文件")
    print("请输入要搜索的内容，如果要结束，请输入“exit”或点击右上角“×”关闭")
    print("无法保证从这里下载的安装包能正常安装/运行")

if __name__ == "__main__":
    if "--help" in sys.argv:
        print("作者：gfdgd xi、为什么您不喜欢熊出没和阿布呢")
        print("版本：1.0.0")
        print("本程序可以更方便的在 wine 容器中安装指定应用")
        sys.exit()
    if len(sys.argv) <= 2 or sys.argv[1] == "" or sys.argv[2] == "":
        print("您未指定需要安装的容器和使用的 wine，无法继续")
        print("参数：")
        print("XXX 参数一 参数二")
        print("参数一为需要安装的容器，参数二为需要使用的wine，两个参数位置不能颠倒")
        sys.exit()

    CleanTerminal()
    while True:
        search = input(">")
        if search.replace(" ", "").replace("\n", "") == "":
            continue
        if search.lower() == "exit":  # 输入“exit”
            break  # 结束程序

        # 获取初步 API
        apiReturn = json.loads(requests.get(f"https://s.pcmgr.qq.com/tapi/web/searchcgi.php?type=search&callback=searchCallback&keyword={parse.quote(search)}&page=1&pernum=30").text[:-2][15:])
        option = 0
        downloadUrl = []
        if not "list" in apiReturn:
            print("没有搜到结果，尝试换一个关键词试试")
            input("按回车键继续")
            CleanTerminal()
            continue
        for i in apiReturn["list"]:  # 遍历选项
            htmlShow = i["xmlInfo"]
            url = pyquery.PyQuery(htmlShow)("url").text()
            if url[-3:] != "exe":  # 格式非 exe，忽略
                continue
            print(option, i["SoftName"], url)
            downloadUrl.append(url)
            option += 1

        if option == 0:
            print("没有搜到结果，尝试换一个关键词试试")
            input("按回车键继续")
            CleanTerminal()
            continue
        while True:
            try:
                choose = input("请输入选项编号（输入“exit”取消） >")
                if choose.lower() == "exit":
                    choose = choose.lower()
                    break
                choose = int(choose)
            except:
                print("输入有误，请正确输入编号")
                continue
            if not 0 <= choose or not choose < len(downloadUrl):
                print("输入的值超出范围，请正确输入编号")
                continue
            break
        if choose == "exit":
            CleanTerminal()
            continue
        print("开始下载……")
        os.system("rm -rf /tmp/wineappstore")
        os.system("mkdir -p /tmp/wineappstore")
        os.system(f"aria2c -x 16 -s 16 -d /tmp/wineappstore -o install.exe \"{downloadUrl[choose]}\"")
        print("开始安装……")
        os.system(f"WINEPREFIX={sys.argv[1]} {sys.argv[2]} /tmp/wineappstore/install.exe")
        print("安装结束……")
        input("按回车键继续……")
        CleanTerminal()
