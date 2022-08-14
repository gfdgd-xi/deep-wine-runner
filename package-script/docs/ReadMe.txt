本文打包容器指的是打包deepin-wine维护的应用，主要讲如何将一个容器制作成安装包，以及一些辅助脚本的说明。

## 准备容器

这里主要讲打包相关的问题，如何制作容器不在这里赘述。本文前提是已经有了一个可能正常运行的容器。主要注意如下几点问题：

1. 容器存放目录最好是在~/.deepinwine目录下，因为打包的容器默认是解压到这个目录。放在这个目录方便以后更新容器可以直接在之前打包解压的容器基础之上更新。

2. 将容器尽量清理干净，不要有个人信息，尽量不要有太多多余的文件。打包过程中会清理一些通用不必要的文件，针对不同容器可能需要特殊处理，可以在cleanbottle.sh脚步中添加。

对于更新容器的情况，不需要重新创建容器，直接执行运行脚本就可以创建之前打包的容器，如/opt/deepinwine/apps/Deepin-QQ/run.sh -c（注意先删除之前的容器，保证容器是干净的）。
通过命令生成容器之后，在这个容器基础上修改，然后打包。

## 创建配置文件

这里的配置文件就是一个打包脚本，可以参考[打包工具](https://gitlab.deepin.io/wine/wine-package-script)中package-QQ.sh编写，这个脚本主要是定义一些环境变量，如：

*   app_description 安装包的描述

*   app_name 应用程序的英文名

*   app_name_zh_cn 应用程序的中文名

*   origin_bottle_name 指定打包容器的名字，如果用这个会在home目录查找这个目录打包。一般都不用这个，统一放到~/.deepinwine目录之后就没有必要。

*   public_bottle_name 安装之后运行解压的目录名称，存放在~/.deepinwine目录，目前默认也是用这个参数选择打包容器。

*   desktop_file_categories 应用程序类型，便于系统对应用程序进行分类。打包脚本中如果这个参数为空则不制作desktop文件，下面的两个参数就不需要

*   desktop_file_main_exe desktop文件中StartupWMClass字段。用于让桌面组件将窗口类名与desktop文件相对应。这个值为实际运行的主程序EXE的文件名，wine在程序运行后会将文件名设置为窗口类名。

*   exec_path 应用程序运行的路径，这里指定的是Windows格式的文件路径。

*   deb_package_name 生成安装包的包名。UOS上面命名规则是域名倒序+deepin,如com.qq.im.deepin；之前版本是deepin+域名倒序，如deepin.com.qq.im

*   deb_version_string 生成安装包的版本号。版本号规则是原始版本号+deepin+小版本号，如应用程序原始版本号是9.0.0，那么打包的第一个版本可以是9.0.0deepin0

*   old_package_name 某些情况同一个应用程序包名会改变，在更新之后需要能替换之前的安装包。这样就可以在安装包的replace字段中添加旧的包名达到目的。

*   package_depends 指定安装的依赖，为空的时候为默认通用的依赖。

## 暗藏机关

如果容器没有特殊情况，创建上一步的配置文件就可以构建成一个安装包，但是实际情况中往往会有一些各种各样的需求，下面就列举下目前已经存在的可配置项：

*   应用程序图标：定义了desktop_file_categories字段的应用程序会创建desktop文件，里面指定的图标文件名是包名。图标来源有两个，一是系统主题自带，另一个就是我们打包带上图标。现在打包脚本默认都会带上图标，有两种处理方式，一是手动将svg的图标命名成packagename.svg放到icons目录，如果没有svg图片，打包脚步会自动提取exec_path指定的二进制中的图标文件放到icons目录。mkicons.sh是基于icoutils里面的工具做的，可以自动解压出PE文件中的图标文件，git中icotool和wrestool是有解决一个问题的版本，源码找不到了。

*   [UOS商店上架应用规范](https://shimo.im/docs/dhQd9R3PYprtPVDj/read):新的规范主要限制了文件存放的目录、禁用安装脚本、添加权限配置等。打包脚步对应的分支是v20-uos，之前版本对应的分支是elephant。后面需要合并维护到一个分支，一次打包出两个版本。

*   安装文件：打包脚本有两种方式处理安装文件，一种是通用的，如desktop、容器压缩包等；另一种是在specified目录创建对应包名的目录，打包脚本会拷贝这个目录下的文件到安装目录。包名目录下有两个目录：bottle存放的文件会拷贝到容器中，最终会存放于容器压缩包中
；root存放的文件会拷贝到系统目录，最终安装到系统中会保持原来的目录结构，如root/usr/share/deepin-wine/test最终会安装到系统的/usr/share/deepin-wine/test。

*   容器更新规则：启动脚本在启动过程中会把当前的版本号写到容器根目录的PACKAGE_VERSION文件中，下次启动会对比版本，如果不一样会执行更新流程。更新用的是deepin-wine-helper中的[updater](https://gitlab.deepin.io/wine/deepin-wine-tools/tree/master/updater)。

*  文件和注册表覆盖规则：更新就会存在文件覆盖的问题，默认的规则文件放在specified/temp/bottle/update.policy，如果打包应用如要修改可以在specified目录创建对应包名的目录，然后在这个目录下存放bottle/update.policy文件。修改bottle/update.policy这个文件就可以达到想要效果。如何配置可以参考specified/temp/bottle/update.policy文件。

*   启动脚本：目前有三个版本启动脚本，参看helper/opt/deepinwine/tools/目录下的，run.sh、run_v2和run_v3.sh，目的是兼容不同的版本。run.sh中启动的参数是独立的，每添加一个包都需要修改这个文件添加；run_v2.sh有通用的启动函数调用，如无特殊需要可以不修改，目前elephant分支用的就是这个；run_v3.sh添加UOS版本支持，v20-uos分支用的这个。

*   退出wine容器：helper/opt/deepinwine/tools/kill.sh，参数加容器中运行的进程名，可以自动查找对应进程所在的容器，退出容器所有的进程。如果参数是services则是退出当前系统运行的所有wine容器。

*   收集日志： helper/opt/deepinwine/tools/log.sh，第一个参数指定容器，兼容v20-uos和elephant两个分支，v20-uos版本传入包名，elephant版本传入public_bottle_name指定的名字；第二个参数指定日志通道，就是指定WINEDEBUG的环境变量；第三个参数可以指定运行的windows程序的第一个参数。

*   文件选择对话框： deepin-wine提供了支持Windows程序使用系统原生对话框的机制，需要依赖[deepin-wine-plugin](https://gitlab.deepin.io/wine/deepin-wine-tools/tree/master/deepin-wine-plugin)。如果需要用系统原生对话框，可以参考微信修改启动脚本(helper/opt/deepinwine/tools/run.sh)，添加ATTACH_FILE_DIALOG的环境变量

*   64位依赖：因为我们目前打的容器包都是32位的，某些情况下需要添加64位的依赖(或者是根据当前系统的版本安装，64位系统安装64位的依赖，32位系统安装32位的依赖)，目前的做法是添加了一个deepin-wine-plugin-virtual的虚包，将这种情况的依赖写到虚包的depends里面。

*   package-deb.sh: 打包目录中DEBIAN目录配置号之后可用此脚本一键打包，如./package-deb.sh helper/

*   使用仓库版本deepin-wine:

    使用deepin-wine6-stable:
```
    export package_depends="deepin-wine6-stable:amd64 (>= 6.0.0.12-1), deepin-wine-helper (>= 5.1.25-1)"
    export apprun_cmd="deepin-wine6-stable"
```

    使用deepin-wine5-stable
```
    export package_depends="deepin-wine5-stable:amd64 (>= 5.0.29-1), deepin-wine-helper (>= 5.1.25-1)"
    export apprun_cmd="deepin-wine5-stable"
```

根据需求定制之后，就可以执行之前配置的脚本进行打包了，比如./package-WeChat.sh

