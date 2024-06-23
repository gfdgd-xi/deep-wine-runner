<p width=100px align="center"><img src="https://storage.deepin.org/thread/202208031419283599_deepin-wine-runner.png"></p>
<h1 align="center">Wine 运行器 Qemu 拓展</h1>
<hr>
<a href='https://gitee.com/gfdgd-xi/deep-wine-runner-qemu-system/stargazers'><img src='https://gitee.com/gfdgd-xi/deep-wine-runner-qemu-system/badge/star.svg?theme=dark' alt='star'></img></a>
<a href='https://gitee.com/gfdgd-xi/deep-wine-runner-qemu-system/members'><img src='https://gitee.com/gfdgd-xi/deep-wine-runner-qemu-system/badge/fork.svg?theme=dark' alt='fork'></img></a>  
<br>
Wine 运行器：<a href='https://gitee.com/gfdgd-xi/deep-wine-runner/stargazers'><img src='https://gitee.com/gfdgd-xi/deep-wine-runner/badge/star.svg?theme=dark' alt='star'></img></a>
<a href='https://gitee.com/gfdgd-xi/deep-wine-runner/members'><img src='https://gitee.com/gfdgd-xi/deep-wine-runner/badge/fork.svg?theme=dark' alt='fork'></img></a>  

## 介绍
该组件内置了更新版本的 Qemu 并不与系统源内的 Qemu 冲突，让 deepin/UOS 吃上更新版本的 Qemu  
（内置了支持龙芯新世界的 qemu-system-loongarch64）  
安装此包后在后续版本的 Wine 运行器虚拟机配置工具将支持调用该新版本的 Qemu（当前的 Wine 运行器 3.9.1 暂无法调用）  
Github Action：[![Wine Runner Qemu Extra Builder](https://github.com/gfdgd-xi/deep-wine-runner-qemu-system/actions/workflows/building-deb.yml/badge.svg?branch=master)](https://github.com/gfdgd-xi/deep-wine-runner-qemu-system/actions/workflows/building-deb.yml)  
## 如何编译
### 拉取源码
```bash
sudo apt update
sudo apt install git
git clone https://gitee.com/gfdgd-xi/deep-wine-runner-qemu-system
```
### 安装编译依赖
```bash
cd deep-wine-runner-qemu-system
sudo apt build-dep qemu
sudo apt build-dep .
# Debian 10/UOS/deepin 20 用户需要安装 py 的编译依赖
sudo apt build-dep python3.7
```
### 编译前准备（只限 Debian10/UOS/deepin 20）
```bash
cd deep-wine-runner-qemu-system
make build-python -j4
make install-to-qemu-python -j4
```
### 构建 deb 包
```bash
dpkg-buildpackage -b
```

# ©2020～Now gfdgd xi