#!/bin/bash

#   Copyright (C) 2016 Deepin, Inc.
#
#   Author:     Li LongYu <lilongyu@linuxdeepin.com>
#               Peng Hao <penghao@linuxdeepin.com>
BOTTLENAME="$1"
WINEPREFIX="$HOME/.deepinwine/$1"
APPDIR="/opt/apps/${DEB_PACKAGE_NAME}/files"
APPVER=""
APPTAR="files.7z"
WINE_CMD="deepin-wine"
LOG_FILE=$0
PUBLIC_DIR="/var/public"
export WINEBANNER=1

SHELL_DIR=${0%/*}
if [ $SPECIFY_SHELL_DIR ]; then
    SHELL_DIR=$SPECIFY_SHELL_DIR
fi

if [ $APPRUN_CMD ]; then
    WINE_CMD=$APPRUN_CMD
fi

if [ $SPECIFY_SHELL_DIR ]; then
    SHELL_DIR=$SPECIFY_SHELL_DIR
fi

UsePublicDir()
{
    if [ -z "$USE_PUBLIC_DIR" ]; then
        echo "Don't use public dir"
        return 1
    fi
    if [ ! -d "$PUBLIC_DIR" ];then
        echo "Not found $PUBLIC_DIR"
        return 1
    fi
    if [ ! -r "$PUBLIC_DIR" ];then
        echo "Can't read for $PUBLIC_DIR"
        return 1
    fi
    if [ ! -w "$PUBLIC_DIR" ];then
        echo "Can't write for $PUBLIC_DIR"
        return 1
    fi
    if [ ! -x "$PUBLIC_DIR" ];then
        echo "Can't excute for $PUBLIC_DIR"
        return 1
    fi

    return 0
}

_DeleteRegistry()
{
    env WINEPREFIX="$WINEPREFIX" $WINE_CMD reg DELETE "$1" /f &> /dev/null
}

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
    echo "${1}"
}

HelpApp()
{
	echo " Extra Commands:"
	echo " -r/--reset     Reset app to fix errors"
	echo " -e/--remove    Remove deployed app files"
	echo " -h/--help      Show program help info"
}

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
        if [[ $WINE_CMD == *"deepin-wine8-stable"* ]];then
            check_link "$HOME/Documents" Documents
        else
            check_link "$HOME/Documents" "My Documents"
        fi
        cd $CUR_DIR
        #ls -l "${WINEPREFIX}/dosdevices"
    fi
}

DisableWrite()
{
    if [ -d "${1}" ]; then
        chmod +w "${1}"
        rm -rf "${1}"
    fi

    mkdir "${1}"
    chmod -w "${1}"
}

is_autostart()
{
    AUTOSTART="/opt/deepinwine/tools/autostart"
    if [ -f "$AUTOSTART.all" ]&&[ -f "/opt/apps/$1/files/run.sh" ];then
        return 0
    fi

    if [ -f $AUTOSTART ];then
        grep -c "$1" $AUTOSTART > /dev/null
        return $?
    fi

    return 1
}

#arg 1: windows process file path
#arg 2-*: windows process args
CallProcess()
{
    #get file full path
    path="$1"
    path=${path/c:/${WINEPREFIX}/drive_c}
    path=${path//\\/\/}

    #kill bloack process
    is_autostart $DEB_PACKAGE_NAME
    autostart=$?
    if [[ $autostart -ne 0 ]] && [[ "$1" != *"pluginloader.exe" ]];then
        $SHELL_DIR/kill.sh "$BOTTLENAME" block
    fi

    #change current dir to excute path
    path=${path%/*}
    cd "$path"
    #pwd

    #Set default mime type
    if [ -n "$MIME_TYPE" ]; then
        xdg-mime default "$DEB_PACKAGE_NAME".desktop "$MIME_TYPE"
    fi

    debug_log "Starting process $* ..."
    env WINEPREFIX="$WINEPREFIX" $WINE_CMD "$@" &

    #start autobottle
    if [ $autostart -eq 0 ];then
        $SHELL_DIR/autostart_wine.sh $DEB_PACKAGE_NAME
    fi
}

CallZhuMu()
{
    #change current dir to excute path
    path=$(dirname "$path")
    cd "$path"
    pwd

    #Set default mime type
    if [ -n "$MIME_TYPE" ]; then
        xdg-mime default "$DEB_PACKAGE_NAME".desktop "$MIME_TYPE"
    fi

    debug_log_to_file "Starting process $* ..."
    if [ -n "$2" ];then
        env WINEPREFIX="$WINEPREFIX" $WINE_CMD "$1" "--url=$2" &
    else
        env WINEPREFIX="$WINEPREFIX" $WINE_CMD "$1" &
    fi
}

CallQQGame()
{
    debug_log "run $1"
    $SHELL_DIR/kill.sh qqgame block
    env WINEPREFIX="$WINEPREFIX" $WINE_CMD "$1" &
}

CallQQ()
{
    if [ ! -f "$WINEPREFIX/../.QQ_run" ]; then
        debug_log "first run time"
        $SHELL_DIR/add_hotkeys
        $SHELL_DIR/fontconfig
        touch "$WINEPREFIX/../.QQ_run"
    fi

    DisableWrite "${WINEPREFIX}/drive_c/Program Files/Tencent/QQ/Bin/QQLiveMPlayer"
    DisableWrite "${WINEPREFIX}/drive_c/Program Files/Tencent/QQ/Bin/QQLiveMPlayer1"
    DisableWrite "${WINEPREFIX}/drive_c/Program Files/Tencent/QzoneMusic"

    DisableWrite "${WINEPREFIX}/drive_c/Program Files/Tencent/QQBrowser"
    DisableWrite "${WINEPREFIX}/drive_c/Program Files/Common Files/Tencent/QQBrowser"
    DisableWrite "${WINEPREFIX}/drive_c/users/Public/Application Data/Tencent/QQBrowserBin"
    DisableWrite "${WINEPREFIX}/drive_c/users/Public/Application Data/Tencent/QQBrowserDefault"
    DisableWrite "${WINEPREFIX}/drive_c/users/${USER}/Application Data/Tencent/QQBrowserDefault"

    DisableWrite "${WINEPREFIX}/drive_c/users/Public/Application Data/Tencent/QQPCMgr"
    DisableWrite "${WINEPREFIX}/drive_c/Program Files/Common Files/Tencent/QQPCMgr"

    DisableWrite "${WINEPREFIX}/drive_c/Program Files/Common Files/Tencent/HuaYang"
    DisableWrite "${WINEPREFIX}/drive_c/users/${USER}/Application Data/Tencent/HuaYang"

    CallProcess "$@"
}

CallTIM()
{
    if [ ! -f "$WINEPREFIX/../.QQ_run" ]; then
        debug_log "first run time"
        $SHELL_DIR/add_hotkeys
        $SHELL_DIR/fontconfig
        # If the bottle not exists, run reg may cost lots of times
        # So create the bottle befor run reg
        env WINEPREFIX="$WINEPREFIX" $WINE_CMD uninstaller --list
        touch $WINEPREFIX/../.QQ_run
    fi

    CallProcess "$@"

    #disable Tencent MiniBrowser
    _DeleteRegistry "HKCU\\Software\\Tencent\\MiniBrowser"
}

CallWeChat()
{
    export DISABLE_RENDER_CLIPBOARD=1
    CallProcess "$@"
}

CallWangWang()
{
    chmod 700 "$WINEPREFIX/drive_c/Program Files/AliWangWang/9.12.10C/wwbizsrv.exe"
    chmod 700 "$WINEPREFIX/drive_c/Program Files/Alibaba/wwbizsrv/wwbizsrv.exe"
    if [ $# = 3 ] && [ -z "$3" ];then
        EXEC_PATH="c:/Program Files/AliWangWang/9.12.10C/WWCmd.exe"
        env WINEPREFIX="$WINEPREFIX" $WINE_CMD "$EXEC_PATH" "$2" &
    else
    	CallProcess "$@"
    fi
}

CallWXWork()
{
    if [ -d "${WINEPREFIX}/drive_c/users/${USER}/Application Data/Tencent/WXWork/Update" ]; then
        rm -rf "${WINEPREFIX}/drive_c/users/${USER}/Application Data/Tencent/WXWork/Update"
    fi
    if [ -d "${WINEPREFIX}/drive_c/users/${USER}/Application Data/Tencent/WXWork/upgrade" ]; then
        rm -rf "${WINEPREFIX}/drive_c/users/${USER}/Application Data/Tencent/WXWork/upgrade"
    fi
    #Support use native file dialog

    CallProcess "$@"
}

CallDingTalk()
{
    debug_log "run $1"
    $SHELL_DIR/kill.sh DingTalk block

    CallProcess "$@"
}

urldecode() { : "${*//+/ }"; echo -e "${_//%/\\x}"; }

CallMeiTuXiuXiu()
{
    #set -- "$1" "${2#file://*}"
    local path=$(urldecode "$2")
    path=${path/file:\/\//}
    set -- "$1" $path
    CallProcess "$@"
}

CallFastReadPDF()
{
    #set -- "$1" "${2#file://*}"
    local path=$(urldecode "$2")
    path=${path/file:\/\//}
    set -- "$1" $path
    CallProcess "$@"
}

CallEvernote()
{
    local path=$(urldecode "$2")
    path=${path/file:\/\//}
    set -- "$1" $path
    CallProcess "$@"
}

CallTencentVideo()
{
    if [ -f "${WINEPREFIX}/drive_c/Program Files/Tencent/QQLive/Upgrade.dll" ]; then
        rm -rf "${WINEPREFIX}/drive_c/Program Files/Tencent/QQLive/Upgrade.dll"
    fi

    CallProcess "$@"
}

CallFoxmail()
{
    sed -i '/LogPixels/d' ${WINEPREFIX}/user.reg
    CallProcess "$@"
}

CallTHS()
{
    $SHELL_DIR/kill.sh ths block

    debug_log "Start run $1"
    #get file full path
    path="$1"
    path=$(echo ${path/c:/${WINEPREFIX}/drive_c})
    path=$(echo ${path//\\/\/})

    #kill bloack process
    name="${path##*/}"
    $SHELL_DIR/kill.sh "$name" block

    #change current dir to excute path
    path=$(dirname "$path")
    cd "$path"
    pwd

    #Set default mime type
    if [ -n "$MIME_TYPE" ]; then
        xdg-mime default "$DEB_PACKAGE_NAME".desktop "$MIME_TYPE"
    fi

    env WINEPREFIX="$WINEPREFIX" $WINE_CMD "$@" &
}

CallQQGameV2()
{
    debug_log "run $1"
    $SHELL_DIR/kill.sh QQMicroGameBox block
    env WINEPREFIX="$WINEPREFIX" $WINE_CMD "$1" -action:force_download -appid:${2} -pid:8 -bin_version:1.1.2.4 -loginuin: &
}

CallPsCs6()
{
    #get file full path
    path="$1"
    path=$(echo ${path/c:/${WINEPREFIX}/drive_c})
    path=$(echo ${path//\\/\/})

    #kill bloack process
    name="${path##*/}"
    $SHELL_DIR/kill.sh "$name" block

    #change current dir to excute path
    path=$(dirname "$path")
    cd "$path"
    pwd

    #Set default mime type
    if [ -n "$MIME_TYPE" ]; then
        xdg-mime default "$DEB_PACKAGE_NAME".desktop "$MIME_TYPE"
    fi

    debug_log_to_file "Starting process $* ..."

    env WINEPREFIX="$WINEPREFIX" $WINE_CMD "$@" &
}

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
CallApp()
{
    FixLink
    debug_log "CallApp $BOTTLENAME arg count $#: $*"

    if [ -f "/opt/apps/${DEB_PACKAGE_NAME}/files/pre_run.sh" ];then
        source "/opt/apps/${DEB_PACKAGE_NAME}/files/pre_run.sh"
        CallPreRun "$@"
    fi

    case $BOTTLENAME in
        "Deepin-WangWang")
            CallWangWang "$@"
            ;;
        "Deepin-ZhuMu")
            CallZhuMu "$@"
            ;;
        "Deepin-QQ")
            CallQQ "$@"
            ;;
        "Deepin-TIM")
            CallTIM "$@"
            ;;
        "Deepin-QQGame"*)
            CallQQGame "$@"
            ;;
        "Deepin-ATM")
            CallATM "$@"
            ;;
        "Deepin-WeChat")
            CallWeChat "$@"
            ;;
        "Deepin-WXWork")
            CallWXWork "$@"
            ;;
        "Deepin-Dding")
            CallDingTalk "$@"
            ;;
        "Deepin-MTXX")
            CallMeiTuXiuXiu "$@"
            ;;
        "Deepin-FastReadPDF")
            CallFastReadPDF "$@"
            ;;
        "Deepin-Evernote")
            CallEvernote "$@"
            ;;
        "Deepin-TencentVideo")
            CallTencentVideo "$@"
            ;;
        "Deepin-Foxmail")
            CallFoxmail "$@"
            ;;
        "Deepin-THS")
            CallTHS "$@"
            ;;
        "Deepin-QQHlddz")
            CallQQGameV2 "$1" 363
            ;;
        "Deepin-QQBydr")
            CallQQGameV2 "$1" 1104632801
            ;;
        "Deepin-QQMnsj")
            CallQQGameV2 "$1" 1105856612
            ;;
        "Deepin-QQSszb")
            CallQQGameV2 "$1" 1105640244
            ;;
        "Deepin-CS6")
            CallPsCs6 "$@"
            ;;
        *)
            CallProcess "$@"
            ;;
    esac
}
ExtractApp()
{
    $SHELL_DIR/deepin-wine-banner unpack &
	mkdir -p "$1"
	7z x "$APPDIR/$APPTAR" -o"$1"
    if [ $? != 0 ];then
        $SHELL_DIR/deepin-wine-banner info "解压失败"
        rm -rf "$1"
        exit 1
    fi
	mv "$1/drive_c/users/@current_user@" "$1/drive_c/users/$USER"
	sed -i "s#@current_user@#$USER#" $1/*.reg
    FixLink
    $SHELL_DIR/deepin-wine-banner unpacked
}
DeployApp()
{
	ExtractApp "$WINEPREFIX"

    if UsePublicDir;then
        chgrp -R users "$WINEPREFIX"
        chmod -R 0775 "$WINEPREFIX"
    fi

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

    if [ -f "/opt/apps/${DEB_PACKAGE_NAME}/files/pre_update.sh" ];then
        source "/opt/apps/${DEB_PACKAGE_NAME}/files/pre_update.sh"
        CallPreUpdate
        return
    fi

    case $BOTTLENAME in
        "Deepin-Intelligent" | "Deepin-QQ" | "Deepin-TIM" | "Deepin-WeChat" | "Deepin-WXWork" | "Deepin-Dding")
            rm -rf "$WINEPREFIX"
            DeployApp
            return
            ;;
    esac

	ExtractApp "${WINEPREFIX}.tmpdir"
	$SHELL_DIR/updater -s "${WINEPREFIX}.tmpdir" -c "${WINEPREFIX}" -v

    if UsePublicDir;then
        chgrp -R users "$WINEPREFIX"
        chmod -R 0775 "$WINEPREFIX"
    fi

	rm -rf "${WINEPREFIX}.tmpdir"
	echo "$APPVER" > "$WINEPREFIX/PACKAGE_VERSION"
}
RunApp()
{
    $SHELL_DIR/deepin-wine-banner
    if [[ $? != 0 ]]; then
        debug_log "检测到 deepin-wine-banner 运行， exit 1"
        exit 1
    fi

    $SHELL_DIR/deepin-wine-banner start &

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

# Check if some visual feedback is possible
if command -v zenity >/dev/null 2>&1; then
	progressbar()
	{
		WINDOWID="" zenity --progress --title="$1" --text="$2" --pulsate --width=400 --auto-close --no-cancel ||
		WINDOWID="" zenity --progress --title="$1" --text="$2" --pulsate --width=400 --auto-close
	}

else
	progressbar()
	{
		cat -
	}
fi

if [ $# -lt 3 ]; then
    debug_log "参数个数小于3个"
    exit 0
fi

if UsePublicDir;then
    WINEPREFIX="$PUBLIC_DIR/$1"
fi

if [ -f "$APPDIR/files.md5sum" ];then
    APPVER="$(cat $APPDIR/files.md5sum)"
else
    APPVER="$2"
fi

# ARM 需要指定模拟器参数
if [ -f "/opt/deepinemu/tools/init_emu.sh" ];then
    source "/opt/deepinemu/tools/init_emu.sh"
    export EMU_CMD="$EMU_CMD"
    export EMU_ARGS="$EMU_ARGS"
fi

debug_log "Run $*"

if [ -z "$WINE_WMCLASS" ]; then
    export WINE_WMCLASS="$DEB_PACKAGE_NAME"
fi

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
