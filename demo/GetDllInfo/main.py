import json
import pyquery
import requests
lists = {}
def A(link):
    r = requests.get(f"http://www.2cto.com/shouce/system/dlllibrary/riched32/default.htm/../{link}")
    r.encoding = "gbk"
    programUrl = pyquery.PyQuery(r.text)
    iii = 0
    #print()
    miaoshu = ""
    for i in programUrl("font").items():
        if i.attr.size == "2" and iii == 4: #and not "<a" in i.text():
            #print(i.text())
            miaoshu = i.text()
            pass
        if i.attr.size == "2" and iii == 5: #and not "<a" in i.text():
            #print(i)
            for k in i.items("font"):
                if link.replace("../", "").replace("/default.htm", "") + ".dll" == "default.htm.dll":
                    continue
                print((link.replace("../", "").replace("/default.htm", "") + ".dll").lower())
                lists[(link.replace("../", "").replace("/default.htm", "") + ".dll").lower()] = miaoshu + "\n" + k.text().splitlines()[0].replace("属于：", "属于：").replace("系统 DLL文件：", "\n系统 DLL文件：").replace("常见错误：", "\n常见错误：") + "\n\n资料来源：https://www.2cto.com/shouce/system/dlllibrary"
                break
            #things = i.text()
            #print(things)
            #print(things[things.index("应用程序DLL文件")])
        iii += 1
        if iii == 3:
            #break
            pass
# https://www.2cto.com/shouce/system/dlllibrary/3dfxcmn/default.htm
# https://www.2cto.com/shouce/system/dlllibrary/2ndsrch/default.htm
# https://www.2cto.com/shouce/system/dlllibrary/admxprox/default.htm
for b in ["https://www.2cto.com/shouce/system/dlllibrary/3dfxcmn/default.htm",
"https://www.2cto.com/shouce/system/dlllibrary/2ndsrch/default.htm", "https://www.2cto.com/shouce/system/dlllibrary/admxprox/default.htm"]:
    r = requests.get(b)
    r.encoding = "gbk"
    programUrl = pyquery.PyQuery(r.text)
#programUrl = pyquery.PyQuery(requests.get(f"http://www.2cto.com/shouce/system/dlllibrary/riched32/default.htm", ).text)
    '''for i in programUrl("table table").items():
    print(i)'''
    iii = 0
    for i in programUrl("font a").items():
        #if i.attr.size == "2":
        A(i.attr.href)
     #   for k in i.items():
      #      print(k)
#exit()
#exit()
with open("lists.json", "w") as file:
    file.write(json.dumps(lists, ensure_ascii=False))