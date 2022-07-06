# wine 运行器 1.5.2

## 介绍
一个图形化了以下命令的程序  
```bash
env WINEPREFIX=容器路径 wine（wine的路径） 可执行文件路径
```
让你可以简易方便的使用 wine  
是使用 Python3 的 tkinter 构建的    
（自己美术功底太差，图标只能在网络上找了）    
（测试平台：deepin 20.6；UOS 家庭版 21；Ubuntu 22.04）    
![image.png](https://storage.deepin.org/thread/202207061004446872_image.png)
而打包器可以方便的把您的 wine 容器打包成 deb 包供他人使用，程序创建的 deb 构建临时文件夹目录树如下：  
```bash
/XXX
├── DEBIAN
│   └── control
└── opt
└── apps
    └── XXX
        ├── entries
        │   ├── applications
        │   │   └── XXX.desktop
        │   └── icons
        │       └── hicolor
        │           └── scalable
        │               └── apps
        │                   └── XXX.png（XXX.svg）
        ├── files
        │   ├── files.7z
        │   └── run.sh
        └── info

11 directories, 6 files
```

## 软件架构
i386 和 amd64，deepin-wine、deepin-wine5、wine、wine64、deepin-wine5-stable、deepin-wine6-stable、spark-wine7-devel、ukylin-wine 运行在哪就运行在哪  


## 使用说明

### 均在软件的“小提示”里有说明
### 运行器
1、使用终端运行该程序，可以看到 wine 以及程序本身的提示和报错;  
2、wine 32 位和 64 位的容器互不兼容;  
3、所有的 wine 和 winetricks 均需要自行安装（可以从 菜单栏=>程序 里面进行安装）  
4、本程序支持带参数运行 wine 程序（之前版本也可以），只需要按以下格式即可：  
```bash
exe路径\' 参数 \'  
```
即可（单引号需要输入）  
5、wine 容器如果没有指定，则会默认为 ~/.wine  
### 打包器
1、deb 打包软件包名要求：  
软件包名只能含有小写字母(a-z)、数字(0-9)、加号(+)和减号(-)、以及点号(.)，软件包名最短长度两个字符；它必须以字母开头
2、如果要填写路径，有“浏览……”按钮的是要填本计算机对应文件的路径，否则就是填写安装到其他计算机使用的路径  
3、输入 wine 的容器路径时最后面请不要输入“/”  
4、输入可执行文件的运行路径时是以“C:/XXX/XXX.exe”的格式进行输入，默认是以 C： 为开头，不用“\”做命令的分隔，而是用“/”  
5、.desktop 的图标只支持 PNG 格式和 SVG 格式，其他格式无法显示图标  

## 更新日志
### 1.5.2
**※1、添加并翻新了 deepin-wine5 打包器，改为 wine 打包器，支持常见 wine 的打包**  
**※2、新增 Visual Studio C++ 的安装程序**  
**※3、新增从系统安装镜像提取 DLL 到 wine 容器的功能（当前只支持 Windows XP 和 Windows Server 2003 的官方安装镜像）**  
4、修复了安装星火应用商店的 wine 运行器右键打开方式没有 wine 运行器选项的问题  
5、新增脚本，优化 deepin terminal 调用本程序脚本显示不佳的问题  
![image.png](https://storage.deepin.org/thread/202207061004446872_image.png)
![image.png](https://storage.deepin.org/thread/202207061005149959_image.png)
![image.png](https://storage.deepin.org/thread/202207061005251446_image.png)


### 1.5.1
**※1、支持打开 spark-wine7-devel 的专门缩放设置（如未安装则此按钮禁用）**  
**※2、支持提取选择的 exe 文件的图标**  
**※3、支持向指定的 wine 容器安装 mono、gecko、.net framework（此功能在菜单栏“Wine”中，卸载只需要使用程序的卸载按钮打开 Geek Uninstaller 即可）**  
**※4、支持指定特定的 wine 容器调用 winetricks**  
**※5、在没有指定 wine 容器的情况下，将自动设置为 ~/.wine**  
6、新增 ukylin-wine  
7、将默认选择的 wine 改为 deepin-wine6 stable  
8、支持打开指定容器的 winecfg、winver、regedit、taskmgr  
9、双击使用 wine 运行器打开 exe（不知道能不能生效） 
![image.png](https://storage.deepin.org/thread/202207042234078682_image.png)


### 1.5.0
**※1、支持显示 wine 程序运行时的返回内容**  
**※2、优化打包方式，减少从 pip 安装的库，并将 pip 源设为阿里源提升下载速度**  
**※3、新增 spark-wine7-devel**  
**※4、支持从程序启动用于安装 wine 的程序（在菜单栏的“程序”）**  
5、优化 wine 安装脚本，在安装星火应用商店的 wine 时支持检测是否有 ss-apt-fast，如果有就调用替代 apt 提升安装速度  
6、支持关闭指定 wine 的进程，以及访问对应 wine 容器的目录和字体目录  
7、从生成shell脚本改为升级到desktop文件  
![image.png](https://storage.deepin.org/thread/202207031902414162_image.png)


### 1.4.0
**※1、修改了 wine 选项的说明和 wine 的启动方式;**  
**※2、设置了窗口主题;**  
**※3、修改了打包以及 .desktop 文件**  
4、删除了以前的残略调试代码;  
5、优化了 wine 列表的显示流程;  
6、更新了“关于”窗口  
7、更新了提示内容  
8、在 gitee/github 仓库上添加了 wine 安装脚本  
![](https://images.gitee.com/uploads/images/2021/0727/151226_750579c2_7896131.png)  

### 1.3.1
1、添加了历史记录，使用更加方便  
2、增加“更新内容”项  
3、支持浏览窗口的默认路径为上次访问的路径  
4、支持清空历史记录  
5、代码结构优化  
6、修改了控件大小  
![run](https://images.gitee.com/uploads/images/2021/0523/155621_95e6fea5_7896131.png "截图录屏_选择区域_20210523153529.png")
![run](https://images.gitee.com/uploads/images/2021/0523/155633_b7ab458a_7896131.png "截图录屏_选择区域_20210523153548.png")
![run](https://images.gitee.com/uploads/images/2021/0523/155643_fc933b76_7896131.png "截图录屏_选择区域_20210523153929.png")
![run](https://images.gitee.com/uploads/images/2021/0523/155654_90ceb8ce_7896131.png "截图录屏_选择区域_20210523153947.png")
![run](https://images.gitee.com/uploads/images/2021/0523/155702_66841e22_7896131.png "截图录屏_选择区域_20210523154007.png")

### 1.3.0 
1. 修改了窗口显示控件的库（从 tkinter 到 tkinter.ttk）
2. 添加了更多 wine 可以选择（deepin-wine、deepin-wine5、wine、wine64、deepin-wine5-stable、deepin-wine6-stable）
3. 修改了程序的提示信息
![输入图片说明](https://images.gitee.com/uploads/images/2021/0522/175640_a592db4d_7896131.png "截图录屏_tk_20210522170529.png")

### 1.2.0 
1. 修改布局方式
2. 轻度梳理代码布局
![输入图片说明](https://images.gitee.com/uploads/images/2021/0314/181320_cb4cbf72_7896131.png "屏幕截图.png")

### 1.1.2 （未发布发行版）
1. 进行了细节优化

### 1.1.1
1. 使用多线程，防止界面假死
2. 添加软件图标
![](https://images.gitee.com/uploads/images/2021/0131/143557_40911a67_7896131.png)

### 1.1
1. 修改了代码的部分内容，使其支持容器路径可带空格无需“\”转义，以及支持手动保存运行脚本到桌面

### 1.0
1. 实现内容

## 更多
+ https://gitee.com/gfdgd-xi/deep-wine-runner
+ https://github.com/gfdgd-xi/deep-wine-runner
+ https://www.gitlink.org.cn/gfdgd_xi/deep-wine-runner

# ©2020-Now