    if [ -f "${WINEPREFIX}/drive_c/users/${USER}/Application Data/douyin" ]; then
       rm "${WINEPREFIX}/drive_c/users/${USER}/Application Data/douyin"
       mv ${WINEPREFIX}/drive_c/users/${USER}/Application\ Data/*.tmp ${WINEPREFIX}/drive_c/users/${USER}/Application\ Data/douyin
       chmod 755 ${WINEPREFIX}/drive_c/users/${USER}/Application\ Data/douyin
    fi
    CallProcess "$@"
