#!/bin/bash
SHELL_FOLDER=$(cd "$(dirname "$0")";pwd)
# /opt 目录识别
option=""

if [[ -d /usr/lib32 ]] && [[ -d $SHELL_FOLDER/lib32 ]]; then
    option="$option --dev-bind $SHELL_FOLDER/lib32 /usr/lib32 "
fi

if [[ -d /usr/lib64 ]] && [[ -d $SHELL_FOLDER/lib64 ]]; then
    option="$option --dev-bind $SHELL_FOLDER/lib64 /usr/lib64 "
fi

bwrap --dev-bind / / \
    --dev-bind "$SHELL_FOLDER/bin" /usr/bin \
    --dev-bind "$SHELL_FOLDER/lib" /usr/lib \
    --dev-bind /usr/lib/locale /usr/lib/locale \
    --dev-bind "$SHELL_FOLDER/share" /usr/share \
    $option \
    $SHELL_FOLDER/runner/deepin-wine-runner $*
