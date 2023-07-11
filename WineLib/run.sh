#!/bin/bash
CURRENT_DIR=$(cd $(dirname $0); pwd)
if [[ ! -d "$CURRENT_DIR/usr" ]]; then
    zenity --info --text=未安装运行库，无法运行 --no-wrap
    exit
fi
if [[ ! -d /lib64 ]]; then
    pkexec mkdir /lib64 -p
fi
bwrap --dev-bind / / \
    --ro-bind "$CURRENT_DIR/lib" /lib \
    --ro-bind "$CURRENT_DIR/lib64" /lib \
    --ro-bind "$CURRENT_DIR/usr" /usr \
    --ro-bind /usr/share /usr/share \
    --ro-bind /usr/bin /usr/bin \
    --ro-bind /usr/sbin /usr/sbin \
    -- "$@"
