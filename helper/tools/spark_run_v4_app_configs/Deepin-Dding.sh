    debug_log "run $1"
    $SHELL_DIR/spark_kill.sh DingTalk block

    CallProcess "$@"
