    if [ -e ${WINEPREFIX}/drive_c/Program\ Files/Tencent/QQMusic/QQMusic.exe ]; then
    sleep 1
    rm -rf ${WINEPREFIX}/drive_c/Program\ Files/Tencent/QQMusic/*.log
    else
       mkdir ${WINEPREFIX}/drive_c/Program\ Files/Tencent/updatetemp
       mv ${WINEPREFIX}/drive_c/Program\ Files/Tencent/QQMusic/*.dll ${WINEPREFIX}/drive_c/Program\ Files/Tencent/updatetemp
       mv ${WINEPREFIX}/drive_c/Program\ Files/Tencent/QQMusic/*.exe ${WINEPREFIX}/drive_c/Program\ Files/Tencent/updatetemp
       mv ${WINEPREFIX}/drive_c/Program\ Files/Tencent/QQMusic/*.rdb ${WINEPREFIX}/drive_c/Program\ Files/Tencent/updatetemp
       mv ${WINEPREFIX}/drive_c/Program\ Files/Tencent/QQMusic/*.log ${WINEPREFIX}/drive_c/Program\ Files/Tencent/updatetemp
       mv ${WINEPREFIX}/drive_c/Program\ Files/Tencent/QQMusic/QQMusic* ${WINEPREFIX}/drive_c/Program\ Files/Tencent
       rm -rf ${WINEPREFIX}/drive_c/Program\ Files/Tencent/QQMusic
       rm -rf ${WINEPREFIX}/drive_c/Program\ Files/Tencent/updatetemp
       rm -rf ${WINEPREFIX}/drive_c/Program\ Files/Tencent/*.log
       mv ${WINEPREFIX}/drive_c/Program\ Files/Tencent/QQMusic* ${WINEPREFIX}/drive_c/Program\ Files/Tencent/QQMusic
    fi
    CallProcess "$@"
