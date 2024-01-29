#!/bin/bash

BASE_DIR="$HOME/.deepinwine/Deepin-QQ"
WINE_CMD="deepin-wine"
PUBLIC_DIR="/var/public"

SHELL_DIR="/opt/deepinwine/tools"

if [ $SPECIFY_SHELL_DIR ]; then
    SHELL_DIR=$SPECIFY_SHELL_DIR
fi

_SetRegistryValue()
{
    env WINEPREFIX="$BASE_DIR" $WINE_CMD reg ADD "$1" /v "$2" /t $3 /d "$4" /f
}

_SetOverride()
{
    _SetRegistryValue 'HKCU\Software\Wine\DllOverrides' "$2" REG_SZ "$1"
}

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

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Please input two args, first is dpi, second is bottle name"
    exit 0
fi

if (("$1" < 96)) || (($1 > 400)) ; then
    echo "Invaild dpi vaule, min 96 max 400"
    exit 0
fi

BASE_DIR="$HOME/.deepinwine/$2"

if UsePublicDir; then
    BASE_DIR="$PUBLIC_DIR/$2"
fi

if [ ! -d "$BASE_DIR" ]; then
    echo "Invaild bottle name, $2 is not exist"
    exit 0
fi

$SHELL_DIR/kill.sh $2

_SetRegistryValue 'HKCU\Control Panel\Desktop' LogPixels REG_DWORD $1

exit 0
