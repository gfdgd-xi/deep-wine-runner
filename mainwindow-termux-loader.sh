#!/data/data/com.termux/files/usr/bin/bash
CURRENT_DIR=$(dirname $(readlink -f "$0"))
if [[ ! -d $TMPDIR/tmp ]]; then
    mkdir -p $TMPDIR/tmp
fi
noVNCOption="--listen localhost:6080"
VNCServerOption="-localhost yes"
if [[ -f $HOME/.config/deepin-wine-runner/vnc-public ]]; then
    unset noVNCOption
    unset VNCServerOption
fi
if [[ $DISPLAY == "" ]] && [[ $WAYLAND_DISPLAY == "" ]] && [[ -f /data/data/com.termux/files/usr/bin/vncpasswd ]]; then
    # 自动配置 NoVNC
    export DISPLAY=:5
    vncserver -kill :5
    vncserver $DISPLAY $VNCServerOption &
    sleep 3
    xfwm4 &
    if [[ -f /data/data/com.termux/files/usr/bin/startxfce4 ]]; then
        startxfce4 &      
    fi
    $CURRENT_DIR/novnc/utils/novnc_proxy --vnc localhost:5905 $noVNCOption &
fi
python3 $CURRENT_DIR/mainwindow.py
