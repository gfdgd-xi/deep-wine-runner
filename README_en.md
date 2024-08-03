<p width=100px align="center"><img src="https://storage.deepin.org/thread/202208031419283599_deepin-wine-runner.png"></p>
<h1 align="center">Wine Runner 3.4.0.1</h1>
<hr>
<a href='https://gitee.com/gfdgd-xi/deep-wine-runner/stargazers'><img src='https://gitee.com/gfdgd-xi/deep-wine-runner/badge/star.svg?theme=dark' alt='star'></img></a>
<a href='https://gitee.com/gfdgd-xi/deep-wine-runner/members'><img src='https://gitee.com/gfdgd-xi/deep-wine-runner/badge/fork.svg?theme=dark' alt='fork'></img></a>  

## Introduce
Wine Runner is a program that help Linux user to run Windows program. However, 

![截图_选择区域_20221002221112.png](https://storage.deepin.org/thread/202210022215217037_截图_选择区域_20221002221112.png)  

[![star](https://gitee.com/gfdgd-xi/deep-wine-runner/badge/star.svg?theme=dark)](https://gitee.com/gfdgd-xi/deep-wine-runner/stargazers)    
最后感谢 [@鹤舞白沙](https://bbs.deepin.org/user/227203) 编写的《Wine运行器和Wine打包器傻瓜式使用教程（小白专用）》，链接：https://bbs.deepin.org/post/246837  

Wine Runner Packager Video tutorial: https://www.bilibili.com/video/BV1Bh4y1Q7nT/  
Wine Runner QQ communication group:762985460  

## Program Support Architecture
Runner is able to run for common architecture if these system can run Python.  
Non-x86 system will use `box86/box64`, `exagear`, `qemu` and so on.

## Wine Runner Auto Builder(Newest Version)
This version can't sure what bug will happen when you are using.  
Download Website: https://github.com/gfdgd-xi/deep-wine-runner/actions/workflows/auto-building.yml  

## Which App Store You Can Download Wine Runner
### Deepin/UOS App Store
![图片.png](https://storage.deepin.org/thread/202304192211278050_图片.png)  

### Spark Store
![图片.png](https://storage.deepin.org/thread/202304192212308212_图片.png)  
### Loongson App Store
![图片.png](https://storage.deepin.org/thread/20230603201852396_图片.png)

## Git Branch Introduce
### main
The main branch

## Different Of Version(It No longer Distinguishing From 3.1.0)
### Normal
Normal Version(It usually from Gitee, Github, Gitlink, etc)
### `-spark` In Version
Install runner from Spark Store
### `-uos` In Version
Install runner from Deepin/UOS App Store, and you can install without open the develop mode.
### `-52` In Version
It only release for 52pojie, and some function was removed such as updater, bug uploader and so on.  
![image.png](https://storage.deepin.org/thread/202209251259142818_image.png)  
Nobody want to see this error when you are using.  

## Program Tips
I don't want to write, it's too long and too old.

## Update Log
### 3.4.0.1(August 18th, 2023)
1. **Repair some machine tips `无效的压缩参数` when you are packing program in Wine Runner Packager, you also can see this isscue: https://gitee.com/gfdgd-xi/deep-wine-runner/issues/I7SMTJ**
2. **Runner support to set program font size, you also can see this isscue: https://gitee.com/gfdgd-xi/deep-wine-runner/issues/I7SAYE**
### 3.4.0(August 11th, 2023)
1. **Repair Easy Packager can't open and check wine error problem.**
2. **Professional Packager support to set different mimetype value for different .desktop file**
3. **Repair install runner problem in Ubuntu 23.04**
4. **Professional Packager support to save pack info what you are inputing**
5. **Deepin23 support run Winetricks with runner**
6. **Add video help website**
7. and so on