    if [ -d "${WINEPREFIX}/drive_c/users/${USER}/Application Data/Tencent/WXWork/Update" ]; then
        rm -rf "${WINEPREFIX}/drive_c/users/${USER}/Application Data/Tencent/WXWork/Update"
    fi
    if [ -d "${WINEPREFIX}/drive_c/users/${USER}/Application Data/Tencent/WXWork/upgrade" ]; then
        rm -rf "${WINEPREFIX}/drive_c/users/${USER}/Application Data/Tencent/WXWork/upgrade"
    fi
    #Support use native file dialog

    CallProcess "$@"
