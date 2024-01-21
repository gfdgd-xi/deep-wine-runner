    if [ -f "${WINEPREFIX}/drive_c/ProgramData/Microsoft/Windows/Start\ Menu/Programs/MuBu.lnk" ]; then
       chmod 555 ${WINEPREFIX}/drive_c/ProgramData/Microsoft/Windows/Start\ Menu/Programs/MuBu.lnk
    fi
    CallProcess "$@"
