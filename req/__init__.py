# 此库用于实现 52 版不连接程序服务器
import requests

unConnect = False
with open("/var/lib/dpkg/status", "r") as i:
    unConnect = "Package: spark-deepin-wine-runner-52" in open("/var/lib/dpkg/status", "r").read()
if unConnect:
    print("52专版，将会无法连接服务器")

class Respon:
    text = ""

def get(url, timeout=None): # -> requests.Response:
    if unConnect:
        # 全部 Url 都拦截
        raise Exception("52专版不支持连接服务器")
    if timeout == None:
        return requests.get(url)
    return requests.get(url, timeout=timeout)

def post(url, data, timeout=None):
    if unConnect:
        # 全部 Url 都拦截
        raise Exception("52专版不支持连接服务器")
    if timeout == None:
        return requests.post(url, data)
    return requests.post(url, data, timeout=timeout)