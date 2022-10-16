#!/bin/bash

# $1 key value
# $2 process name , default QQ|TIM
# $3 control mode , default ctrl+alt
#    0   no control key
#    1   shift+
#    2   ctrl+
#    3   alt+
#    4   ctrl+alt+
#    5   ctrl+shift+
#    6   alt+shift+

SHELL_DIR=$(dirname $0)
SHELL_DIR=$(realpath "$SHELL_DIR")
if [ $SPECIFY_SHELL_DIR ]; then
    SHELL_DIR=$SPECIFY_SHELL_DIR
fi

get_wine_by_pid()
{
    cat /proc/$1/maps | grep -E "\/wine$|\/wine64$|\/wine |\/wine64 " | head -1 | awk '{print $6}'
}

is_wine_process()
{
    wine_module=$(get_wine_by_pid $1)
    if [ -z "$wine_module" ];then
        wine_module=$(cat /proc/$1/maps | grep -E "\/wineserver$" | head -1)
    fi
    echo $wine_module
}

get_prefix_by_pid()
{
    WINE_PREFIX=$(xargs -0 printf '%s\n' < /proc/$1/environ | grep WINEPREFIX)
    WINE_PREFIX=${WINE_PREFIX##*=}
    if [ -z "$WINE_PREFIX" ] && [ -n "$(is_wine_process $1)" ]; then
        #不指定容器的情况用默认容器目录
        WINE_PREFIX="$HOME/.wine"
    fi
    WINE_PREFIX=$(realpath $WINE_PREFIX)
    echo $WINE_PREFIX
}

get_bottle_path_by_process_id()
{
    PID_LIST="$1"
    PREFIX_LIST=""

    for pid_var in $PID_LIST ; do
        WINE_PREFIX=$(get_prefix_by_pid $pid_var)
        for path in $(echo -e $PREFIX_LIST) ; do
            prefix=${path#*=}
            if [ "$prefix" == "$WINE_PREFIX" ]; then
                WINE_PREFIX=""
            fi
        done
        if [ -n "$WINE_PREFIX" ];then
            PREFIX_LIST+="\n$pid_var=$WINE_PREFIX"
        fi
    done
    echo -e $PREFIX_LIST
}

get_bottle_path_by_process_name()
{
    PID_LIST=""
    for pid_var in $(ps -ef | grep -E -i "$1" | grep -v grep | awk '{print $2}');do
        #通过判断是否加载wine来判断是不是wine进程
        if [ -n "$(is_wine_process $pid_var)" ];then
            PID_LIST+=" $pid_var"
        fi
    done
    get_bottle_path_by_process_id "$PID_LIST"
}

send_to_process()
{
    if [ -z "$2" ]; then
        return 0
    fi

    for path in $(get_bottle_path_by_process_name $2); do
        proc_pid=${path%=*}
        prefix=${path#*=}
        wine_cmd=$(get_wine_by_pid $proc_pid)
        wine_name=$(echo $wine_cmd | awk -F / '{print $(NF-2)}')
        if command -v $wine_name > /dev/null 2>&1; then
            wine_cmd="$wine_name"
        fi
        echo "send to $path by $wine_cmd"

        env WINEPREFIX="$prefix" "$wine_cmd" "$SHELL_DIR/sendkeys.exe" $1 $3
    done
}

if [ -z "$1" ]; then
    echo "Please input a key [a-zA-Z]"
    exit 0
fi

if [ -n "$2" ]; then
    send_to_process $1 $2 $3
else
    send_to_process $1 "QQ|TIM"
fi
