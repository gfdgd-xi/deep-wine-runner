    if [ -f "${WINEPREFIX}/drive_c/Program Files/Tencent/QQLive/Upgrade.dll" ]; then
        rm -rf "${WINEPREFIX}/drive_c/Program Files/Tencent/QQLive/Upgrade.dll"
    fi

    CallProcess "$@"
