#!/bin/bash

DEB_PACKAGE_NAME="com.qq.im.deepin"

get_value()
{
    cat $1 | grep -m 1 ${2}= | awk -F = '{print $NF}' | awk -F \" '{print $2}'
}

if [ -n "$1" ];then
    DEB_PACKAGE_NAME="$1"
fi

RUN_FILE="/opt/apps/$DEB_PACKAGE_NAME/files/run.sh"

if [ ! -f "$RUN_FILE" ];then
    echo "$DEB_PACKAGE_NAME 未安装"
    exit
fi

BOTTLENAME="$(get_value $RUN_FILE BOTTLENAME)"
APPRUN_CMD="$(get_value $RUN_FILE APPRUN_CMD)"
BOTTLEPATH="$HOME/.deepinwine/$BOTTLENAME"

bottle_started()
{
ps -ef | grep startbottle.exe | while read startb;do
    starts=(${startb// / })
    envfile=/proc/${starts[1]}/environ
    if [ -f $envfile ];then
        grep -c $BOTTLENAME /proc/${starts[1]}/environ > /dev/null
        if [ $? -eq 0 ];then
		echo ${starts[1]}
		break
        fi
    fi
done
}

if [ "$(bottle_started)" ];then
	exit
fi

$RUN_FILE -c

if [ -d "$BOTTLEPATH" ];then
    APPRUN_CMD=${APPRUN_CMD/\$HOME/$HOME}

    if [ ! -f "$APPRUN_CMD" ];then
        export WINEDLLPATH=/opt/$APPRUN_CMD/lib:/opt/$APPRUN_CMD/lib64
    fi

    ARCHIVE_FILE_DIR="/opt/apps/$DEB_PACKAGE_NAME/files"
    export WINEPREDLL="$ARCHIVE_FILE_DIR/dlls"

    WINEPREFIX="$BOTTLEPATH" $APPRUN_CMD /opt/deepinwine/tools/startbottle.exe &
fi

