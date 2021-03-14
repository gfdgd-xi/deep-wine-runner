# deepin-wine 运行器

#### 介绍
一个图形化了以下命令的程序

```
WINEPREFIX=容器路径 deepin-wine 可执行文件路径
```
让你的 deepin-wine 打包轻松一点

是使用 Python3 的 tkinter 构建的

（自己美术功底太差，图标只能在网络上找了）

（测试平台：deepin 20.1 1030）

#### 软件架构
i386 和 amd64，deepin-wine 和 deepin-wine5 运行在哪就运行在哪


#### 安装教程

1.  安装所需依赖

```
sudo apt install deepin-wine python3 python3-tk git
```

2.  下载本程序

```
git clone https://gitee.com/gfdgd-xi/deep-wine-runner.git
```

3.  运行本程序

```
cd deep-wine-runner
chmod 777 main.py
./main.py
```


#### 使用说明

（均在软件的“小提示”里有说明）
1.  使用终端运行该程序，可以看到 deepin-wine（deepin-wine5）以及程序本身的提示和报错

#### 更新日志
1.2.0 更新内容：
    1、修改布局方式

    2、轻度梳理代码布局

1.1.2 更新内容（未发布发行版）：
    1、进行了细节优化

1.1.1 更新内容：
    1、使用多线程，防止界面假死
    2、添加软件图标

1.1 更新内容：
    1、修改了代码的部分内容，使其支持容器路径可带空格无需“\”转义，以及支持手动保存运行脚本到桌面

1.0 更新内容：
    1、实现内容

#### 特技

难道是使用 tkinter 进行构建吗？所以没有咯
