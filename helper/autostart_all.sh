#!/bin/bash

get_value()
{
    cat $1 | grep -m 1 ${2}= | awk -F = '{print $NF}' | awk -F \" '{print $2}'
}

init_bottle()
{
    RUN_FILE=$1

    if [ ! -f "$RUN_FILE" ];then
        echo "$RUN_FILE 未安装"
        return
    fi

    DEB_PACKAGE_NAME="$(get_value $RUN_FILE DEB_PACKAGE_NAME)"
    BOTTLENAME="$(get_value $RUN_FILE BOTTLENAME)"
    APPRUN_CMD="$(get_value $RUN_FILE APPRUN_CMD)"
    BOTTLEPATH="$HOME/.deepinwine/$BOTTLENAME"

    if [ $2 ]&&[ $2 == "-c" ];then
	$RUN_FILE -c
    fi

#    KILL="/opt/deepinwine/tools/kill.bak"
#    if [ -f $KILL ];then
#	$KILL "$BOTTLENAME"
#    fi

    if [ -d "$BOTTLEPATH" ];then
        APPRUN_CMD=${APPRUN_CMD/\$HOME/$HOME}

        if [ ! -f "$APPRUN_CMD" ];then
            export WINEDLLPATH=/opt/$APPRUN_CMD/lib:/opt/$APPRUN_CMD/lib64
        fi

        ARCHIVE_FILE_DIR="/opt/apps/$DEB_PACKAGE_NAME/files"
        export WINEPREDLL="$ARCHIVE_FILE_DIR/dlls"

	WINEPREFIX="$BOTTLEPATH" $APPRUN_CMD /opt/deepinwine/tools/startbottle.exe &
    fi
}

AUTOSTART="/opt/deepinwine/tools/autostart"
if [ -f "$AUTOSTART.all" ];then
	find /opt/apps -name run.sh | while read package;do
	    init_bottle $package "$@"
	done
elif [ -f $AUTOSTART ];then
	debs=`cat $AUTOSTART`
	for deb in $debs
	do
		debname=`echo $deb | sed -e 's/\s//g'`
		init_bottle "/opt/apps/$debname/files/run.sh" "$@"
	done
fi
