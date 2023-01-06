import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import zipfile
import subprocess
import re

class getsavexml():

    def savexml(self,apkFilePath,xmlpath,iconSavePath):
        cmddumpid = "aapt dump xmltree "+ apkFilePath + " " + xmlpath
        print(cmddumpid)
        xmltree =  subprocess.getoutput(cmddumpid)
        xmls = xmltree.splitlines()
        # find strs ,print next line
        def FindStrs(lines,strs):
            i=0
            while i < len(lines):
                if re.search(strs,lines[i]):
                    tmpstr = lines[i+1]
                    i += 1
                    Resultstr = tmpstr.split(":")[-1].split("=")[-1].split("0x")[-1] 
                    return Resultstr
                else:
                    i += 1
        #从apk的信息中获取前后景图片的ID号
        backimgid =  FindStrs(xmls,"background")
        foreimgid =  FindStrs(xmls,"foreground")
        print(backimgid)
        print(foreimgid)

        # 直接从apk resource文件获取前后两层图片路径及ID字符串
        resource =  subprocess.getoutput("aapt dump --values resources " +  apkFilePath + "| grep -iE -A1 " +  "\"" + backimgid + "|" + foreimgid + "\"")
        resourcelines = resource.splitlines()
        print(resourcelines)

        # 从过滤出的字符串中获取所有相同ID的图片路径
        def Findpicpath(lines,imgid):
            i=0
            Resultstr = []
            while i < len(lines):
                if re.search(imgid,lines[i]) and re.search("string8",lines[i+1]) :
                    print(lines[i+1])
                    tmpstr = lines[i+1].replace("\"","")
                    i += 1 
                    Resultstr.append(tmpstr.split()[-1])
                else:
                    i += 1
            return Resultstr

        #获取所有带前后图片ID的图片路径（相同背景或者前景的图片ID但分辨率不一样）
        backimgs =  Findpicpath(resourcelines,backimgid)
        foreimgs =  Findpicpath(resourcelines,foreimgid)
        print(backimgs)
        print(foreimgs)
        #获取分辨率最高的图片路径
        def getmaxsize(imgs):
            j = 0
            size=(0,0)
            zipapk = zipfile.ZipFile(apkFilePath)
            imgpath = ""
            while j < len(imgs):
                print(imgs[j])
                img = Image.open(zipapk.open(imgs[j]))
                print(imgs[j])
                print(img.size)
                if size < img.size:
                    size = img.size
                    imgpath = imgs[j]
                j += 1
            return imgpath

        # 获取到文件列表后，进行比较分辨率，选取分辨率最高的张图片
        iconbackpath = getmaxsize(backimgs)
        iconforepath = getmaxsize(foreimgs)
        print(iconbackpath + " " + iconforepath)

        #从APK文件获取最终图片
        zipapk = zipfile.ZipFile(apkFilePath)
        iconback = zipapk.open(iconbackpath)
        iconfore = zipapk.open(iconforepath)


        # 叠加图片，mask 设置前景为蒙版
        iconbackimg =  Image.open(iconback).convert("RGBA")
        iconforeimg =  Image.open(iconfore).convert("RGBA")
        iconbackimg.paste(iconforeimg,mask=iconforeimg)


        # 圆角图片函数，网上拷贝的
        def circle_corner(img, radii):  #把原图片变成圆角，这个函数是从网上找的，原址 https://www.pyget.cn/p/185266
            """
            圆角处理
            :param img: 源图象。
            :param radii: 半径，如：30。
            :return: 返回一个圆角处理后的图象。
            """
            # 画圆（用于分离4个角）
            circle = Image.new('L', (radii * 2, radii * 2), 0)  # 创建一个黑色背景的画布
            draw = ImageDraw.Draw(circle)
            draw.ellipse((0, 0, radii * 2, radii * 2), fill=255)  # 画白色圆形
            # 原图
            img = img.convert("RGBA")
            w, h = img.size
            # 画4个角（将整圆分离为4个部分）
            alpha = Image.new('L', img.size, 255)
            alpha.paste(circle.crop((0, 0, radii, radii)), (0, 0))  # 左上角
            alpha.paste(circle.crop((radii, 0, radii * 2, radii)), (w - radii, 0))  # 右上角
            alpha.paste(circle.crop((radii, radii, radii * 2, radii * 2)), (w - radii, h - radii))  # 右下角
            alpha.paste(circle.crop((0, radii, radii, radii * 2)), (0, h - radii))  # 左下角
            # alpha.show()
            img.putalpha(alpha)  # 白色区域透明可见，黑色区域不可见
            return img

        #  圆角半径1/8边长,保存icon图片
        w,h = iconbackimg.size
        iconimg = circle_corner(iconbackimg,int(w/8))
        iconimg.save(iconSavePath)

