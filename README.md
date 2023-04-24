# Windows虚拟机安装工具 
## 介绍
基于VirtualBox/Qemu制作的小白Windows虚拟机安装工具，可以做到只需要用户下载系统镜像并点击安装即可，无需顾及虚拟机安装、创建、虚拟机的分区等等  
此为 Wine 运行器子项目：https://gitee.com/gfdgd-xi/deep-wine-runner  
依照 GPLV3 协议开源  

![图片.png](https://storage.deepin.org/thread/202304092224497604_图片.png)

![图片.png](https://storage.deepin.org/thread/202304092224396099_图片.png)

![图片.png](https://storage.deepin.org/thread/202304092224315599_图片.png)

## 如何使用
安装最新版本的 Wine 运行器即可，最新版本的 Wine 运行器自带此安装工具  

## 编译指南
```bash
git clone https://gitee.com/gfdgd-xi/windows-virtual-machine-installer-for-wine-runner.git
cd windows-virtual-machine-installer-for-wine-runner
qmake .
make -j4
```
## 预编译版本
https://gitee.com/gfdgd-xi/deep-wine-runner/tree/main/VM

# ©2020~2023 gfdgd xi