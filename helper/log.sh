#!/bin/bash

BOTTLE_NAME="Deepin-QQ"
DEBUG_MSG="+pid,+tid,+timestamp"
SHELL_DIR=$(dirname $0)
SHELL_DIR=$(realpath "$SHELL_DIR")
if [ $SPECIFY_SHELL_DIR ]; then
    SHELL_DIR=$SPECIFY_SHELL_DIR
fi

if [ -n "$1" ]; then
    BOTTLE_NAME="$1"
fi

if [ -n "$2" ]; then
    DEBUG_MSG="$2"
fi

RUN_CMD="/opt/deepinwine/apps/${BOTTLE_NAME}/run.sh"

if [ ! -f "$RUN_CMD" ]; then
    RUN_CMD="/opt/apps/$BOTTLE_NAME/files/run.sh"
    if [ ! -f "$RUN_CMD" ]; then
        echo "Invaild bottle name, $BOTTLE_NAME is not exist"
        exit 0
    fi
fi

mkdir $HOME/log &> /dev/null

export  DEBUG_LOG="$HOME/log"

dpkg -l | grep "Deepin Wine" > $HOME/log/${BOTTLE_NAME}.log
dpkg -l | grep deepin-wine >> $HOME/log/${BOTTLE_NAME}.log
ps -ef | grep -i c: >> $HOME/log/${BOTTLE_NAME}.log

$SHELL_DIR/kill.sh ${BOTTLE_NAME}

if [ -z "$3" ]; then
    WINEDEBUG=${DEBUG_MSG} $RUN_CMD &>> $HOME/log/${BOTTLE_NAME}.log &
else
    WINEDEBUG=${DEBUG_MSG} $RUN_CMD -u "$3" &>> $HOME/log/${BOTTLE_NAME}.log &
fi
dde-file-manager $HOME/log &> /dev/null &
