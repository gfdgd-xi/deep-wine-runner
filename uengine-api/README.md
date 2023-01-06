# API 介绍
# 必知
1. 此 API 只支持可以运行 UEngine 的 Linux 上，Windows 上无法使用
2. 部分函数需要 root 权限
3. 这是 UEngine 运行器的函数重构，所以一些 UEngine 运行器上没有的 bug 可能在这个 API 里有
## ProgramInformation
用于获取一些程序信息，详细如下（未特殊表明的是变量，否则是函数）：
| 变量/函数名 | 变量/函数介绍 |
|:-:|:-:|
| programPath | 获取程序所在路径 |
| version | API 版本 |
| updateTime | 更新时间 |
| websize | 程序官网 |
| home | 用户 home（用户文件）目录 |
| developer | 参与的开发者列表 |
| language | 当前语言 |
| DesktopPath() | （函数）用户桌面目录 |

## Check
用于检查 API 所需的东西是否完整，详细如下：  
| 函数名 | 函数介绍 |
|:-:|:-:|
| CheckDepend() | 检查 API 所需的依赖是否完整 |  

## ROOT
用于检查 ROOT 方面问题，详细如下：
| 函数名 | 函数介绍 |
|:-:|:-:|
| GetRoot() | 检查程序/API是否以 ROOT 权限运行 |

## APK
这是面向对象的写法，所以应用方式也不一样：
```python
import api
xxx = api.APK("APK 所在路径")
```
具体函数介绍：  
| 函数名 | 函数介绍 |
|:-:|:-:|
| xxx.install() | 安装这个 APK 包（需要 Root） |
| xxx.uninstall()| 卸载这个 APK 包（需要 Root） |
| xxx.information()| 获取从 aapt 获取到的 APK 信息 |
| xxx.activityName() | 获取 APK 的 Activity 信息 |
| xxx.packageName() | 获取 APK 包名 |
| xxx.chineseLabel() | 获取 APK 中文名称 |
| xxx.saveApkIcon("图标保存路径") | 保存 APK 的图标到指定路径 |
| xxx.version() | 获取 APK 版本号 |
| xxx.saveDesktopFile("图标保存路径", "快捷方式保存路径") | 保存支持 UEngine 启动的 APK 快捷方式 |
| xxx.run() | 运行该应用（需要保证已经安装） |
| xxx.buildDeb("deb 包保存路径", qianZhui) | 打包为 deb 包（“qianZhui”是布尔值，可略，True代表有前缀为“uengine-dc”，False代表没有前缀） |

## UEngine
用于对 UEngine 进行一点点操控，详细如下：
| 函数名 | 函数介绍 |
|:-:|:-:|
| UengineAppManager() | 显示 UEngine 安装应用程序管理器 |
| OpenApp("应用包名", "应用Activity") | 运行指定的应用（需要保证程序已经安装） |
| UengineDataClean() | 清空 UEngine 数据（需要 Root） |
| RemoveUengineCheck() | 删除 UEngine 的检查脚本（需要 Root） |
| CPUCheck() | 检查 CPU 是否支持运行 UEngine |
| BuildUengineRootImage() | 构建 UEngine 的 Root 镜像 |
| OpenUengineRootData() | 打开 UEngine 数据目录 |
| InstallRootUengineImage() | 安装已经被 Root 过的 UEngine 镜像（需要 Root） |
| Services | 用于操控 UEngine 服务的类，见下（需要 Root） |
| InternetBridge | 用于操控 UEngine 网络桥接的类，见下（需要 Root） |
### Services
关于 UEngine 的服务控制：
| 函数名 | 函数介绍 |
|:-:|:-:|
| Services.Open() | 打开 UEngine 服务（需要 Root） | 
| Services.Close() | 关闭 UEngine 服务（需要 Root） |
| Services.Restart() | 重启 UEngine 服务（需要 Root） |
### InternetBridge
关于 UEngine 的网络桥接控制：
| 函数名 | 函数介绍 |
|:-:|:-:|
| InternetBridge.Open() | 打开 UEngine 网络桥接（需要 Root） | 
| InternetBridge.Close() | 关闭 UEngine 网络桥接（需要 Root） |
| InternetBridge.Restart() | 重启 UEngine 网络桥接（需要 Root） |
| InternetBridge.Reload() | 重新加载 UEngine 网络桥接（需要 Root） |
| InternetBridge.ForceReload() | 强制加载 UEngine 网络桥接（需要 Root） |
## Adb
用于对 Adb 的部分操控
| 函数名 | 函数介绍 |
|:-:|:-:|
| Services | 用于操控 Adb 服务的类，见下 |
### Service
关于 Adb 的服务控制：
| 函数名 | 函数介绍 |
|:-:|:-:|
| Services.Open() | 打开 Adb 服务 | 
| Services.Close() | 关闭 Adb 服务 |
| Services.Kill() | 杀死 Adb 进程 |
## File
关于文件的读取和写入，这是面向对象的写法，所以应用方式也不一样：
```python
import api
xxx = api.File("文件所在路径")
```
| 函数名 | 函数介绍 |
|:-:|:-:|
| xxx.read() | 读取这个文件 |
| xxx.write("写入内容") | 写入这个文件 |

## UengineRunner
用于 UEngine 运行器的部分操控（请保证安装了 UEngine 运行器）
| 函数名 | 函数介绍 |
|:-:|:-:|
| CleanHistory() | 清理 UEngine 运行器的历史记录 |