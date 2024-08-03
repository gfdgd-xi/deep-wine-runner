#!/bin/bash

#   Copyright (C) 2016 Deepin, Inc.
#   Copyright (C) 2022 The Spark Project
#
#   Author:     Li LongYu <lilongyu@linuxdeepin.com>
#               Peng Hao <penghao@linuxdeepin.com>
#
#   Modifier:   shenmo <shenmo@spark-app.store>
#		   
#
SHELL_DIR=$(dirname $(realpath $0))

export SHELL_DIR
source ${SHELL_DIR}/bashimport/log-function.bashimport
source ${SHELL_DIR}/bashimport/transhell.bashimport 
load_transhell_debug

#########Preload functions
function get_app_name() {
    local app_name_orig=$(grep -m 1 '^Name=' "/usr/share/applications/$1.desktop" | cut -d '=' -f 2)
    local app_name_i18n=$(grep -m 1 "^Name\[$LANGUAGE\]\=" "/usr/share/applications/$1.desktop" | cut -d '=' -f 2)
    local app_name=""
    
    if [ -z "$app_name_i18n" ]; then
        app_name="$app_name_orig"
    else
        app_name="$app_name_i18n"
    fi
    
    echo "$app_name"
}
######### Vars
BOTTLENAME="$1"
WINEPREFIX="$HOME/.deepinwine/$1"
APPDIR="/opt/apps/${DEB_PACKAGE_NAME}/files"
APPVER=""
APPTAR="files.7z"
BOTTLENAME=""
WINE_CMD="deepin-wine"
#这里会被后续覆盖
LOG_FILE=$0
PUBLIC_DIR="/var/public"
if [ -z $WINE_WMCLASS ];then
export WINE_WMCLASS="$DEB_PACKAGE_NAME"
fi
export WINE_APP_NAME=$(get_app_name ${DEB_PACKAGE_NAME})
if [ -z "$WINE_APP_NAME" ];then
export WINE_APP_NAME=$BOTTLENAME
fi




if [ -e /opt/p7zip-legacy/bin/7z ];then
log.debug "Using p7zip-legacy as unpacker"
UNPACK_CMD=/opt/p7zip-legacy/bin/7z
else
UNPACK_CMD=7z
log.debug "Using system 7z as unpacker"
fi


if [ $APPRUN_CMD ]; then
    WINE_CMD=$APPRUN_CMD
fi

#####################

if [ "$WINE_CMD" = "deepin-wine8-stable" ] && [ "$(arch)" != "x86_64" ];then

WINE_CMD="${SHELL_DIR}/spark-dwine-helper/deepin-wine8-stable-wrapper/deepin-wine8-stable"
log.warn "Using deepin-wine8-stable wrapper to fix arm problem"
fi


##################### Functions
	progressbar()
	{
		WINDOWID="" zenity --progress --title="$1" --text="$2" --pulsate --width=400 --auto-close --no-cancel ||
		WINDOWID="" zenity --progress --title="$1" --text="$2" --pulsate --width=400 --auto-close
	}


_DeleteRegistry()
{
    env WINEPREFIX="$WINEPREFIX" $WINE_CMD reg DELETE "$1" /f &> /dev/null
}
#########功能：删除注册表
init_log_file()
{
    if [ ! -d "$DEBUG_LOG" ];then
        return
    fi

    LOG_DIR=$(realpath $DEBUG_LOG)
    if [ -d "$LOG_DIR" ];then
        LOG_FILE="${LOG_DIR}/${LOG_FILE##*/}.log"
        echo "" > "$LOG_FILE"
        debug_log "LOG_FILE=$LOG_FILE"
    fi
}

debug_log_to_file()
{
    if [ -d "$DEBUG_LOG" ];then
        echo -e "${1}" >> "$LOG_FILE"
    fi
}

debug_log()
{
    log.debug "${1}"
}
################log相关功能
HelpApp()
{
	echo " Extra Commands:"
	echo " -r/--reset     Reset app to fix errors"
	echo " -e/--remove    Remove deployed app files"
	echo " -h/--help      Show program help info"
}
#############帮助文件

check_link()
{
    if [ ! -d "$1" ];then
        echo "$1 不是目录，不能创建$2软连接"
        return
    fi
    link_path=$(realpath "$2")
    target_path=$(realpath "$1")
    if [ "$link_path" != "$target_path" ];then
        if [ -d "$2" ];then
            mv "$2" "${2}.bak"
        else
            rm "$2"
        fi
        echo "修复$2软连接为$1"
        ln -s -f "$1" "$2"
    fi
}

FixLink()
{
    if [ -d ${WINEPREFIX} ]; then
        CUR_DIR=$PWD
	cd "${WINEPREFIX}/dosdevices"
 	check_link ../drive_c c:
        check_link / z:
        check_link $HOME y:
        cd "../drive_c/users/$USER"
        check_link "$HOME/Desktop" Desktop
        check_link "$HOME/Downloads" Downloads
        # Link to Document
if [ -L "$WINEPREFIX/drive_c/users/$(whoami)/My Documents" ]; then
        env WINEPREFIX="$WINEPREFIX" $WINE_CMD reg add 'HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders' /t REG_EXPAND_SZ  /v Personal /d "%USERPROFILE%\My Documents" /f

else
        env WINEPREFIX="$WINEPREFIX" $WINE_CMD reg add 'HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders' /t REG_EXPAND_SZ  /v Personal /d "%USERPROFILE%\Documents" /f

fi
        cd $CUR_DIR
        #ls -l "${WINEPREFIX}/dosdevices"
    fi
}
###########会在应用启动和解压时执行，驱动器绑定
DisableWrite()
{
    if [ -d "${1}" ]; then
        chmod +w "${1}"
        rm -rf "${1}"
    fi

    mkdir "${1}"
    chmod -w "${1}"
}
########如果有该文件夹则删除，然后再创建一个不允许写入的
is_autostart()
{
    AUTOSTART="/opt/deepinwine/tools/autostart"
    if [[ -f "$SHELL_DIR/autostart" ]]; then
        # 如果打包时自带 autostart，则使用自带的
        AUTOSTART="$SHELL_DIR/autostart"
    fi
    if [ -f "$AUTOSTART.all" ]&&[ -f "/opt/apps/$1/files/run.sh" ];then
        return 0
    fi

    if [ -f $AUTOSTART ];then
        grep -c "$1" $AUTOSTART > /dev/null
        return $?
    fi

    return 1
}
#########自动启动相关，等用到了再研究

Test_GL_wine()
{
    gl_wine_path="${SHELL_DIR}/spark_gl-wine"

    #如果不支持32的GLX,d3d改为gdi的实现
    if [[ ! -f "${WINEPREFIX}/.init_d3d" ]];then
        if [[ $WINE_CMD == *"deepin-wine8-stable"* ]];then
            gl_wine="${gl_wine_path}/gl-wine64"
        else
            gl_wine="${gl_wine_path}/run_gl.sh"
        fi

        run_gl=`${gl_wine} 2>&1`

        #如果opengl测试程序运行失败，所有进程的渲染方式改为gdi渲染模式
        if [ $? != 0 ];then
            WINEPREFIX="$WINEPREFIX" $WINE_CMD regedit /S "${gl_wine_path}/gdid3d.reg"
        fi

        touch "${WINEPREFIX}/.init_d3d"
    fi
}
urldecode() { : "${*//+/ }"; echo -e "${_//%/\\x}"; }
#######url转义

#arg 1: windows process file path
#arg 2-*: windows process args
CallProcess()
{
    #get file full path
    path="$1"
    path=$(echo ${path/c:/${WINEPREFIX}/drive_c})
    path=$(echo ${path//\\/\/})

    #kill bloack process
    is_autostart $DEB_PACKAGE_NAME
    autostart=$?
    if [[ $autostart -ne 0 ]] && [[ "$1" != *"pluginloader.exe" ]];then
        $SHELL_DIR/spark_kill.sh "$BOTTLENAME" block
    fi
	#run gl-wine for test opengl
    get_arch=`uname -m`
    if [[ $get_arch = "x86_64" ]];then
        Test_GL_wine
    fi
    #change current dir to excute path
    path=$(dirname "$path")
    cd "$path"
    pwd

    #Set default mime type
    if [ -n "$MIME_TYPE" ]; then
        xdg-mime default "$DEB_PACKAGE_NAME".desktop "$MIME_TYPE"
    fi
    # Disable winemenubuilder
    env  WINEPREFIX="$WINEPREFIX" $WINE_CMD reg add 'HKEY_CURRENT_USER\Software\Wine\DllOverrides' /v winemenubuilder.exe /f

    

    
    
    debug_log "Starting process $* ..."

	#############  WARNING: Here is the modified content: Now will run set-dwine-scale.sh
	${SHELL_DIR}/spark-dwine-helper/scale-set-helper/set-wine-scale.sh "$WINEPREFIX"
	$SHELL_DIR/spark-wine-banner &
    env WINEPREFIX="$WINEPREFIX" $WINE_CMD "$@"

    #start autobottle
    if [ $autostart -eq 0 ];then
        $SHELL_DIR/autostart_wine.sh $DEB_PACKAGE_NAME
    fi
}
###通用启动APP逻辑。对于没有被case捕捉的非适配APP，则直接执行此部分。似乎已经有了防止残留的功能
###一些自定义的应用不会使用这个启动，而另一些则会调用这个
###有设置mimetype和自动启动(这个暂时没分析)的功能

###########专属优化段：


UnixUriToDosPath()
{
    OPEN_FILE="$1"
    if [ -f "$OPEN_FILE" ]; then
        OPEN_FILE=$(realpath "$OPEN_FILE")
        OPEN_FILE="z:$OPEN_FILE"
        OPEN_FILE=$(echo $OPEN_FILE | sed -e 's/\//\\\\/g')
    fi
    echo $OPEN_FILE
}

#arg 1: exec file path
#arg 2: autostart ,or exec arg 1
#arg 3: exec arg 2

#### CallApp段，根据容器名找专属优化，没有就走通用启动
CallApp()
{


    
    FixLink
    debug_log "CallApp $BOTTLENAME arg count $#: $*"
    if [ -f "/opt/apps/${DEB_PACKAGE_NAME}/files/pre_run.sh" ];then
        source "/opt/apps/${DEB_PACKAGE_NAME}/files/pre_run.sh"
        CallPreRun "$@"
    fi
if [ -e  "/opt/deepinwine/tools/spark_run_v4_app_configs/${BOTTLENAME}.sh" ];then
APP_CONFIG_PATH="/opt/deepinwine/tools/spark_run_v4_app_configs/${BOTTLENAME}.sh"
else
APP_CONFIG_PATH="${SHELL_DIR}/spark_run_v4_app_configs/${BOTTLENAME}.sh"
fi
if [ -f "$APP_CONFIG_PATH" ]; then
  echo "执行 ${BOTTLENAME}.sh ..."
  source $APP_CONFIG_PATH
else
  echo "$APP_CONFIG_PATH 文件不存在，执行通用启动"
  CallProcess "$@" 
fi


}
ExtractApp()
{


local tmp_log=$(mktemp)
	mkdir -p "$1"
	(${UNPACK_CMD} x "$APPDIR/$APPTAR" -o"$1" -bsp1 -bb1 -bse2 | grep --line-buffered -oP "(\d+(\.\d+)?(?=%))" > $tmp_log)&

	cmd_pid=$!
(while kill -0 $cmd_pid 2> /dev/null; do
        tail -n 1 "${tmp_log}"
        sleep 1
    done)|  zenity --progress --title="${TRANSHELL_CONTENT_SPARK_WINDOWS_COMPATIBILITY_TOOL}" --text="${TRANSHELL_CONTENT_UNPACKING} $WINE_APP_NAME..."  --width=600 --auto-close --no-cancel 
rm $tmp_log


	mv "$1/drive_c/users/@current_user@" "$1/drive_c/users/$USER"
	sed -i "s#@current_user@#$USER#" $1/*.reg
    FixLink
}
DeployApp()
{
	ExtractApp "$WINEPREFIX"


	echo "$APPVER" > "$WINEPREFIX/PACKAGE_VERSION"

}
RemoveApp()
{
	rm -rf "$WINEPREFIX"
}
ResetApp()
{
	debug_log "Reset $PACKAGENAME....."
	read -p "*	Are you sure?(Y/N)" ANSWER
	if [ "$ANSWER" = "Y" -o "$ANSWER" = "y" -o -z "$ANSWER" ]; then
		EvacuateApp
		DeployApp
		CallApp
	fi
}
UpdateApp()
{
	if [ -d "${WINEPREFIX}.tmpdir" ]; then
		rm -rf "${WINEPREFIX}.tmpdir"
	fi
	if [ -f "$WINEPREFIX/PACKAGE_VERSION" ] && [ "$(cat "$WINEPREFIX/PACKAGE_VERSION")" = "$APPVER" ]; then
		return
	fi

    if [ -f "/opt/apps/${DEB_PACKAGE_NAME}/files/pre_update.sh" ];then
        source "/opt/apps/${DEB_PACKAGE_NAME}/files/pre_update.sh"
        CallPreUpdate
        return
    fi


    case $BOTTLENAME in
        "Deepin-Intelligent" | "Deepin-QQ" | "Deepin-TIM" | "Deepin-WeChat" | "Deepin-WXWork" | "Deepin-Dding" | "Wine-QQ" | "Spark-QQ" | "Spark-weixin")
            rm -rf "$WINEPREFIX"
            DeployApp
            return
            ;;
    esac

	ExtractApp "${WINEPREFIX}.tmpdir"
	$SHELL_DIR/spark_updater -s "${WINEPREFIX}.tmpdir" -c "${WINEPREFIX}" -v


	rm -rf "${WINEPREFIX}.tmpdir"
	echo "$APPVER" > "$WINEPREFIX/PACKAGE_VERSION"
}
RunApp()
{


    progpid=$(ps -ef | grep "zenity --progress --title=${BOTTLENAME}" | grep -v grep)
    debug_log "run ${BOTTLENAME} progress pid $progpid"
    if [ -n "$progpid" ]; then
        debug_log "$BOTTLENAME is running"
        exit 0
    fi
    	
 	if [ -d "$WINEPREFIX" ]; then
        	    if [ ! -f "$WINEPREFIX/PACKAGE_VERSION" ] || [ "$(cat "$WINEPREFIX/PACKAGE_VERSION")" != "$APPVER" ]; then
			UpdateApp
	    fi
 	else
        DeployApp 
 	fi

    CallApp "$@"
}

CreateBottle()
{
    if [ -d "$WINEPREFIX" ]; then
	    if [ ! -f "$WINEPREFIX/PACKAGE_VERSION" ] || [ "$(cat "$WINEPREFIX/PACKAGE_VERSION")" != "$APPVER" ]; then
            UpdateApp
	    fi
    else
        DeployApp
    fi
}

ParseArgs()
{
    if [ $# -eq 4 ];then
	    RunApp "$3"
    elif [ -f "$5" ];then
	    if [ -n "$MIME_EXEC" ];then
		    RunApp "$MIME_EXEC" "$(UnixUriToDosPath "$5")" "${@:6}"
	    else
		    RunApp "$3" "$(UnixUriToDosPath "$5")" "${@:6}"
	    fi
    else
	    RunApp "$3" "${@:5}"
    fi
}

#init_log_file





#####准备启动进程，分析在 https://blog.shenmo.tech/post/deepin-wine6%E7%9A%84run_v4%E8%84%9A%E6%9C%AC%E6%8E%A2%E7%B4%A2%E5%90%AF%E5%8A%A8%E6%96%B9%E5%BC%8F/
if [ $# -lt 3 ]; then
    debug_log "参数个数小于3个"
    exit 0
fi


APPDIR="/opt/apps/${DEB_PACKAGE_NAME}/files"
if [ -f "$APPDIR/files.md5sum" ];then
    APPVER="$(cat $APPDIR/files.md5sum)"
else
    APPVER="$2"
fi

debug_log "Run $*"


#执行lnk文件通过判断第5个参数是否是“/Unix”来判断
if [ "$4" == "/Unix" ];then
    RunApp "$3" "$4" "$5"
    exit 0
fi

if [ $# -lt 4 ]; then
	RunApp "$3"
	exit 0
fi
case $4 in
	"-r" | "--reset")
		ResetApp
		;;
	"-cb" | "--create")
		CreateBottle
		;;
	"-e" | "--remove")
		RemoveApp
		;;
	"-u" | "--uri")
        ParseArgs "$@"
		;;
	"-f" | "--file")
        ParseArgs "$@"
		;;
	"-h" | "--help")
		HelpApp
		;;
	*)
		echo "Invalid option: $4"
		echo "Use -h|--help to get help"
		exit 1
		;;
esac
exit 0
