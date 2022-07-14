#!/bin/sh

#   Copyright (C) 2016 Deepin, Inc.
#
#   Author:     Li LongYu <lilongyu@linuxdeepin.com>
#               Peng Hao <penghao@linuxdeepin.com>

BOTTLENAME="@public_bottle_name@"
APPVER="@deb_version_string@"
EXEC_PATH="@exec_path@"
START_SHELL_PATH="@start_shell_path@"
export MIME_TYPE="@mime_type@"
export DEB_PACKAGE_NAME="@deb_package_name@"
export APPRUN_CMD="@apprun_cmd@"
export PATCH_LOADER_ENV="@patch_loader@"

if [ -n "$EXEC_PATH" ];then
    $START_SHELL_PATH $BOTTLENAME $APPVER "$EXEC_PATH" "$@"
else
    $START_SHELL_PATH $BOTTLENAME $APPVER "uninstaller.exe" "$@"
fi
