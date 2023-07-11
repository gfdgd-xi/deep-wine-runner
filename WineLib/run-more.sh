#!/bin/bash
CURRENT_DIR=$1
if [[ ! -d "$CURRENT_DIR/usr" ]]; then
    zenity --info --text=未安装运行库，无法运行 --no-wrap
    exit
fi
if [[ ! -d "$CURRENT_DIR/usr/lib64" ]]; then
    bwrap --dev-bind / / \
        --ro-bind "$CURRENT_DIR/usr/lib" /lib \
        --ro-bind "$CURRENT_DIR/usr" /usr \
        --ro-bind /usr/share /usr/share \
        --ro-bind /usr/bin /usr/bin \
        --ro-bind /usr/sbin /usr/sbin \
        -- "$@"
    exit
fi
if [[ ! -f /lib64 ]] && [[ ! -d /lib64 ]] && [[ ! -L /lib64 ]]; then
    pkexec ln -s /usr/lib64 /lib64
fi
bwrap --dev-bind / / \
    --ro-bind "$CURRENT_DIR/usr/lib" /lib \
    --ro-bind "$CURRENT_DIR/usr/lib64" /lib \
    --ro-bind "$CURRENT_DIR/usr" /usr \
    --ro-bind /usr/share /usr/share \
    --ro-bind /usr/bin /usr/bin \
    --ro-bind /usr/sbin /usr/sbin \
    -- "$@"
