#!/data/data/com.termux/files/usr/bin/bash
CURRENT_DIR=$(dirname $(readlink -f "$0"))

if [[ $DISPLAY == "" ]] && [[ $WAYLAND_DISPLAY == "" ]]; then
    # 自动配置 NoVNC
    export DISPLAY=:5
    vncserver $DISPLAY &
    sleep 3
    xfwm4 &
    if [[ -f /data/data/com.termux/files/usr/bin/startxfce4 ]]; then
        startxfce4 &      
    fi
    $CURRENT_DIR/novnc/utils/novnc_proxy --vnc localhost:5905 &
fi
python3 $CURRENT_DIR/mainwindow.py
