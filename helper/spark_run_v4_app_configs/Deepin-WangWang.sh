#/bin/bash
    chmod 700 "$WINEPREFIX/drive_c/Program Files/AliWangWang/9.12.10C/wwbizsrv.exe"
    chmod 700 "$WINEPREFIX/drive_c/Program Files/Alibaba/wwbizsrv/wwbizsrv.exe"
    if [ $# = 3 ] && [ -z "$3" ];then
        EXEC_PATH="c:/Program Files/AliWangWang/9.12.10C/WWCmd.exe"
        env WINEPREFIX="$WINEPREFIX" $WINE_CMD "$EXEC_PATH" "$2" &
    else
    	CallProcess "$@"
    fi
