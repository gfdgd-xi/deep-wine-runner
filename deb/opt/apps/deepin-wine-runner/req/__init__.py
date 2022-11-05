# 此库用于实现 52 版不连接程序服务器
import requests

unConnect = False
with open("/var/lib/dpkg/status", "r") as i:
    unConnect = "Package: spark-deepin-wine-runner-52" in open("/var/lib/dpkg/status", "r").read()
if unConnect:
    print("52专版，将会无法连接服务器")

badUrl = [
    "http://120.25.153.144",
    "https://304626p927.goho.co",
    "https://30x46269h2.goho.co"
]

class Respon:
    text = ""

def get(url, timeout=None): # -> requests.Response:
    if unConnect:
        # 筛选 Url，只有特定的 url 才会被拦截
        for i in badUrl:
            if i in url:
                raise Exception("52专版不支持连接作者服务器")
    if timeout == None:
        return requests.get(url)
    return requests.get(url, timeout=timeout)

def post(url, data, timeout=None):
    if unConnect:
        # 筛选 Url，只有特定的 url 才会被拦截
        for i in badUrl:
            if i in url:
                raise Exception("52专版不支持连接作者服务器")
    if timeout == None:
        return requests.post(url, data)
    return requests.post(url, data, timeout=timeout)