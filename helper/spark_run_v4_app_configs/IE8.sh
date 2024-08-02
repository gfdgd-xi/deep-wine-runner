    rm -f "$WINEPREFIX/system.reg"
    cp $APPDIR/system.reg "$WINEPREFIX/system.reg"
    CallProcess "$@"
