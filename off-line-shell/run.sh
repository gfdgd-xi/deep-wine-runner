#!/bin/bash
SHELL_FOLDER=$(cd "$(dirname "$0")";pwd)
"$SHELL_FOLDER/bwrap" --dev-bind / / \
    --dev-bind "$SHELL_FOLDER/opt" /opt \
    --dev-bind "$SHELL_FOLDER/bin" /usr/bin \
    --dev-bind "$SHELL_FOLDER/lib" /usr/lib \
    --dev-bind "$SHELL_FOLDER/lib32" /usr/lib32 \
    --dev-bind "$SHELL_FOLDER/lib64" /usr/lib64 \
    --dev-bind /usr/lib/locale /usr/lib/locale\
    deepin-wine-runner
