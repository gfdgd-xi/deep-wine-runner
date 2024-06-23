#!/bin/bash
export DEBIAN_FRONTEND=noninteractive  # 防止卡 tzdate
brew install libffi gettext glib pkg-config autoconf automake pixman ninja
exit 0