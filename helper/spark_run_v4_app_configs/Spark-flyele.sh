    if [ -w ${WINEPREFIX}/drive_c/users/${USER}/Application\ Data/飞项/Crashpad/reports ]; then
       rm -rf ${WINEPREFIX}/drive_c/users/${USER}/Application\ Data/飞项/Crashpad/reports/*
       chmod 555 ${WINEPREFIX}/drive_c/users/${USER}/Application\ Data/飞项/Crashpad/reports
    fi
    CallProcess "$@"
