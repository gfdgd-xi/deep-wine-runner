    sed -i '/LogPixels/d' ${WINEPREFIX}/user.reg
    CallProcess "$@"
