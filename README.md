<p width=100px align="center"><img src="https://storage.deepin.org/thread/202208031419283599_deepin-wine-runner.png"></p>
<h1 align="center">Wine 运行器 Aptss 安装器</h1>
<hr>
<a href='https://gitee.com/gfdgd-xi/deep-wine-runner/stargazers'><img src='https://gitee.com/gfdgd-xi/deep-wine-runner/badge/star.svg?theme=dark' alt='star'></img></a>
<a href='https://gitee.com/gfdgd-xi/deep-wine-runner/members'><img src='https://gitee.com/gfdgd-xi/deep-wine-runner/badge/fork.svg?theme=dark' alt='fork'></img></a>

## 介绍
此工具用于在 Debian 发行版调试/安装Wine运行器打包的应用，不需要手动输入星火的命令/等上架商店就可以安装来自星火应用商店的依赖如 deepin-wine6-stable、spark-dwine-helper 等常用打包依赖  
## 如何编译
```
sudo apt install qtbase5-dev qttools5-dev-tools
git clone https://gitee.com/gfdgd-xi/deep-wine-runner
cd deep-wine-runner
git checkout AptssInstaller
qmake .
make -j4
./aptss-installer
```