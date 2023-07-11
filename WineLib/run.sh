#!/bin/bash
CURRENT_DIR=$(cd $(dirname $0); pwd)
if [[ ! -d "$CURRENT_DIR/usr" ]]; then
    zenity --info --text=未安装运行库，无法运行 --no-wrap
    exit
fi
systemNeedCommand=""
for libr in `ls /usr/lib`
do
    if [[ -f /usr/lib/$libr/libc.so.6 ]]; then
        if [[ ! -f "$CURRENT_DIR/usr/lib/$libr/libc.so.6" ]]; then
            echo $libr
            systemNeedCommand="$systemNeedCommand --ro-bind /usr/lib/$libr/ /usr/lib/$libr/ "
            mkdir -p "$CURRENT_DIR/usr/lib/$libr"
        fi
    fi
done
for libr in `ls /usr/lib/ld*.so*`
do
    if [[ -f $libr ]]; then
        if [[ ! -f "$CURRENT_DIR/$libr" ]]; then
            systemNeedCommand="$systemNeedCommand --ro-bind $libr $libr "        
            touch "$CURRENT_DIR/$libr"
        else
            if [[ ! -s "$CURRENT_DIR/$libr" ]]; then
                systemNeedCommand="$systemNeedCommand --ro-bind $libr $libr "        
            fi
        fi
    fi
done
if [[ -d /usr/lib64 ]] && [[ ! -d "$CURRENT_DIR/usr/lib64" ]]; then
    mkdir -p "$CURRENT_DIR/usr/lib64"
fi
if [[ -d /usr/lib64/ ]]; then
    for libr in `ls /usr/lib64/ld*.so*`
    do
        if [[ -f $libr ]]; then
            if [[ ! -f "$CURRENT_DIR/$libr" ]]; then
                systemNeedCommand="$systemNeedCommand --ro-bind $libr $libr "        
                touch "$CURRENT_DIR/$libr"
            else
                if [[ ! -s "$CURRENT_DIR/$libr" ]]; then
                    systemNeedCommand="$systemNeedCommand --ro-bind $libr $libr "        
                fi
            fi
        fi
    done
fi
if [[ ! -d "$CURRENT_DIR/usr/lib/locale" ]]; then
    systemNeedCommand="$systemNeedCommand --ro-bind /usr/lib/locale /usr/lib/locale "      
fi

if [[ ! -d "$CURRENT_DIR/usr/lib64" ]]; then
    bwrap --dev-bind / / \
        --bind "$CURRENT_DIR/usr/lib" /lib \
        --bind "$CURRENT_DIR/usr" /usr \
        --ro-bind /usr/share /usr/share \
        --ro-bind /usr/bin /usr/bin \
        --ro-bind /usr/sbin /usr/sbin \
        $systemNeedCommand \
        -- "$@"
    exit
fi
if [[ ! -f /lib64 ]] && [[ ! -d /lib64 ]] && [[ ! -L /lib64 ]]; then
    pkexec ln -s /usr/lib64 /lib64
fi
if [[ -L /lib64 ]] || [[ -d /lib64 ]] || [[ -f /lib64 ]];then
    bwrap --dev-bind / / \
        --bind "$CURRENT_DIR/usr/lib" /lib \
        --bind "$CURRENT_DIR/usr/lib64" /lib \
        --bind "$CURRENT_DIR/usr" /usr \
        --ro-bind /usr/share /usr/share \
        --ro-bind /usr/bin /usr/bin \
        --ro-bind /usr/sbin /usr/sbin \
        $systemNeedCommand \
        -- "$@"
    exit
fi
bwrap --dev-bind / / \
    --bind "$CURRENT_DIR/usr/lib" /lib \
    --bind "$CURRENT_DIR/usr" /usr \
    --ro-bind /usr/share /usr/share \
    --ro-bind /usr/bin /usr/bin \
    --ro-bind /usr/sbin /usr/sbin \
    $systemNeedCommand \
    -- "$@"
