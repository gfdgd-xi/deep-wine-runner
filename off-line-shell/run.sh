#!/bin/bash
SHELL_FOLDER=$(cd "$(dirname "$0")";pwd)
# /opt 目录识别
option=""
for path in `ls /opt`
do
    echo /opt/$path
    if [[ $path != wine-staging ]]; then
        # 支持识别正确的 wine
        mkdir -pv "$SHELL_FOLDER/opt/$path"
        option="$option --dev-bind /opt/$path /opt/$path"
    fi
done
wineName=(deepin-wine
    deepin-wine8-stable
    deepin-wine6-stable
    deepin-wine5-stable
    spark-wine
    spark-wine8
    deepin-wine6-vannila
    spark-wine7-devel
    spark-wine8-wow
    deepin-wine5
    ukylin-wine
    okylin-wine
    bookworm-run
)
for i in ${wineName[*]}; do
    if [[ -e /usr/bin/$i ]]; then
        option="$option --dev-bind /usr/bin/$i /usr/bin/$i"
        if [[ ! -e "$SHELL_FOLDER/bin/$i" ]]; then
            touch "$SHELL_FOLDER/bin/$i"
        fi
    fi
done
"$SHELL_FOLDER/bwrap" --dev-bind / / \
    --dev-bind "$SHELL_FOLDER/opt" /opt \
    --dev-bind "$SHELL_FOLDER/bin" /usr/bin \
    --dev-bind "$SHELL_FOLDER/lib" /usr/lib \
    --dev-bind "$SHELL_FOLDER/lib32" /usr/lib32 \
    --dev-bind "$SHELL_FOLDER/lib64" /usr/lib64 \
    --dev-bind /usr/lib/locale /usr/lib/locale \
    $option \
    $SHELL_FOLDER/runner/deepin-wine-runner
