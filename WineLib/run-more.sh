#!/bin/bash
CURRENT_DIR=$1
if [[ ! -d "$CURRENT_DIR/usr" ]]; then
    zenity --info --text=未安装运行库，无法运行 --no-wrap
    exit
fi
command=""
if [[ -d "$CURRENT_DIR/usr/lib/i386-linux-gnu" ]]; then
    command=" $command --ro-bind \"$CURRENT_DIR/usr/lib/i386-linux-gnu\" /usr/lib/i386-linux-gnu "
    if [[ ! -d /usr/lib/i386-linux-gnu ]] && ; then
        pkexec mkdir -p /usr/lib/i386-linux-gnu
    fi
fi
if [[ -d "$CURRENT_DIR/usr/lib/x86_64-linux-gnu" ]]; then
    command=" $command --ro-bind \"$CURRENT_DIR/usr/lib/x86_64-linux-gnu\" /usr/lib/x86_64-linux-gnu "
    if [[ ! -d /usr/lib/x86_64-linux-gnu/ ]]; then
        pkexec mkdir -p /usr/lib/x86_64-linux-gnu/
    fi
fi
if [[ -d "$CURRENT_DIR/usr/lib/arm-linux-gnueabihf" ]]; then
    command=" $command --ro-bind \"$CURRENT_DIR/usr/lib/arm-linux-gnueabihf\" /usr/lib/arm-linux-gnueabihf "
    if [[ ! -d /usr/lib/arm-linux-gnueabihf/ ]]; then
        pkexec mkdir -p /usr/lib/arm-linux-gnueabihf/
    fi
fi
if [[ -d "$CURRENT_DIR/usr/lib/aarch64-linux-gnu" ]]; then
    command=" $command --ro-bind \"$CURRENT_DIR/usr/lib/aarch64-linux-gnu\" /usr/lib/aarch64-linux-gnu "
    if [[ ! -d /usr/lib/aarch64-linux-gnu/ ]]; then
        pkexec mkdir -p /usr/lib/aarch64-linux-gnu/
    fi
fi
if [[ -d "$CURRENT_DIR/usr/lib64" ]]; then
    command=" $command --ro-bind \"$CURRENT_DIR/usr/lib64\" /lib64 "
    if [[ ! -d /lib64 ]]; then
        pkexec ln -s /usr/lib64 /lib64
    fi
fi
if [[ -f "$CURRENT_DIR/usr/lib/ld-linux-aarch64.so.1" ]]; then
    command=" $command --ro-bind \"$CURRENT_DIR/usr/lib/ld-linux-aarch64.so.1\" /usr/lib/ld-linux-aarch64.so.1 "
    if [[ ! -f /usr/lib/ld-linux-aarch64.so.1 ]] && [[ ! -L /usr/lib/ld-linux-aarch64.so.1 ]]; then
        pkexec bash /usr/lib/ld-linux-aarch64.so.1
    fi
fi
if [[ -f "$CURRENT_DIR/usr/lib/ld-linux-armhf.so.3" ]]; then
    command=" $command --ro-bind \"$CURRENT_DIR/usr/lib/ld-linux-armhf.so.3\" ld-linux-armhf.so.3 "
    if [[ ! -f /usr/lib/ld-linux-armhf.so.3 ]]; then
        pkexec touch /usr/lib/ld-linux-armhf.so.3
    fi
fi
if [[ -f "$CURRENT_DIR/usr/lib/ld-linux.so.2" ]]; then
    command=" $command --ro-bind \"$CURRENT_DIR/usr/lib/ld-linux.so.2\" ld-linux.so.2 "
    if [[ ! -f /usr/lib/ld-linux.so.2 ]]; then
        pkexec touch /usr/lib/ld-linux.so.2
    fi
fi
if [[ -f "$CURRENT_DIR/usr/lib64/ld-linux-x86-64.so.2" ]]; then
    command=" $command --ro-bind \"$CURRENT_DIR/usr/lib64/ld-linux-x86-64.so.2\" ld-linux-x86-64.so.2 "
    if [[ ! -f /usr/lib64/ld-linux-x86-64.so.2 ]]; then
        pkexec touch /usr/lib64/ld-linux-x86-64.so.2
    fi
fi

bwrap --dev-bind / / \
    --ro-bind "$CURRENT_DIR/usr/lib" /lib \
    --ro-bind "$CURRENT_DIR/usr/lib64" /lib \
    --ro-bind "$CURRENT_DIR/usr" /usr \
    --ro-bind /usr/share /usr/share \
    --ro-bind /usr/bin /usr/bin \
    --ro-bind /usr/sbin /usr/sbin \
    -- "${@:2}"
