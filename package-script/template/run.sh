#!/bin/bash

#   Copyright (C) 2016 Deepin, Inc.
#
#   Author:     Li LongYu <lilongyu@linuxdeepin.com>
#               Peng Hao <penghao@linuxdeepin.com>
#
#
#   Copyright (C) 2022 The Spark Project
#
#
#   Modifier    shenmo <shenmo@spark-app.store>
#
#
#

#######################函数段。下文调用的额外功能会在此处声明

Get_Dist_Name()
{
    if grep -Eqii "Deepin" /etc/issue || grep -Eq "Deepin" /etc/*-release; then
        DISTRO='Deepin'
    elif grep -Eqi "UnionTech" /etc/issue || grep -Eq "UnionTech" /etc/*-release; then
        DISTRO='UniontechOS'
    elif grep -Eqi "UOS" /etc/issue || grep -Eq "UOS" /etc/*-release; then
        DISTRO='UniontechOS'
    elif grep -Eqi "GXDE" /etc/issue || grep -Eq "GXDE" /etc/*-release; then
        DISTRO='GXDE'
    else
	 DISTRO='OtherOS'
	fi
}


####获得发行版名称

#########################预设值段

version_gt() { test "$(echo "$@" | tr " " "\n" | sort -V | head -n 1)" != "$1"; }
####用于比较版本？未实装
BOTTLENAME="@public_bottle_name@"
APPVER="@deb_version_string@"
EXEC_PATH="@exec_path@"
##### 软件在wine中的启动路径
START_SHELL_PATH="@start_shell_path@"
ENABLE_DOT_NET=""
####若使用spark-wine时需要用到.net，则请把ENABLE_DOT_NET设为true，同时在依赖中写spark-wine7-mono
export MIME_TYPE="@mime_type@"

export DEB_PACKAGE_NAME="@deb_package_name@"
####这里写包名才能在启动的时候正确找到files.7z,似乎也和杀残留进程有关
export APPRUN_CMD="@apprun_cmd@"
#####wine启动指令，建议
#EXPORT_ENVS="wine的动态链接库路径"
##例如我的wine应用是使用的dwine6的32位容器，那么我要填LD_LIBRARY_PATH=$LD_LIBRARY;/opt/deepin-wine6-stable/lib
## 如果用不到就不填，不要删除前面的注释用的#

export SPECIFY_SHELL_DIR=`dirname $START_SHELL_PATH`

ARCHIVE_FILE_DIR="/opt/apps/$DEB_PACKAGE_NAME/files"

export WINEDLLPATH=/opt/$APPRUN_CMD/lib:/opt/$APPRUN_CMD/lib64

export WINEPREDLL="$ARCHIVE_FILE_DIR/dlls"

DISABLE_ATTACH_FILE_DIALOG=""
##默认为空。若为1，则不使用系统自带的文件选择，而是使用wine的
##对于deepin/UOS，大部分的应用都不需要使用wine的，如果有需求（比如wine应用选择的限定种类文件系统的文管不支持）
##请填1。
##注意：因为非DDE的环境不确定，所以默认会在非Deepin/UOS发行版上禁用这个功能。如果你确认在适配的发行版上可以正常启动，请注释或者删除下面这段

##############<<<<<<<<<禁用文件选择工具开始
Get_Dist_Name
#此功能实现参见开头函数段
if [ "$DISTRO" != "Deepin" ] && [ "$DISTRO" != "UniontechOS" ] && [ "$DISTRO" != "GXDE" ];then
DISABLE_ATTACH_FILE_DIALOG="1"
echo "非deepin/UOS，默认关闭系统自带的文件选择工具，使用Wine的"
echo "如果你想改变这个行为，请到/opt/apps/$DEB_PACKAGE_NAME/files/$0处修改"
echo "To打包者：如果你要打开自带请注意在适配的发行版上进行测试"
echo "To用户：打包者没有打开这个功能，这证明启用这个功能可能造成运行问题。如果你要修改这个行为，请确保你有一定的动手能力"
fi
##############>>>>>>>>>禁用文件选择工具结束

##############<<<<<<<<<屏蔽mono和gecko安装器开始
##默认屏蔽mono和gecko安装器
if [ "$APPRUN_CMD" = "spark-wine9" ] || [ "$APPRUN_CMD" = "spark-wine" ]|| [ "$APPRUN_CMD" = "spark-wine8" ] && [ -z "$ENABLE_DOT_NET" ];then

export WINEDLLOVERRIDES="mscoree=d,mshtml=d"
export WINEDLLOVERRIDES="control.exe=d"
#### "为了降低打包体积，默认关闭gecko和momo，如有需要，注释此行（仅对spark-wine7-devel有效）"

fi
##############>>>>>>>>>屏蔽mono和gecko安装器结束

#########################执行段




if [ -z "$DISABLE_ATTACH_FILE_DIALOG" ];then
    export ATTACH_FILE_DIALOG=1
fi

if [ -n "$EXPORT_ENVS" ];then
    export $EXPORT_ENVS
fi

if [ -n "$EXEC_PATH" ];then
    if [ -z "${EXEC_PATH##*.lnk*}" ];then
        $START_SHELL_PATH $BOTTLENAME $APPVER "C:/windows/command/start.exe" "/Unix" "$EXEC_PATH" "$@"
    else
        $START_SHELL_PATH $BOTTLENAME $APPVER "$EXEC_PATH" "$@"
    fi
else
    $START_SHELL_PATH $BOTTLENAME $APPVER "uninstaller.exe" "$@"
fi


