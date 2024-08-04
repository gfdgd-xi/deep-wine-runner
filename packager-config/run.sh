#!/bin/sh

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

version_gt() { test "$(echo "$@" | tr " " "
" | sort -V | head -n 1)" != "$1"; }

extract_archive()
{
    archive=$1
    version_file=$2
    dest_dir=$3
    if [ -f "$archive" ] && [ -n "$dest_dir" ] && [ "$dest_dir" != "." ];then
        archive_version=`cat $version_file`
        if [ -d "$dest_dir" ];then
            if [ -f "$dest_dir/VERSION" ];then
                dest_version=`cat $dest_dir/VERSION`
                if version_gt "$archive_version" "$dest_version";then
                    7z x "$archive" -o/"$dest_dir" -aoa
                    echo "$archive_version" > "$dest_dir/VERSION"
                fi
            fi
        else
            mkdir -p $dest_dir
            7z x "$archive" -o/"$dest_dir" -aoa
            echo "$archive_version" > "$dest_dir/VERSION"
        fi
    fi
}

Get_Dist_Name()
{
    if grep -Eqii "Deepin" /etc/issue || grep -Eq "Deepin" /etc/*-release; then
        DISTRO='Deepin'
    elif grep -Eqi "UnionTech" /etc/issue || grep -Eq "UnionTech" /etc/*-release; then
        DISTRO='UniontechOS'
    elif grep -Eqi "UOS" /etc/issue || grep -Eq "UOS" /etc/*-release; then
        DISTRO='UniontechOS'
    else
	 DISTRO='OtherOS'
	fi
}


####获得发行版名称

#########################预设值段

version_gt() { test "$(echo "$@" | tr " " "\n" | sort -V | head -n 1)" != "$1"; }
####用于比较版本？未实装
BOTTLENAME="@@@BOTTLENAME@@@"
APPVER="@@@APPVER@@@"
EXEC_PATH="@@@EXEC_PATH@@@"
##### 软件在wine中的启动路径
SHELL_DIR=$(dirname $(realpath $0))
START_SHELL_PATH="/opt/deepinwine/tools/run_v4.sh"
if [ -e "$SHELL_DIR/deepinwine/tools/spark_run_v4.sh" ] ;then
    # 如果 helper 在 run.sh 相同目录的 deepinwine/tools/spark_run_v4.sh 则可以调用
    START_SHELL_PATH="$SHELL_DIR/deepinwine/tools/spark_run_v4.sh"
fi
if [ -e "/opt/deepinwine/tools/run_v4.sh" ] ;then
    START_SHELL_PATH="/opt/deepinwine/tools/run_v4.sh"
fi
if [ -e "/opt/deepinwine/tools/spark_run_v4.sh" ] ;then
    START_SHELL_PATH="/opt/deepinwine/tools/spark_run_v4.sh"
fi
ENABLE_DOT_NET=""
####若使用spark-wine时需要用到.net，则请把ENABLE_DOT_NET设为true，同时在依赖中写spark-wine7-mono
#export BOX86_EMU_CMD="/opt/spark-box86/box86"
####仅在Arm且不可使用exagear时可用，作用是强制使用box86而不是deepin-box86.如果你想要这样做，请取消注释
export MIME_TYPE=""

export DEB_PACKAGE_NAME="@@@DEB_PACKAGE_NAME@@@"
####这里写包名才能在启动的时候正确找到files.7z,似乎也和杀残留进程有关
export APPRUN_CMD="@@@APPRUN_CMD@@@"
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
if [ "$DISTRO" != "Deepin" ] && [ "$DISTRO" != "UniontechOS" ];then
DISABLE_ATTACH_FILE_DIALOG="1"
echo "非deepin/UOS，默认关闭系统自带的文件选择工具，使用Wine的"
echo "如果你想改变这个行为，请到/opt/apps/$DEB_PACKAGE_NAME/files/$0处修改"
echo "To打包者：如果你要打开自带请注意在适配的发行版上进行测试"
echo "To用户：打包者没有打开这个功能，这证明启用这个功能可能造成运行问题。如果你要修改这个行为，请确保你有一定的动手能力"
fi
##############>>>>>>>>>禁用文件选择工具结束

##############<<<<<<<<<屏蔽mono和gecko安装器开始
##默认屏蔽mono和gecko安装器
if [ "$APPRUN_CMD" = "spark-wine7-devel" ] || [ "$APPRUN_CMD" = "spark-wine" ]|| [ "$APPRUN_CMD" = "spark-wine8" ] && [ -z "$ENABLE_DOT_NET" ];then

#export WINEDLLOVERRIDES="mscoree=d,mshtml=d,control.exe=d"
export WINEDLLOVERRIDES="control.exe=d"
#### "为了降低打包体积，默认关闭gecko和momo，如有需要，注释此行（仅对spark-wine7-devel有效）"

fi
##############>>>>>>>>>屏蔽mono和gecko安装器结束

##############<<<<<<<<<解压自行封装的 Wine（如果存在的话）
if [ -e "$ARCHIVE_FILE_DIR/wine_archive.7z" ]; then
    WINE_BIN_DIR=`dirname $APPRUN_CMD`
    WINE_DIR=`dirname $WINE_BIN_DIR`
    extract_archive "$ARCHIVE_FILE_DIR/wine_archive.7z" "$ARCHIVE_FILE_DIR/wine_archive.md5sum" "$WINE_DIR"
fi
##############>>>>>>>>>

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
        $START_SHELL_PATH $BOTTLENAME $APPVER "C:/windows/command/start.exe" "/Unix" "$EXEC_PATH" "$@"
    fi
else
    $START_SHELL_PATH $BOTTLENAME $APPVER "uninstaller.exe" "$@"
fi