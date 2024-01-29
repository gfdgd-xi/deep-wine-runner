#!/bin/bash
    debug_log "run $1"
    $SHELL_DIR/spark_kill.sh qqgame block
    env WINEPREFIX="$WINEPREFIX" $WINE_CMD "$1" &
