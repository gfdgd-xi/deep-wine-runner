    debug_log "run $1"
    $SHELL_DIR/spark_kill.sh QQMicroGameBox block
    CallProcess "$1" -action:force_download -appid:363 -pid:8 -bin_version:1.1.2.4 -loginuin: 
